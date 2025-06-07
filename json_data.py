# -*- coding: utf-8 -*-
"""
Простий менеджер даних без PostgreSQL
Для роботи TechCare без бази даних
"""

import json
import os
from datetime import datetime

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
                'temperature': data.get('temperature')
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