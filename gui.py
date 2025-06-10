# gui.py
# -*- coding: utf-8 -*-
"""
TechCare 2025 — сучасний GUI у темному пастельному стилі з анімаціями
"""
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from ai_tab import AITab
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess
from PIL import Image, ImageDraw
import pystray
import threading


# ======== Глобальна кольорова схема для темної теми ========
DARK_BG       = "#181D23"
CARD_BG       = "#232A33"
ACCENT        = "#80FFD0"
ACCENT_2      = "#44A6FF"
ACCENT_FADE   = "#2A4D4D"
NEON          = "#00DDEB"
TEXT_MAIN     = "#E9F6F2"
TEXT_FADED    = "#92A6B6"
SHADOW        = "#1A222C"
RED           = "#FF6384"
YELLOW        = "#FFD580"
GREEN         = "#B6FFB0"

# ========== Анімований сучасний прогрес-бар ==========
class SmoothProgressBar(tk.Canvas):
    def __init__(self, parent, width=260, height=20, bg=CARD_BG, fg=ACCENT, radius=12, **kwargs):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0, bd=0, **kwargs)
        self.fg = fg

        self.radius = radius
        self.fg = fg
        self.bg_color = bg
        self._progress = 0
        self._target = 0
        self.width = width
        self.height = height
        self._bar = None
        self._animating = False
        self.draw_background()

    def draw_background(self):
        self.delete("all")
        # фоновий прогресбар з легким прозорим акцентом
        self.create_rounded_rect(2, 2, self.width-2, self.height-2, self.radius, fill=ACCENT_FADE, outline="")
        self._bar = self.create_rounded_rect(2, 2, 2, self.height-2, self.radius, fill=self.fg, outline="")

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        # Малюємо скруглений прямокутник
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def set_progress(self, value, animate=True):
        value = min(max(value, 0), 100)
        self._target = value
        if animate and not self._animating:
            self._animating = True
            self._animate()
        else:
            self._progress = value
            self._update_bar()

    def _animate(self):
        diff = self._target - self._progress
        if abs(diff) < 0.4:
            self._progress = self._target
            self._animating = False
            self._update_bar()
            return
        self._progress += diff * 0.18  # плавний easing
        self._update_bar()
        self.after(18, self._animate)

    def _update_bar(self):
        fill_width = 2 + (self.width-4) * (self._progress / 100.0)
        self.coords(self._bar, 
                    *self._rounded_rect_coords(2, 2, fill_width, self.height-2, self.radius)
        )

    def _rounded_rect_coords(self, x1, y1, x2, y2, r):
        return [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
    def set_bar_color(self, color):
        self.fg = color
        # Перемалювати бар з новим кольором
        self.itemconfig(self._bar, fill=self.fg)

# ========== Екран завантаження з fade-in/out і плавним індикатором ==========
class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Завантаження TechCare")
        self.window.geometry("440x220")
        self.window.configure(bg=DARK_BG)
        self.window.resizable(False, False)
        # Центруємо
        w, h = 440, 220
        x = (root.winfo_screenwidth() - w)//2
        y = (root.winfo_screenheight() - h)//2
        self.window.geometry(f"{w}x{h}+{x}+{y}")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self._alpha = 0.0
        self.window.attributes("-alpha", self._alpha)
        self.create_widgets()
        
        self._fade_in()

    

    def create_widgets(self):
        frame = tk.Frame(self.window, bg=DARK_BG)
        frame.pack(expand=True, fill="both")

        self.logo = tk.Label(frame, text="🪐", font=("Segoe UI", 56), bg=DARK_BG, fg=ACCENT)
        self.logo.pack(pady=(10, 6))
        frame.config(highlightbackground=SHADOW, highlightthickness=5)

        self.title = tk.Label(frame, text="TechCare", font=("Segoe UI", 23, "bold"), bg=DARK_BG, fg=ACCENT)
        self.title.pack(pady=(0, 5))

        self.progress = SmoothProgressBar(frame, width=290, height=16, fg=ACCENT, bg=CARD_BG)
        self.progress.pack(pady=(18, 2))

        self.status = tk.Label(frame, text="Запуск...", font=("Segoe UI", 10), fg=TEXT_FADED, bg=DARK_BG)
        self.status.pack(pady=(2, 0))
        self.percent = tk.Label(frame, text="0%", font=("Segoe UI", 11, "bold"), fg=ACCENT, bg=DARK_BG)
        self.percent.pack()

    def update_progress(self, value, message):
        self.progress.set_progress(value, animate=True)
        self.percent.config(text=f"{int(value)}%")
        self.status.config(text=message)
        self.window.update_idletasks()

    def _fade_in(self):
        if self._alpha < 1.0:
            self._alpha += 0.04
            self.window.attributes("-alpha", self._alpha)
            self.window.after(12, self._fade_in)

    def close(self):
        self._fade_out()

    def _fade_out(self):
        if self._alpha > 0:
            self._alpha -= 0.07
            self.window.attributes("-alpha", max(0, self._alpha))
            self.window.after(12, self._fade_out)
        else:
            self.window.destroy()

class TechCareGUI:
    def __init__(self, update_callback):
        self.update_callback = update_callback
        self.app_ref = None
        self.root = tk.Tk()
        self.root.withdraw()
        self.loading_screen = LoadingScreen(self.root)
        self.root.update_idletasks()
        self.root.update()
        self.loading_screen.update_progress(15, "Ініціалізація інтерфейсу...")
        self.setup_window()
        self.create_tray_icon()
        self.loading_screen.update_progress(40, "Створення віджетів...")
        self.create_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.metric_targets = {
            'cpu': 0,
            'ram': 0,
            'disk': 0,
            
        }
        self.metric_current = {
            'cpu': 0,
            'ram': 0,
            'disk': 0,
            
        }
        self.animating_metrics = False
        self.start_metrics_animation()
        self.app_ref = None
        self.loading_screen.update_progress(80, "Підготовка системи...")
        self.last_alerts = {
            "cpu": datetime.min,
            
            "disk": datetime.min,
            "ram": datetime.min,
            "backup": datetime.min
        }
        self.alert_cooldown = timedelta(minutes=60) # 60 хвилин між сповіщеннями одного типу
       

    # функція для контролю частоти повідомлень
    def can_alert(self, alert_type):
        now = datetime.now()
        if now - self.last_alerts.get(alert_type, datetime.min) > self.alert_cooldown:
            self.last_alerts[alert_type] = now
            return True
        return False

    def finish_loading(self):
        self.loading_screen.update_progress(100, "Готово!")
        time.sleep(0.1)
        self.loading_screen.close()
        self.root.deiconify()
        self.root.update()

    def setup_window(self):
        self.root.title("TechCare 2025")
        self.root.geometry("700x820")
        self.root.configure(bg=DARK_BG)
        self.root.resizable(True, True)
        self.root.minsize(640, 700)
        # Шрифт по дефолту для всіх віджетів
        self.root.option_add("*Font", ("Segoe UI", 11))
        # Власний стиль для ttk (темний фон)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=DARK_BG, borderwidth=0)
        style.configure('TNotebook.Tab', background=CARD_BG, foreground=ACCENT, padding=(18, 8), font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                  background=[('selected', CARD_BG), ('active', ACCENT_FADE)],
                  foreground=[('selected', ACCENT), ('active', ACCENT_2)])
        style.configure('TFrame', background=DARK_BG)
        style.configure('TLabel', background=DARK_BG, foreground=TEXT_MAIN)
        style.configure('TButton', background=CARD_BG, foreground=ACCENT, borderwidth=0)
        # Scrollbar dark
        style.configure("Vertical.TScrollbar", background=CARD_BG, troughcolor=DARK_BG, bordercolor=SHADOW)

    def start_metrics_animation(self):
        # Запускає регулярне плавне оновлення метрик (кожні 35мс)
        self.animating_metrics = True
        self.animate_metrics()
    
    def auto_update_metrics(self):
        if self.app_ref and hasattr(self.app_ref, 'data_manager'):
            data = self.app_ref.data_manager.get_current_metrics()
            if data:
                self.update_main_metrics(data)
        self.root.after(2000, self.auto_update_metrics)

    def animate_metrics(self):
        # Плавно наближує поточні значення до цільових
        changed = False
        for key in self.metric_targets:
            cur = self.metric_current[key]
            target = self.metric_targets[key]
            # Змінюємо повільно
            diff = target - cur
            if abs(diff) > 0.2:
                self.metric_current[key] += diff * 0.23  # Чим менше — тим плавніше
                changed = True
            else:
                self.metric_current[key] = target
        # Оновлюємо віджети
        self.cpu_label.config(text=f"{int(self.metric_current['cpu'])}%")
        self.cpu_bar.set_progress(self.metric_current['cpu'])
        self.ram_label.config(text=f"{int(self.metric_current['ram'])}%")
        self.ram_bar.set_progress(self.metric_current['ram'])
        self.disk_label.config(text=f"{int(self.metric_current['disk'])}%")
        self.disk_bar.set_progress(self.metric_current['disk'])
        
        # Повторити через 35мс, якщо ще анімується
        if self.animating_metrics:
            self.root.after(35, self.animate_metrics)

    def create_widgets(self):
        # Хедер з назвою
        self.create_modern_header()

        # Вкладки
        self.tab_control = ttk.Notebook(self.root, style='TNotebook')
        self.tab_control.pack(fill='both', expand=True, padx=12, pady=(5, 12))

        # Головна вкладка
        self.create_main_tab()

        # AI-Tab — сучасний аналітичний
        self.ai_tab = AITab(self.tab_control, self.app_ref)
        self.tab_control.add(self.ai_tab.frame, text="AI Аналітика")

        self.hardware_tab = tk.Frame(self.tab_control, bg=DARK_BG)
        self.tab_control.add(self.hardware_tab, text="Складові ПК")
        self.hardware_initialized = False  # Флаг ініціалізації

        def on_tab_change(event):
            selected = event.widget.index("current")
            tab_text = event.widget.tab(selected, "text")
            if tab_text == "Складові ПК" and not self.hardware_initialized:
                self.create_hardware_info_tab()
                self.hardware_initialized = True

        self.tab_control.bind("<<NotebookTabChanged>>", on_tab_change)
    #    Вкладки для інших функцій
        self.create_achievements_tab()
        self.create_schedule_tab()

        self.create_status_bar()
        self.create_help_tab()

        

       

    def create_modern_header(self):
        header = tk.Frame(self.root, bg=DARK_BG, height=76)
        header.pack(fill='x', padx=0, pady=(10, 7))
        header.pack_propagate(False)
        # Тінь/лінія
        shadow = tk.Frame(header, bg=ACCENT_FADE, height=3)
        shadow.pack(fill='x', side='bottom')
        # Назва
        label = tk.Label(header, text="TechCare 2025", font=("Segoe UI", 21, "bold"), bg=DARK_BG, fg=ACCENT)
        label.pack(pady=(8, 0))
        subtitle = tk.Label(header, text="Захист. Аналітика. Продуктивність.", font=("Segoe UI", 11), bg=DARK_BG, fg=TEXT_FADED)
        subtitle.pack()

    def create_status_bar(self):
        bar = tk.Frame(self.root, bg=SHADOW, height=30)
        bar.pack(fill='x', side='bottom')
        bar.pack_propagate(False)
        self.status_label = tk.Label(bar, text="🟢 Готовий до роботи", bg=SHADOW, fg=ACCENT, font=("Segoe UI", 10, "bold"))
        self.status_label.pack(side='left', padx=10, pady=0)

    # ======== ГОЛОВНА ВКЛАДКА — сучасні метрики =======
    def create_main_tab(self):
        main = ttk.Frame(self.tab_control)
        self.tab_control.add(main, text="Головна")

        wrapper = tk.Frame(main, bg=DARK_BG)
        wrapper.pack(fill="both", expand=True, padx=26, pady=22)

        title = tk.Label(wrapper, text="Основні показники системи", font=("Segoe UI", 15, "bold"), bg=DARK_BG, fg=ACCENT)
        title.pack(pady=(5, 20))

        # Сітка 2x3 з анімованими метриками
        grid = tk.Frame(wrapper, bg=DARK_BG)
        grid.pack(expand=True)
        grid.grid_columnconfigure((0, 1, 2), weight=1)
        grid.grid_rowconfigure((0, 1), weight=1)

        # CPU
        self.cpu_card = self.create_metric_card(grid, "💻 CPU", "0%", 0, 0, ACCENT_2)
        self.cpu_label = self.cpu_card["value"]
        self.cpu_bar = self.cpu_card["bar"]

        # RAM
        self.ram_card = self.create_metric_card(grid, "🧠 RAM", "0%", 0, 1, ACCENT)
        self.ram_label = self.ram_card["value"]
        self.ram_bar = self.ram_card["bar"]

        # Диск
        self.disk_card = self.create_metric_card(grid, "💾 Диск", "0%", 0, 2, YELLOW)
        self.disk_label = self.disk_card["value"]
        self.disk_bar = self.disk_card["bar"]

       

        # Аптайм
        self.uptime_card = self.create_metric_card(grid, "⏰ Час роботи", "—", 1, 2, GREEN)
        self.uptime_label = self.uptime_card["value"]
        self.uptime_bar = self.uptime_card["bar"]

        # Вікна
        self.windows_card = self.create_metric_card(grid, "🔲 Вікна", "0", 1, 1, ACCENT_2)
        self.windows_label = self.windows_card["value"]
        self.windows_bar = self.windows_card["bar"]

        # GPU (поки що просто як місце для майбутнього)
        self.gpu_card = self.create_metric_card(grid, "🎮 GPU", "—", 1, 0, "#80FFD0")
        self.gpu_label = self.gpu_card["value"]
        self.gpu_bar = self.gpu_card["bar"]

        

        # Оновити
        btn_frame = tk.Frame(wrapper, bg=DARK_BG)
        btn_frame.pack(pady=22)
        self.create_modern_button(btn_frame, "🔄 Оновити дані", self.update_callback, width=210)

    def create_metric_card(self, parent, title, value, row, col, bar_color):
        card = tk.Frame(parent, bg=CARD_BG, bd=0, highlightthickness=0)
        card.grid(row=row, column=col, padx=16, pady=14, sticky='nsew')
        card.grid_propagate(False)
        card.config(width=180, height=116)
        t = tk.Label(card, text=title, font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=ACCENT)
        t.pack(anchor="nw", padx=12, pady=(10, 0))
        v = tk.Label(card, text=value, font=("Segoe UI", 24, "bold"), bg=CARD_BG, fg=TEXT_MAIN)
        v.pack(anchor="center", pady=(0, 8))
        bar = SmoothProgressBar(card, width=142, height=12, fg=bar_color, bg=ACCENT_FADE)
        bar.pack(pady=(0, 8), padx=14, anchor="center")
        return {"frame": card, "value": v, "bar": bar}

    def create_modern_button(self, parent, text, command, width=160):
        b = tk.Button(
            parent, text=text, font=("Segoe UI", 11, "bold"),
            bg=ACCENT_FADE, fg=ACCENT,
            activebackground=ACCENT, activeforeground=DARK_BG,
            bd=0, relief="flat", cursor="hand2",
            width=int(width//10), pady=8,
            highlightthickness=0, highlightbackground=ACCENT)
        b.pack(padx=6, pady=0)
        b.bind("<Enter>", lambda e: b.config(bg=ACCENT, fg=DARK_BG))
        b.bind("<Leave>", lambda e: b.config(bg=ACCENT_FADE, fg=ACCENT))
        b.config(command=command)
        return b

    def add_event_to_outlook(self, subject, body, start_time):
        # Додає подію у Outlook календар
        try:
            vbs = f'''
Set olApp = CreateObject("Outlook.Application")
Set olNS = olApp.GetNamespace("MAPI")
Set olCalendar = olNS.GetDefaultFolder(9)
Set olAppt = olCalendar.Items.Add()
olAppt.Subject = "{subject}"
olAppt.Body = "{body}"
olAppt.Start = "{start_time.strftime('%m/%d/%Y %H:%M')}"
olAppt.Duration = 30
olAppt.ReminderSet = True
olAppt.Save
'''
            with open("addevent.vbs", "w") as f:
                f.write(vbs)
            subprocess.Popen(["wscript.exe", "addevent.vbs"])
        except Exception as e:
            self.show_notification("Календар", f"Не вдалося додати подію: {e}")

    # ========= API для оновлення метрик =========
    def update_main_metrics(self, data):
        # Оновлення індикаторів
        self.metric_targets['cpu'] = data.get("cpu_percent", 0)
        self.metric_targets['ram'] = data.get("ram_percent", 0)
        self.metric_targets['disk'] = data.get("disk_percent", 0)

        window_count = data.get("window_count", 0)
        self.windows_label.config(text=f"{window_count}")
        self.windows_bar.set_progress(min(window_count, 100))
        
        cpu = data.get("cpu_percent", 0)
        self.cpu_label.config(text=f"{int(cpu)}%")
        self.cpu_bar.set_progress(cpu)
        ram = data.get("ram_percent", 0)
        self.ram_label.config(text=f"{int(ram)}%")
        self.ram_bar.set_progress(ram)
        disk = data.get("disk_percent", 0)
        self.disk_label.config(text=f"{int(disk)}%")
        self.disk_bar.set_progress(disk)
       
        uptime_hours = data.get("uptime_hours", 0)
        uptime_minutes = data.get("uptime_minutes", 0)
        uptime_total_min = uptime_hours * 60 + uptime_minutes
        uptime_str = data.get("uptime_str", "—")

        # Оновлення GPU
        gpu_load = data.get("gpu_load")
        if gpu_load is not None:
            self.gpu_label.config(text=f"{gpu_load:.0f}%")
            self.gpu_bar.set_progress(gpu_load)
        else:
            self.gpu_label.config(text="Н/Д")
            self.gpu_bar.set_progress(0)

        # Оновлення аптайму
        progress = min(uptime_total_min / (24 * 60) * 100, 100)
        self.uptime_bar.set_progress(progress)
        if uptime_hours >= 24:
            self.uptime_bar.set_bar_color("#E65F53")  
            if not hasattr(self, "notified_uptime_over_24") or not self.notified_uptime_over_24:
                self.show_notification(
                    "Uptime > 24 год",
                    "Комп’ютер працює більше доби! Рекомендуємо перезавантажити."
                )
                self.notified_uptime_over_24 = True
        else:
            self.uptime_bar.set_bar_color("#6bf9d3")  
            self.notified_uptime_over_24 = False

        self.uptime_label.config(text=uptime_str)

        # SMART-логіка, інтеграція з календарем і system tray!
        disk_free = data.get('disk_percent_free', 100)
        # --- Smart-попередження!
        if cpu > 90 and self.can_alert("cpu"):
            self.show_notification("Високе навантаження", "Ваш процесор завантажений >90%.")
            self.show_tray_notification("Високе навантаження", "Ваш процесор завантажений >90%.")
            self.smart_add_schedule_task("Перевірити фонові процеси", "18:00")
            self.show_reminder_options(
                "Високе навантаження CPU",
                "Рекомендовано закрити непотрібні програми для зниження навантаження.",
                datetime.now()
            )
        
        if disk_free < 10 and self.can_alert("disk"):
            self.show_notification("Мало вільного місця", "Залишилось менше 10% місця на диску!")
            self.show_tray_notification("Мало вільного місця", "Залишилось менше 10% місця на диску!")
            self.smart_add_schedule_task("Очистити диск C", "20:00")
            self.show_reminder_options(
                "Очищення диску",
                "Рекомендовано очистити диск C для стабільної роботи.",
                datetime.now()
            )
        if ram > 90 and self.can_alert("ram"):
            self.show_notification("Мало оперативної пам'яті", "Використання ОЗП перевищило 90%.")
            self.show_tray_notification("Мало оперативної пам'яті", "Використання ОЗП перевищило 90%.")
            self.smart_add_schedule_task("Перезавантажити комп'ютер", "21:00")
            self.show_reminder_options(
                "Перевантаження ОЗП",
                "Рекомендуємо перезавантажити комп'ютер для звільнення пам'яті.",
                datetime.now()
            )
        # Smart-планування бекапу
        last_backup = None
        if self.app_ref and hasattr(self.app_ref, 'data_manager') and hasattr(self.app_ref.data_manager, 'get_last_backup_time'):
            last_backup = self.app_ref.data_manager.get_last_backup_time()
        if not last_backup or datetime.now() - last_backup > timedelta(days=7):
            if self.can_alert("backup"):
                self.smart_add_schedule_task("Зробити резервну копію", "18:30")
                self.show_notification("Рекомендуємо бекап", "Не робили резервну копію більше тижня!")
                self.show_tray_notification("Бекап", "Не забувайте робити резервні копії щотижня!")
                self.show_reminder_options(
                    "Зробити резервну копію",
                    "Рекомендуємо зробити резервну копію важливих файлів.",
                    datetime.now()
                )

    
    def shutdown(self): # Завершення роботи програми
        self.auto_collect_running = False
        if hasattr(self, 'tray_icon'):
            try:
                self.tray_icon.stop()
            except Exception:
                pass
        self.root.quit()
        self.root.destroy()
        print("GUI закритий")


    def smart_add_schedule_task(self, name, time):
        # Перевіряє, чи є вже така задача — не дублює!
        for i in range(self.scheduled_listbox.size()):
            if name in self.scheduled_listbox.get(i):
                return
        self.scheduled_listbox.insert(tk.END, f"{name} о {time}")

    def set_app_ref(self, app_ref):
        self.app_ref = app_ref
        if hasattr(self, 'ai_tab'):
            self.ai_tab.app_ref = app_ref
            self.ai_tab.update_ai_analysis()
        self.auto_update_metrics()
        

    def show_reminder_options(self, subject, body, default_time=None):
        """
        Показує pop-up для вибору способу нагадування (календар/email).
        subject — тема/назва нагадування, body — текст
        default_time — datetime для календаря (можна None)
        """
        popup = tk.Toplevel(self.root)
        popup.title("Додати нагадування")
        popup.configure(bg=CARD_BG)
        popup.geometry("380x210+{}+{}".format(self.root.winfo_x()+60, self.root.winfo_y()+120))
        popup.resizable(False, False)
        popup.grab_set()  # Фіксуємо фокус

        label = tk.Label(popup, text="Як хочете отримати нагадування?", font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=ACCENT)
        label.pack(pady=(18,10), padx=10)
        tk.Label(popup, text=subject, bg=CARD_BG, fg=TEXT_MAIN, font=("Segoe UI", 11)).pack(pady=(0,10))

        def add_to_calendar():
            time = default_time or datetime.now()
            self.show_reminder_options(subject, body, time)
            self.show_notification("Календар", "Подія додана в Outlook!")
            popup.destroy()

        def send_email():
            def send():
                email = email_entry.get().strip()
                if not email or "@" not in email:
                    status.config(text="❗ Введіть коректний email!", fg="red")
                    return
                self.send_email_reminder(subject, body, email)
                self.show_notification("Пошта", f"Нагадування надіслано на {email}")
                popup.destroy()

            for widget in popup.winfo_children():
                widget.destroy()
            tk.Label(popup, text="Введіть email:", bg=CARD_BG, fg=TEXT_MAIN, font=("Segoe UI", 11)).pack(pady=(30, 5))
            email_entry = tk.Entry(popup, font=("Segoe UI", 11), width=30)
            email_entry.pack(pady=5)
            status = tk.Label(popup, text="", bg=CARD_BG, fg=ACCENT)
            status.pack()
            tk.Button(popup, text="Надіслати", command=send, bg=ACCENT_2, fg=TEXT_MAIN,
                    font=("Segoe UI", 11, "bold"), relief="flat", padx=16, pady=4).pack(pady=(14, 6))

        btn_frame = tk.Frame(popup, bg=CARD_BG)
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="Додати до Outlook", command=add_to_calendar,
                bg=ACCENT, fg=DARK_BG, font=("Segoe UI", 11, "bold"), relief="flat", padx=14, pady=5).pack(side='left', padx=10)
        tk.Button(btn_frame, text="Надіслати email", command=send_email,
                bg=ACCENT_2, fg=DARK_BG, font=("Segoe UI", 11, "bold"), relief="flat", padx=14, pady=5).pack(side='left', padx=10)
        tk.Button(popup, text="Скасувати", command=popup.destroy,
                bg=SHADOW, fg=ACCENT, font=("Segoe UI", 10), relief="flat", padx=8, pady=3).pack(pady=(4,8))
        
    def send_email_reminder(self, subject, body, to_email):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"]    = "forchatix@gmail.com"     # ваша реальна адреса
        msg["To"]      = to_email
        try:
            s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            # сюди вставте App Password, згенерований у налаштуваннях Google
            s.login("forchatix@gmail.com", "yhsq kvjt ldmd gdgf")
            # ТУТ має бути точно така ж адреса, що в login()
            s.sendmail("forchatix@gmail.com", [to_email], msg.as_string())
            s.quit()
        except Exception as e:
            self.show_notification("Помилка пошти", str(e))

# Точка входу (factory для main.py)
    def create_gui(update_callback):
        return TechCareGUI(update_callback)
    

    def plot_history(self):
        from json_data import JsonDataManager
        manager = JsonDataManager()
        history = manager.get_historical_data()
        if not history:
            return

        timestamps = [entry["timestamp"].split('T')[1].split('.')[0] for entry in history[-15:]]
        
        cpu = [entry.get("cpu_percent", 0) for entry in history[-15:]]
        ram = [entry.get("ram_percent", 0) for entry in history[-15:]]

        fig, ax = plt.subplots(figsize=(7, 4), facecolor=DARK_BG)
        ax.set_facecolor(CARD_BG)

        
        ax.plot(timestamps, cpu, label="CPU (%)", color=GREEN, linewidth=2.3)
        ax.plot(timestamps, ram, label="RAM (%)", color=RED, linewidth=2.3)

        ax.set_title("Історія показників системи", color=ACCENT, fontsize=14, fontweight='bold')
        ax.set_xlabel("Час", color=TEXT_MAIN)
        ax.set_ylabel("Значення", color=TEXT_MAIN)
        ax.tick_params(axis='x', labelrotation=45, colors=TEXT_FADED)
        ax.tick_params(axis='y', colors=TEXT_FADED)
        for spine in ax.spines.values():
            spine.set_color(ACCENT_FADE)
        ax.legend(facecolor=DARK_BG, edgecolor=ACCENT, labelcolor=ACCENT, fontsize=9)

        fig.tight_layout()

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_achievements_tab(self):
        achievements_frame = tk.Frame(self.tab_control, bg=DARK_BG)
        self.tab_control.add(achievements_frame, text="Досягнення")

        title = tk.Label(achievements_frame, text="🏆 Досягнення та прогрес",
                        font=("Segoe UI", 14, "bold"), fg=ACCENT, bg=DARK_BG)
        title.pack(pady=(16, 10))

        # Level
        level_frame = tk.Frame(achievements_frame, bg=CARD_BG, highlightbackground=YELLOW, highlightthickness=2)
        level_frame.pack(fill='x', padx=22, pady=(0, 20), ipady=8)
        level_title = tk.Label(level_frame, text="⭐ Ваш рівень", font=("Segoe UI", 12), fg=TEXT_FADED, bg=CARD_BG)
        level_title.pack(pady=(7, 2))
        self.level_label = tk.Label(level_frame, text="Рівень 1 (0 очок)",
                                    font=("Segoe UI", 16, "bold"), fg=YELLOW, bg=CARD_BG)
        self.level_label.pack()

        # List of achievements
        achievements_list_frame = tk.Frame(achievements_frame, bg=CARD_BG, highlightbackground=ACCENT_2, highlightthickness=2)
        achievements_list_frame.pack(fill='both', expand=True, padx=22, pady=(0, 18), ipady=8)

        achievements_title = tk.Label(achievements_list_frame, text="🎯 Список досягнень",
                                    font=("Segoe UI", 12, "bold"), fg=ACCENT, bg=CARD_BG)
        achievements_title.pack(pady=(7, 3))

        list_container = tk.Frame(achievements_list_frame, bg=CARD_BG)
        list_container.pack(fill='both', expand=True, padx=8, pady=(0, 15))

        self.achievements_listbox = tk.Listbox(list_container, bg=SHADOW, fg=TEXT_MAIN,
                                            font=("Segoe UI", 10),
                                            selectbackground=ACCENT_2,
                                            selectforeground=DARK_BG,
                                            relief='flat', bd=0,
                                            activestyle='none', highlightthickness=0)
        self.achievements_listbox.pack(side='left', fill='both', expand=True)

        achievements_scrollbar = tk.Scrollbar(list_container, bg=CARD_BG,
                                            troughcolor=SHADOW,
                                            activebackground=ACCENT_2)
        achievements_scrollbar.pack(side='right', fill='y')
        self.achievements_listbox.config(yscrollcommand=achievements_scrollbar.set)
        achievements_scrollbar.config(command=self.achievements_listbox.yview)

        self.update_achievements_display()

    def update_achievements_display(self):
        if self.app_ref and hasattr(self.app_ref, 'data_manager') and hasattr(self.app_ref, 'achievements'):
            user_stats = self.app_ref.data_manager.get_user_stats()
            total_points = user_stats.get('total_points', 0)
            level = self.app_ref.achievements.get_user_level(total_points)
            self.level_label.config(text=f"Рівень {level} ({total_points} очок)")

            self.achievements_listbox.delete(0, tk.END)
            all_achievements = self.app_ref.achievements.get_all_achievements()
            for ach_id, achievement in all_achievements.items():
                is_unlocked = self.app_ref.achievements.is_achievement_unlocked(ach_id)
                status = "✓" if is_unlocked else "✗"
                color = ACCENT if is_unlocked else TEXT_FADED
                self.achievements_listbox.insert(tk.END, f"{status} {achievement['name']} - {achievement['description']}")
                self.achievements_listbox.itemconfig(tk.END, fg=color)
        else:
            self.level_label.config(text="Рівень 1 (0 очок)")
            self.achievements_listbox.delete(0, tk.END)
            self.achievements_listbox.insert(tk.END, "✗ Перший запуск - Запустити TechCare")

    def create_schedule_tab(self):
        schedule_tab = tk.Frame(self.tab_control, bg=DARK_BG)
        self.tab_control.add(schedule_tab, text="Розклад")

        title = tk.Label(schedule_tab, text="🗓️ Заплановані завдання",
                        font=("Segoe UI", 14, "bold"), fg=ACCENT, bg=DARK_BG)
        title.pack(pady=(14, 10))

        # Форма для додавання завдання
        form_frame = tk.Frame(schedule_tab, bg=CARD_BG)
        form_frame.pack(fill='x', padx=20, pady=(0, 18))

        name_label = tk.Label(form_frame, text="Назва:", font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_FADED)
        name_label.grid(row=0, column=0, sticky="e", pady=5, padx=6)
        self.task_name_entry = tk.Entry(form_frame, bg=SHADOW, fg=TEXT_MAIN, insertbackground=ACCENT, relief="flat", font=("Segoe UI", 11), width=20)
        self.task_name_entry.grid(row=0, column=1, pady=5, padx=6)

        time_label = tk.Label(form_frame, text="Час (ГГ:ХХ):", font=("Segoe UI", 10), bg=CARD_BG, fg=TEXT_FADED)
        time_label.grid(row=1, column=0, sticky="e", pady=5, padx=6)
        self.task_time_entry = tk.Entry(form_frame, bg=SHADOW, fg=TEXT_MAIN, insertbackground=ACCENT, relief="flat", font=("Segoe UI", 11), width=8)
        self.task_time_entry.grid(row=1, column=1, pady=5, padx=6, sticky="w")

        add_btn = tk.Button(form_frame, text="➕ Додати",
                            font=("Segoe UI", 11, "bold"),
                            bg=ACCENT_2, fg=TEXT_MAIN,
                            activebackground=ACCENT, activeforeground=DARK_BG,
                            relief="flat", bd=0, padx=18, pady=4, cursor="hand2",
                            command=self.add_schedule_task)
        add_btn.grid(row=0, column=2, rowspan=2, padx=(14, 6), pady=5)
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg=ACCENT, fg=DARK_BG))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg=ACCENT_2, fg=TEXT_MAIN))

        # Список запланованих
        list_frame = tk.Frame(schedule_tab, bg=CARD_BG)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 18))

        self.scheduled_listbox = tk.Listbox(list_frame, bg=SHADOW, fg=TEXT_MAIN, font=("Segoe UI", 10),
                                            selectbackground=ACCENT_2, selectforeground=DARK_BG,
                                            relief="flat", bd=0, activestyle='none', highlightthickness=0)
        self.scheduled_listbox.pack(side="left", fill="both", expand=True, padx=(0, 0), pady=(4, 4))

        scroll = tk.Scrollbar(list_frame, bg=CARD_BG, troughcolor=SHADOW)
        scroll.pack(side="right", fill="y")
        self.scheduled_listbox.config(yscrollcommand=scroll.set)
        scroll.config(command=self.scheduled_listbox.yview)

        self.load_schedule_tasks()

    def add_schedule_task(self):
        name = self.task_name_entry.get().strip()
        t = self.task_time_entry.get().strip()
        if not name or not t:
            self.status_label.config(text="❗️ Введіть всі поля!")
            return
        # Валідація формату часу (груба)
        import re
        if not re.match(r"^\d{1,2}:\d{2}$", t):
            self.status_label.config(text="❗️ Час має бути у форматі ГГ:ХХ")
            return
        task = f"{name} о {t}"
        self.scheduled_listbox.insert(tk.END, task)
        self.status_label.config(text="🟢 Завдання додано!")
        # Можна зберігати у data_manager чи json:
        if hasattr(self, 'app_ref') and self.app_ref and hasattr(self.app_ref, 'data_manager'):
            self.app_ref.data_manager.save_scheduled_task({"name": name, "time": t})

    def load_schedule_tasks(self):
        self.scheduled_listbox.delete(0, tk.END)
        # Якщо є менеджер даних:
        if hasattr(self, 'app_ref') and self.app_ref and hasattr(self.app_ref, 'data_manager'):
            # Приклад:
            # tasks = self.app_ref.data_manager.get_scheduled_tasks()
            tasks = []  # (бо в json_data це stub, але якщо реалізуєш — воно буде тут)
            for task in tasks:
                self.scheduled_listbox.insert(tk.END, f"{task['name']} о {task['time']}")

    def show_notification(self, title, message, duration=3400):
        # Сучасний toast поверх усіх вікон, fade-in/fade-out
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.configure(bg=ACCENT)
        toast.attributes("-topmost", True)
        w, h = 340, 88
        x = self.root.winfo_x() + (self.root.winfo_width() - w)//2
        y = self.root.winfo_y() + 56
        toast.geometry(f"{w}x{h}+{x}+{y}")

        frame = tk.Frame(toast, bg=ACCENT, bd=0)
        frame.pack(fill="both", expand=True)
        title_lbl = tk.Label(frame, text=title, font=("Segoe UI", 12, "bold"), bg=ACCENT, fg=DARK_BG)
        title_lbl.pack(pady=(14, 2), padx=10, anchor="w")
        msg_lbl = tk.Label(frame, text=message, font=("Segoe UI", 10), bg=ACCENT, fg=DARK_BG, wraplength=w-28, justify="left")
        msg_lbl.pack(pady=(2, 8), padx=14, anchor="w")

        

        def fade_out(alpha=1.0):
            alpha -= 0.09
            if alpha <= 0:
                toast.destroy()
            else:
                toast.attributes("-alpha", max(alpha, 0))
                toast.after(25, lambda: fade_out(alpha))
        # Fade-in
        toast.attributes("-alpha", 0.0)
        def fade_in(alpha=0.0):
            alpha += 0.10
            if alpha >= 1.0:
                toast.attributes("-alpha", 1.0)
                toast.after(duration, fade_out)
            else:
                toast.attributes("-alpha", alpha)
                toast.after(18, lambda: fade_in(alpha))
        fade_in()
    def create_tray_icon(self):
    # Створюємо іконку для трей-менеджера
        img = Image.new('RGBA', (64, 64), (30, 40, 50, 255))
        d = ImageDraw.Draw(img)
        d.ellipse((8, 8, 56, 56), fill="#80FFD0")
        self.tray_icon = pystray.Icon("TechCare", img, "TechCare Smart Reminder")
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_tray_notification(self, title, message):
        # Показати balloon-tip у system tray (тільки якщо tray icon створена)
        if hasattr(self, 'tray_icon'):
            self.tray_icon.notify(message, title)

    def create_help_tab(self):
        help_tab = tk.Frame(self.tab_control, bg=DARK_BG)
        self.tab_control.add(help_tab, text="Гід")
        guide = (
            "🟢 Коротка інструкція користувача:\n"
            "\n"
            "• На головній сторінці відображаються основні метрики системи: CPU, RAM, Диск, Кількість вікон, Час роботи\n"
            "• Вкладка 'AI Аналітика' — отримай поради щодо стану ПК на основі аналітики\n"
            "• Вкладка 'Історія' — переглядай графіки змін показників системи\n"
            "• 'Досягнення' — дивись свій прогрес і нові відкриті ачивки\n"
            "• 'Розклад' — плануй обслуговування (додавай свої завдання!)\n"
            "\n"
            "📢 Програма автоматично попереджає про перевищення навантаження чи проблеми (CPU, RAM, диск)\n"
            "• Всі нагадування можуть дублюватися через системний tray, email, або календар (опційно)\n"
            "\n"
            "🛡️ Корисні поради по догляду за ПК:\n"
            "• Чистіть системний блок від пилу кожні 3-6 місяців\n"
            "• Робіть резервні копії важливих файлів\n"
            "• Оновлюйте антивірус і драйвери\n"
            "• Видаляйте непотрібні файли та програми\n"
            "• Не перевантажуйте систему великою кількістю одночасних вікон\n"
            "• Контролюйте використання ресурсів через TechCare!\n"
        )
        txt = tk.Text(help_tab, bg=CARD_BG, fg=TEXT_MAIN, font=("Segoe UI", 11), wrap="word", relief="flat")
        txt.insert(tk.END, guide)
        txt.config(state="disabled")
        txt.pack(fill="both", expand=True, padx=14, pady=12)

    def on_close(self):
        self.animating_metrics = False
        try:
            if hasattr(self, "tray_icon"):
                self.tray_icon.stop()
        except Exception:
            pass
        self.root.destroy()
        import os
        os._exit(0)
    
    def fill_hardware_info(self, frame):
        # Очистити фрейм
        for widget in frame.winfo_children():
            widget.destroy()

        import platform
        import psutil

        # Дані про систему
        try:
            cpu = platform.processor()
            cpu_count = psutil.cpu_count(logical=True)
            ram = psutil.virtual_memory().total // (1024**3)
            system = platform.system()
            release = platform.release()
            machine = platform.machine()
            node = platform.node()
            gpu = "—"  # Якщо треба — підключити GPU інфо через сторонні бібліотеки
            disks = psutil.disk_partitions()
            disk_str = ""
            for d in disks:
                usage = psutil.disk_usage(d.mountpoint)
                disk_str += f"{d.device}: {usage.total//(1024**3)} ГБ  "

            items = [
                ("Система", f"{system} {release} ({machine})"),
                ("Комп'ютер", node),
                ("Процесор", f"{cpu} ({cpu_count} потоків)"),
                ("Оперативна пам'ять", f"{ram} ГБ"),
                ("Диски", disk_str),
                # ("Відеокарта", gpu), # якщо потрібно
            ]
        except Exception as e:
            items = [("Помилка", str(e))]

        for label, val in items:
            row = tk.Frame(frame, bg=DARK_BG)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=label + ":", font=("Segoe UI", 11, "bold"),
                    bg=DARK_BG, fg=ACCENT, width=14, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=("Segoe UI", 11),
                    bg=DARK_BG, fg=TEXT_MAIN, anchor="w", wraplength=420, justify="left").pack(side="left", fill="x", expand=True)

    
    def create_hardware_info_tab(self):
        import platform
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            gpu_info = gpus[0].name if gpus else "—"
        except Exception:
            gpu_info = "Н/Д"
        try:
            import psutil
            ram = f"{round(psutil.virtual_memory().total / (1024 ** 3), 1)} GB"
        except Exception:
            ram = "Н/Д"
        info = [
            ("Процесор", platform.processor()),
            ("Система", f"{platform.system()} {platform.release()}"),
            ("Архітектура", platform.machine()),
            ("Відеокарта", gpu_info),
            ("ОЗП", ram),
            ("Ім'я ПК", platform.node())
        ]
        for widget in self.hardware_tab.winfo_children():
            widget.destroy()  # Очищення вкладки при повторному виклику
        title = tk.Label(self.hardware_tab, text="🛠️ Складові ПК", font=("Segoe UI", 14, "bold"), fg=ACCENT, bg=DARK_BG)
        title.pack(pady=(16, 10))
        for name, val in info:
            frame = tk.Frame(self.hardware_tab, bg=CARD_BG)
            frame.pack(fill="x", padx=24, pady=6)
            label = tk.Label(frame, text=name, font=("Segoe UI", 11, "bold"), fg=ACCENT_2, bg=CARD_BG, width=14, anchor="w")
            label.pack(side="left")
            value = tk.Label(frame, text=val, font=("Segoe UI", 11), fg=TEXT_MAIN, bg=CARD_BG, anchor="w")
            value.pack(side="left", padx=(16,0))

    


def create_gui(update_callback):
    return TechCareGUI(update_callback)

