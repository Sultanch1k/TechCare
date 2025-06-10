import tkinter as tk
from tkinter import ttk
from monitor import get_system_data, get_network_data
from tests import SimpleTests
import matplotlib.pyplot as plt

# Кольори (як у твоєму gui.py)
DARK_BG    = "#181D23"
CARD_BG    = "#232A33"
ACCENT     = "#80FFD0"
ACCENT_2   = "#44A6FF"
TEXT_MAIN  = "#E9F6F2"
TEXT_FADED = "#92A6B6"
RED        = "#FF6384"
YELLOW     = "#FFD580"
GREEN      = "#B6FFB0"
SHADOW     = "#1A222C"

try:
    from gui import SmoothProgressBar
except ImportError:
    class SmoothProgressBar(tk.Canvas):
        def __init__(self, parent, width=220, height=16, bg="#1A222C", fg="#44A6FF", radius=12, **kwargs):
            super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0, bd=0, **kwargs)
            self.fg = fg
        def set_progress(self, v, animate=True): pass

class AITab:
    def __init__(self, parent, app_ref):
        self.frame = tk.Frame(parent, bg=DARK_BG)
        self.app_ref = app_ref
        self.auto_refresh_enabled = tk.BooleanVar(value=True)
        self.last_score = 0
        self._init_ui()
        self._auto_refresh()
        

    def _init_ui(self):
        tk.Label(self.frame, text="🤖 AI Аналітика", font=("Segoe UI", 15, "bold"), fg=ACCENT, bg=DARK_BG).pack(pady=(16, 5))

        # SCORE + прогресбар
        bar_frame = tk.Frame(self.frame, bg=DARK_BG)
        bar_frame.pack(pady=(0, 10))
        self.health_label = tk.Label(bar_frame, text="🧠 AI Health Score: --%", font=("Segoe UI", 13, "bold"), fg=ACCENT, bg=DARK_BG)
        self.health_label.pack()
        self.health_bar = SmoothProgressBar(bar_frame, width=210, height=16, fg=ACCENT_2, bg=SHADOW)
        self.health_bar.pack(pady=(4, 0))
        self.status_canvas = tk.Canvas(bar_frame, width=32, height=32, bg=DARK_BG, highlightthickness=0, bd=0)
        self.status_canvas.pack(pady=(6, 2))
        self._draw_status_circle(0)

        # Порада
        self.advice_label = tk.Label(self.frame, text="", font=("Segoe UI", 12), bg=DARK_BG, fg=YELLOW, wraplength=340, justify="left")
        self.advice_label.pack(pady=(3, 11))

        # Деталізація
        self.predictions_text = tk.Text(self.frame, height=8, bg=CARD_BG, fg=TEXT_MAIN, insertbackground=ACCENT, font=("Consolas", 11), relief="flat", bd=0, wrap="word", padx=8, pady=6)
        self.predictions_text.pack(fill="both", expand=True, padx=12, pady=(4, 8))
        self.predictions_text.config(state="disabled")
        self.predictions_text.tag_configure("warn", foreground=YELLOW)
        self.predictions_text.tag_configure("error", foreground=RED)
        self.predictions_text.tag_configure("success", foreground=GREEN)
        self.predictions_text.tag_configure("pred", foreground=ACCENT_2)

        # Кнопки
        btn_fr = tk.Frame(self.frame, bg=DARK_BG)
        btn_fr.pack(pady=(0, 8))
        self._refresh_btn = tk.Button(btn_fr, text="🔄 Оновити AI аналіз", font=("Segoe UI", 11, "bold"),
            bg=ACCENT_2, fg=TEXT_MAIN, activebackground=ACCENT, activeforeground=DARK_BG,
            relief="flat", bd=0, padx=22, pady=6, cursor="hand2", highlightthickness=0,
            command=self.update_ai_analysis)
        self._refresh_btn.pack(side="left", padx=8)
        self.trend_btn = tk.Button(btn_fr, text="📈 Тренд", font=("Segoe UI", 11),
            bg=SHADOW, fg=ACCENT, relief="flat", bd=0, command=self._show_trend)
        self.trend_btn.pack(side="left", padx=8)

        # Чекбокс
        self.auto_checkbox = tk.Checkbutton(self.frame, text="Автооновлення", variable=self.auto_refresh_enabled,
            onvalue=True, offvalue=False, bg=DARK_BG, fg=ACCENT,
            activebackground=DARK_BG, activeforeground=ACCENT, selectcolor=CARD_BG, font=("Segoe UI", 10, "bold"))
        self.auto_checkbox.pack()

    def _auto_refresh(self):
        if self.auto_refresh_enabled.get():
            self.update_ai_analysis()
        self.frame.after(10000, self._auto_refresh)

    def _draw_status_circle(self, score):
        color = GREEN if score >= 70 else YELLOW if score >= 45 else RED
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(4, 4, 28, 28, fill=color, outline="")

    def _show_trend(self):
        # 1) Перевірки наявності даних
        if not self.app_ref or not hasattr(self.app_ref, "data_manager"):
            return
        history = self.app_ref.data_manager.get_historical_data(days=7)
        if not history:
            return

        # 2) Імпорти
        import matplotlib.pyplot as plt
        from datetime import datetime

        # 3) Підготовка даних
        # Конвертуємо ISO-рядок у datetime, щоб на осі Х було видно годину та хвилину
        times = [
            datetime.fromisoformat(h["timestamp"])
            for h in history[-30:]
        ]
        cpu   = [h.get("cpu_percent", 0)  for h in history[-30:]]
        ram   = [h.get("ram_percent", 0)  for h in history[-30:]]
        disk  = [h.get("disk_percent", 0) for h in history[-30:]]
        ai_sc = [100 - ((c + r) / 2)        for c, r in zip(cpu, ram)]

        # 4) Створюємо фігуру і вісь ПЕРЕД будь-яким викликом ax.plot
        fig, ax = plt.subplots(figsize=(8, 4), facecolor=DARK_BG)
        ax.set_facecolor(CARD_BG)

        # 5) Малюємо лінії
        ax.plot_date(times, cpu,   '-', label="CPU (%)", lw=2)
        ax.plot_date(times, ram,   '-', label="RAM (%)", lw=2)
        ax.plot_date(times, disk,  '-', label="Disk (%)", lw=2)
        ax.plot_date(times, ai_sc, '-', label="AI Health Score", lw=2)

        # 6) Оформлення
        ax.set_title("AI Тренд (CPU, RAM, Disk, AI Score)", color=ACCENT)
        ax.legend()
        fig.autofmt_xdate()          # повертаємо підписи дат під кутом
        fig.tight_layout()

        # 7) Показуємо графік
        plt.show()

    def update_ai_analysis(self):
        # Отримай дані (останній зібраний зріз)
        if not self.app_ref or not hasattr(self.app_ref, "data_manager"):
            return
        data = self.app_ref.data_manager.get_current_metrics()
        #
        cpu, ram, disk = data.get("cpu_percent", 0), \
                 data.get("ram_percent",   0), \
                 data.get("disk_percent",  0)

        # призначаємо ваги
        w_cpu, w_ram, w_disk = 0.4, 0.4, 0.2

        # інверсія навантаження
        usable_cpu  = 100 - cpu
        usable_ram  = 100 - ram
        usable_disk = 100 - disk

        # обчислення середньозваженого балу
        score_float = (usable_cpu * w_cpu +
                    usable_ram * w_ram +
                    usable_disk * w_disk)
        score = int(max(0, min(100, score_float)))

        self._animate_score(score)
        self._draw_status_circle(score)
        self.health_label.config(text=f"🧠 AI Health Score: {score}%")
        # Порада
        advice = ""
        if cpu > 90:
            advice = "🔴 Високе навантаження на процесор. Закрийте зайві програми."
        elif ram > 85:
            advice = "🟠 Високе використання пам'яті. Рекомендуємо перезавантажити ПК."
        elif disk > 90:
            advice = "🔴 Диск майже заповнений. Очистіть його."
        else:
            advice = "🟢 Система стабільна!"
        self.advice_label.config(text=advice)

        # Деталізація
        self.predictions_text.config(state="normal")
        self.predictions_text.delete(1.0, tk.END)
        self.predictions_text.insert(tk.END, f"CPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%\n", "bold")
        # Додати результати швидкого тесту диску
        try:
            disk_score = SimpleTests(self.app_ref.data_manager).run_disk_test().get("disk_score", 0)
            self.predictions_text.insert(tk.END, f"💽 Disk Speed Test: {disk_score}%\n", "pred")
        except Exception:
            pass
        # Мережа
        try:
            net = get_network_data(interval=1)
            recv, sent = net.get("net_recv_mb_s", 0), net.get("net_sent_mb_s", 0)
            self.predictions_text.insert(tk.END, f"📡 Мережа: ↓ {recv*8:.1f} Мбіт/с | ↑ {sent*8:.1f} Мбіт/с\n", "pred")
        except Exception:
            pass
        self.predictions_text.config(state="disabled")

    def _animate_score(self, target):
        # Плавно анімуй до target
        step = 2 if abs(self.last_score - target) > 10 else 1
        if self.last_score < target:
            self.last_score += step
            if self.last_score > target:
                self.last_score = target
            self.health_bar.set_progress(self.last_score)
            self.frame.after(15, lambda: self._animate_score(target))
        elif self.last_score > target:
            self.last_score -= step
            if self.last_score < target:
                self.last_score = target
            self.health_bar.set_progress(self.last_score)
            self.frame.after(15, lambda: self._animate_score(target))
        else:
            self.health_bar.set_progress(target)
