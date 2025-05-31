# -*- coding: utf-8 -*-
"""
TechCare AI - Data Manager Module
Модуль управління даними та базою даних
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import json
import os

class DataManager:
    def __init__(self, db_path='techcare_data.db'):
        """Ініціалізація менеджера даних"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Ініціалізація бази даних"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Таблиця системних даних
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    cpu_temp REAL,
                    cpu_percent REAL,
                    ram_percent REAL,
                    disk_percent REAL,
                    uptime_seconds INTEGER,
                    fan_speed REAL,
                    additional_data TEXT
                )
            ''')
            
            # Таблиця досягнень користувача
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    achievement_id TEXT UNIQUE,
                    name TEXT,
                    description TEXT,
                    unlocked BOOLEAN DEFAULT FALSE,
                    unlocked_date DATETIME,
                    exp_reward INTEGER,
                    progress INTEGER DEFAULT 0,
                    target INTEGER DEFAULT 100
                )
            ''')
            
            # Таблиця активності користувача
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_activity (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    activity_type TEXT,
                    exp_earned INTEGER,
                    description TEXT
                )
            ''')
            
            # Таблиця бенчмарків
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS benchmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
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
            
            # Таблиця автоматичних ремонтів
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auto_repairs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    issue_type TEXT,
                    description TEXT,
                    action_taken TEXT,
                    success BOOLEAN,
                    result TEXT
                )
            ''')
            
            # Таблиця розкладу завдань
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scheduled_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    scheduled_date DATE,
                    scheduled_time TIME,
                    priority TEXT,
                    category TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    completed_date DATETIME,
                    auto_generated BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Таблиця налаштувань
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Ініціалізація базових даних
            self.init_default_data()
            
        except Exception as e:
            print(f"Помилка ініціалізації бази даних: {e}")
    
    def init_default_data(self):
        """Ініціалізація базових даних"""
        # Ініціалізація досягнень
        default_achievements = [
            {
                'achievement_id': 'first_launch',
                'name': 'Перший запуск',
                'description': 'Запустіть TechCare AI вперше',
                'exp_reward': 100,
                'target': 1
            },
            {
                'achievement_id': 'daily_user',
                'name': 'Щоденний користувач',
                'description': 'Використовуйте TechCare AI 7 днів поспіль',
                'exp_reward': 500,
                'target': 7
            },
            {
                'achievement_id': 'system_optimizer',
                'name': 'Оптимізатор системи',
                'description': 'Виконайте 10 автоматичних оптимізацій',
                'exp_reward': 300,
                'target': 10
            },
            {
                'achievement_id': 'benchmark_master',
                'name': 'Майстер бенчмарку',
                'description': 'Запустіть 5 бенчмарків',
                'exp_reward': 250,
                'target': 5
            },
            {
                'achievement_id': 'health_monitor',
                'name': 'Спостерігач здоров\'я',
                'description': 'Підтримуйте здоров\'я ПК вище 90% протягом тижня',
                'exp_reward': 400,
                'target': 7
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for achievement in default_achievements:
            cursor.execute('''
                INSERT OR IGNORE INTO user_achievements 
                (achievement_id, name, description, exp_reward, target)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                achievement['achievement_id'],
                achievement['name'],
                achievement['description'],
                achievement['exp_reward'],
                achievement['target']
            ))
        
        conn.commit()
        conn.close()
    
    def save_system_data(self, data):
        """Збереження системних даних"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Підготовка додаткових даних
            additional_data = {
                'uptime_str': data.get('uptime_str', ''),
                'timestamp': data.get('timestamp', datetime.now()).isoformat()
            }
            
            cursor.execute('''
                INSERT INTO system_data 
                (cpu_temp, cpu_percent, ram_percent, disk_percent, uptime_seconds, fan_speed, additional_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('cpu_temp'),
                data.get('cpu_percent'),
                data.get('ram_percent'),
                data.get('disk_percent'),
                data.get('uptime_seconds'),
                data.get('fan_speed'),
                json.dumps(additional_data)
            ))
            
            conn.commit()
            conn.close()
            
            # Очищення старих даних (залишаємо тільки останні 30 днів)
            self.cleanup_old_data()
            
        except Exception as e:
            print(f"Помилка збереження системних даних: {e}")
    
    def get_historical_data(self, days=7, hours=None):
        """Отримання історичних даних"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            if hours:
                since_time = datetime.now() - timedelta(hours=hours)
                query = '''
                    SELECT * FROM system_data 
                    WHERE timestamp >= ?
                    ORDER BY timestamp
                '''
                df = pd.read_sql_query(query, conn, params=[since_time])
            else:
                since_date = datetime.now() - timedelta(days=days)
                query = '''
                    SELECT * FROM system_data 
                    WHERE timestamp >= ?
                    ORDER BY timestamp
                '''
                df = pd.read_sql_query(query, conn, params=[since_date])
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            conn.close()
            return df
            
        except Exception as e:
            print(f"Помилка отримання історичних даних: {e}")
            return pd.DataFrame()
    
    def cleanup_old_data(self):
        """Очищення старих даних"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Видалення даних старших 30 днів
            cutoff_date = datetime.now() - timedelta(days=30)
            cursor.execute('DELETE FROM system_data WHERE timestamp < ?', [cutoff_date])
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Помилка очищення старих даних: {e}")
    
    def save_user_activity(self, activity_type, exp_earned, description=""):
        """Збереження активності користувача"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_activity (date, activity_type, exp_earned, description)
                VALUES (DATE('now'), ?, ?, ?)
            ''', (activity_type, exp_earned, description))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Помилка збереження активності: {e}")
    
    def get_user_stats(self):
        """Отримання статистики користувача"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Загальний досвід
            cursor.execute('SELECT SUM(exp_earned) FROM user_activity')
            total_exp = cursor.fetchone()[0] or 0
            
            # Досвід за сьогодні
            cursor.execute('SELECT SUM(exp_earned) FROM user_activity WHERE date = DATE("now")')
            today_exp = cursor.fetchone()[0] or 0
            
            # Кількість досягнень
            cursor.execute('SELECT COUNT(*) FROM user_achievements WHERE unlocked = 1')
            achievements_unlocked = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT COUNT(*) FROM user_achievements')
            total_achievements = cursor.fetchone()[0] or 0
            
            # Розрахунок рівня
            level = max(1, int(total_exp / 1000) + 1)
            current_level_exp = total_exp % 1000
            exp_for_next_level = 1000
            exp_to_next = exp_for_next_level - current_level_exp
            
            # Streak (дні поспіль)
            cursor.execute('''
                SELECT COUNT(DISTINCT date) FROM user_activity 
                WHERE date >= DATE('now', '-7 days')
            ''')
            streak = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                'level': level,
                'total_exp': total_exp,
                'today_exp': today_exp,
                'current_level_exp': current_level_exp,
                'exp_for_next_level': exp_for_next_level,
                'exp_to_next': exp_to_next,
                'achievements_unlocked': achievements_unlocked,
                'total_achievements': total_achievements,
                'streak': streak,
                'streak_active': today_exp > 0,
                'reward_points': total_exp // 100  # 1 бал за кожні 100 XP
            }
            
        except Exception as e:
            print(f"Помилка отримання статистики: {e}")
            return {
                'level': 1, 'total_exp': 0, 'today_exp': 0,
                'current_level_exp': 0, 'exp_for_next_level': 1000,
                'exp_to_next': 1000, 'achievements_unlocked': 0,
                'total_achievements': 0, 'streak': 0,
                'streak_active': False, 'reward_points': 0
            }
    
    def unlock_achievement(self, achievement_id):
        """Відкриття досягнення"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Перевірка чи досягнення вже відкрито
            cursor.execute('SELECT unlocked FROM user_achievements WHERE achievement_id = ?', [achievement_id])
            result = cursor.fetchone()
            
            if result and not result[0]:
                # Відкриття досягнення
                cursor.execute('''
                    UPDATE user_achievements 
                    SET unlocked = 1, unlocked_date = CURRENT_TIMESTAMP 
                    WHERE achievement_id = ?
                ''', [achievement_id])
                
                # Отримання нагороди
                cursor.execute('SELECT exp_reward, name FROM user_achievements WHERE achievement_id = ?', [achievement_id])
                reward_data = cursor.fetchone()
                
                if reward_data:
                    exp_reward, name = reward_data
                    self.save_user_activity('achievement', exp_reward, f'Досягнення: {name}')
                
                conn.commit()
                conn.close()
                return True
            
            conn.close()
            return False
            
        except Exception as e:
            print(f"Помилка відкриття досягнення: {e}")
            return False
    
    def save_benchmark_result(self, results):
        """Збереження результатів бенчмарку"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO benchmarks 
                (overall_score, cpu_score, ram_score, disk_score, network_score, stability_score, efficiency_score, detailed_results)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                results.get('overall_score', 0),
                results.get('cpu_score', 0),
                results.get('ram_score', 0),
                results.get('disk_score', 0),
                results.get('network_score', 0),
                results.get('stability_score', 0),
                results.get('efficiency_score', 0),
                json.dumps(results.get('detailed_results', {}))
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Помилка збереження бенчмарку: {e}")
    
    def get_benchmark_history(self):
        """Отримання історії бенчмарків"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            df = pd.read_sql_query('''
                SELECT * FROM benchmarks 
                ORDER BY timestamp DESC 
                LIMIT 30
            ''', conn)
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            conn.close()
            return df
            
        except Exception as e:
            print(f"Помилка отримання історії бенчмарків: {e}")
            return pd.DataFrame()
    
    def save_repair_record(self, repair_data):
        """Збереження запису про ремонт"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO auto_repairs 
                (issue_type, description, action_taken, success, result)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                repair_data.get('issue_type', ''),
                repair_data.get('description', ''),
                repair_data.get('action_taken', ''),
                repair_data.get('success', False),
                repair_data.get('result', '')
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Помилка збереження запису ремонту: {e}")
    
    def get_repair_history(self):
        """Отримання історії ремонтів"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
                SELECT * FROM auto_repairs 
                ORDER BY timestamp DESC 
                LIMIT 50
            '''
            
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            repairs = []
            for row in rows:
                repairs.append({
                    'id': row[0],
                    'timestamp': datetime.fromisoformat(row[1]),
                    'issue_type': row[2],
                    'description': row[3],
                    'action_taken': row[4],
                    'success': bool(row[5]),
                    'result': row[6]
                })
            
            conn.close()
            return repairs
            
        except Exception as e:
            print(f"Помилка отримання історії ремонтів: {e}")
            return []
    
    def save_scheduled_task(self, task_data):
        """Збереження запланованого завдання"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO scheduled_tasks 
                (title, description, scheduled_date, scheduled_time, priority, category, auto_generated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                task_data.get('title', ''),
                task_data.get('description', ''),
                task_data.get('date', ''),
                task_data.get('time', ''),
                task_data.get('priority', 'medium'),
                task_data.get('category', 'general'),
                task_data.get('auto_generated', False)
            ))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Помилка збереження завдання: {e}")
            return False
    
    def get_setting(self, key, default_value=None):
        """Отримання налаштування"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM settings WHERE key = ?', [key])
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return result[0]
            return default_value
            
        except Exception as e:
            print(f"Помилка отримання налаштування: {e}")
            return default_value
    
    def set_setting(self, key, value):
        """Збереження налаштування"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value)
                VALUES (?, ?)
            ''', [key, str(value)])
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Помилка збереження налаштування: {e}")
