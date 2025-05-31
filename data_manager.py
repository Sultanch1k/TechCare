# -*- coding: utf-8 -*-
"""
TechCare AI - PostgreSQL Data Manager Module
Модуль управління даними та PostgreSQL базою даних
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime, timedelta
import json
import os

class DataManager:
    def __init__(self):
        """Ініціалізація менеджера даних"""
        self.database_url = os.getenv('DATABASE_URL')
        self.init_database()
    
    def get_connection(self):
        """Створення з'єднання з базою даних"""
        return psycopg2.connect(self.database_url)
    
    def init_database(self):
        """Ініціалізація бази даних"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Таблиця системних даних
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_data (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    cpu_temp REAL,
                    cpu_percent REAL,
                    ram_percent REAL,
                    ram_available BIGINT,
                    ram_total BIGINT,
                    disk_percent REAL,
                    disk_free BIGINT,
                    disk_total BIGINT,
                    network_bytes_sent BIGINT,
                    network_bytes_recv BIGINT,
                    battery_percent REAL,
                    battery_plugged BOOLEAN,
                    process_count INTEGER,
                    boot_time TIMESTAMP
                )
            ''')
            
            # Таблиця активності користувача
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_activities (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activity_type VARCHAR(50),
                    experience_gained INTEGER DEFAULT 0,
                    description TEXT
                )
            ''')
            
            # Таблиця досягнень
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS achievements (
                    id SERIAL PRIMARY KEY,
                    achievement_id VARCHAR(50) UNIQUE,
                    unlocked_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    experience_reward INTEGER DEFAULT 0
                )
            ''')
            
            # Таблиця результатів бенчмарків
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS benchmark_results (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    overall_score INTEGER,
                    cpu_score INTEGER,
                    ram_score INTEGER,
                    disk_score INTEGER,
                    network_score INTEGER,
                    stability_score INTEGER,
                    efficiency_score INTEGER,
                    detailed_results TEXT
                )
            ''')
            
            # Таблиця історії ремонтів
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS repair_history (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    issue_type VARCHAR(100),
                    description TEXT,
                    action_taken TEXT,
                    success BOOLEAN,
                    result TEXT
                )
            ''')
            
            # Таблиця запланованих завдань
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scheduled_tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200),
                    description TEXT,
                    scheduled_date DATE,
                    scheduled_time TIME,
                    priority VARCHAR(20),
                    category VARCHAR(50),
                    completed BOOLEAN DEFAULT FALSE,
                    auto_generated BOOLEAN DEFAULT FALSE,
                    completed_date TIMESTAMP
                )
            ''')
            
            # Таблиця налаштувань
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key VARCHAR(100) PRIMARY KEY,
                    value TEXT
                )
            ''')
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Ініціалізація базових даних
            self.init_default_data()
            
        except Exception as e:
            print(f"Помилка ініціалізації бази даних: {e}")
    
    def init_default_data(self):
        """Ініціалізація базових даних"""
        try:
            # Додавання початкових налаштувань
            default_settings = {
                'user_level': '1',
                'total_experience': '0',
                'auto_repair_enabled': 'true',
                'notifications_enabled': 'true'
            }
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            for key, value in default_settings.items():
                cursor.execute('''
                    INSERT INTO settings (key, value) 
                    VALUES (%s, %s) 
                    ON CONFLICT (key) DO NOTHING
                ''', (key, value))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Помилка ініціалізації базових даних: {e}")
    
    def save_system_data(self, data):
        """Збереження системних даних"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO system_data 
                (cpu_temp, cpu_percent, ram_percent, ram_available, ram_total,
                 disk_percent, disk_free, disk_total, network_bytes_sent, 
                 network_bytes_recv, battery_percent, battery_plugged, 
                 process_count, boot_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                data.get('cpu_temp'),
                data.get('cpu_percent'),
                data.get('ram_percent'),
                data.get('ram_available'),
                data.get('ram_total'),
                data.get('disk_percent'),
                data.get('disk_free'),
                data.get('disk_total'),
                data.get('network_bytes_sent'),
                data.get('network_bytes_recv'),
                data.get('battery_percent'),
                data.get('battery_plugged'),
                data.get('process_count'),
                data.get('boot_time')
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            # Очищення старих даних
            self.cleanup_old_data()
            
        except Exception as e:
            print(f"Помилка збереження системних даних: {e}")
    
    def get_historical_data(self, days=7, hours=None):
        """Отримання історичних даних"""
        try:
            conn = self.get_connection()
            
            if hours:
                time_filter = f"timestamp >= NOW() - INTERVAL '{hours} hours'"
            else:
                time_filter = f"timestamp >= NOW() - INTERVAL '{days} days'"
            
            query = f'''
                SELECT * FROM system_data 
                WHERE {time_filter}
                ORDER BY timestamp DESC
            '''
            
            df = pd.read_sql(query, conn)
            conn.close()
            
            return df
            
        except Exception as e:
            print(f"Помилка отримання історичних даних: {e}")
            return pd.DataFrame()
    
    def cleanup_old_data(self):
        """Очищення старих даних"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Видалення даних старших за 30 днів
            cursor.execute('''
                DELETE FROM system_data 
                WHERE timestamp < NOW() - INTERVAL '30 days'
            ''')
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Помилка очищення старих даних: {e}")
    
    def save_user_activity(self, activity_type, exp_earned, description=""):
        """Збереження активності користувача"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_activities (activity_type, experience_gained, description)
                VALUES (%s, %s, %s)
            ''', (activity_type, exp_earned, description))
            
            # Оновлення загального досвіду
            cursor.execute('''
                SELECT value FROM settings WHERE key = 'total_experience'
            ''')
            result = cursor.fetchone()
            current_exp = int(result[0]) if result else 0
            new_exp = current_exp + exp_earned
            
            cursor.execute('''
                INSERT INTO settings (key, value) VALUES ('total_experience', %s)
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
            ''', (str(new_exp),))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Помилка збереження активності користувача: {e}")
    
    def get_user_stats(self):
        """Отримання статистики користувача"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Загальний досвід
            cursor.execute("SELECT value FROM settings WHERE key = 'total_experience'")
            total_exp_result = cursor.fetchone()
            total_experience = int(total_exp_result['value']) if total_exp_result else 0
            
            # Рівень користувача
            level = (total_experience // 100) + 1
            exp_for_next_level = (level * 100) - total_experience
            
            # Кількість досягнень
            cursor.execute("SELECT COUNT(*) as count FROM achievements")
            achievements_count = cursor.fetchone()['count']
            
            # Активність за останні 30 днів
            cursor.execute('''
                SELECT COUNT(*) as count FROM user_activities 
                WHERE timestamp >= NOW() - INTERVAL '30 days'
            ''')
            recent_activities = cursor.fetchone()['count']
            
            cursor.close()
            conn.close()
            
            return {
                'level': level,
                'total_experience': total_experience,
                'exp_for_next_level': exp_for_next_level,
                'achievements_unlocked': achievements_count,
                'recent_activities': recent_activities
            }
            
        except Exception as e:
            print(f"Помилка отримання статистики користувача: {e}")
            return {
                'level': 1,
                'total_experience': 0,
                'exp_for_next_level': 100,
                'achievements_unlocked': 0,
                'recent_activities': 0
            }
    
    def unlock_achievement(self, achievement_id):
        """Відкриття досягнення"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO achievements (achievement_id, experience_reward)
                VALUES (%s, %s)
                ON CONFLICT (achievement_id) DO NOTHING
            ''', (achievement_id, 50))
            
            if cursor.rowcount > 0:
                # Додати досвід за досягнення
                self.save_user_activity('achievement', 50, f'Відкрито досягнення: {achievement_id}')
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Помилка відкриття досягнення: {e}")
            return False
    
    def save_benchmark_result(self, results):
        """Збереження результатів бенчмарку"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO benchmark_results 
                (overall_score, cpu_score, ram_score, disk_score, 
                 network_score, stability_score, efficiency_score, detailed_results)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                results.get('overall_score'),
                results.get('cpu_score'),
                results.get('ram_score'),
                results.get('disk_score'),
                results.get('network_score'),
                results.get('stability_score'),
                results.get('efficiency_score'),
                json.dumps(results.get('detailed_results', {}))
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Помилка збереження результатів бенчмарку: {e}")
    
    def get_benchmark_history(self):
        """Отримання історії бенчмарків"""
        try:
            conn = self.get_connection()
            
            df = pd.read_sql('''
                SELECT * FROM benchmark_results 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''', conn)
            
            conn.close()
            return df
            
        except Exception as e:
            print(f"Помилка отримання історії бенчмарків: {e}")
            return pd.DataFrame()
    
    def save_repair_record(self, repair_data):
        """Збереження запису про ремонт"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO repair_history 
                (issue_type, description, action_taken, success, result)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                repair_data.get('issue_type'),
                repair_data.get('description'),
                repair_data.get('action_taken'),
                repair_data.get('success'),
                repair_data.get('result')
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Помилка збереження запису про ремонт: {e}")
    
    def get_repair_history(self):
        """Отримання історії ремонтів"""
        try:
            conn = self.get_connection()
            
            df = pd.read_sql('''
                SELECT * FROM repair_history 
                ORDER BY timestamp DESC 
                LIMIT 20
            ''', conn)
            
            conn.close()
            return df
            
        except Exception as e:
            print(f"Помилка отримання історії ремонтів: {e}")
            return pd.DataFrame()
    
    def save_scheduled_task(self, task_data):
        """Збереження запланованого завдання"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO scheduled_tasks 
                (title, description, scheduled_date, scheduled_time, 
                 priority, category, auto_generated)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                task_data.get('title'),
                task_data.get('description'),
                task_data.get('date'),
                task_data.get('time'),
                task_data.get('priority'),
                task_data.get('category'),
                task_data.get('auto_generated', False)
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Помилка збереження запланованого завдання: {e}")
            return False
    
    def get_setting(self, key, default_value=None):
        """Отримання налаштування"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM settings WHERE key = %s', (key,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return result[0] if result else default_value
            
        except Exception as e:
            print(f"Помилка отримання налаштування: {e}")
            return default_value
    
    def set_setting(self, key, value):
        """Збереження налаштування"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO settings (key, value) VALUES (%s, %s)
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
            ''', (key, str(value)))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"Помилка збереження налаштування: {e}")