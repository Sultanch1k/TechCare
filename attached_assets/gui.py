# -*- coding: utf-8 -*-
"""
TechCare - GUI Module
Модуль графічного інтерфейсу користувача
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import threading
import time
from datetime import datetime

class TechCareGUI:
    def __init__(self, update_callback):
        self.update_callback = update_callback
        self.root = tk.Tk()
        self.setup_window()
        self.setup_fonts()
        self.create_widgets()
        self.setup_updates()
        
    def setup_window(self):
        """Налаштування основного вікна"""
        self.root.title("TechCare")
        self.root.geometry("450x600")
        self.root.configure(bg="#1E1E1E")
        self.root.resizable(False, False)
        
        # Створення градієнтного фону
        self.create_gradient_background()
        
    def create_gradient_background(self):
        """Створює градієнтний фон від #1E1E1E до #2D2D2D"""
        # Симуляція градієнта через кілька кольорових смуг
        colors = [
            "#1E1E1E", "#202020", "#222222", "#242424", 
            "#262626", "#282828", "#2A2A2A", "#2C2C2C", "#2D2D2D"
        ]
        
        self.gradient_frame = tk.Frame(self.root, bg="#1E1E1E")
        self.gradient_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        stripe_height = 500 // len(colors)
        for i, color in enumerate(colors):
            stripe = tk.Frame(self.gradient_frame, bg=color, height=stripe_height)
            stripe.place(x=0, y=i * stripe_height, relwidth=1, height=stripe_height)
    
    def setup_fonts(self):
        """Налаштування шрифтів"""
        try:
            self.title_font = font.Font(family="Roboto", size=16, weight="bold")
            self.subtitle_font = font.Font(family="Roboto", size=10)
            self.label_font = font.Font(family="Roboto", size=12)
            self.value_font = font.Font(family="Roboto", size=12, weight="bold")
            self.button_font = font.Font(family="Roboto", size=10)
        except:
            # Fallback на системні шрифти
            self.title_font = font.Font(size=16, weight="bold")
            self.subtitle_font = font.Font(size=10)
            self.label_font = font.Font(size=12)
            self.value_font = font.Font(size=12, weight="bold")
            self.button_font = font.Font(size=10)
    
    def create_widgets(self):
        """Створює всі віджети інтерфейсу"""
        # Основний контейнер
        self.main_frame = tk.Frame(self.root, bg="#1E1E1E")
        self.main_frame.place(x=10, y=10, width=380, height=480)
        
        # Заголовок
        self.title_label = tk.Label(
            self.main_frame,
            text="TechCare",
            font=self.title_font,
            fg="#00DDEB",
            bg="#1E1E1E"
        )
        self.title_label.pack(pady=(10, 5))
        
        # Підзаголовок
        self.subtitle_label = tk.Label(
            self.main_frame,
            text="Твій помічник для догляду за ПК",
            font=self.subtitle_font,
            fg="#BBBBBB",
            bg="#1E1E1E"
        )
        self.subtitle_label.pack(pady=(0, 20))
        
        # Секція моніторингу
        self.create_monitoring_section()
        
        # Секція рекомендацій
        self.create_recommendations_section()
        
        # Секція кнопок
        self.create_buttons_section()
    
    def create_monitoring_section(self):
        """Створює секцію моніторингу"""
        # Контейнер для параметрів
        monitor_frame = tk.Frame(self.main_frame, bg="#1E1E1E")
        monitor_frame.pack(pady=10, padx=10, fill="x")
        
        # Параметри для відображення
        self.monitor_labels = {}
        self.monitor_values = {}
        
        parameters = [
            ("temp", "Температура:"),
            ("uptime", "Час роботи:"),
            ("ram", "RAM:"),
            ("disk", "Диск:"),
            ("fan", "Вентилятори:"),
            ("drivers", "Драйвери:"),
            ("health", "Здоров'я ПК:")
        ]
        
        for param, label_text in parameters:
            self.create_parameter_row(monitor_frame, param, label_text)
    
    def create_parameter_row(self, parent, param, label_text):
        """Створює рядок з параметром"""
        # Контейнер для параметра
        param_frame = tk.Frame(
            parent,
            bg="#2D2D2D",
            highlightbackground="#00DDEB",
            highlightthickness=1
        )
        param_frame.pack(fill="x", pady=2, padx=5)
        
        # Мітка параметра
        label = tk.Label(
            param_frame,
            text=label_text,
            font=self.label_font,
            fg="#FFFFFF",
            bg="#2D2D2D",
            anchor="w"
        )
        label.pack(side="left", padx=10, pady=5)
        
        # Значення параметра
        value = tk.Label(
            param_frame,
            text="Н/Д",
            font=self.value_font,
            fg="#00FF66",
            bg="#2D2D2D",
            anchor="e"
        )
        value.pack(side="right", padx=10, pady=5)
        
        self.monitor_labels[param] = label
        self.monitor_values[param] = value
    
    def create_recommendations_section(self):
        """Створює секцію рекомендацій"""
        # Контейнер рекомендацій
        rec_frame = tk.Frame(
            self.main_frame,
            bg="#333333",
            highlightbackground="#00DDEB",
            highlightthickness=1
        )
        rec_frame.pack(pady=20, padx=10, fill="x")
        
        # Текст статусу
        self.status_label = tk.Label(
            rec_frame,
            text="Статус: Усе в нормі",
            font=self.label_font,
            fg="#00FF66",
            bg="#333333",
            wraplength=350,
            justify="left"
        )
        self.status_label.pack(padx=10, pady=10)
    
    def create_buttons_section(self):
        """Створює секцію кнопок"""
        buttons_frame = tk.Frame(self.main_frame, bg="#1E1E1E")
        buttons_frame.pack(pady=20, fill="x")
        
        # Перший рядок кнопок
        row1 = tk.Frame(buttons_frame, bg="#1E1E1E")
        row1.pack(pady=5)
        
        self.clear_btn = self.create_button(row1, "Очистити", self.clear_action)
        self.clear_btn.pack(side="left", padx=5)
        
        self.postpone_btn = self.create_button(row1, "Відкласти", self.postpone_action)
        self.postpone_btn.pack(side="left", padx=5)
        
        # Другий рядок кнопок
        row2 = tk.Frame(buttons_frame, bg="#1E1E1E")
        row2.pack(pady=5)
        
        self.details_btn = self.create_button(row2, "Деталі", self.details_action)
        self.details_btn.pack(side="left", padx=5)
        
        self.refresh_btn = self.create_button(row2, "Оновити", self.refresh_action)
        self.refresh_btn.pack(side="left", padx=5)
        
        # Третій рядок кнопок для додаткових функцій
        row3 = tk.Frame(buttons_frame, bg="#1E1E1E")
        row3.pack(pady=5)
        
        self.optimization_btn = self.create_button(row3, "Оптимізація", self.optimization_action)
        self.optimization_btn.pack(side="left", padx=5)
        
        self.analysis_btn = self.create_button(row3, "Аналіз", self.analysis_action)
        self.analysis_btn.pack(side="left", padx=5)
    
    def create_button(self, parent, text, command):
        """Створює стилізовану кнопку"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=self.button_font,
            bg="#333333",
            fg="#FFFFFF",
            activebackground="#00DDEB",
            activeforeground="#FFFFFF",
            highlightbackground="#00DDEB",
            highlightthickness=1,
            width=12,
            relief="flat",
            cursor="hand2"
        )
        
        # Ефект наведення
        def on_enter(e):
            btn.configure(bg="#00DDEB", fg="#000000")
        
        def on_leave(e):
            btn.configure(bg="#333333", fg="#FFFFFF")
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def update_display(self, data, status=None, advanced_data=None):
        """Оновлює відображення даних з розширеною інформацією"""
        try:
            # Оновлення температури
            if data.get('cpu_temp') is not None:
                temp_text = f"{int(data['cpu_temp'])}°C"
                temp_color = "#FF6347" if data['cpu_temp'] > 70 else "#00FF66"
            else:
                temp_text = f"{int(data['cpu_percent'])}%"
                temp_color = "#FF6347" if data['cpu_percent'] > 80 else "#00FF66"
            
            self.monitor_values['temp'].configure(text=temp_text, fg=temp_color)
            
            # Оновлення часу роботи
            uptime_color = "#FF6347" if data['uptime_seconds'] > 86400 else "#00FF66"
            self.monitor_values['uptime'].configure(text=data['uptime_str'], fg=uptime_color)
            
            # Оновлення RAM
            ram_text = f"{int(data['ram_percent'])}%"
            ram_color = "#FF6347" if data['ram_percent'] > 90 else "#00FF66"
            self.monitor_values['ram'].configure(text=ram_text, fg=ram_color)
            
            # Оновлення диска
            disk_text = f"{int(data['disk_percent'])}%"
            disk_color = "#FF6347" if data['disk_percent'] > 90 else "#00FF66"
            self.monitor_values['disk'].configure(text=disk_text, fg=disk_color)
            
            # Оновлення вентиляторів з розширеною логікою
            if advanced_data and 'fan_details' in advanced_data:
                fan_details = advanced_data['fan_details']
                if fan_details['total_fans'] > 0:
                    fan_text = f"{fan_details['working_fans']}/{fan_details['total_fans']}"
                    if fan_details['status'] == 'critical':
                        fan_color = "#FF0000"
                    elif fan_details['status'] == 'warning':
                        fan_color = "#FF6347"
                    elif fan_details['status'] == 'good':
                        fan_color = "#00FF66"
                    else:
                        fan_color = "#BBBBBB"
                else:
                    fan_text = "Н/Д"
                    fan_color = "#BBBBBB"
            else:
                # Fallback до старої логіки
                if data.get('fan_speed') is not None:
                    fan_text = f"{int(data['fan_speed'])} RPM"
                    fan_color = "#FF6347" if data['fan_speed'] > 4000 else "#00FF66"
                else:
                    fan_text = "Н/Д"
                    fan_color = "#BBBBBB"
            
            self.monitor_values['fan'].configure(text=fan_text, fg=fan_color)
            
            # Оновлення драйверів
            if advanced_data and 'driver_status' in advanced_data:
                driver_status = advanced_data['driver_status']
                if driver_status['status'] == 'unavailable':
                    driver_text = "Недоступно"
                    driver_color = "#BBBBBB"
                else:
                    driver_text = f"Застарілих: {len(driver_status.get('outdated_drivers', []))}"
                    if driver_status['status'] == 'critical':
                        driver_color = "#FF0000"
                    elif driver_status['status'] == 'warning':
                        driver_color = "#FF6347"
                    else:
                        driver_color = "#00FF66"
            else:
                driver_text = "Завантаження..."
                driver_color = "#BBBBBB"
                
            self.monitor_values['drivers'].configure(text=driver_text, fg=driver_color)
            
            # Оновлення загального здоров'я
            if advanced_data and 'health_score' in advanced_data:
                health_score = advanced_data['health_score']
                health_text = f"{health_score['score']}/100"
                health_color = health_score['color']
            else:
                health_text = "Аналіз..."
                health_color = "#BBBBBB"
                
            self.monitor_values['health'].configure(text=health_text, fg=health_color)
            
            # Оновлення статусу
            if status:
                status_text, status_color = status
                self.status_label.configure(text=f"Статус: {status_text}", fg=status_color)
            elif advanced_data and 'health_score' in advanced_data:
                health_score = advanced_data['health_score']
                self.status_label.configure(
                    text=f"Статус: {health_score['level']} ({health_score['score']}/100)", 
                    fg=health_score['color']
                )
            
        except Exception as e:
            print(f"Помилка при оновленні дисплея: {e}")
    
    def show_notification(self, title, message, bg_color="#FFFFFF"):
        """Показує анімоване сповіщення"""
        # Створення вікна сповіщення
        notif = tk.Toplevel(self.root)
        notif.title(title)
        notif.geometry("300x100")
        notif.configure(bg=bg_color)
        notif.attributes("-topmost", True)
        notif.resizable(False, False)
        
        # Позиціонування у правому верхньому кутку
        notif.geometry("+{}+{}".format(
            self.root.winfo_rootx() + 400,
            self.root.winfo_rooty()
        ))
        
        # Заголовок сповіщення
        title_label = tk.Label(
            notif,
            text=title,
            font=self.value_font,
            fg="#FF6347",
            bg=bg_color
        )
        title_label.pack(pady=10)
        
        # Повідомлення
        msg_label = tk.Label(
            notif,
            text=message,
            font=self.label_font,
            fg="#000000",
            bg=bg_color,
            wraplength=280
        )
        msg_label.pack(pady=5)
        
        # Автоматичне закриття через 5 секунд
        notif.after(5000, notif.destroy)
    
    def clear_action(self):
        """Дія кнопки Очистити"""
        try:
            result = self.update_callback.clear_state()
            self.show_notification(
                "Очищення виконано",
                result,
                "#E6FFE6"
            )
        except Exception as e:
            print(f"Помилка при очищенні: {e}")
    
    def postpone_action(self):
        """Дія кнопки Відкласти"""
        try:
            result = self.update_callback.postpone_reminders()
            self.show_notification(
                "Нагадування відкладено",
                result,
                "#FFFFCC"
            )
        except Exception as e:
            print(f"Помилка при відкладенні: {e}")
    
    def details_action(self):
        """Дія кнопки Деталі"""
        try:
            history = self.update_callback.get_history()
            
            # Створення вікна деталей
            details_window = tk.Toplevel(self.root)
            details_window.title("Деталі системи")
            details_window.geometry("400x300")
            details_window.configure(bg="#1E1E1E")
            
            # Заголовок
            title_label = tk.Label(
                details_window,
                text="Історія та деталі",
                font=self.title_font,
                fg="#00DDEB",
                bg="#1E1E1E"
            )
            title_label.pack(pady=10)
            
            # Список деталей
            details_frame = tk.Frame(details_window, bg="#2D2D2D")
            details_frame.pack(pady=10, padx=10, fill="both", expand=True)
            
            for detail in history:
                detail_label = tk.Label(
                    details_frame,
                    text=f"• {detail}",
                    font=self.label_font,
                    fg="#FFFFFF",
                    bg="#2D2D2D",
                    anchor="w",
                    justify="left"
                )
                detail_label.pack(fill="x", pady=2, padx=10)
            
        except Exception as e:
            print(f"Помилка при відображенні деталей: {e}")
    
    def refresh_action(self):
        """Дія кнопки Оновити"""
        try:
            self.update_callback.manual_update()
        except Exception as e:
            print(f"Помилка при оновленні: {e}")
    
    def optimization_action(self):
        """Дія кнопки Оптимізація - показує рекомендації для покращення"""
        try:
            recommendations = self.update_callback.get_optimization_tips()
            
            # Створення вікна оптимізації
            opt_window = tk.Toplevel(self.root)
            opt_window.title("Рекомендації з оптимізації")
            opt_window.geometry("500x400")
            opt_window.configure(bg="#1E1E1E")
            
            # Заголовок
            title_label = tk.Label(
                opt_window,
                text="Поради для покращення продуктивності",
                font=self.title_font,
                fg="#00DDEB",
                bg="#1E1E1E"
            )
            title_label.pack(pady=10)
            
            # Скролабельна область для рекомендацій
            canvas = tk.Canvas(opt_window, bg="#2D2D2D", highlightthickness=0)
            scrollbar = tk.Scrollbar(opt_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#2D2D2D")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Додавання рекомендацій
            for i, rec in enumerate(recommendations):
                rec_frame = tk.Frame(scrollable_frame, bg="#333333", pady=5)
                rec_frame.pack(fill="x", pady=5, padx=10)
                
                # Пріоритет кольором
                priority_colors = {
                    'high': '#FF6347',
                    'medium': '#FFA500', 
                    'low': '#90EE90'
                }
                priority_color = priority_colors.get(rec['priority'], '#BBBBBB')
                
                # Категорія
                cat_label = tk.Label(
                    rec_frame,
                    text=f"[{rec['category']}]",
                    font=self.value_font,
                    fg=priority_color,
                    bg="#333333"
                )
                cat_label.pack(anchor="w", padx=5)
                
                # Проблема
                issue_label = tk.Label(
                    rec_frame,
                    text=f"Проблема: {rec['issue']}",
                    font=self.label_font,
                    fg="#FFFFFF",
                    bg="#333333",
                    wraplength=450,
                    justify="left"
                )
                issue_label.pack(anchor="w", padx=5)
                
                # Рекомендація
                rec_label = tk.Label(
                    rec_frame,
                    text=f"Рішення: {rec['recommendation']}",
                    font=self.label_font,
                    fg="#00FF66",
                    bg="#333333",
                    wraplength=450,
                    justify="left"
                )
                rec_label.pack(anchor="w", padx=5, pady=(0, 5))
            
            canvas.pack(side="left", fill="both", expand=True, padx=10)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            print(f"Помилка при відображенні оптимізації: {e}")
    
    def analysis_action(self):
        """Дія кнопки Аналіз - показує детальний аналіз системи"""
        try:
            analysis_data = self.update_callback.get_detailed_analysis()
            
            # Створення вікна аналізу
            analysis_window = tk.Toplevel(self.root)
            analysis_window.title("Детальний аналіз системи")
            analysis_window.geometry("600x500")
            analysis_window.configure(bg="#1E1E1E")
            
            # Заголовок
            title_label = tk.Label(
                analysis_window,
                text="Повний аналіз здоров'я системи",
                font=self.title_font,
                fg="#00DDEB",
                bg="#1E1E1E"
            )
            title_label.pack(pady=10)
            
            # Notebook для вкладок
            from tkinter import ttk
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('TNotebook', background='#1E1E1E')
            style.configure('TNotebook.Tab', background='#333333', foreground='#FFFFFF')
            
            notebook = ttk.Notebook(analysis_window)
            
            # Вкладка "Автозапуск"
            startup_frame = tk.Frame(notebook, bg="#2D2D2D")
            startup_info = analysis_data.get('startup', {})
            
            startup_label = tk.Label(
                startup_frame,
                text=f"Програм в автозапуску: {startup_info.get('total_count', 0)}\n"
                     f"Час завантаження: {startup_info.get('startup_time_estimate', 'невідомо')}\n"
                     f"Рекомендація: {startup_info.get('recommendation', 'немає')}",
                font=self.label_font,
                fg="#FFFFFF",
                bg="#2D2D2D",
                justify="left",
                wraplength=550
            )
            startup_label.pack(pady=20, padx=20)
            
            notebook.add(startup_frame, text="Автозапуск")
            
            # Вкладка "Диски"
            disk_frame = tk.Frame(notebook, bg="#2D2D2D")
            disk_info = analysis_data.get('disk_health', {})
            
            disk_text = f"Дисків: {disk_info.get('total_disks', 0)}\n"
            disk_text += f"Здорових: {disk_info.get('healthy_disks', 0)}\n"
            if disk_info.get('warnings'):
                disk_text += "Попередження:\n" + "\n".join(disk_info['warnings'])
            
            disk_label = tk.Label(
                disk_frame,
                text=disk_text,
                font=self.label_font,
                fg="#FFFFFF",
                bg="#2D2D2D",
                justify="left",
                wraplength=550
            )
            disk_label.pack(pady=20, padx=20)
            
            notebook.add(disk_frame, text="Диски")
            
            # Вкладка "Мережа"
            network_frame = tk.Frame(notebook, bg="#2D2D2D")
            network_info = analysis_data.get('network', {})
            
            network_text = f"Активних з'єднань: {network_info.get('active_connections', 0)}\n"
            network_text += f"DNS відгук: {network_info.get('dns_response_time', 'невідомо')}\n"
            network_text += f"Відправлено: {network_info.get('bytes_sent', 0)} МБ\n"
            network_text += f"Отримано: {network_info.get('bytes_received', 0)} МБ"
            
            network_label = tk.Label(
                network_frame,
                text=network_text,
                font=self.label_font,
                fg="#FFFFFF",
                bg="#2D2D2D",
                justify="left"
            )
            network_label.pack(pady=20, padx=20)
            
            notebook.add(network_frame, text="Мережа")
            
            # Вкладка "Безпека"
            security_frame = tk.Frame(notebook, bg="#2D2D2D")
            security_info = analysis_data.get('security', {})
            
            security_text = f"Антивірус: {security_info.get('antivirus_status', 'невідомо')}\n"
            security_text += f"Брандмауер: {security_info.get('firewall_status', 'невідомо')}\n"
            security_text += f"Бал безпеки: {security_info.get('security_score', 0)}/100\n"
            security_text += f"Статус: {security_info.get('overall_status', 'невідомо')}"
            
            security_label = tk.Label(
                security_frame,
                text=security_text,
                font=self.label_font,
                fg="#FFFFFF",
                bg="#2D2D2D",
                justify="left"
            )
            security_label.pack(pady=20, padx=20)
            
            notebook.add(security_frame, text="Безпека")
            
            notebook.pack(expand=True, fill="both", padx=10, pady=10)
            
        except Exception as e:
            print(f"Помилка при відображенні аналізу: {e}")
    
    def setup_updates(self):
        """Налаштування автоматичних оновлень"""
        def update_loop():
            while True:
                try:
                    self.root.after(0, self.update_callback.periodic_update)
                    time.sleep(10)  # Оновлення кожні 10 секунд
                except Exception as e:
                    print(f"Помилка в циклі оновлень: {e}")
                    time.sleep(10)
        
        # Запуск циклу оновлень в окремому потоці
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def run(self):
        """Запуск GUI"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Програму зупинено користувачем")
        except Exception as e:
            print(f"Помилка GUI: {e}")

def create_gui(update_callback):
    """Створює та повертає GUI"""
    return TechCareGUI(update_callback)

if __name__ == "__main__":
    # Тестування GUI
    class MockCallback:
        def periodic_update(self):
            pass
        
        def manual_update(self):
            pass
        
        def clear_state(self):
            return "Тест очищення"
        
        def postpone_reminders(self):
            return "Тест відкладення"
        
        def get_history(self):
            return ["Тестова історія 1", "Тестова історія 2"]
    
    gui = create_gui(MockCallback())
    gui.run()
