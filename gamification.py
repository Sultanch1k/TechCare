# -*- coding: utf-8 -*-
"""
TechCare AI - Gamification System Module
Модуль геймифікації для мотивації користувачів
"""

import pandas as pd
from datetime import datetime, timedelta
import json

class GamificationSystem:
    def __init__(self, data_manager):
        """Ініціалізація системи геймифікації"""
        self.data_manager = data_manager
        self.achievement_definitions = self.init_achievements()
        self.reward_definitions = self.init_rewards()
    
    def init_achievements(self):
        """Ініціалізація визначень досягнень"""
        return {
            'first_launch': {
                'name': 'Перший запуск',
                'description': 'Запустіть TechCare AI вперше',
                'exp_reward': 100,
                'category': 'початківець',
                'icon': '🚀'
            },
            'daily_user': {
                'name': 'Щоденний користувач',
                'description': 'Використовуйте TechCare AI 7 днів поспіль',
                'exp_reward': 500,
                'category': 'активність',
                'icon': '📅'
            },
            'system_optimizer': {
                'name': 'Оптимізатор системи',
                'description': 'Виконайте 10 автоматичних оптимізацій',
                'exp_reward': 300,
                'category': 'оптимізація',
                'icon': '⚡'
            },
            'benchmark_master': {
                'name': 'Майстер бенчмарку',
                'description': 'Запустіть 5 бенчмарків',
                'exp_reward': 250,
                'category': 'тестування',
                'icon': '📊'
            },
            'health_monitor': {
                'name': 'Спостерігач здоров\'я',
                'description': 'Підтримуйте здоров\'я ПК вище 90% протягом тижня',
                'exp_reward': 400,
                'category': 'здоров\'я',
                'icon': '❤️'
            },
            'problem_solver': {
                'name': 'Розв\'язувач проблем',
                'description': 'Виправте 5 проблем системи',
                'exp_reward': 350,
                'category': 'ремонт',
                'icon': '🔧'
            },
            'data_collector': {
                'name': 'Збирач даних',
                'description': 'Зберіть 1000 записів системних даних',
                'exp_reward': 200,
                'category': 'дані',
                'icon': '📈'
            },
            'streak_hero': {
                'name': 'Герой серії',
                'description': 'Досягніть 30-денної серії використання',
                'exp_reward': 1000,
                'category': 'активність',
                'icon': '🔥'
            },
            'performance_guru': {
                'name': 'Гуру продуктивності',
                'description': 'Покращте загальну продуктивність на 20%',
                'exp_reward': 600,
                'category': 'продуктивність',
                'icon': '🏆'
            },
            'security_expert': {
                'name': 'Експерт безпеки',
                'description': 'Пройдіть всі перевірки безпеки',
                'exp_reward': 450,
                'category': 'безпека',
                'icon': '🛡️'
            }
        }
    
    def init_rewards(self):
        """Ініціалізація нагород"""
        return [
            {
                'id': 'theme_unlock',
                'name': 'Нова тема інтерфейсу',
                'description': 'Відкрийте додаткову тему для інтерфейсу',
                'cost': 500,
                'type': 'cosmetic',
                'icon': '🎨'
            },
            {
                'id': 'advanced_reports',
                'name': 'Розширені звіти',
                'description': 'Доступ до детальних аналітичних звітів',
                'cost': 1000,
                'type': 'feature',
                'icon': '📋'
            },
            {
                'id': 'priority_support',
                'name': 'Пріоритетна підтримка',
                'description': 'Швидша обробка запитів підтримки',
                'cost': 1500,
                'type': 'service',
                'icon': '🎫'
            },
            {
                'id': 'custom_alerts',
                'name': 'Персональні сповіщення',
                'description': 'Налаштування власних правил сповіщень',
                'cost': 800,
                'type': 'feature',
                'icon': '🔔'
            },
            {
                'id': 'export_data',
                'name': 'Експорт даних',
                'description': 'Можливість експорту всіх даних',
                'cost': 600,
                'type': 'feature',
                'icon': '💾'
            }
        ]
    
    def get_user_stats(self):
        """Отримання статистики користувача"""
        return self.data_manager.get_user_stats()
    
    def award_experience(self, activity_type, exp_amount, description=""):
        """Нарахування досвіду користувачу"""
        try:
            # Збереження активності
            self.data_manager.save_user_activity(activity_type, exp_amount, description)
            
            # Перевірка досягнень
            self.check_achievements()
            
            return True
        except Exception as e:
            print(f"Помилка нарахування досвіду: {e}")
            return False
    
    def check_achievements(self):
        """Перевірка та відкриття досягнень"""
        user_stats = self.get_user_stats()
        unlocked_achievements = []
        
        try:
            # Перевірка кожного досягнення
            for achievement_id, achievement_info in self.achievement_definitions.items():
                if not self.is_achievement_unlocked(achievement_id):
                    if self.check_achievement_condition(achievement_id, user_stats):
                        if self.data_manager.unlock_achievement(achievement_id):
                            unlocked_achievements.append(achievement_info['name'])
            
            return unlocked_achievements
        except Exception as e:
            print(f"Помилка перевірки досягнень: {e}")
            return []
    
    def check_achievement_condition(self, achievement_id, user_stats):
        """Перевірка умови для конкретного досягнення"""
        try:
            if achievement_id == 'first_launch':
                return user_stats['total_exp'] > 0
            
            elif achievement_id == 'daily_user':
                return user_stats['streak'] >= 7
            
            elif achievement_id == 'system_optimizer':
                # Підрахунок оптимізацій з історії активності
                optimization_count = self.count_activity_type('optimization')
                return optimization_count >= 10
            
            elif achievement_id == 'benchmark_master':
                benchmark_count = self.count_activity_type('benchmark')
                return benchmark_count >= 5
            
            elif achievement_id == 'health_monitor':
                # Перевірка підтримання здоров'я вище 90% протягом тижня
                return self.check_health_maintenance(90, 7)
            
            elif achievement_id == 'problem_solver':
                repair_count = self.count_activity_type('repair')
                return repair_count >= 5
            
            elif achievement_id == 'data_collector':
                # Підрахунок записів системних даних
                data_count = self.count_system_data_records()
                return data_count >= 1000
            
            elif achievement_id == 'streak_hero':
                return user_stats['streak'] >= 30
            
            elif achievement_id == 'performance_guru':
                return self.check_performance_improvement(20)
            
            elif achievement_id == 'security_expert':
                return self.check_security_completion()
            
            return False
        except Exception as e:
            print(f"Помилка перевірки умови досягнення {achievement_id}: {e}")
            return False
    
    def is_achievement_unlocked(self, achievement_id):
        """Перевірка чи досягнення вже відкрито"""
        try:
            conn = self.data_manager.db_path
            import sqlite3
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT unlocked FROM user_achievements WHERE achievement_id = ?', [achievement_id])
            result = cursor.fetchone()
            
            conn.close()
            
            return result and result[0] == 1
        except Exception as e:
            print(f"Помилка перевірки досягнення: {e}")
            return False
    
    def get_achievements(self):
        """Отримання всіх досягнень з їх статусом"""
        try:
            import sqlite3
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            achievements = []
            for achievement_id, achievement_info in self.achievement_definitions.items():
                cursor.execute('''
                    SELECT unlocked, unlocked_date, progress 
                    FROM user_achievements 
                    WHERE achievement_id = ?
                ''', [achievement_id])
                
                result = cursor.fetchone()
                
                achievement_data = {
                    'id': achievement_id,
                    'name': achievement_info['name'],
                    'description': achievement_info['description'],
                    'exp_reward': achievement_info['exp_reward'],
                    'category': achievement_info['category'],
                    'icon': achievement_info['icon'],
                    'unlocked': bool(result[0]) if result else False,
                    'unlocked_date': result[1] if result and result[1] else None,
                    'progress': result[2] if result else 0,
                    'target': 100  # Стандартна ціль
                }
                
                achievements.append(achievement_data)
            
            conn.close()
            return achievements
        except Exception as e:
            print(f"Помилка отримання досягнень: {e}")
            return []
    
    def get_activity_history(self, days=30):
        """Отримання історії активності"""
        try:
            import sqlite3
            conn = sqlite3.connect(self.data_manager.db_path)
            
            since_date = datetime.now() - timedelta(days=days)
            query = '''
                SELECT date, SUM(exp_earned) as exp_earned
                FROM user_activity 
                WHERE date >= ?
                GROUP BY date
                ORDER BY date
            '''
            
            df = pd.read_sql_query(query, conn, params=[since_date.date()])
            
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
            
            conn.close()
            return df
        except Exception as e:
            print(f"Помилка отримання історії активності: {e}")
            return pd.DataFrame()
    
    def get_category_stats(self):
        """Отримання статистики по категоріях активності"""
        try:
            import sqlite3
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT activity_type, SUM(exp_earned) as total_exp
                FROM user_activity
                GROUP BY activity_type
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            category_stats = {}
            for activity_type, total_exp in results:
                category_stats[activity_type] = total_exp
            
            return category_stats
        except Exception as e:
            print(f"Помилка отримання статистики категорій: {e}")
            return {}
    
    def get_streak_stats(self):
        """Отримання статистики streak"""
        try:
            import sqlite3
            conn = sqlite3.connect(self.data_manager.db_path)
            
            # Отримання всіх дат активності
            query = '''
                SELECT DISTINCT date 
                FROM user_activity 
                ORDER BY date DESC
            '''
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if df.empty:
                return {'current': 0, 'longest': 0, 'average': 0, 'total_streaks': 0}
            
            df['date'] = pd.to_datetime(df['date'])
            dates = df['date'].dt.date.tolist()
            
            # Розрахунок streaks
            streaks = []
            current_streak = 1
            longest_streak = 1
            
            for i in range(1, len(dates)):
                if (dates[i-1] - dates[i]).days == 1:
                    current_streak += 1
                else:
                    streaks.append(current_streak)
                    longest_streak = max(longest_streak, current_streak)
                    current_streak = 1
            
            streaks.append(current_streak)
            longest_streak = max(longest_streak, current_streak)
            
            # Поточний streak (від останньої дати до сьогодні)
            today = datetime.now().date()
            current_active_streak = 0
            
            if dates and (today - dates[0]).days <= 1:
                current_active_streak = current_streak
            
            return {
                'current': current_active_streak,
                'longest': longest_streak,
                'average': sum(streaks) / len(streaks) if streaks else 0,
                'total_streaks': len(streaks)
            }
        except Exception as e:
            print(f"Помилка розрахунку streak статистики: {e}")
            return {'current': 0, 'longest': 0, 'average': 0, 'total_streaks': 0}
    
    def get_available_rewards(self):
        """Отримання доступних нагород"""
        return self.reward_definitions
    
    def redeem_reward(self, reward_id):
        """Викуп нагороди"""
        try:
            # Знаходження нагороди
            reward = next((r for r in self.reward_definitions if r['id'] == reward_id), None)
            if not reward:
                return {'success': False, 'message': 'Нагорода не знайдена'}
            
            # Перевірка балів користувача
            user_stats = self.get_user_stats()
            if user_stats['reward_points'] < reward['cost']:
                return {'success': False, 'message': 'Недостатньо балів'}
            
            # Списання балів (реалізація залежить від логіки системи)
            # Тут можна додати логіку збереження викуплених нагород
            
            return {'success': True, 'message': f'Нагороду "{reward["name"]}" успішно отримано!'}
        except Exception as e:
            print(f"Помилка викупу нагороди: {e}")
            return {'success': False, 'message': 'Помилка при викупі нагороди'}
    
    def get_leaderboard(self, limit=10):
        """Отримання таблиці лідерів (заглушка для демонстрації)"""
        # В реальному застосунку тут би була логіка отримання даних інших користувачів
        user_stats = self.get_user_stats()
        
        return [{
            'rank': 1,
            'username': 'Поточний користувач',
            'level': user_stats['level'],
            'exp': user_stats['total_exp'],
            'achievements': user_stats['achievements_unlocked']
        }]
    
    # Допоміжні методи для перевірки умов досягнень
    def count_activity_type(self, activity_type):
        """Підрахунок активностей певного типу"""
        try:
            import sqlite3
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) FROM user_activity 
                WHERE activity_type = ?
            ''', [activity_type])
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else 0
        except Exception as e:
            print(f"Помилка підрахунку активності: {e}")
            return 0
    
    def count_system_data_records(self):
        """Підрахунок записів системних даних"""
        try:
            import sqlite3
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM system_data')
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else 0
        except Exception as e:
            print(f"Помилка підрахунку системних даних: {e}")
            return 0
    
    def check_health_maintenance(self, threshold, days):
        """Перевірка підтримання здоров'я системи"""
        try:
            # Логіка перевірки здоров'я за останні дні
            # (спрощена реалізація)
            historical_data = self.data_manager.get_historical_data(days=days)
            
            if historical_data.empty:
                return False
            
            # Розрахунок середнього "здоров'я" на основі системних метрик
            health_scores = []
            for _, row in historical_data.iterrows():
                score = 100
                
                # Зниження за високе використання ресурсів
                if row.get('cpu_percent', 0) > 80:
                    score -= 20
                if row.get('ram_percent', 0) > 90:
                    score -= 15
                if row.get('disk_percent', 0) > 90:
                    score -= 10
                
                health_scores.append(max(0, score))
            
            if health_scores:
                avg_health = sum(health_scores) / len(health_scores)
                return avg_health >= threshold
            
            return False
        except Exception as e:
            print(f"Помилка перевірки здоров'я: {e}")
            return False
    
    def check_performance_improvement(self, threshold_percent):
        """Перевірка покращення продуктивності"""
        try:
            # Порівняння поточної та минулої продуктивності
            # (спрощена логіка)
            current_data = self.data_manager.get_historical_data(days=7)
            past_data = self.data_manager.get_historical_data(days=14)
            
            if current_data.empty or past_data.empty:
                return False
            
            # Розрахунок середньої продуктивності
            current_performance = self.calculate_avg_performance(current_data)
            past_performance = self.calculate_avg_performance(past_data.iloc[:-len(current_data)])
            
            if past_performance > 0:
                improvement = ((current_performance - past_performance) / past_performance) * 100
                return improvement >= threshold_percent
            
            return False
        except Exception as e:
            print(f"Помилка перевірки покращення продуктивності: {e}")
            return False
    
    def calculate_avg_performance(self, data):
        """Розрахунок середньої продуктивності"""
        if data.empty:
            return 0
        
        # Спрощений розрахунок на основі обернених метрик використання
        avg_cpu = data['cpu_percent'].mean() if 'cpu_percent' in data else 0
        avg_ram = data['ram_percent'].mean() if 'ram_percent' in data else 0
        avg_disk = data['disk_percent'].mean() if 'disk_percent' in data else 0
        
        # Обернена логіка - менше використання = краща продуктивність
        performance = 100 - ((avg_cpu + avg_ram + avg_disk) / 3)
        return max(0, performance)
    
    def check_security_completion(self):
        """Перевірка завершення всіх перевірок безпеки"""
        try:
            # Тут би була логіка перевірки всіх пройдених перевірок безпеки
            # (спрощена реалізація)
            return True  # Заглушка
        except Exception as e:
            print(f"Помилка перевірки безпеки: {e}")
            return False
