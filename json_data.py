# -*- coding: utf-8 -*-
"""
Простий менеджер даних без PostgreSQL
Для роботи TechCare без бази даних
"""

import json
import os
from datetime import datetime
import psutil
import time

import GPUtil

def get_gpu_load():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            return gpus[0].load * 100  # Повертає % завантаження першої відеокарти
        else:
            return 0
    except Exception as e:
        print("[DEBUG] GPU Error:", e)
        return None


def get_uptime_str():
    try:
        import psutil, time
        boot_time = psutil.boot_time()
        now = time.time()
        uptime = int(now - boot_time)
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        return f"{hours} год {minutes} хв"
    except Exception as e:
        print(f"[DEBUG] Uptime error: {e}")
        return "—"
        
def get_window_count():
    try:
        import pygetwindow as gw
        return len([w for w in gw.getAllWindows() if w.title.strip()])
    except Exception:
        return 0

class JsonDataManager:
    def __init__(self):
        """Ініціалізація простого менеджера даних"""
        self.data_file = "techcare_data.json"
        self.load_data()
    
    def load_data(self):
        """Завантаження даних з файлу"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = {
                    'user_stats': {'total_points': 0, 'level': 1},
                    'achievements': [],
                    'system_history': [],
                    'settings': {}
                }
        except Exception:
            self.data = {
                'user_stats': {'total_points': 0, 'level': 1},
                'achievements': [],
                'system_history': [],
                'settings': {}
            }
    
    def save_data(self):
        """Збереження даних у файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Помилка збереження: {e}")
    
    def save_system_data(self, data):
        """Збереження системних даних"""
        try:
            record = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': data.get('cpu_percent', 0),
                'ram_percent': data.get('ram_percent', 0),
                'disk_percent': data.get('disk_percent', 0),
                
            }
            self.data['system_history'].append(record)
            
            # Зберігаємо тільки останні 100 записів
            if len(self.data['system_history']) > 100:
                self.data['system_history'] = self.data['system_history'][-100:]
            
            self.save_data()
            return True
        except Exception:
            return False
    
    def get_user_stats(self):
        """Отримання статистики користувача"""
        return self.data.get('user_stats', {'total_points': 0, 'level': 1})
    
    def save_user_activity(self, activity_type, exp_earned, description=""):
        """Збереження активності користувача"""
        try:
            stats = self.data.get('user_stats', {'total_points': 0})
            stats['total_points'] = stats.get('total_points', 0) + exp_earned
            self.data['user_stats'] = stats
            self.save_data()
            return True
        except Exception:
            return False
    
    def unlock_achievement(self, achievement_id):
        """Відкриття досягнення"""
        try:
            if achievement_id not in self.data['achievements']:
                self.data['achievements'].append(achievement_id)
                self.save_data()
            return True
        except Exception:
            return False
    
    def get_historical_data(self, days=7, hours=None):
        """Отримання історичних даних"""
        return self.data.get('system_history', [])
    
    def cleanup_old_data(self):
        """Очищення старих даних"""
        # Залишаємо тільки останні 50 записів
        if len(self.data['system_history']) > 50:
            self.data['system_history'] = self.data['system_history'][-50:]
            self.save_data()
    
    
    
    
    
    def save_scheduled_task(self, task_data):
        """Збереження запланованого завдання"""
        return True
    
    def get_setting(self, key, default_value=None):
        """Отримання налаштування"""
        return self.data.get('settings', {}).get(key, default_value)
    
    def set_setting(self, key, value):
        """Збереження налаштування"""
        if 'settings' not in self.data:
            self.data['settings'] = {}
        self.data['settings'][key] = value
        self.save_data()
        return True
    
    
    # Отримання поточних метрик системи
    def get_current_metrics(self):
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('C:\\').percent
        gpu_load = get_gpu_load()
        window_count = get_window_count()
        def get_uptime_hours_and_minutes():
            import psutil, time
            boot_time = psutil.boot_time()
            now = time.time()
            uptime = int(now - boot_time)
            hours = uptime // 3600
            minutes = (uptime % 3600) // 60
            return hours, minutes
        hours, minutes = get_uptime_hours_and_minutes()
        uptime_str = f"{hours} год {minutes} хв"
        return {
            "cpu_percent": cpu,
            "ram_percent": ram,
            "disk_percent": disk,
            "window_count": window_count,
            "uptime_hours": hours,
            "uptime_minutes": minutes,
            "gpu_load": gpu_load,
            "uptime_str": uptime_str  
        }

        

        
    