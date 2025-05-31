# -*- coding: utf-8 -*-
"""
TechCare - Desktop застосунок для моніторингу ПК
Головний файл з інтеграцією всіх модулів

Для локального запуску:
1. Встанови Python 3.11 і бібліотеки: pip install psutil schedule tkinter winsound psycopg2-binary scikit-learn numpy
2. Запусти: python main.py

Для .exe:
1. Встанови PyInstaller: pip install pyinstaller
2. Скомпілюй: pyinstaller --onefile main.py
"""

import tkinter as tk
import threading
import time

# Імпорт наших модулів
from monitor import get_system_data
from data_manager import DataManager
from ai import SimpleAI
from repair import SimpleRepair
from achievements import SimpleAchievements
from tests import SimpleTests
from gui import create_gui

class TechCareApp:
    def __init__(self):
        """Ініціалізація TechCare додатка"""
        # Ініціалізація компонентів
        self.data_manager = DataManager()
        self.ai_engine = SimpleAI(self.data_manager)
        self.repair_system = SimpleRepair()
        self.achievements = SimpleAchievements(self.data_manager)
        self.tests = SimpleTests(self.data_manager)
        
        # Пороги для сповіщень
        self.thresholds = {
            'cpu_warning': 80,
            'ram_warning': 85,
            'disk_warning': 90,
            'temp_warning': 70,
            'uptime_warning': 24
        }
        
        # Стан додатка
        self.state = {
            'last_notification': {},
            'monitoring_active': True,
            'current_data': {}
        }
        
        # Створення GUI
        self.gui = create_gui(self.update_data)
        
        # Запуск автодіагностики при старті
        self.run_startup_diagnosis()
        
        # Запуск моніторингу в фоновому режимі
        self.start_monitoring()
    
    def run_startup_diagnosis(self):
        """Автодіагностика при запуску"""
        try:
            data = get_system_data()
            health = self.ai_engine.predict_system_health(data)
            
            if health['warnings']:
                message = "\n".join(health['warnings'][:3])  # Показуємо перші 3 попередження
                self.gui.show_notification("Попередження при запуску", message)
                
        except Exception as e:
            print(f"Помилка при автодіагностиці: {e}")
    
    def start_monitoring(self):
        """Запуск фонового моніторингу"""
        def monitor_loop():
            while self.state['monitoring_active']:
                try:
                    self.check_system_health()
                    time.sleep(30)  # Перевірка кожні 30 секунд
                except Exception as e:
                    print(f"Помилка моніторингу: {e}")
                    time.sleep(60)  # При помилці - перевірка рідше
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def check_system_health(self):
        """Перевірка здоров'я системи та сповіщення"""
        try:
            data = get_system_data()
            self.state['current_data'] = data
            
            # Збереження даних в базу
            self.data_manager.save_system_data(data)
            
            # AI аналіз
            health = self.ai_engine.predict_system_health(data)
            
            # Перевірка порогів та сповіщення
            self.check_thresholds(data, health)
            
        except Exception as e:
            print(f"Помилка перевірки системи: {e}")
    
    def check_thresholds(self, data, health):
        """Перевірка порогів та відправка сповіщень"""
        current_time = time.time()
        
        # Перевірка критичних попереджень
        for warning in health['warnings']:
            if any(critical in warning.lower() for critical in ['охолодіть', 'перезапустіть', 'очистіть']):
                # Показуємо критичні попередження не частіше ніж раз на 10 хвилин
                if current_time - self.state['last_notification'].get('critical', 0) > 600:
                    self.gui.show_notification("Критичне попередження!", warning)
                    self.state['last_notification']['critical'] = current_time
                    break
        
        # Перевірка інших порогів
        if data['cpu_percent'] > self.thresholds['cpu_warning']:
            if current_time - self.state['last_notification'].get('cpu', 0) > 1800:  # 30 хвилин
                self.gui.show_notification("Високе навантаження CPU", 
                                         f"CPU: {data['cpu_percent']:.1f}%")
                self.state['last_notification']['cpu'] = current_time
        
        if data['ram_percent'] > self.thresholds['ram_warning']:
            if current_time - self.state['last_notification'].get('ram', 0) > 1800:
                self.gui.show_notification("Мало вільної пам'яті", 
                                         f"RAM: {data['ram_percent']:.1f}%")
                self.state['last_notification']['ram'] = current_time
    
    def update_data(self):
        """Оновлення даних в GUI (викликається по кнопці)"""
        try:
            data = get_system_data()
            self.state['current_data'] = data
            
            # Оновлення метрик в GUI
            self.gui.update_main_metrics(data)
            
            # AI аналіз для вкладки аналітики
            health = self.ai_engine.predict_system_health(data)
            
            # Оновлення AI вкладки
            health_color = '#00FF00' if health['health_score'] > 70 else '#FFFF00' if health['health_score'] > 40 else '#FF0000'
            self.gui.health_label.config(text=f"{health['health_score']}%", fg=health_color)
            
            # Оновлення попереджень
            self.gui.predictions_text.delete(1.0, tk.END)
            if health['warnings']:
                for warning in health['warnings']:
                    self.gui.predictions_text.insert(tk.END, f"⚠ {warning}\n")
            else:
                self.gui.predictions_text.insert(tk.END, "✓ Все працює нормально!\n")
            
            if health['predictions']:
                self.gui.predictions_text.insert(tk.END, "\nПрогнози:\n")
                for prediction in health['predictions']:
                    self.gui.predictions_text.insert(tk.END, f"• {prediction}\n")
            
            # Оновлення статистики досягнень
            try:
                stats = self.data_manager.get_user_stats()
                level = self.achievements.get_user_level(stats.get('total_points', 0))
                self.gui.level_label.config(text=f"Рівень {level} ({stats.get('total_points', 0)} очок)")
            except:
                pass
            
        except Exception as e:
            print(f"Помилка оновлення даних: {e}")
            self.gui.show_notification("Помилка", f"Не вдалося оновити дані: {e}")
    
    def run(self):
        """Запуск додатка"""
        try:
            # Перше оновлення даних
            self.update_data()
            
            # Запуск GUI
            self.gui.run()
            
        except Exception as e:
            print(f"Критична помилка: {e}")
        finally:
            # Зупинка моніторингу при закритті
            self.state['monitoring_active'] = False

def main():
    """Головна функція"""
    try:
        app = TechCareApp()
        app.run()
    except Exception as e:
        print(f"Помилка запуску додатка: {e}")
        import tkinter.messagebox as msgbox
        msgbox.showerror("Помилка", f"Не вдалося запустити TechCare:\n{e}")

if __name__ == "__main__":
    main()