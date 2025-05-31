# -*- coding: utf-8 -*-
"""
TechCare - GUI модуль з Tkinter
Графічний інтерфейс для desktop додатка
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

# Безпечний імпорт winsound (тільки для Windows)
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

class TechCareGUI:
    def __init__(self, update_callback):
        self.update_callback = update_callback
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Налаштування головного вікна"""
        self.root.title("TechCare")
        self.root.geometry("400x500")
        self.root.configure(bg='#1E1E1E')
        self.root.resizable(False, False)
        
        # Стилі
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1E1E1E')
        style.configure('TNotebook.Tab', background='#2D2D2D', foreground='white')
        style.configure('TFrame', background='#1E1E1E')
        style.configure('TLabel', background='#1E1E1E', foreground='white')
        style.configure('TButton', background='#333333', foreground='white')
        
    def create_widgets(self):
        """Створення віджетів інтерфейсу"""
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#1E1E1E')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(title_frame, text="TechCare", 
                              font=('Roboto', 16, 'bold'), 
                              fg='#00DDEB', bg='#1E1E1E')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Твій помічник для догляду за ПК",
                                 font=('Roboto', 10), 
                                 fg='#BBBBBB', bg='#1E1E1E')
        subtitle_label.pack()
        
        # Notebook з вкладками
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Створення вкладок
        self.create_main_tab()
        self.create_ai_tab()
        self.create_repair_tab()
        self.create_achievements_tab()
        self.create_tests_tab()
        self.create_schedule_tab()
        
    def create_main_tab(self):
        """Вкладка 'Головна'"""
        main_frame = ttk.Frame(self.notebook)
        self.notebook.add(main_frame, text="Головна")
        
        # Показники системи
        metrics_frame = tk.Frame(main_frame, bg='#1E1E1E')
        metrics_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # CPU
        self.cpu_frame = tk.Frame(metrics_frame, bg='#1E1E1E', relief='solid', bd=1)
        self.cpu_frame.grid(row=0, column=0, padx=2, pady=2, sticky='ew')
        self.cpu_label = tk.Label(self.cpu_frame, text="CPU: 0%", 
                                 font=('Roboto', 10), fg='white', bg='#1E1E1E')
        self.cpu_label.pack(pady=5)
        
        # RAM
        self.ram_frame = tk.Frame(metrics_frame, bg='#1E1E1E', relief='solid', bd=1)
        self.ram_frame.grid(row=0, column=1, padx=2, pady=2, sticky='ew')
        self.ram_label = tk.Label(self.ram_frame, text="RAM: 0%", 
                                 font=('Roboto', 10), fg='white', bg='#1E1E1E')
        self.ram_label.pack(pady=5)
        
        # Диск
        self.disk_frame = tk.Frame(metrics_frame, bg='#1E1E1E', relief='solid', bd=1)
        self.disk_frame.grid(row=1, column=0, padx=2, pady=2, sticky='ew')
        self.disk_label = tk.Label(self.disk_frame, text="Диск: 0%", 
                                  font=('Roboto', 10), fg='white', bg='#1E1E1E')
        self.disk_label.pack(pady=5)
        
        # Температура
        self.temp_frame = tk.Frame(metrics_frame, bg='#1E1E1E', relief='solid', bd=1)
        self.temp_frame.grid(row=1, column=1, padx=2, pady=2, sticky='ew')
        self.temp_label = tk.Label(self.temp_frame, text="Температура: 0°C", 
                                  font=('Roboto', 10), fg='white', bg='#1E1E1E')
        self.temp_label.pack(pady=5)
        
        # Час роботи
        self.uptime_frame = tk.Frame(metrics_frame, bg='#1E1E1E', relief='solid', bd=1)
        self.uptime_frame.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky='ew')
        self.uptime_label = tk.Label(self.uptime_frame, text="Час роботи: 0 год", 
                                    font=('Roboto', 10), fg='white', bg='#1E1E1E')
        self.uptime_label.pack(pady=5)
        
        # Вентилятори
        self.fan_frame = tk.Frame(metrics_frame, bg='#1E1E1E', relief='solid', bd=1)
        self.fan_frame.grid(row=3, column=0, columnspan=2, padx=2, pady=2, sticky='ew')
        self.fan_label = tk.Label(self.fan_frame, text="Вентилятори: Н/Д", 
                                 font=('Roboto', 10), fg='white', bg='#1E1E1E')
        self.fan_label.pack(pady=5)
        
        # Налаштування сітки
        metrics_frame.columnconfigure(0, weight=1)
        metrics_frame.columnconfigure(1, weight=1)
        
        # Кнопка оновлення
        update_btn = tk.Button(main_frame, text="Оновити", 
                              font=('Roboto', 10), bg='#333333', fg='white',
                              command=self.update_callback)
        update_btn.pack(pady=10)
        
    def create_ai_tab(self):
        """Вкладка 'AI Аналітика'"""
        ai_frame = ttk.Frame(self.notebook)
        self.notebook.add(ai_frame, text="AI Аналітика")
        
        # Індекс здоров'я
        health_frame = tk.Frame(ai_frame, bg='#1E1E1E')
        health_frame.pack(fill='x', padx=5, pady=5)
        
        health_title = tk.Label(health_frame, text="Індекс здоров'я системи", 
                               font=('Roboto', 12, 'bold'), fg='#00DDEB', bg='#1E1E1E')
        health_title.pack()
        
        self.health_label = tk.Label(health_frame, text="85%", 
                                    font=('Roboto', 20), fg='#00FF00', bg='#1E1E1E')
        self.health_label.pack()
        
        # Прогнози
        predictions_frame = tk.Frame(ai_frame, bg='#1E1E1E')
        predictions_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        predictions_title = tk.Label(predictions_frame, text="Прогнози та попередження", 
                                     font=('Roboto', 12, 'bold'), fg='#00DDEB', bg='#1E1E1E')
        predictions_title.pack()
        
        self.predictions_text = tk.Text(predictions_frame, height=10, 
                                       bg='#2D2D2D', fg='white', font=('Roboto', 9))
        self.predictions_text.pack(fill='both', expand=True, pady=5)
        
    def create_repair_tab(self):
        """Вкладка 'Ремонт'"""
        repair_frame = ttk.Frame(self.notebook)
        self.notebook.add(repair_frame, text="Ремонт")
        
        # Кнопки діагностики
        buttons_frame = tk.Frame(repair_frame, bg='#1E1E1E')
        buttons_frame.pack(fill='x', padx=5, pady=5)
        
        diagnose_btn = tk.Button(buttons_frame, text="Діагностика", 
                                font=('Roboto', 10), bg='#333333', fg='white',
                                command=self.run_diagnosis)
        diagnose_btn.pack(side='left', padx=5)
        
        fix_btn = tk.Button(buttons_frame, text="Виправити", 
                           font=('Roboto', 10), bg='#333333', fg='white',
                           command=self.run_repairs)
        fix_btn.pack(side='left', padx=5)
        
        # Список проблем
        problems_frame = tk.Frame(repair_frame, bg='#1E1E1E')
        problems_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        problems_title = tk.Label(problems_frame, text="Знайдені проблеми", 
                                 font=('Roboto', 12, 'bold'), fg='#00DDEB', bg='#1E1E1E')
        problems_title.pack()
        
        self.problems_listbox = tk.Listbox(problems_frame, bg='#2D2D2D', fg='white', 
                                          font=('Roboto', 9))
        self.problems_listbox.pack(fill='both', expand=True, pady=5)
        
    def create_achievements_tab(self):
        """Вкладка 'Досягнення'"""
        achievements_frame = ttk.Frame(self.notebook)
        self.notebook.add(achievements_frame, text="Досягнення")
        
        # Рівень користувача
        level_frame = tk.Frame(achievements_frame, bg='#1E1E1E')
        level_frame.pack(fill='x', padx=5, pady=5)
        
        level_title = tk.Label(level_frame, text="Ваш рівень", 
                              font=('Roboto', 12, 'bold'), fg='#00DDEB', bg='#1E1E1E')
        level_title.pack()
        
        self.level_label = tk.Label(level_frame, text="Рівень 1 (0 очок)", 
                                   font=('Roboto', 14), fg='#FFD700', bg='#1E1E1E')
        self.level_label.pack()
        
        # Список досягнень
        achievements_list_frame = tk.Frame(achievements_frame, bg='#1E1E1E')
        achievements_list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        achievements_title = tk.Label(achievements_list_frame, text="Досягнення", 
                                     font=('Roboto', 12, 'bold'), fg='#00DDEB', bg='#1E1E1E')
        achievements_title.pack()
        
        self.achievements_listbox = tk.Listbox(achievements_list_frame, bg='#2D2D2D', fg='white', 
                                              font=('Roboto', 9))
        self.achievements_listbox.pack(fill='both', expand=True, pady=5)
        
    def create_tests_tab(self):
        """Вкладка 'Тести'"""
        tests_frame = ttk.Frame(self.notebook)
        self.notebook.add(tests_frame, text="Тести")
        
        # Кнопки тестів
        tests_buttons_frame = tk.Frame(tests_frame, bg='#1E1E1E')
        tests_buttons_frame.pack(fill='x', padx=5, pady=5)
        
        cpu_test_btn = tk.Button(tests_buttons_frame, text="Тест CPU", 
                                font=('Roboto', 10), bg='#333333', fg='white',
                                command=self.run_cpu_test)
        cpu_test_btn.pack(side='left', padx=5)
        
        ram_test_btn = tk.Button(tests_buttons_frame, text="Тест RAM", 
                                font=('Roboto', 10), bg='#333333', fg='white',
                                command=self.run_ram_test)
        ram_test_btn.pack(side='left', padx=5)
        
        disk_test_btn = tk.Button(tests_buttons_frame, text="Тест диска", 
                                 font=('Roboto', 10), bg='#333333', fg='white',
                                 command=self.run_disk_test)
        disk_test_btn.pack(side='left', padx=5)
        
        # Результати тестів
        results_frame = tk.Frame(tests_frame, bg='#1E1E1E')
        results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        results_title = tk.Label(results_frame, text="Результати тестів", 
                                font=('Roboto', 12, 'bold'), fg='#00DDEB', bg='#1E1E1E')
        results_title.pack()
        
        self.results_text = tk.Text(results_frame, height=10, 
                                   bg='#2D2D2D', fg='white', font=('Roboto', 9))
        self.results_text.pack(fill='both', expand=True, pady=5)
        
    def create_schedule_tab(self):
        """Вкладка 'Розклад'"""
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="Розклад")
        
        # Кнопка додавання завдання
        add_task_btn = tk.Button(schedule_frame, text="Додати завдання", 
                                font=('Roboto', 10), bg='#333333', fg='white',
                                command=self.add_task)
        add_task_btn.pack(pady=5)
        
        # Список завдань
        tasks_frame = tk.Frame(schedule_frame, bg='#1E1E1E')
        tasks_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        tasks_title = tk.Label(tasks_frame, text="Заплановані завдання", 
                              font=('Roboto', 12, 'bold'), fg='#00DDEB', bg='#1E1E1E')
        tasks_title.pack()
        
        self.tasks_listbox = tk.Listbox(tasks_frame, bg='#2D2D2D', fg='white', 
                                       font=('Roboto', 9))
        self.tasks_listbox.pack(fill='both', expand=True, pady=5)
        
    def update_main_metrics(self, data):
        """Оновлення метрик на головній вкладці"""
        self.cpu_label.config(text=f"CPU: {data['cpu_percent']:.1f}%")
        self.ram_label.config(text=f"RAM: {data['ram_percent']:.1f}%")
        self.disk_label.config(text=f"Диск: {data['disk_percent']:.1f}%")
        self.temp_label.config(text=f"Температура: {data.get('temperature', 'Н/Д')}°C")
        self.uptime_label.config(text=f"Час роботи: {data.get('uptime_hours', 0):.1f} год")
        
        fan_speed = data.get('fan_speed')
        if fan_speed:
            self.fan_label.config(text=f"Вентилятори: {fan_speed} RPM")
        else:
            self.fan_label.config(text="Вентилятори: Н/Д")
    
    def show_notification(self, title, message):
        """Показ сповіщення з звуком"""
        if HAS_WINSOUND:
            try:
                import winsound
                winsound.Beep(1000, 500)  # Звук 1000Hz на 500ms
            except:
                pass  # Якщо звук не працює
        
        messagebox.showwarning(title, message)
    
    def run_diagnosis(self):
        """Запуск діагностики"""
        self.problems_listbox.delete(0, tk.END)
        self.problems_listbox.insert(tk.END, "Запуск діагностики...")
    
    def run_repairs(self):
        """Запуск ремонту"""
        messagebox.showinfo("Ремонт", "Ремонт виконано!")
    
    def run_cpu_test(self):
        """Запуск тесту CPU"""
        self.results_text.insert(tk.END, "Запуск тесту CPU...\n")
    
    def run_ram_test(self):
        """Запуск тесту RAM"""
        self.results_text.insert(tk.END, "Запуск тесту RAM...\n")
    
    def run_disk_test(self):
        """Запуск тесту диска"""
        self.results_text.insert(tk.END, "Запуск тесту диска...\n")
    
    def add_task(self):
        """Додавання завдання"""
        self.tasks_listbox.insert(tk.END, "Нове завдання")
    
    def run(self):
        """Запуск GUI"""
        self.root.mainloop()

def create_gui(update_callback):
    """Створення GUI інтерфейсу"""
    return TechCareGUI(update_callback)