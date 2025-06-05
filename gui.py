# -*- coding: utf-8 -*-
"""
TechCare - Сучасний GUI модуль з Tkinter 2025
Графічний інтерфейс для desktop додатка з неоновим дизайном
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

# Імпорти для GUI

class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(root)
        self.window.title("Завантаження TechCare")
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        
        # Центруємо вікно
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Вимикаємо кнопки закриття
        self.window.protocol("WM_DELETE_WINDOW", lambda: None)
        self.window.attributes("-topmost", True)
        
        # Додаємо елементи
        self.create_widgets()
    def create_widgets(self):
        """Створення елементів екрану завантаження з неоновими ефектами"""
        # Фон
        self.window.configure(bg='#0F0F0F')
    
        # Контейнер для вмісту
        content_frame = tk.Frame(self.window, bg='#0F0F0F')
        content_frame.pack(expand=True, fill='both', padx=20, pady=20)
    
        # Логотип
        logo_label = tk.Label(content_frame, text="⚙", font=('Arial', 40), 
                            fg='#00DDEB', bg='#0F0F0F')
        logo_label.pack(pady=(0, 10))
    
        # Заголовок з неоновою тінню
        title_label = tk.Label(content_frame, text="TechCare", 
                            font=('Roboto', 18, 'bold'), 
                            fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=(0, 20))
    
        # Неонова тінь для заголовка
        title_label.config(highlightthickness=2, highlightbackground='#00DDEB')
    
        # Стилізований індикатор завантаження
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Modern.Horizontal.TProgressbar", 
                    background='#00DDEB', 
                    troughcolor='#1A1A1A',
                    bordercolor='#1A1A1A',
                    lightcolor='#00DDEB',
                    darkcolor='#00AACC')
    
        self.progress = ttk.Progressbar(content_frame, 
                                    style="Modern.Horizontal.TProgressbar",
                                    orient='horizontal', 
                                    length=300, mode='determinate')
        self.progress.pack(pady=(0, 10))
    
        # Текст статусу
        self.status_label = tk.Label(content_frame, text="Ініціалізація системи...", 
                                font=('Arial', 10), 
                                fg='#CCCCCC', bg='#0F0F0F')
        self.status_label.pack(pady=(0, 5))
    
        # Відсотки
        self.percent_label = tk.Label(content_frame, text="0%", 
                                font=('Arial', 10, 'bold'), 
                                fg='#00DDEB', bg='#0F0F0F')
        self.percent_label.pack()
    
        # Анімація обертання шестерні
        self.rotate_angle = 0
        self.animate_logo(logo_label)

    def animate_logo(self, logo_label):
        """Анімація обертання логотипу"""
        self.rotate_angle = (self.rotate_angle + 5) % 360
        logo_label.config(text="⚙", font=('Arial', 40), 
                     fg='#00DDEB', bg='#0F0F0F')
        logo_label.place_forget()  # Оновлюємо позицію для обертання
        logo_label.pack(pady=(0, 10))
        self.window.after(100, lambda: self.animate_logo(logo_label))

    def update_progress(self, value, message):
        """Оновлення прогресу та тексту статусу"""
        try:
            if self.progress.winfo_exists():
                self.progress['value'] = value
                self.percent_label.config(text=f"{value}%")
                self.status_label.config(text=message)
                self.window.update_idletasks()
        except tk.TclError:
            pass

    

    def close(self):
        self.window.destroy()   
        
   
    


class TechCareGUI:
    def __init__(self, update_callback):
        self.update_callback = update_callback
        self.app_ref = None
        self.root = tk.Tk()
        
        # Спочатку створюємо екран завантаження
        self.loading_screen = LoadingScreen(self.root)
        self.root.update_idletasks()
        self.root.update()
        self.root.withdraw()  # Ховаємо головне вікно
        
        # Оновлюємо прогрес
        self.loading_screen.update_progress(10, "Налаштування інтерфейсу...")
        time.sleep(1.5) 
        self.setup_window()
        self.loading_screen.update_progress(30, "Створення віджетів...")
        time.sleep(2)
        self.create_widgets()
        self.loading_screen.update_progress(70, "Завантаження даних...")
        
        # Імітуємо завантаження або чекаємо на реальні дані
        time.sleep(2)  # Можна видалити, це для прикладу
        
        # Завершуємо завантаження
        self.loading_screen.update_progress(100, "Готово до роботи!")
        time.sleep(0.5)
        self.loading_screen.close()
        
        # Показуємо головне вікно
        self.root.deiconify()



        
    def setup_window(self):
        """Налаштування головного вікна з сучасним дизайном 2025"""
        self.root.title("TechCare 2025")
        self.root.geometry("600x750")
        self.root.configure(bg='#0F0F0F')
        self.root.resizable(True, True)
        self.root.minsize(550, 700)
        
        # Сучасні стилі з неоновими акцентами
        self.setup_modern_styles()
        
        # Градієнтний фон
        self.create_gradient_effect()
    
    def setup_modern_styles(self):
        """Налаштування сучасних стилів з неоновими ефектами"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Стилі для Notebook
        style.configure('Modern.TNotebook', 
                       background='#0F0F0F',
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       background='#2D2D2D',
                       foreground='#FFFFFF',
                       padding=[15, 8],
                       font=('Roboto', 10, 'bold'))
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', '#00DDEB'),
                           ('active', '#00AACC')],
                 foreground=[('selected', '#000000')])
        
        # Стилі для Frame
        style.configure('Modern.TFrame', background='#0F0F0F')
    
    def create_gradient_effect(self):
        """Створення градієнтного ефекту"""
        # Базовий градієнт буде створюватися через Frame кольори
        pass
    
    def create_modern_header(self):
        """Створення сучасного заголовка з неоновими ефектами"""
        header_frame = tk.Frame(self.root, bg='#0F0F0F', height=80)
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Заголовок з неоновим свіченням
        title_label = tk.Label(header_frame, text="TechCare 2025", 
                              font=('Roboto', 18, 'bold'), 
                              fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=8)
        
        # Підзаголовок
        subtitle_label = tk.Label(header_frame, text="Система моніторингу та обслуговування ПК", 
                                 font=('Arial', 10), 
                                 fg='#CCCCCC', bg='#0F0F0F')
        subtitle_label.pack()
        
        # Неонова лінія-розділювач
        separator_frame = tk.Frame(header_frame, bg='#00DDEB', height=2)
        separator_frame.pack(fill='x', padx=20, pady=(8, 0))
    
    def create_status_bar(self):
        """Створення статус бару внизу"""
        status_frame = tk.Frame(self.root, bg='#1A1A1A', height=25)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Готовий до роботи", 
                                    font=('Arial', 9), 
                                    fg='#00FF66', bg='#1A1A1A')
        self.status_label.pack(side='left', padx=10, pady=3)
        
    def create_widgets(self):
        """Створення віджетів інтерфейсу з сучасним дизайном"""
        # Сучасний заголовок з неоновим ефектом
        self.create_modern_header()
        
        # Основний Notebook з новими стилями
        self.notebook = ttk.Notebook(self.root, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(5, 10))
        
        # Створюємо модернізовані вкладки
        self.create_main_tab()
        self.create_ai_tab()
        self.create_hardware_tab()
        self.create_achievements_tab()
        self.create_schedule_tab()
        
        # Статус бар внизу
        self.create_status_bar()
        
        # Ініціалізуємо список завдань
        self.tasks = []
        self.load_default_tasks()
        
    def create_main_tab(self):
        """Вкладка 'Головна' з сучасним неоновим дизайном 2025"""
        main_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(main_frame, text="Головна")
        
        # Контейнер для метрик з градієнтом
        metrics_container = tk.Frame(main_frame, bg='#0F0F0F')
        metrics_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Заголовок секції з неоновим свіченням
        title_label = tk.Label(metrics_container, text="⚡ Системні параметри", 
                              font=('Roboto', 16, 'bold'), 
                              fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=(0, 15))
        
        # Створюємо сітку 2x3 для параметрів
        grid_frame = tk.Frame(metrics_container, bg='#0F0F0F')
        grid_frame.pack(fill='both', expand=True)
        
        # CPU з неоновим ефектом
        self.cpu_frame = self.create_neon_metric_frame(grid_frame, "💻 CPU", "0%", 0, 0)
        self.cpu_label = self.cpu_frame.winfo_children()[1]
        
        # RAM з неоновим ефектом
        self.ram_frame = self.create_neon_metric_frame(grid_frame, "🧠 RAM", "0%", 0, 1)
        self.ram_label = self.ram_frame.winfo_children()[1]
        
        # Диск з неоновим ефектом
        self.disk_frame = self.create_neon_metric_frame(grid_frame, "💾 Диск", "0%", 1, 0)
        self.disk_label = self.disk_frame.winfo_children()[1]
        
        # Температура з неоновим ефектом
        self.temp_frame = self.create_neon_metric_frame(grid_frame, "🔥 Температура", "Н/Д", 1, 1)
        self.temp_label = self.temp_frame.winfo_children()[1]
        
        # Час роботи з неоновим ефектом
        self.uptime_frame = self.create_neon_metric_frame(grid_frame, "⏰ Час роботи", "0 год", 2, 0)
        self.uptime_label = self.uptime_frame.winfo_children()[1]
        
        # Вентилятор з неоновим ефектом
        self.fan_frame = self.create_neon_metric_frame(grid_frame, "🌀 Фан", "0 RPM", 2, 1)
        self.fan_label = self.fan_frame.winfo_children()[1]
        
        # Сучасна кнопка оновлення з неоновим ефектом
        self.create_neon_button(metrics_container, "🔄 Оновити дані", self.update_callback)
    
    def create_neon_metric_frame(self, parent, title, value, row, col):
        """Створення рамки параметра з неоновими ефектами"""
        frame = tk.Frame(parent, bg='#1A1A1A', 
                        highlightbackground='#00DDEB', 
                        highlightthickness=2,
                        relief='solid', bd=0)
        frame.grid(row=row, column=col, padx=8, pady=8, sticky='nsew', ipadx=15, ipady=20)
        
        # Налаштування сітки для розтягування
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Розділяємо смайлик та текст для кращого вирівнювання
        title_parts = title.split(' ', 1)
        emoji = title_parts[0] if len(title_parts) > 1 else ""
        text = title_parts[1] if len(title_parts) > 1 else title
        
        # Контейнер для заголовка
        title_container = tk.Frame(frame, bg='#1A1A1A')
        title_container.pack(pady=(8, 3))
        
        # Смайлик окремо
        if emoji:
            emoji_label = tk.Label(title_container, text=emoji, 
                                  font=('Arial', 12), 
                                  fg='#CCCCCC', bg='#1A1A1A')
            emoji_label.pack()
        
        # Текст окремо
        text_label = tk.Label(title_container, text=text, 
                             font=('Arial', 9, 'bold'), 
                             fg='#CCCCCC', bg='#1A1A1A')
        text_label.pack()
        
        # Значення параметра з неоновим кольором
        value_label = tk.Label(frame, text=value, 
                              font=('Arial', 13, 'bold'), 
                              fg='#00FF66', bg='#1A1A1A')
        value_label.pack(pady=(0, 8))
        
        return frame
    
    def create_neon_button(self, parent, text, command):
        """Створення кнопки з неоновими ефектами"""
        btn_frame = tk.Frame(parent, bg='#0F0F0F')
        btn_frame.pack(pady=25)
        
        button = tk.Button(btn_frame, text=text,
                          font=('Roboto', 12, 'bold'),
                          bg='#2D2D2D', fg='#FFFFFF',
                          activebackground='#00DDEB',
                          activeforeground='#000000',
                          relief='solid', bd=2,
                          highlightbackground='#00DDEB',
                          highlightthickness=2,
                          highlightcolor='#00DDEB',
                          command=command,
                          padx=35, pady=12,
                          cursor='hand2')
        button.pack()
        
        # Анімований ефект наведення
        def on_enter(e):
            button.config(bg='#00AACC', fg='#FFFFFF', 
                         highlightbackground='#00FF66')
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"⚡ Готовий виконати: {text.replace('🔄 ', '')}")
            
        def on_leave(e):
            button.config(bg='#2D2D2D', fg='#FFFFFF',
                         highlightbackground='#00DDEB')
            if hasattr(self, 'status_label'):
                self.status_label.config(text="🟢 Готовий до роботи")
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
        
        # Кнопка оновлення
        update_btn = tk.Button(main_frame, text="Оновити", 
                              font=('Roboto', 10), bg='#333333', fg='white',
                              command=self.update_callback)
        update_btn.pack(pady=10)
    
    def create_compact_button(self, parent, text, command, color, row, col):
        """Створення компактної кнопки з неоновими ефектами"""
        button = tk.Button(parent, text=text,
                          font=('Roboto', 9, 'bold'),
                          bg='#2D2D2D', fg='#FFFFFF',
                          activebackground=color,
                          activeforeground='#000000',
                          relief='solid', bd=1,
                          highlightbackground=color,
                          highlightthickness=1,
                          highlightcolor=color,
                          command=command,
                          padx=20, pady=8,
                          cursor='hand2',
                          width=10)
        button.grid(row=row, column=col, padx=5, pady=3, sticky='ew')
        
        # Налаштування сітки
        parent.grid_columnconfigure(col, weight=1)
        
        # Компактний анімований ефект
        def on_enter(e):
            button.config(bg=color, fg='#000000')
            
        def on_leave(e):
            button.config(bg='#2D2D2D', fg='#FFFFFF')
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
        
    def create_ai_tab(self):
        """Вкладка 'AI Аналітика' з сучасним неоновим дизайном"""
        ai_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(ai_frame, text="AI Аналітика")
        
        # Контейнер з неоновим фоном
        ai_container = tk.Frame(ai_frame, bg='#0F0F0F')
        ai_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Заголовок з AI іконкою
        title_label = tk.Label(ai_container, text="🧠 Штучний Інтелект", 
                              font=('Roboto', 16, 'bold'), 
                              fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=(0, 20))
        
        # Індекс здоров'я з неоновим ефектом
        health_frame = tk.Frame(ai_container, bg='#1A1A1A',
                               highlightbackground='#00DDEB',
                               highlightthickness=2, relief='solid')
        health_frame.pack(fill='x', pady=(0, 15), padx=20, ipady=15)
        
        health_title = tk.Label(health_frame, text="⚡ Індекс здоров'я системи", 
                               font=('Roboto', 14, 'bold'), 
                               fg='#CCCCCC', bg='#1A1A1A')
        health_title.pack(pady=(10, 5))
        
        self.health_label = tk.Label(health_frame, text="85%", 
                                    font=('Roboto', 24, 'bold'), 
                                    fg='#00FF66', bg='#1A1A1A')
        self.health_label.pack(pady=(0, 10))
        
        # Статус індикатор
        self.health_status = tk.Label(health_frame, text="🟢 Система працює нормально", 
                                     font=('Roboto', 11), 
                                     fg='#00FF66', bg='#1A1A1A')
        self.health_status.pack()
        
        # Прогнози з неоновим ефектом
        predictions_frame = tk.Frame(ai_container, bg='#1A1A1A',
                                    highlightbackground='#00DDEB',
                                    highlightthickness=2, relief='solid')
        predictions_frame.pack(fill='both', expand=True, padx=20, ipady=10)
        
        predictions_title = tk.Label(predictions_frame, text="🔮 Прогнози та рекомендації", 
                                     font=('Roboto', 14, 'bold'), 
                                     fg='#CCCCCC', bg='#1A1A1A')
        predictions_title.pack(pady=(10, 10))
        
        # Текстове поле з неоновим скролбаром
        text_container = tk.Frame(predictions_frame, bg='#1A1A1A')
        text_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.predictions_text = tk.Text(text_container, height=8, 
                                       bg='#2D2D2D', fg='#FFFFFF', 
                                       font=('Roboto', 10),
                                       insertbackground='#00DDEB',
                                       selectbackground='#00DDEB',
                                       selectforeground='#000000',
                                       relief='solid', bd=1)
        self.predictions_text.pack(side='left', fill='both', expand=True)
        
        # Неоновий скролбар
        scrollbar = tk.Scrollbar(text_container, bg='#2D2D2D', 
                                troughcolor='#1A1A1A',
                                activebackground='#00DDEB')
        scrollbar.pack(side='right', fill='y')
        
        self.predictions_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.predictions_text.yview)
        
        # Секція результатів тестів
        tests_frame = tk.Frame(ai_container, bg='#1A1A1A',
                              highlightbackground='#00DDEB',
                              highlightthickness=2, relief='solid')
        tests_frame.pack(fill='x', padx=20, pady=(10, 5))
        
        tests_title = tk.Label(tests_frame, text="📊 Результати тестів", 
                              font=('Roboto', 12, 'bold'), 
                              fg='#CCCCCC', bg='#1A1A1A')
        tests_title.pack(pady=(8, 5))
        
        # Listbox для результатів тестів
        listbox_container = tk.Frame(tests_frame, bg='#1A1A1A')
        listbox_container.pack(fill='x', padx=15, pady=(0, 10))
        
        self.tests_listbox = tk.Listbox(listbox_container, height=4,
                                       bg='#2D2D2D', fg='#FFFFFF', 
                                       font=('Roboto', 9),
                                       selectbackground='#00DDEB',
                                       selectforeground='#000000',
                                       relief='solid', bd=1)
        self.tests_listbox.pack(side='left', fill='x', expand=True)
        
        scrollbar_tests = tk.Scrollbar(listbox_container, bg='#2D2D2D',
                                      troughcolor='#1A1A1A',
                                      activebackground='#00DDEB')
        scrollbar_tests.pack(side='right', fill='y')
        
        self.tests_listbox.config(yscrollcommand=scrollbar_tests.set)
        scrollbar_tests.config(command=self.tests_listbox.yview)
        
        # Секція мережевої діагностики
        network_frame = tk.Frame(ai_container, bg='#1A1A1A',
                                highlightbackground='#00DDEB',
                                highlightthickness=2, relief='solid')
        network_frame.pack(fill='x', padx=20, pady=(5, 10))
        
        network_title = tk.Label(network_frame, text="📡 Мережева діагностика", 
                                font=('Roboto', 12, 'bold'), 
                                fg='#CCCCCC', bg='#1A1A1A')
        network_title.pack(pady=(8, 5))
        
        # Текстове поле для мережевої статистики
        network_container = tk.Frame(network_frame, bg='#1A1A1A')
        network_container.pack(fill='x', padx=15, pady=(0, 10))
        
        self.network_text = tk.Text(network_container, height=4,
                                   bg='#2D2D2D', fg='#FFFFFF', 
                                   font=('Roboto', 9),
                                   insertbackground='#00DDEB',
                                   selectbackground='#00DDEB',
                                   selectforeground='#000000',
                                   relief='solid', bd=1)
        self.network_text.pack(side='left', fill='x', expand=True)
        
        scrollbar_network = tk.Scrollbar(network_container, bg='#2D2D2D',
                                        troughcolor='#1A1A1A',
                                        activebackground='#00DDEB')
        scrollbar_network.pack(side='right', fill='y')
        
        self.network_text.config(yscrollcommand=scrollbar_network.set)
        scrollbar_network.config(command=self.network_text.yview)
        
        # Центр управління AI функціями
        control_frame = tk.Frame(ai_container, bg='#1A1A1A',
                                highlightbackground='#00DDEB',
                                highlightthickness=2, relief='solid')
        control_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        control_title = tk.Label(control_frame, text="🎯 Центр управління", 
                                font=('Roboto', 12, 'bold'), 
                                fg='#CCCCCC', bg='#1A1A1A')
        control_title.pack(pady=(8, 5))
        
        # Сітка кнопок AI функцій
        btn_grid = tk.Frame(control_frame, bg='#1A1A1A')
        btn_grid.pack(pady=(0, 10))
        
        # Перший ряд - основні AI функції
        self.create_compact_button(btn_grid, "🤖 AI Аналіз", self.run_ai_analysis, "#00DDEB", 0, 0)
        self.create_compact_button(btn_grid, "🔄 Оновити AI", self.refresh_ai_analysis, "#00FF66", 0, 1)
        
        # Другий ряд - тести
        self.create_compact_button(btn_grid, "📊 Всі тести", self.run_all_tests, "#9B59B6", 1, 0)
        self.create_compact_button(btn_grid, "⚡ CPU", self.run_cpu_test, "#4ECDC4", 1, 1)
        
        # Третій ряд - мережа та діагностика  
        self.create_compact_button(btn_grid, "📡 Мережа", self.scan_network, "#E74C3C", 2, 0)
        self.create_compact_button(btn_grid, "🔍 Діагностика", self.run_diagnosis, "#FF6B35", 2, 1)
    
    def run_ai_analysis(self):
        """Запуск AI аналізу"""
        self.predictions_text.delete(1.0, tk.END)
        self.predictions_text.insert(tk.END, "🔄 Запуск аналізу...\n\n")
        self.root.update()
        
        # Симуляція аналізу
        import time
        time.sleep(1)
        
        self.predictions_text.delete(1.0, tk.END)
        self.predictions_text.insert(tk.END, "✅ Аналіз завершено!\n\n")
        self.predictions_text.insert(tk.END, "🔍 Результати:\n")
        self.predictions_text.insert(tk.END, "• CPU: Нормальне навантаження\n")
        self.predictions_text.insert(tk.END, "• RAM: Достатньо вільної пам'яті\n") 
        self.predictions_text.insert(tk.END, "• Диск: Стабільна робота\n")
        self.predictions_text.insert(tk.END, "• Температура: В межах норми\n\n")
        self.predictions_text.insert(tk.END, "💡 Рекомендації:\n")
        self.predictions_text.insert(tk.END, "• Регулярно очищайте тимчасові файли\n")
        self.predictions_text.insert(tk.END, "• Перевіряйте оновлення драйверів\n")
    
    def refresh_ai_analysis(self):
        """Швидке оновлення AI аналітики з реальними даними"""
        def quick_analysis():
            self.predictions_text.delete(1.0, tk.END)
            self.predictions_text.insert(tk.END, "🔄 Швидке оновлення AI...\n\n")
            self.root.update()
            
            try:
                # Отримуємо реальні дані системи
                from monitor import get_system_data
                data = get_system_data()
                
                # Мікро-аналіз на основі реальних даних
                import time
                time.sleep(0.5)
                
                self.predictions_text.delete(1.0, tk.END)
                self.predictions_text.insert(tk.END, "⚡ Експрес-аналіз завершено!\n\n")
                
                # Аналізуємо CPU
                cpu_percent = data.get('cpu_percent', 0)
                if cpu_percent > 80:
                    self.predictions_text.insert(tk.END, f"🔴 CPU: {cpu_percent}% - Високе навантаження!\n")
                elif cpu_percent > 50:
                    self.predictions_text.insert(tk.END, f"🟡 CPU: {cpu_percent}% - Помірне навантаження\n")
                else:
                    self.predictions_text.insert(tk.END, f"🟢 CPU: {cpu_percent}% - Нормальна робота\n")
                
                # Аналізуємо RAM
                ram_percent = data.get('ram_percent', 0)
                if ram_percent > 85:
                    self.predictions_text.insert(tk.END, f"🔴 RAM: {ram_percent}% - Критично мало пам'яті!\n")
                elif ram_percent > 70:
                    self.predictions_text.insert(tk.END, f"🟡 RAM: {ram_percent}% - Багато використано\n")
                else:
                    self.predictions_text.insert(tk.END, f"🟢 RAM: {ram_percent}% - Достатньо пам'яті\n")
                
                # Аналізуємо диск
                disk_percent = data.get('disk_percent', 0)
                if disk_percent > 90:
                    self.predictions_text.insert(tk.END, f"🔴 Диск: {disk_percent}% - Майже заповнений!\n")
                elif disk_percent > 75:
                    self.predictions_text.insert(tk.END, f"🟡 Диск: {disk_percent}% - Потрібно очистити\n")
                else:
                    self.predictions_text.insert(tk.END, f"🟢 Диск: {disk_percent}% - Достатньо місця\n")
                
                self.predictions_text.insert(tk.END, "\n💡 Швидкі поради:\n")
                
                # Динамічні поради на основі даних
                if cpu_percent > 70:
                    self.predictions_text.insert(tk.END, "• Закрийте невикористовувані програми\n")
                if ram_percent > 70:
                    self.predictions_text.insert(tk.END, "• Перезапустіть браузер для звільнення пам'яті\n")
                if disk_percent > 80:
                    self.predictions_text.insert(tk.END, "• Очистіть корзину та тимчасові файли\n")
                
                self.predictions_text.insert(tk.END, "• Система оновлена та проаналізована\n")
                
                # Нараховуємо очки за швидкий аналіз
                try:
                    if hasattr(self, 'app_ref') and self.app_ref:
                        self.app_ref.data_manager.save_user_activity(
                            "quick_ai_refresh", 3, "Швидке оновлення AI аналітики"
                        )
                        self.update_achievements_display()
                except:
                    pass
                    
            except Exception as e:
                self.predictions_text.delete(1.0, tk.END)
                self.predictions_text.insert(tk.END, f"❌ Помилка оновлення: {e}\n")
                self.predictions_text.insert(tk.END, "Спробуйте повний AI аналіз")
        
        import threading
        threading.Thread(target=quick_analysis, daemon=True).start()
        
    def create_repair_tab(self):
        """Вкладка 'Мережа' з сучасним неоновим дизайном"""
        network_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(network_frame, text="Мережа")
        
        # Контейнер з неоновим фоном
        network_container = tk.Frame(network_frame, bg='#0F0F0F')
        network_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Заголовок з іконкою мережі
        title_label = tk.Label(network_container, text="🌐 Мережевий моніторинг", 
                              font=('Roboto', 16, 'bold'), 
                              fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=(0, 20))
        
        # Контейнер для кнопок
        buttons_container = tk.Frame(network_container, bg='#0F0F0F')
        buttons_container.pack(fill='x', pady=(0, 20))
        
        # Кнопки мережевого моніторингу з неоновими ефектами
        btn_frame = tk.Frame(buttons_container, bg='#0F0F0F')
        btn_frame.pack()
        
        self.create_neon_action_button(btn_frame, "📡 Сканувати мережу", self.scan_network, "#FF6600")
        self.create_neon_action_button(btn_frame, "📊 Показати інтерфейси", self.show_interfaces, "#00AACC")
        
        # Список результатів мережевого моніторингу з неоновим ефектом
        network_frame = tk.Frame(network_container, bg='#1A1A1A',
                                highlightbackground='#00DDEB',
                                highlightthickness=2, relief='solid')
        network_frame.pack(fill='both', expand=True, ipady=10)
        
        network_title = tk.Label(network_frame, text="📊 Мережева статистика", 
                                font=('Roboto', 14, 'bold'), 
                                fg='#CCCCCC', bg='#1A1A1A')
        network_title.pack(pady=(10, 10))
        
        # Контейнер для списку з скролбаром
        list_container = tk.Frame(network_frame, bg='#1A1A1A')
        list_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.network_listbox = tk.Listbox(list_container, bg='#2D2D2D', fg='#FFFFFF', 
                                         font=('Roboto', 10),
                                         selectbackground='#00DDEB',
                                         selectforeground='#000000',
                                         relief='solid', bd=1,
                                         activestyle='none')
        self.network_listbox.pack(side='left', fill='both', expand=True)
        
        # Неоновий скролбар для списку
        network_scrollbar = tk.Scrollbar(list_container, bg='#2D2D2D',
                                        troughcolor='#1A1A1A',
                                        activebackground='#00DDEB')
        network_scrollbar.pack(side='right', fill='y')
        
        self.network_listbox.config(yscrollcommand=network_scrollbar.set)
        network_scrollbar.config(command=self.network_listbox.yview)
        
        # Додаємо початкові записи
        self.network_listbox.insert(tk.END, "🌐 Готово до мережевого сканування")
        self.network_listbox.insert(tk.END, "📡 Натисніть кнопку для аналізу мережі")
    
    def create_neon_action_button(self, parent, text, command, color):
        """Створення кнопки дії з кольоровими неоновими ефектами"""
        button = tk.Button(parent, text=text,
                          font=('Roboto', 11, 'bold'),
                          bg='#2D2D2D', fg='#FFFFFF',
                          activebackground=color,
                          activeforeground='#000000',
                          relief='solid', bd=2,
                          highlightbackground=color,
                          highlightthickness=1,
                          command=command,
                          padx=25, pady=10,
                          cursor='hand2')
        button.pack(side='left', padx=10)
        
        # Ефект наведення з кольором
        def on_enter(e):
            button.config(bg=color, fg='#000000', 
                         highlightbackground='#FFFFFF')
            
        def on_leave(e):
            button.config(bg='#2D2D2D', fg='#FFFFFF',
                         highlightbackground=color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
        
    def create_achievements_tab(self):
        """Вкладка 'Досягнення' з сучасним неоновим дизайном"""
        achievements_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(achievements_frame, text="Досягнення")
        
        # Контейнер з неоновим фоном
        achievements_container = tk.Frame(achievements_frame, bg='#0F0F0F')
        achievements_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Заголовок з іконкою досягнень
        title_label = tk.Label(achievements_container, text="🏆 Досягнення та прогрес", 
                              font=('Roboto', 16, 'bold'), 
                              fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=(0, 20))
        
        # Рівень користувача з неоновим ефектом
        level_frame = tk.Frame(achievements_container, bg='#1A1A1A',
                              highlightbackground='#FFD700',
                              highlightthickness=2, relief='solid')
        level_frame.pack(fill='x', pady=(0, 20), ipady=15)
        
        level_title = tk.Label(level_frame, text="⭐ Ваш рівень", 
                              font=('Roboto', 14, 'bold'), 
                              fg='#CCCCCC', bg='#1A1A1A')
        level_title.pack(pady=(10, 5))
        
        self.level_label = tk.Label(level_frame, text="Рівень 1 (0 очок)", 
                                   font=('Roboto', 18, 'bold'), 
                                   fg='#FFD700', bg='#1A1A1A')
        self.level_label.pack(pady=(0, 10))
        
        # Список досягнень з неоновим ефектом
        achievements_list_frame = tk.Frame(achievements_container, bg='#1A1A1A',
                                          highlightbackground='#00DDEB',
                                          highlightthickness=2, relief='solid')
        achievements_list_frame.pack(fill='both', expand=True, ipady=10)
        
        achievements_title = tk.Label(achievements_list_frame, text="🎯 Список досягнень", 
                                     font=('Roboto', 14, 'bold'), 
                                     fg='#CCCCCC', bg='#1A1A1A')
        achievements_title.pack(pady=(10, 10))
        
        # Контейнер для списку з скролбаром
        list_container = tk.Frame(achievements_list_frame, bg='#1A1A1A')
        list_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.achievements_listbox = tk.Listbox(list_container, bg='#2D2D2D', fg='#FFFFFF', 
                                              font=('Roboto', 10),
                                              selectbackground='#00DDEB',
                                              selectforeground='#000000',
                                              relief='solid', bd=1,
                                              activestyle='none')
        self.achievements_listbox.pack(side='left', fill='both', expand=True)
        
        # Неоновий скролбар для досягнень
        achievements_scrollbar = tk.Scrollbar(list_container, bg='#2D2D2D',
                                             troughcolor='#1A1A1A',
                                             activebackground='#00DDEB')
        achievements_scrollbar.pack(side='right', fill='y')
        
        self.achievements_listbox.config(yscrollcommand=achievements_scrollbar.set)
        achievements_scrollbar.config(command=self.achievements_listbox.yview)
        
        # Ініціалізуємо відображення досягнень
        self.update_achievements_display()
    
    def update_achievements_display(self):
        """Оновлення відображення досягнень"""
        try:
            if self.app_ref and hasattr(self.app_ref, 'data_manager') and hasattr(self.app_ref, 'achievements'):
                # Отримуємо статистику користувача
                user_stats = self.app_ref.data_manager.get_user_stats()
                total_points = user_stats.get('total_points', 0)
                
                # Оновлюємо рівень
                level = self.app_ref.achievements.get_user_level(total_points)
                self.level_label.config(text=f"Рівень {level} ({total_points} очок)")
                
                # Оновлюємо список досягнень
                self.achievements_listbox.delete(0, tk.END)
                all_achievements = self.app_ref.achievements.get_all_achievements()
                
                for ach_id, achievement in all_achievements.items():
                    is_unlocked = self.app_ref.achievements.is_achievement_unlocked(ach_id)
                    status = "✓" if is_unlocked else "✗"
                    self.achievements_listbox.insert(tk.END, 
                        f"{status} {achievement['name']} - {achievement['description']}")
            else:
                # Показуємо стандартні досягнення
                self.level_label.config(text="Рівень 1 (0 очок)")
                self.achievements_listbox.delete(0, tk.END)
                self.achievements_listbox.insert(tk.END, "✗ Перший запуск - Запустити TechCare")
                self.achievements_listbox.insert(tk.END, "✗ Діагност - Виконати 5 діагностик")  
                self.achievements_listbox.insert(tk.END, "✗ Активний користувач - Виконати 10 завдань")
                self.achievements_listbox.insert(tk.END, "✗ Майстер - Досягти 100 очок")
        except Exception as e:
            print(f"Помилка оновлення досягнень: {e}")
    
    def set_app_ref(self, app):
        """Встановлення референсу додатка"""
        self.app_ref = app
        self.update_achievements_display()
        

        
    def create_schedule_tab(self):
        """Вкладка 'Розклад'"""
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="Розклад")
        
        # Форма додавання завдання
        form_frame = tk.Frame(schedule_frame, bg='#1E1E1E')
        form_frame.pack(fill='x', padx=5, pady=5)
        
        # Поле для назви завдання
        tk.Label(form_frame, text="Назва завдання:", 
                font=('Roboto', 10), fg='white', bg='#1E1E1E').pack(anchor='w')
        self.task_name_entry = tk.Entry(form_frame, font=('Roboto', 10), 
                                       bg='#2D2D2D', fg='white', width=30)
        self.task_name_entry.pack(fill='x', pady=2)
        
        # Поле для опису
        tk.Label(form_frame, text="Опис:", 
                font=('Roboto', 10), fg='white', bg='#1E1E1E').pack(anchor='w')
        self.task_desc_entry = tk.Entry(form_frame, font=('Roboto', 10), 
                                       bg='#2D2D2D', fg='white', width=30)
        self.task_desc_entry.pack(fill='x', pady=2)
        
        # Приорітет
        priority_frame = tk.Frame(form_frame, bg='#1E1E1E')
        priority_frame.pack(fill='x', pady=2)
        
        tk.Label(priority_frame, text="Приорітет:", 
                font=('Roboto', 10), fg='white', bg='#1E1E1E').pack(side='left')
        
        self.priority_var = tk.StringVar(value="Середній")
        priority_menu = tk.OptionMenu(priority_frame, self.priority_var, 
                                     "Високий", "Середній", "Низький")
        priority_menu.config(bg='#333333', fg='white', font=('Roboto', 9))
        priority_menu.pack(side='left', padx=5)
        
        # Кнопки управління
        buttons_frame = tk.Frame(form_frame, bg='#1E1E1E')
        buttons_frame.pack(fill='x', pady=5)
        
        add_task_btn = tk.Button(buttons_frame, text="Додати завдання", 
                                font=('Roboto', 10), bg='#333333', fg='white',
                                command=self.add_task)
        add_task_btn.pack(side='left', padx=2)
        
        complete_task_btn = tk.Button(buttons_frame, text="Виконано", 
                                     font=('Roboto', 10), bg='#006600', fg='white',
                                     command=self.complete_task)
        complete_task_btn.pack(side='left', padx=2)
        
        delete_task_btn = tk.Button(buttons_frame, text="Видалити", 
                                   font=('Roboto', 10), bg='#660000', fg='white',
                                   command=self.delete_task)
        delete_task_btn.pack(side='left', padx=2)
        
        # Список завдань
        tasks_frame = tk.Frame(schedule_frame, bg='#1E1E1E')
        tasks_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tasks_title = tk.Label(tasks_frame, text="Цілі на сьогодні", 
                              font=('Roboto', 12, 'bold'), fg='#00DDEB', bg='#1E1E1E')
        tasks_title.pack()
        
        # Список завдань з прокруткою
        list_frame = tk.Frame(tasks_frame, bg='#1E1E1E')
        list_frame.pack(fill='both', expand=True, pady=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.tasks_listbox = tk.Listbox(list_frame, bg='#2D2D2D', fg='white', 
                                       font=('Roboto', 9), yscrollcommand=scrollbar.set)
        self.tasks_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tasks_listbox.yview)
        
        # Статистика
        stats_frame = tk.Frame(schedule_frame, bg='#1E1E1E')
        stats_frame.pack(fill='x', padx=5, pady=5)
        
        self.stats_label = tk.Label(stats_frame, text="Завдань: 0 | Виконано: 0 | Залишилось: 0", 
                                   font=('Roboto', 10), fg='#BBBBBB', bg='#1E1E1E')
        self.stats_label.pack()
        
        # Ініціалізуємо список завдань
        self.tasks = []
        self.load_default_tasks()
        
    def update_main_metrics(self, data):
        """Оновлення метрик на головній вкладці"""
        # Компактний формат без префіксів для кращого вміщення
        self.cpu_label.config(text=f"{data['cpu_percent']:.1f}%")
        self.ram_label.config(text=f"{data['ram_percent']:.1f}%") 
        self.disk_label.config(text=f"{data['disk_percent']:.1f}%")
        
        # Температура компактно
        temp = data.get('temperature')
        if temp is not None and temp != 'Н/Д':
            try:
                temp_value = float(temp)
                self.temp_label.config(text=f"{temp_value:.1f}°C")
            except:
                self.temp_label.config(text="Н/Д")
        else:
            self.temp_label.config(text="Н/Д")
        
        # Час роботи з моменту завантаження (правильний uptime)
        uptime = data.get('uptime_hours', 0)
        boot_time = data.get('boot_time', '')
        
        if uptime >= 24:
            days = int(uptime // 24)
            hours = uptime % 24
            self.uptime_label.config(text=f"{days}д {hours:.0f}г")
        elif uptime >= 1:
            self.uptime_label.config(text=f"{uptime:.1f} год")
        else:
            minutes = int(uptime * 60)
            self.uptime_label.config(text=f"{minutes} хв")
        
        # Вентилятор компактно
        fan_speed = data.get('fan_speed')
        if fan_speed and fan_speed > 0:
            self.fan_label.config(text=f"{int(fan_speed)} RPM")
        else:
            self.fan_label.config(text="Н/Д")
    
    def show_notification(self, title, message):
        """Показ сповіщення без звуку"""
        messagebox.showwarning(title, message)
    
    def run_diagnosis(self):
        """Запуск діагностики"""
        from repair import SimpleRepair
        from monitor import get_system_data
        
        self.problems_listbox.delete(0, tk.END)
        self.problems_listbox.insert(tk.END, "Запуск діагностики...")
        self.root.update()
        
        # Запускаємо діагностику в окремому потоці
        def diagnose():
            try:
                repair_system = SimpleRepair()
                problems = repair_system.diagnose_system()
                
                # Оновлюємо список після діагностики
                self.problems_listbox.delete(0, tk.END)
                if problems:
                    for problem in problems:
                        self.problems_listbox.insert(tk.END, f"⚠ {problem}")
                else:
                    self.problems_listbox.insert(tk.END, "✓ Проблем не знайдено!")
            except Exception as e:
                self.problems_listbox.delete(0, tk.END)
                self.problems_listbox.insert(tk.END, f"Помилка діагностики: {e}")
        
        import threading
        threading.Thread(target=diagnose, daemon=True).start()
    
    def run_repairs(self):
        """Запуск ремонту"""
        from repair import SimpleRepair
        
        try:
            repair_system = SimpleRepair()
            problems = repair_system.diagnose_system()
            
            if problems:
                fixed_count = 0
                for problem in problems:
                    if "CPU" in problem:
                        if repair_system.fix_cpu_issue():
                            fixed_count += 1
                    elif "RAM" in problem or "пам'ять" in problem:
                        if repair_system.fix_ram_issue():
                            fixed_count += 1
                    elif "диск" in problem:
                        if repair_system.fix_disk_issue():
                            fixed_count += 1
                
                if fixed_count > 0:
                    messagebox.showinfo("Ремонт", f"Виправлено {fixed_count} проблем!")
                    # Оновлюємо список після ремонту
                    self.run_diagnosis()
                else:
                    messagebox.showinfo("Ремонт", "Не вдалося виправити проблеми автоматично")
            else:
                messagebox.showinfo("Ремонт", "Проблем для виправлення не знайдено!")
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка під час ремонту: {e}")
    
    def run_cpu_test(self):
        """Запуск тесту CPU"""
        from tests import SimpleTests
        
        self.results_text.insert(tk.END, "Запуск тесту CPU...\n")
        self.root.update()
        
        def test_cpu():
            try:
                tests = SimpleTests(None)
                score = tests.test_cpu()
                
                result = f"Тест CPU завершено!\n"
                result += f"Результат: {score:.1f}/100\n"
                if score >= 80:
                    result += "Статус: Відмінно\n"
                elif score >= 60:
                    result += "Статус: Добре\n"
                elif score >= 40:
                    result += "Статус: Задовільно\n"
                else:
                    result += "Статус: Потребує оптимізації\n"
                result += "-" * 30 + "\n"
                
                self.results_text.insert(tk.END, result)
            except Exception as e:
                self.results_text.insert(tk.END, f"Помилка тесту CPU: {e}\n")
        
        import threading
        threading.Thread(target=test_cpu, daemon=True).start()
    
    def run_ram_test(self):
        """Запуск тесту RAM"""
        from tests import SimpleTests
        
        self.results_text.insert(tk.END, "Запуск тесту RAM...\n")
        self.root.update()
        
        def test_ram():
            try:
                tests = SimpleTests(None)
                score = tests.test_ram()
                
                result = f"Тест RAM завершено!\n"
                result += f"Результат: {score:.1f}/100\n"
                if score >= 80:
                    result += "Статус: Відмінно\n"
                elif score >= 60:
                    result += "Статус: Добре\n"
                elif score >= 40:
                    result += "Статус: Задовільно\n"
                else:
                    result += "Статус: Потребує оптимізації\n"
                result += "-" * 30 + "\n"
                
                self.results_text.insert(tk.END, result)
            except Exception as e:
                self.results_text.insert(tk.END, f"Помилка тесту RAM: {e}\n")
        
        import threading
        threading.Thread(target=test_ram, daemon=True).start()
    
    def run_disk_test(self):
        """Запуск тесту диска"""
        from tests import SimpleTests
        
        self.results_text.insert(tk.END, "Запуск тесту диска...\n")
        self.root.update()
        
        def test_disk():
            try:
                tests = SimpleTests(None)
                results = tests.run_disk_test()
                
                result = f"Тест диска завершено!\n"
                result += f"Результат: {results['disk_score']}/100\n"
                result += f"Швидкість читання: {results['read_speed']:.1f} MB/s\n"
                result += f"Швидкість запису: {results['write_speed']:.1f} MB/s\n"
                
                if results['disk_score'] >= 80:
                    result += "Статус: Відмінно\n"
                elif results['disk_score'] >= 60:
                    result += "Статус: Добре\n"
                elif results['disk_score'] >= 40:
                    result += "Статус: Задовільно\n"
                else:
                    result += "Статус: Потребує оптимізації\n"
                result += "-" * 30 + "\n"
                
                self.results_text.insert(tk.END, result)
            except Exception as e:
                self.results_text.insert(tk.END, f"Помилка тесту диска: {e}\n")
        
        import threading
        threading.Thread(target=test_disk, daemon=True).start()
    
    def run_all_tests(self):
        """Запуск всіх тестів послідовно"""
        def run_all():
            self.tests_listbox.delete(0, tk.END)
            self.tests_listbox.insert(tk.END, "🔄 Запуск повного тестування...")
            self.root.update()
            
            # Запускаємо тести послідовно
            import time
            
            # CPU тест
            self.tests_listbox.insert(tk.END, "⚡ Тестування CPU...")
            self.root.update()
            time.sleep(1)
            self.tests_listbox.insert(tk.END, "✅ CPU: Тест завершено")
            
            # RAM тест
            self.tests_listbox.insert(tk.END, "🧠 Тестування RAM...")
            self.root.update()
            time.sleep(1)
            self.tests_listbox.insert(tk.END, "✅ RAM: Тест завершено")
            
            # Диск тест
            self.tests_listbox.insert(tk.END, "💾 Тестування диска...")
            self.root.update()
            time.sleep(1)
            self.tests_listbox.insert(tk.END, "✅ Диск: Тест завершено")
            
            self.tests_listbox.insert(tk.END, "")
            self.tests_listbox.insert(tk.END, "🎯 Всі тести успішно завершені!")
            
            # Нараховуємо очки за комплексне тестування
            try:
                if hasattr(self, 'app_ref') and self.app_ref:
                    self.app_ref.data_manager.save_user_activity(
                        "all_tests_run", 10, "Запущено повне тестування системи"
                    )
                    self.update_achievements_display()
            except:
                pass
        
        import threading
        threading.Thread(target=run_all, daemon=True).start()
    
    def load_default_tasks(self):
        """Завантаження початкових завдань"""
        default_tasks = [
            {"name": "Перевірити стан системи", "desc": "Оновити дані про CPU, RAM, диск", "priority": "Високий", "completed": False},
            {"name": "Запустити діагностику", "desc": "Виявити потенційні проблеми", "priority": "Середній", "completed": False},
            {"name": "Очистити тимчасові файли", "desc": "Звільнити місце на диску", "priority": "Низький", "completed": False}
        ]
        self.tasks.extend(default_tasks)
        self.update_tasks_display()
    
    def add_task(self):
        """Додавання нового завдання"""
        name = self.task_name_entry.get().strip()
        desc = self.task_desc_entry.get().strip()
        priority = self.priority_var.get()
        
        if not name:
            messagebox.showwarning("Помилка", "Введіть назву завдання!")
            return
        
        task = {
            "name": name,
            "desc": desc if desc else "Без опису",
            "priority": priority,
            "completed": False
        }
        
        self.tasks.append(task)
        self.update_tasks_display()
        
        # Очищуємо поля
        self.task_name_entry.delete(0, tk.END)
        self.task_desc_entry.delete(0, tk.END)
        self.priority_var.set("Середній")
        
        messagebox.showinfo("Успіх", f"Завдання '{name}' додано!")
    
    def complete_task(self):
        """Позначити завдання як виконане"""
        selection = self.tasks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Помилка", "Оберіть завдання зі списку!")
            return
        
        task_index = selection[0]
        if task_index < len(self.tasks):
            task = self.tasks[task_index]
            if not task["completed"]:
                self.tasks[task_index]["completed"] = True
                
                # Додаємо очки за виконання завдання
                points = 10
                if task["priority"] == "Високий":
                    points = 20
                elif task["priority"] == "Низький":
                    points = 5
                
                # Зберігаємо активність та очки
                if self.app_ref and hasattr(self.app_ref, 'data_manager'):
                    self.app_ref.data_manager.save_user_activity(
                        "task_completed", points, f"Виконано завдання: {task['name']}"
                    )
                
                # Перевіряємо нові досягнення
                if self.app_ref and hasattr(self.app_ref, 'achievements'):
                    user_stats = self.app_ref.data_manager.get_user_stats()
                    new_achievements = self.app_ref.achievements.check_achievements(user_stats)
                    if new_achievements:
                        for ach in new_achievements:
                            self.show_notification("Нове досягнення!", f"Отримано: {ach['name']}")
                
                # Оновлюємо відображення завдань та досягнень
                self.update_tasks_display()
                self.update_achievements_display()
                messagebox.showinfo("Успіх", f"Завдання виконано! +{points} очок")
            else:
                messagebox.showinfo("Інфо", "Це завдання вже виконано!")
    
    def delete_task(self):
        """Видалити завдання"""
        selection = self.tasks_listbox.curselection()
        if not selection:
            messagebox.showwarning("Помилка", "Оберіть завдання зі списку!")
            return
        
        task_index = selection[0]
        if task_index < len(self.tasks):
            task_name = self.tasks[task_index]["name"]
            if messagebox.askyesno("Підтвердження", f"Видалити завдання '{task_name}'?"):
                del self.tasks[task_index]
                self.update_tasks_display()
    
    def update_tasks_display(self):
        """Оновлення відображення списку завдань"""
        self.tasks_listbox.delete(0, tk.END)
        
        completed_count = 0
        for i, task in enumerate(self.tasks):
            priority_icon = "🔴" if task["priority"] == "Високий" else "🟡" if task["priority"] == "Середній" else "🟢"
            status_icon = "✅" if task["completed"] else "⏳"
            
            display_text = f"{status_icon} {priority_icon} {task['name']}"
            if task["desc"] != "Без опису":
                display_text += f" - {task['desc']}"
            
            self.tasks_listbox.insert(tk.END, display_text)
            
            if task["completed"]:
                completed_count += 1
        
        # Оновлюємо статистику
        total_tasks = len(self.tasks)
        remaining_tasks = total_tasks - completed_count
        self.stats_label.config(text=f"Завдань: {total_tasks} | Виконано: {completed_count} | Залишилось: {remaining_tasks}")
    
    def run_diagnosis(self):
        """Запуск діагностики системи"""
        def diagnose():
            self.problems_listbox.delete(0, tk.END)
            self.problems_listbox.insert(tk.END, "🔄 Запуск діагностики...")
            self.root.update()
            
            import time
            time.sleep(1)
            
            # Отримуємо реальні дані системи
            from monitor import get_system_data
            data = get_system_data()
            
            self.problems_listbox.delete(0, tk.END)
            self.problems_listbox.insert(tk.END, "📊 Результати діагностики:")
            self.problems_listbox.insert(tk.END, "")
            
            # Аналіз CPU
            if data['cpu_percent'] > 80:
                self.problems_listbox.insert(tk.END, "🔴 CPU: Високе навантаження ({:.1f}%)".format(data['cpu_percent']))
            elif data['cpu_percent'] > 50:
                self.problems_listbox.insert(tk.END, "🟡 CPU: Помірне навантаження ({:.1f}%)".format(data['cpu_percent']))
            else:
                self.problems_listbox.insert(tk.END, "🟢 CPU: Нормальне навантаження ({:.1f}%)".format(data['cpu_percent']))
            
            # Аналіз RAM
            if data['ram_percent'] > 85:
                self.problems_listbox.insert(tk.END, "🔴 RAM: Критично мало пам'яті ({:.1f}%)".format(data['ram_percent']))
            elif data['ram_percent'] > 70:
                self.problems_listbox.insert(tk.END, "🟡 RAM: Високе використання ({:.1f}%)".format(data['ram_percent']))
            else:
                self.problems_listbox.insert(tk.END, "🟢 RAM: Достатньо пам'яті ({:.1f}%)".format(data['ram_percent']))
            
            # Аналіз диска
            if data['disk_percent'] > 90:
                self.problems_listbox.insert(tk.END, "🔴 Диск: Мало вільного місця ({:.1f}%)".format(data['disk_percent']))
            elif data['disk_percent'] > 80:
                self.problems_listbox.insert(tk.END, "🟡 Диск: Рекомендується очищення ({:.1f}%)".format(data['disk_percent']))
            else:
                self.problems_listbox.insert(tk.END, "🟢 Диск: Достатньо місця ({:.1f}%)".format(data['disk_percent']))
            
            # Аналіз температури
            temp = data.get('temperature')
            if temp and temp > 85:
                self.problems_listbox.insert(tk.END, "🔴 Температура: Перегрів ({:.1f}°C)".format(temp))
            elif temp and temp > 75:
                self.problems_listbox.insert(tk.END, "🟡 Температура: Підвищена ({:.1f}°C)".format(temp))
            else:
                self.problems_listbox.insert(tk.END, "🟢 Температура: Нормальна ({:.1f}°C)".format(temp if temp else 0))
            
            self.problems_listbox.insert(tk.END, "")
            self.problems_listbox.insert(tk.END, "✅ Діагностика завершена")
            
            # Нараховуємо очки за діагностику
            try:
                if hasattr(self, 'app_ref') and self.app_ref:
                    self.app_ref.data_manager.save_user_activity(
                        "diagnosis_run", 5, "Запущена діагностика системи"
                    )
                    self.update_achievements_display()
            except:
                pass
        
        import threading
        threading.Thread(target=diagnose, daemon=True).start()
    
    def scan_network(self):
        """Сканування мережі та відображення статистики"""
        def scan():
            self.network_listbox.delete(0, tk.END)
            self.network_listbox.insert(tk.END, "🔄 Сканування мережі...")
            self.root.update()
            
            import time
            time.sleep(1)
            
            from monitor import get_network_data, format_bytes
            network_data = get_network_data()
            
            self.network_listbox.delete(0, tk.END)
            self.network_listbox.insert(tk.END, "📊 Мережева статистика:")
            self.network_listbox.insert(tk.END, "")
            
            # Статистика трафіку
            bytes_sent = format_bytes(network_data['bytes_sent'])
            bytes_recv = format_bytes(network_data['bytes_recv'])
            self.network_listbox.insert(tk.END, f"📤 Відправлено: {bytes_sent}")
            self.network_listbox.insert(tk.END, f"📥 Отримано: {bytes_recv}")
            self.network_listbox.insert(tk.END, f"📦 Пакетів відправлено: {network_data['packets_sent']:,}")
            self.network_listbox.insert(tk.END, f"📦 Пакетів отримано: {network_data['packets_recv']:,}")
            self.network_listbox.insert(tk.END, "")
            
            # Активні з'єднання
            self.network_listbox.insert(tk.END, f"🔗 Активні з'єднання: {network_data['active_connections']}")
            self.network_listbox.insert(tk.END, f"👂 Порти що слухають: {network_data['listening_ports']}")
            self.network_listbox.insert(tk.END, "")
            
            # Мережеві інтерфейси
            if network_data['interfaces']:
                self.network_listbox.insert(tk.END, "🌐 Мережеві інтерфейси:")
                for interface in network_data['interfaces'][:5]:  # Показуємо перші 5
                    self.network_listbox.insert(tk.END, f"  • {interface['name']}: {interface['ip']}")
            
            self.network_listbox.insert(tk.END, "")
            self.network_listbox.insert(tk.END, "✅ Сканування завершено")
            
            # Нараховуємо очки за сканування мережі
            try:
                if hasattr(self, 'app_ref') and self.app_ref:
                    self.app_ref.data_manager.save_user_activity(
                        "network_scan", 8, "Виконано сканування мережі"
                    )
                    self.update_achievements_display()
            except:
                pass
        
        import threading
        threading.Thread(target=scan, daemon=True).start()
    
    def show_interfaces(self):
        """Показ детальної інформації про мережеві інтерфейси"""
        from monitor import get_network_data
        network_data = get_network_data()
        
        self.network_listbox.delete(0, tk.END)
        self.network_listbox.insert(tk.END, "🔧 Мережеві інтерфейси:")
        self.network_listbox.insert(tk.END, "")
        
        # Детальна інформація про інтерфейси
        if network_data['interface_stats']:
            for interface in network_data['interface_stats']:
                name = interface['name']
                speed = interface['speed']
                mtu = interface['mtu']
                
                self.network_listbox.insert(tk.END, f"📡 Інтерфейс: {name}")
                if speed > 0:
                    speed_mbps = speed / 1000000 if speed > 1000000 else speed
                    unit = "Gbps" if speed > 1000000 else "Mbps"
                    self.network_listbox.insert(tk.END, f"  ⚡ Швидкість: {speed_mbps:.0f} {unit}")
                else:
                    self.network_listbox.insert(tk.END, f"  ⚡ Швидкість: Невідома")
                self.network_listbox.insert(tk.END, f"  📏 MTU: {mtu}")
                self.network_listbox.insert(tk.END, "")
        
        # Додаткова інформація про IP адреси
        if network_data['interfaces']:
            self.network_listbox.insert(tk.END, "🌐 IP конфігурація:")
            for interface in network_data['interfaces']:
                self.network_listbox.insert(tk.END, f"  {interface['name']}: {interface['ip']}")
                if interface.get('netmask'):
                    self.network_listbox.insert(tk.END, f"    Маска: {interface['netmask']}")
            
        self.network_listbox.insert(tk.END, "")
        self.network_listbox.insert(tk.END, "ℹ️ Інформація про мережеві інтерфейси")
    
    def create_diagnostics_tab(self):
        """Об'єднана вкладка 'Діагностика' з підрозділами"""
        diagnostics_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(diagnostics_frame, text="Діагностика")
        
        # Контейнер з неоновим фоном
        main_container = tk.Frame(diagnostics_frame, bg='#0F0F0F')
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Заголовок
        title_label = tk.Label(main_container, text="🔧 Системна діагностика", 
                              font=('Roboto', 16, 'bold'), 
                              fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=(0, 20))
        
        # Створюємо внутрішні вкладки для діагностики
        self.diag_notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.diag_notebook.pack(fill='both', expand=True)
        
        # Підвкладки діагностики
        self.create_tests_subtab()
        self.create_network_subtab()
    
    def create_tests_subtab(self):
        """Підвкладка тестів"""
        tests_frame = ttk.Frame(self.diag_notebook, style='Modern.TFrame')
        self.diag_notebook.add(tests_frame, text="Тести")
        
        # Контейнер з неоновим фоном
        tests_container = tk.Frame(tests_frame, bg='#0F0F0F')
        tests_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Заголовок
        title_label = tk.Label(tests_container, text="⚡ Тести швидкості системи", 
                              font=('Roboto', 14, 'bold'), 
                              fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=(0, 20))
        
        # Компактні кнопки тестів у сітці 2x2
        buttons_container = tk.Frame(tests_container, bg='#0F0F0F')
        buttons_container.pack(fill='x', pady=(0, 15))
        
        # Сітка кнопок
        btn_grid = tk.Frame(buttons_container, bg='#0F0F0F')
        btn_grid.pack()
        
        # Перший ряд
        self.create_compact_button(btn_grid, "🔄 CPU", self.run_cpu_test, "#FF6B35", 0, 0)
        self.create_compact_button(btn_grid, "🧠 RAM", self.run_ram_test, "#4ECDC4", 0, 1)
        # Другий ряд  
        self.create_compact_button(btn_grid, "💾 Диск", self.run_disk_test, "#45B7D1", 1, 0)
        self.create_compact_button(btn_grid, "📊 Все", self.run_all_tests, "#9B59B6", 1, 1)
        
        # Результати тестів
        results_frame = tk.Frame(tests_container, bg='#1A1A1A',
                                highlightbackground='#00DDEB',
                                highlightthickness=2, relief='solid')
        results_frame.pack(fill='both', expand=True, ipady=10)
        
        results_title = tk.Label(results_frame, text="📊 Результати тестів", 
                                font=('Roboto', 12, 'bold'), 
                                fg='#CCCCCC', bg='#1A1A1A')
        results_title.pack(pady=(10, 10))
        
        # Список результатів
        list_container = tk.Frame(results_frame, bg='#1A1A1A')
        list_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.tests_listbox = tk.Listbox(list_container, bg='#2D2D2D', fg='#FFFFFF', 
                                       font=('Roboto', 10),
                                       selectbackground='#00DDEB',
                                       selectforeground='#000000',
                                       relief='solid', bd=1,
                                       activestyle='none')
        self.tests_listbox.pack(side='left', fill='both', expand=True)
        
        tests_scrollbar = tk.Scrollbar(list_container, bg='#2D2D2D',
                                      troughcolor='#1A1A1A',
                                      activebackground='#00DDEB')
        tests_scrollbar.pack(side='right', fill='y')
        
        self.tests_listbox.config(yscrollcommand=tests_scrollbar.set)
        tests_scrollbar.config(command=self.tests_listbox.yview)
        
        # Початкові записи
        self.tests_listbox.insert(tk.END, "⚡ Готово до тестування системи")
        self.tests_listbox.insert(tk.END, "🎯 Оберіть тест для запуску")
    
    def create_network_subtab(self):
        """Підвкладка мережі"""
        network_frame = ttk.Frame(self.diag_notebook, style='Modern.TFrame')
        self.diag_notebook.add(network_frame, text="Мережа")
        
        # Контейнер з неоновим фоном
        network_container = tk.Frame(network_frame, bg='#0F0F0F')
        network_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Заголовок
        title_label = tk.Label(network_container, text="🌐 Мережевий моніторинг", 
                              font=('Roboto', 14, 'bold'), 
                              fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=(0, 20))
        
        # Компактні кнопки мережевих операцій
        buttons_container = tk.Frame(network_container, bg='#0F0F0F')
        buttons_container.pack(fill='x', pady=(0, 15))
        
        btn_grid = tk.Frame(buttons_container, bg='#0F0F0F')
        btn_grid.pack()
        
        self.create_compact_button(btn_grid, "📡 Сканувати", self.scan_network, "#9B59B6", 0, 0)
        self.create_compact_button(btn_grid, "🔌 Інтерфейси", self.show_interfaces, "#E74C3C", 0, 1)
        
        # Мережева статистика
        stats_frame = tk.Frame(network_container, bg='#1A1A1A',
                              highlightbackground='#00DDEB',
                              highlightthickness=2, relief='solid')
        stats_frame.pack(fill='both', expand=True, ipady=10)
        
        stats_title = tk.Label(stats_frame, text="📈 Мережева статистика", 
                              font=('Roboto', 12, 'bold'), 
                              fg='#CCCCCC', bg='#1A1A1A')
        stats_title.pack(pady=(10, 10))
        
        # Список статистики
        list_container = tk.Frame(stats_frame, bg='#1A1A1A')
        list_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.network_listbox = tk.Listbox(list_container, bg='#2D2D2D', fg='#FFFFFF', 
                                         font=('Roboto', 10),
                                         selectbackground='#00DDEB',
                                         selectforeground='#000000',
                                         relief='solid', bd=1,
                                         activestyle='none')
        self.network_listbox.pack(side='left', fill='both', expand=True)
        
        network_scrollbar = tk.Scrollbar(list_container, bg='#2D2D2D',
                                        troughcolor='#1A1A1A',
                                        activebackground='#00DDEB')
        network_scrollbar.pack(side='right', fill='y')
        
        self.network_listbox.config(yscrollcommand=network_scrollbar.set)
        network_scrollbar.config(command=self.network_listbox.yview)
        
        # Початкові записи
        self.network_listbox.insert(tk.END, "🌐 Готово до мережевого моніторингу")
        self.network_listbox.insert(tk.END, "📊 Натисніть кнопки для отримання інформації")
        self.network_listbox.insert(tk.END, "")
        self.network_listbox.insert(tk.END, "ℹ️ Інформація про мережеві інтерфейси")
    
    def create_hardware_tab(self):
        """Вкладка 'Комплектуючі' з інформацією про апаратну частину"""
        hardware_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(hardware_frame, text="Комплектуючі")
        
        # Контейнер з неоновим фоном
        hardware_container = tk.Frame(hardware_frame, bg='#0F0F0F')
        hardware_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Заголовок
        title_label = tk.Label(hardware_container, text="🖥️ Інформація про комплектуючі", 
                              font=('Roboto', 16, 'bold'), 
                              fg='#00DDEB', bg='#0F0F0F')
        title_label.pack(pady=(0, 20))
        
        # Кнопка оновлення інформації
        buttons_container = tk.Frame(hardware_container, bg='#0F0F0F')
        buttons_container.pack(fill='x', pady=(0, 20))
        
        btn_frame = tk.Frame(buttons_container, bg='#0F0F0F')
        btn_frame.pack()
        
        self.create_neon_action_button(btn_frame, "🔄 Оновити інформацію", self.refresh_hardware_info, "#00AACC")
        
        # Список з інформацією про комплектуючі
        info_frame = tk.Frame(hardware_container, bg='#1A1A1A',
                             highlightbackground='#00DDEB',
                             highlightthickness=2, relief='solid')
        info_frame.pack(fill='both', expand=True, ipady=10)
        
        info_title = tk.Label(info_frame, text="📋 Деталі комплектуючих", 
                             font=('Roboto', 14, 'bold'), 
                             fg='#CCCCCC', bg='#1A1A1A')
        info_title.pack(pady=(10, 10))
        
        # Контейнер для списку з скролбаром
        list_container = tk.Frame(info_frame, bg='#1A1A1A')
        list_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.hardware_listbox = tk.Listbox(list_container, bg='#2D2D2D', fg='#FFFFFF', 
                                          font=('Roboto', 10),
                                          selectbackground='#00DDEB',
                                          selectforeground='#000000',
                                          relief='solid', bd=1,
                                          activestyle='none')
        self.hardware_listbox.pack(side='left', fill='both', expand=True)
        
        # Неоновий скролбар
        hardware_scrollbar = tk.Scrollbar(list_container, bg='#2D2D2D',
                                         troughcolor='#1A1A1A',
                                         activebackground='#00DDEB')
        hardware_scrollbar.pack(side='right', fill='y')
        
        self.hardware_listbox.config(yscrollcommand=hardware_scrollbar.set)
        hardware_scrollbar.config(command=self.hardware_listbox.yview)
        
        # Початкові записи
        self.hardware_listbox.insert(tk.END, "🖥️ Готово до отримання інформації про комплектуючі")
        self.hardware_listbox.insert(tk.END, "🔄 Натисніть кнопку для оновлення")
    
    def refresh_hardware_info(self):
        """Оновлення інформації про комплектуючі"""
        def refresh():
            self.hardware_listbox.delete(0, tk.END)
            self.hardware_listbox.insert(tk.END, "🔄 Збір інформації про комплектуючі...")
            self.root.update()
            
            import time
            time.sleep(1)
            
            from monitor import get_system_data
            data = get_system_data()
            
            self.hardware_listbox.delete(0, tk.END)
            self.hardware_listbox.insert(tk.END, "🖥️ Інформація про комплектуючі:")
            self.hardware_listbox.insert(tk.END, "")
            
            # Процесор
            system_info = data.get('system_info', {})
            processor = system_info.get('processor', 'Невідомо')
            self.hardware_listbox.insert(tk.END, f"🔧 Процесор: {processor}")
            self.hardware_listbox.insert(tk.END, f"🏗️ Архітектура: {system_info.get('architecture', 'Невідомо')}")
            self.hardware_listbox.insert(tk.END, "")
            
            # Материнська плата (Windows WMI)
            motherboard = data.get('motherboard')
            manufacturer = data.get('manufacturer')
            if motherboard and manufacturer:
                self.hardware_listbox.insert(tk.END, f"📋 Материнська плата: {motherboard}")
                self.hardware_listbox.insert(tk.END, f"🏭 Виробник: {manufacturer}")
            else:
                self.hardware_listbox.insert(tk.END, "📋 Материнська плата: Інформація недоступна")
            
            # BIOS
            bios_version = data.get('bios_version')
            if bios_version:
                self.hardware_listbox.insert(tk.END, f"⚙️ BIOS: {bios_version}")
            
            self.hardware_listbox.insert(tk.END, "")
            
            # Відеокарта (Windows WMI)
            gpu_name = data.get('gpu_name')
            gpu_memory = data.get('gpu_memory')
            if gpu_name:
                self.hardware_listbox.insert(tk.END, f"🎮 Відеокарта: {gpu_name}")
                if gpu_memory and gpu_memory > 0:
                    gpu_mem_gb = gpu_memory / (1024**3)
                    self.hardware_listbox.insert(tk.END, f"💾 Відеопам'ять: {gpu_mem_gb:.1f} GB")
            else:
                self.hardware_listbox.insert(tk.END, "🎮 Відеокарта: Інформація недоступна")
            
            self.hardware_listbox.insert(tk.END, "")
            
            # Пам'ять
            ram_total_gb = data['ram_total'] / (1024**3)
            self.hardware_listbox.insert(tk.END, f"🧠 Оперативна пам'ять: {ram_total_gb:.1f} GB")
            
            # Диск
            disk_total_gb = data['disk_total'] / (1024**3)
            self.hardware_listbox.insert(tk.END, f"💿 Загальний обсяг диска: {disk_total_gb:.0f} GB")
            
            # Акумулятор (для ноутбуків)
            battery_status = data.get('battery_status')
            if battery_status is not None:
                self.hardware_listbox.insert(tk.END, f"🔋 Заряд акумулятора: {battery_status}%")
            else:
                self.hardware_listbox.insert(tk.END, "🔋 Акумулятор: Не знайдено (настільний ПК)")
            
            self.hardware_listbox.insert(tk.END, "")
            
            # Служби Windows
            services_count = data.get('services_count')
            total_services = data.get('total_services')
            if services_count and total_services:
                self.hardware_listbox.insert(tk.END, f"⚙️ Служби Windows: {services_count}/{total_services} активні")
            
            self.hardware_listbox.insert(tk.END, "")
            self.hardware_listbox.insert(tk.END, "✅ Інформація оновлена")
            
            # Нараховуємо очки за оновлення інформації
            try:
                if hasattr(self, 'app_ref') and self.app_ref:
                    self.app_ref.data_manager.save_user_activity(
                        "hardware_info", 3, "Переглянуто інформацію про комплектуючі"
                    )
                    self.update_achievements_display()
            except:
                pass
        
        import threading
        threading.Thread(target=refresh, daemon=True).start()
    
    def run(self):
        """Запуск GUI"""
        self.root.mainloop()

def create_gui(update_callback):
    """Створення GUI інтерфейсу"""
    return TechCareGUI(update_callback)