# -*- coding: utf-8 -*-
"""
TechCare - Main Application Module
Головний модуль додатка для моніторингу здоров'я комп'ютера

ІНСТРУКЦІЇ ДЛЯ ЛОКАЛЬНОГО ЗАПУСКУ:
1. Завантажте код з Replit (Download as zip)
2. Встановіть Python 3.11+ та бібліотеки: pip install psutil schedule flask
3. Desktop версія: python main.py
4. Веб-версія: python web_app.py (відкрийте http://localhost:5000)
5. Для створення .exe: pip install pyinstaller && pyinstaller --onefile main.py
"""

import threading
import time
import schedule
from monitor import get_system_data
from reminder import (
    check_thresholds, schedule_reminders, clear_state, 
    postpone_reminders, get_status_summary, get_detailed_history
)
from advanced_monitor import (
    check_driver_status, check_thermal_paste_status, 
    get_fan_detailed_status, get_system_health_score
)
from additional_features import (
    check_startup_programs, check_disk_health, 
    check_network_performance, check_system_security,
    get_performance_recommendations
)
from gui import create_gui

class TechCareApp:
    def __init__(self):
        """Ініціалізація додатка TechCare"""
        # Порогові значення
        self.thresholds = {
            'cpu_temp': 70,      # Температура CPU в °C
            'cpu_usage': 80,     # Використання CPU в % (якщо температура недоступна)
            'ram_usage': 90,     # Використання RAM в %
            'disk_usage': 90,    # Використання диска в %
            'uptime_restart': 86400  # Час роботи в секундах (24 години)
        }
        
        # Стан системи для відстеження
        self.state = {
            'high_temp_time': 0,   # Час початку високої температури
            'high_ram_time': 0,    # Час початку високого використання RAM
            'delay_until': 0       # Час до якого відкладено нагадування
        }
        
        # Поточні дані системи
        self.current_data = {}
        self.current_status = ("Ініціалізація...", "#BBBBBB")
        
        # GUI
        self.gui = None
        
        # Потік для планувальника
        self.scheduler_thread = None
        self.running = True
        
    def initialize_gui(self):
        """Ініціалізація графічного інтерфейсу"""
        self.gui = create_gui(self)
        
    def periodic_update(self):
        """Періодичне оновлення даних з розширеним аналізом"""
        try:
            # Отримання нових системних даних
            self.current_data = get_system_data()
            
            # Отримання розширених даних
            health_score = get_system_health_score()
            fan_details = get_fan_detailed_status()
            thermal_status = check_thermal_paste_status()
            driver_status = check_driver_status()
            
            # Перевірка порогових значень
            warnings = check_thresholds(self.current_data, self.thresholds, self.state)
            
            # Отримання поточного статусу
            self.current_status = get_status_summary(
                self.current_data, self.thresholds, self.state
            )
            
            # Створення розширеної структури даних
            advanced_data = {
                'health_score': health_score,
                'fan_details': fan_details,
                'thermal_status': thermal_status,
                'driver_status': driver_status
            }
            
            # Оновлення GUI з розширеними даними
            if self.gui:
                self.gui.update_display(
                    self.current_data, 
                    self.current_status, 
                    advanced_data
                )
                
                # Показ попереджень з системи моніторингу
                if warnings:
                    for warning in warnings:
                        self.gui.show_notification(
                            "Попередження системи",
                            warning,
                            "#FFE6E6"
                        )
                
                # Показ попереджень з розширеного аналізу
                if health_score.get('issues'):
                    for issue in health_score['issues']:
                        self.gui.show_notification(
                            "Проблема виявлена",
                            issue,
                            "#FFF3CD"
                        )
                        
        except Exception as e:
            print(f"Помилка при періодичному оновленні: {e}")
    
    def manual_update(self):
        """Ручне оновлення даних"""
        self.periodic_update()
        if self.gui:
            self.gui.show_notification(
                "Оновлення завершено",
                "Дані системи оновлено",
                "#E6F3FF"
            )
    
    def clear_state(self):
        """Очищення стану лічильників"""
        return clear_state(self.state)
    
    def postpone_reminders(self, minutes=30):
        """Відкладення нагадувань"""
        return postpone_reminders(self.state, minutes)
    
    def get_history(self):
        """Отримання детальної історії"""
        return get_detailed_history(self.state)
    
    def get_optimization_tips(self):
        """Отримання рекомендацій з оптимізації"""
        try:
            return get_performance_recommendations()
        except Exception as e:
            print(f"Помилка отримання рекомендацій: {e}")
            return [{'category': 'Помилка', 'issue': 'Не вдалося отримати рекомендації', 'recommendation': str(e), 'priority': 'low'}]
    
    def get_detailed_analysis(self):
        """Отримання детального аналізу системи"""
        try:
            startup_info = check_startup_programs()
            disk_health = check_disk_health()
            network_info = check_network_performance()
            security_info = check_system_security()
            
            return {
                'startup': startup_info,
                'disk_health': disk_health,
                'network': network_info,
                'security': security_info
            }
        except Exception as e:
            print(f"Помилка детального аналізу: {e}")
            return {
                'startup': {'total_count': 0, 'recommendation': 'Помилка аналізу'},
                'disk_health': {'total_disks': 0, 'warnings': []},
                'network': {'active_connections': 0},
                'security': {'security_score': 0}
            }
    
    def reminder_callback(self, warnings, data):
        """Callback для обробки нагадувань"""
        if self.gui:
            for warning in warnings:
                self.gui.show_notification(
                    "Нагадування TechCare",
                    warning,
                    "#FFE6E6"
                )
    
    def start_scheduler(self):
        """Запуск планувальника в окремому потоці"""
        def scheduler_worker():
            # Створення callback з доступом до state
            def callback_with_state(warnings, data):
                self.reminder_callback(warnings, data)
            
            callback_with_state.state = self.state
            
            # Планування нагадувань
            schedule_reminders(
                get_system_data,
                self.thresholds, 
                callback_with_state
            )
            
            # Запуск циклу планувальника
            while self.running:
                try:
                    schedule.run_pending()
                    time.sleep(1)
                except Exception as e:
                    print(f"Помилка планувальника: {e}")
                    time.sleep(5)
        
        self.scheduler_thread = threading.Thread(target=scheduler_worker, daemon=True)
        self.scheduler_thread.start()
    
    def run(self):
        """Запуск головної програми"""
        try:
            print("Запуск TechCare...")
            
            # Початкове отримання даних
            self.periodic_update()
            
            # Запуск планувальника
            self.start_scheduler()
            
            # Ініціалізація та запуск GUI
            self.initialize_gui()
            
            print("Запуск графічного інтерфейсу...")
            self.gui.run()
            
        except KeyboardInterrupt:
            print("\nЗавершення роботи...")
            self.running = False
        except Exception as e:
            print(f"Критична помилка: {e}")
        finally:
            self.running = False
            print("TechCare завершено")

def main():
    """Головна функція"""
    print("=" * 50)
    print("TechCare - Смарт-нагадувач для догляду за комп'ютером")
    print("Версія 1.0")
    print("=" * 50)
    
    try:
        app = TechCareApp()
        app.run()
    except Exception as e:
        print(f"Помилка запуску програми: {e}")
        input("Натисніть Enter для виходу...")

if __name__ == "__main__":
    main()
