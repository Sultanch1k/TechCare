# -*- coding: utf-8 -*-
"""
TechCare - Desktop застосунок для моніторингу ПК з Smart-нагадуванням
"""

import tkinter as tk
import threading
import time
import json
import sys
import multiprocessing
import ctypes
import ctypes.wintypes
from datetime import datetime
import os

from monitor import get_system_data
from json_data import JsonDataManager
from ai import SimpleAI

from achievements import SimpleAchievements
from tests import SimpleTests
from gui import create_gui

def singleton_win_mutex():
    mutex_name = "TechCareAppMutex2025"
    mutex = ctypes.windll.kernel32.CreateMutexW(None, ctypes.wintypes.BOOL(True), mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 183:
        print("TechCare вже запущено (mutex)")
        sys.exit(0)

def measure_time(label, func):
    start_time = time.perf_counter()
    result = func()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    output = f"{label}: {elapsed_time:.4f} секунд"
    print(output)
    with open('timings.log', 'a', encoding='utf-8') as f:
        f.write(output + '\n')
    return result

class TechCareApp:
    def __init__(self):
        print("[DEBUG] App instance created")
        self.gui = create_gui(self.update_data)

        self.gui.loading_screen.update_progress(20, "Ініціалізація модулів...")

        self.data_manager = JsonDataManager()
        self.ai_engine = SimpleAI(self.data_manager)
        
        self.achievements = SimpleAchievements(self.data_manager)
        self.tests = SimpleTests(self.data_manager)

        self.gui.loading_screen.update_progress(40, "Налаштування системи...")

        self.thresholds = {
            'cpu_warning': 80,
            'ram_warning': 85,
            'disk_warning': 90,
            
            'uptime_warning': 24
        }

        self.state = {
            'last_notification': {},
            'monitoring_active': True,
            'current_data': {}
        }

        self.gui.loading_screen.update_progress(60, "Запуск сервісів...")

        self.gui.set_app_ref(self)
        self.gui.root.protocol("WM_DELETE_WINDOW", self.shutdown)

        self.update_data()
        self.auto_collect_running = False

        self.gui.root.after(500, self.gui.finish_loading)
        self.start_auto_collect()

        print("Кінець ініціалізації TechCareApp")
    
    def background_collector(self):
        while self.auto_collect_running:
            try:
                data = get_system_data()
                self.data_manager.save_system_data(data)
            except Exception as e:
                print(f"[ERROR] background_collector: {e}")
            time.sleep(2)

    def start_auto_collect(self):
        self.auto_collect_running = True
        threading.Thread(target=self.background_collector, daemon=True).start()

    def stop_auto_collect(self):
        self.auto_collect_running = False

    def run(self):
        try:
            self.gui.root.after(800, lambda: threading.Thread(
                target=self.run_startup_diagnosis, daemon=True).start())
            self.monitor_thread = threading.Thread(
                target=self.start_monitoring, daemon=True)
            self.monitor_thread.start()
            self.measure_time("GUI run", lambda: self.gui.root.mainloop())
        except Exception as e:
            print(f"Критична помилка: {e}")
        finally:
            self.state['monitoring_active'] = False

    def run_startup_diagnosis(self):
        try:
            import pythoncom
            pythoncom.CoInitialize()
            data = measure_time("Get system data (startup diagnosis)", get_system_data)
            health = measure_time("Predict system health (startup diagnosis)",
                                  lambda: self.ai_engine.predict_system_health(data))

            if health['warnings']:
                message = "\n".join(health['warnings'][:3])
                self.gui.root.after(0, lambda: self.gui.show_notification("Попередження при запуску", message))
        except Exception as e:
            print(f"Помилка при автодіагностиці: {e}")
            self.gui.root.after(0, lambda: self.gui.show_notification("TechCare запущено", "Програма готова до роботи!"))
        finally:
            try:
                import pythoncom
                pythoncom.CoUninitialize()
            except:
                pass

    def measure_time(self, label, func):
        return measure_time(label, func)

    def start_monitoring(self):
        def monitor_loop():
            import pythoncom
            pythoncom.CoInitialize()
            try:
                while self.state['monitoring_active']:
                    try:
                        self.measure_time("Check system health (monitoring)", self.check_system_health)
                        time.sleep(30)
                    except Exception as e:
                        print(f"Помилка моніторингу: {e}")
                        time.sleep(60)
            finally:
                pythoncom.CoUninitialize()
        monitor_loop()
        

    def check_system_health(self):
        try:
            data = self.measure_time("Get system data (health check)", get_system_data)
            # self.save_history_entry(data)
            self.state['current_data'] = data
            # self.generate_smart_reminders(data)
            self.measure_time("Save system data", lambda: self.data_manager.save_system_data(data))
            health = self.measure_time("Predict system health (health check)", lambda: self.ai_engine.predict_system_health(data))
            self.measure_time("Check thresholds", lambda: self.check_thresholds(data, health))

            self.data_manager.save_user_activity("diagnostics_done", 1, "Системна діагностика")
            stats = self.data_manager.get_user_stats()
            self.achievements.check_achievements(stats)
            self.gui.update_achievements_display()

        except Exception as e:
            print(f"Помилка перевірки системи: {e}")

    def shutdown(self):
        """Коректно зупинити моніторинг і закрити програму."""
        print("[DEBUG] Shutting down monitoring threads")
            # сигналізуємо потоку завершитись
        self.state['monitoring_active'] = False
            # чекаємо максимум 5 секунд, щоб потік відреагував
        if hasattr(self, 'monitor_thread'):
                self.monitor_thread.join(timeout=5)
        # після цього чисто закриваємо GUI
        self.gui.root.destroy()

    def check_thresholds(self, data, health):
        current_time = time.time()
        for warning in health['warnings']:
            if any(word in warning.lower() for word in ['охолодіть', 'перезапустіть', 'очистіть']):
                if current_time - self.state['last_notification'].get('critical', 0) > 600:
                    self.gui.root.after(0, lambda: self.gui.show_notification("Критичне попередження!", warning))
                    self.state['last_notification']['critical'] = current_time
                    break

    def update_data(self):
        try:
            data = self.measure_time("Get system data (update data)", get_system_data)
            self.state['current_data'] = data
            # self.generate_smart_reminders(data)
            self.measure_time("Update main metrics", lambda: self.gui.update_main_metrics(data))
            health = self.measure_time("Predict system health (update data)", lambda: self.ai_engine.predict_system_health(data))

            health_color = '#00FF00' if health['health_score'] > 70 else '#FFFF00' if health['health_score'] > 40 else '#FF0000'
            self.measure_time("Update health label", lambda: self.gui.ai_tab.health_label.config(text=f"{health['health_score']}%", fg=health_color))

            self.measure_time("Update predictions text", lambda: self.gui.ai_tab.predictions_text.delete(1.0, tk.END))
            if health['warnings']:
                for warning in health['warnings']:
                    self.gui.ai_tab.predictions_text.insert(tk.END, f"⚠ {warning}\n")
            else:
                self.gui.ai_tab.predictions_text.insert(tk.END, "✓ Все працює нормально!\n")

            if health['predictions']:
                self.gui.ai_tab.predictions_text.insert(tk.END, "\nПрогнози:\n")
                for prediction in health['predictions']:
                    self.gui.ai_tab.predictions_text.insert(tk.END, f"• {prediction}\n")

            stats = self.measure_time("Get user stats", lambda: self.data_manager.get_user_stats())
            level = self.measure_time("Get user level", lambda: self.achievements.get_user_level(stats.get('total_points', 0)))
            self.measure_time("Update level label", lambda: self.gui.level_label.config(text=f"Рівень {level} ({stats.get('total_points', 0)} очок)"))

        except Exception as e:
            print(f"Помилка оновлення даних: {e}")
            self.gui.root.after(0, lambda err=e: self.gui.show_notification("Помилка", f"Не вдалося оновити дані: {err}"))

    
    
    

def main():
    print("Початок запуску програми")
    start_time = time.perf_counter()
    app_instance = measure_time("TechCareApp init", lambda: TechCareApp())
    app_instance.start_auto_collect()
    measure_time("App run", lambda: app_instance.run())
    end_time = time.perf_counter()
    print(f"Загальний час запуску: {end_time - start_time:.4f} секунд")

if __name__ == "__main__":
    singleton_win_mutex()
    multiprocessing.freeze_support()
    main()