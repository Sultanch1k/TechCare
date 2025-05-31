# -*- coding: utf-8 -*-
"""
TechCare AI - Maintenance Scheduler Module
Модуль планувальника обслуговування системи
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta, time
import calendar
import threading
import time as time_module
import os

class MaintenanceScheduler:
    def __init__(self, data_manager):
        """Ініціалізація планувальника"""
        self.data_manager = data_manager
        self.settings = self.load_settings()
        self.running = False
        self.scheduler_thread = None
        
        # Ініціалізація стандартних завдань
        self.init_default_tasks()
    
    def load_settings(self):
        """Завантаження налаштувань планувальника"""
        default_settings = {
            'auto_cleanup': True,
            'auto_defrag': True,
            'auto_updates': True,
            'auto_backup': False,
            'cleanup_time': '02:00',
            'defrag_day': 'Неділя',
            'update_frequency': 'Щотижня'
        }
        
        try:
            # Завантаження збережених налаштувань
            for key in default_settings.keys():
                saved_value = self.data_manager.get_setting(f'scheduler_{key}')
                if saved_value is not None:
                    # Конвертація рядків у булеві значення
                    if key in ['auto_cleanup', 'auto_defrag', 'auto_updates', 'auto_backup']:
                        default_settings[key] = saved_value.lower() == 'true'
                    else:
                        default_settings[key] = saved_value
        except Exception as e:
            print(f"Помилка завантаження налаштувань: {e}")
        
        return default_settings
    
    def init_default_tasks(self):
        """Ініціалізація стандартних завдань"""
        try:
            # Перевірка чи є вже створені автоматичні завдання
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM scheduled_tasks WHERE auto_generated = true')
            auto_tasks_count = cursor.fetchone()[0]
            
            if auto_tasks_count == 0:
                # Створення стандартних завдань
                default_tasks = self.generate_default_tasks()
                
                for task in default_tasks:
                    cursor.execute('''
                        INSERT INTO scheduled_tasks 
                        (title, description, scheduled_date, scheduled_time, priority, category, auto_generated)
                        VALUES (?, ?, ?, ?, ?, ?, 1)
                    ''', (
                        task['title'],
                        task['description'],
                        task['date'],
                        task['time'],
                        task['priority'],
                        task['category']
                    ))
                
                conn.commit()
            
            conn.close()
        except Exception as e:
            print(f"Помилка ініціалізації стандартних завдань: {e}")
    
    def generate_default_tasks(self):
        """Генерація стандартних завдань на тиждень"""
        tasks = []
        today = datetime.now().date()
        
        # Щоденне очищення
        if self.settings['auto_cleanup']:
            cleanup_time = self.settings['cleanup_time']
            for i in range(7):
                task_date = today + timedelta(days=i)
                tasks.append({
                    'title': 'Щоденне очищення системи',
                    'description': 'Автоматичне очищення тимчасових файлів та кешу',
                    'date': task_date,
                    'time': cleanup_time,
                    'priority': 'low',
                    'category': 'Очищення'
                })
        
        # Тижнева дефрагментація
        if self.settings['auto_defrag']:
            defrag_day = self.settings['defrag_day']
            defrag_date = self.get_next_weekday(today, defrag_day)
            tasks.append({
                'title': 'Дефрагментація диска',
                'description': 'Оптимізація розміщення файлів на диску',
                'date': defrag_date,
                'time': '03:00',
                'priority': 'medium',
                'category': 'Оптимізація'
            })
        
        # Перевірка оновлень
        if self.settings['auto_updates']:
            frequency = self.settings['update_frequency']
            if frequency == 'Щодня':
                for i in range(7):
                    task_date = today + timedelta(days=i)
                    tasks.append({
                        'title': 'Перевірка оновлень',
                        'description': 'Перевірка та встановлення оновлень системи',
                        'date': task_date,
                        'time': '12:00',
                        'priority': 'medium',
                        'category': 'Оновлення'
                    })
            elif frequency == 'Щотижня':
                update_date = today + timedelta(days=1)  # Завтра
                tasks.append({
                    'title': 'Перевірка оновлень',
                    'description': 'Перевірка та встановлення оновлень системи',
                    'date': update_date,
                    'time': '12:00',
                    'priority': 'medium',
                    'category': 'Оновлення'
                })
        
        # Резервне копіювання
        if self.settings['auto_backup']:
            backup_date = today + timedelta(days=2)  # Післязавтра
            tasks.append({
                'title': 'Резервне копіювання',
                'description': 'Створення резервної копії важливих файлів',
                'date': backup_date,
                'time': '01:00',
                'priority': 'high',
                'category': 'Резервування'
            })
        
        return tasks
    
    def get_next_weekday(self, start_date, weekday_name):
        """Отримання наступної дати для вказаного дня тижня"""
        weekdays = {
            'Понеділок': 0, 'Вівторок': 1, 'Середа': 2, 'Четвер': 3,
            'П\'ятниця': 4, 'Субота': 5, 'Неділя': 6
        }
        
        target_weekday = weekdays.get(weekday_name, 6)
        current_weekday = start_date.weekday()
        
        days_ahead = target_weekday - current_weekday
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        
        return start_date + timedelta(days=days_ahead)
    
    def get_today_tasks(self):
        """Отримання завдань на сьогодні"""
        try:
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().date()
            
            cursor.execute('''
                SELECT id, title, description, scheduled_time, priority, category, completed
                FROM scheduled_tasks 
                WHERE scheduled_date = ?
                ORDER BY scheduled_time
            ''', [today])
            
            rows = cursor.fetchall()
            tasks = []
            
            for row in rows:
                tasks.append({
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'scheduled_time': row[3],
                    'priority': row[4],
                    'category': row[5],
                    'completed': bool(row[6])
                })
            
            conn.close()
            return tasks
        except Exception as e:
            print(f"Помилка отримання завдань на сьогодні: {e}")
            return []
    
    def get_weekly_schedule(self):
        """Отримання розкладу на тиждень"""
        try:
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().date()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            
            cursor.execute('''
                SELECT scheduled_date, scheduled_time, title, description, priority, completed
                FROM scheduled_tasks 
                WHERE scheduled_date BETWEEN ? AND ?
                ORDER BY scheduled_date, scheduled_time
            ''', [week_start, week_end])
            
            rows = cursor.fetchall()
            
            # Організація завдань по днях
            weekly_schedule = {}
            weekdays = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя']
            
            for row in rows:
                task_date = datetime.strptime(row[0], '%Y-%m-%d').date()
                weekday = weekdays[task_date.weekday()]
                
                if weekday not in weekly_schedule:
                    weekly_schedule[weekday] = []
                
                weekly_schedule[weekday].append({
                    'time': row[1],
                    'title': row[2],
                    'description': row[3],
                    'priority': row[4],
                    'completed': bool(row[5])
                })
            
            conn.close()
            return weekly_schedule
        except Exception as e:
            print(f"Помилка отримання тижневого розкладу: {e}")
            return {}
    
    def add_custom_task(self, task_data):
        """Додавання власного завдання"""
        try:
            # Валідація даних
            required_fields = ['title', 'description', 'date', 'time', 'priority', 'category']
            for field in required_fields:
                if field not in task_data or not task_data[field]:
                    return {'success': False, 'message': f'Поле "{field}" є обов\'язковим'}
            
            # Перевірка дати
            if isinstance(task_data['date'], str):
                try:
                    task_date = datetime.strptime(task_data['date'], '%Y-%m-%d').date()
                except ValueError:
                    return {'success': False, 'message': 'Неправильний формат дати'}
            else:
                task_date = task_data['date']
            
            # Перевірка часу
            if isinstance(task_data['time'], str):
                try:
                    datetime.strptime(task_data['time'], '%H:%M')
                    task_time = task_data['time']
                except ValueError:
                    return {'success': False, 'message': 'Неправильний формат часу'}
            else:
                task_time = task_data['time'].strftime('%H:%M')
            
            # Збереження завдання
            success = self.data_manager.save_scheduled_task({
                'title': task_data['title'],
                'description': task_data['description'],
                'date': task_date,
                'time': task_time,
                'priority': task_data['priority'],
                'category': task_data['category'],
                'auto_generated': False
            })
            
            if success:
                return {'success': True, 'message': 'Завдання успішно додано'}
            else:
                return {'success': False, 'message': 'Помилка збереження завдання'}
                
        except Exception as e:
            return {'success': False, 'message': f'Помилка додавання завдання: {str(e)}'}
    
    def mark_task_completed(self, task_id):
        """Позначення завдання як виконаного"""
        try:
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE scheduled_tasks 
                SET completed = 1, completed_date = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', [task_id])
            
            affected_rows = cursor.rowcount
            conn.commit()
            conn.close()
            
            if affected_rows > 0:
                # Нарахування досвіду за виконання завдання
                self.data_manager.save_user_activity('task_completion', 25, 'Виконано заплановане завдання')
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Помилка позначення завдання як виконаного: {e}")
            return False
    
    def postpone_task(self, task_id, hours=24):
        """Відкладення завдання"""
        try:
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            # Отримання поточної дати та часу завдання
            cursor.execute('SELECT scheduled_date, scheduled_time FROM scheduled_tasks WHERE id = ?', [task_id])
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False
            
            current_date = datetime.strptime(result[0], '%Y-%m-%d').date()
            current_time = datetime.strptime(result[1], '%H:%M').time()
            current_datetime = datetime.combine(current_date, current_time)
            
            # Розрахунок нової дати та часу
            new_datetime = current_datetime + timedelta(hours=hours)
            new_date = new_datetime.date()
            new_time = new_datetime.time().strftime('%H:%M')
            
            # Оновлення завдання
            cursor.execute('''
                UPDATE scheduled_tasks 
                SET scheduled_date = ?, scheduled_time = ?
                WHERE id = ?
            ''', [new_date, new_time, task_id])
            
            affected_rows = cursor.rowcount
            conn.commit()
            conn.close()
            
            return affected_rows > 0
            
        except Exception as e:
            print(f"Помилка відкладення завдання: {e}")
            return False
    
    def update_settings(self, new_settings):
        """Оновлення налаштувань планувальника"""
        try:
            # Оновлення внутрішніх налаштувань
            self.settings.update(new_settings)
            
            # Збереження в базу даних
            for key, value in new_settings.items():
                self.data_manager.set_setting(f'scheduler_{key}', str(value))
            
            # Перегенерація автоматичних завдань якщо потрібно
            self.regenerate_auto_tasks()
            
            return True
        except Exception as e:
            print(f"Помилка оновлення налаштувань: {e}")
            return False
    
    def update_time_settings(self, time_settings):
        """Оновлення часових налаштувань"""
        try:
            # Валідація часових налаштувань
            if 'cleanup_time' in time_settings:
                try:
                    datetime.strptime(time_settings['cleanup_time'], '%H:%M')
                except ValueError:
                    return False
            
            # Оновлення налаштувань
            self.settings.update(time_settings)
            
            # Збереження в базу даних
            for key, value in time_settings.items():
                self.data_manager.set_setting(f'scheduler_{key}', str(value))
            
            return True
        except Exception as e:
            print(f"Помилка оновлення часових налаштувань: {e}")
            return False
    
    def regenerate_auto_tasks(self):
        """Перегенерація автоматичних завдань"""
        try:
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            # Видалення існуючих автоматичних завдань
            cursor.execute('DELETE FROM scheduled_tasks WHERE auto_generated = 1 AND completed = 0')
            
            # Створення нових автоматичних завдань
            new_tasks = self.generate_default_tasks()
            
            for task in new_tasks:
                cursor.execute('''
                    INSERT INTO scheduled_tasks 
                    (title, description, scheduled_date, scheduled_time, priority, category, auto_generated)
                    VALUES (?, ?, ?, ?, ?, ?, 1)
                ''', (
                    task['title'],
                    task['description'],
                    task['date'],
                    task['time'],
                    task['priority'],
                    task['category']
                ))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"Помилка перегенерації автоматичних завдань: {e}")
            return False
    
    def start_scheduler(self):
        """Запуск планувальника"""
        if self.running:
            return False
        
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        return True
    
    def stop_scheduler(self):
        """Зупинка планувальника"""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        return True
    
    def _scheduler_loop(self):
        """Основний цикл планувальника"""
        while self.running:
            try:
                # Перевірка завдань для виконання
                self._check_scheduled_tasks()
                
                # Очікування 60 секунд перед наступною перевіркою
                for _ in range(60):
                    if not self.running:
                        break
                    time_module.sleep(1)
                    
            except Exception as e:
                print(f"Помилка в циклі планувальника: {e}")
                time_module.sleep(60)
    
    def _check_scheduled_tasks(self):
        """Перевірка завдань для виконання"""
        try:
            current_datetime = datetime.now()
            current_date = current_datetime.date()
            current_time = current_datetime.time()
            
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            # Пошук завдань для виконання
            cursor.execute('''
                SELECT id, title, description, category, priority
                FROM scheduled_tasks 
                WHERE scheduled_date = ? 
                AND scheduled_time <= ? 
                AND completed = 0
                AND auto_generated = 1
            ''', [current_date, current_time.strftime('%H:%M')])
            
            tasks_to_execute = cursor.fetchall()
            
            for task in tasks_to_execute:
                task_id, title, description, category, priority = task
                
                # Виконання завдання
                execution_result = self._execute_scheduled_task(title, description, category)
                
                if execution_result['success']:
                    # Позначення як виконаного
                    self.mark_task_completed(task_id)
                    
                    # Логування
                    print(f"Виконано заплановане завдання: {title}")
                else:
                    print(f"Помилка виконання завдання {title}: {execution_result['message']}")
            
            conn.close()
            
        except Exception as e:
            print(f"Помилка перевірки запланованих завдань: {e}")
    
    def _execute_scheduled_task(self, title, description, category):
        """Виконання запланованого завдання"""
        try:
            if 'очищення' in title.lower() or category.lower() == 'очищення':
                return self._execute_cleanup_task()
            elif 'дефрагментація' in title.lower() or category.lower() == 'оптимізація':
                return self._execute_defrag_task()
            elif 'оновлення' in title.lower() or category.lower() == 'оновлення':
                return self._execute_update_task()
            elif 'резервування' in title.lower() or category.lower() == 'резервування':
                return self._execute_backup_task()
            else:
                return {'success': True, 'message': f'Завдання "{title}" виконано (симуляція)'}
                
        except Exception as e:
            return {'success': False, 'message': f'Помилка виконання завдання: {str(e)}'}
    
    def _execute_cleanup_task(self):
        """Виконання завдання очищення"""
        try:
            # Симуляція очищення - в реальності тут би був виклик системи автоматичного ремонту
            import tempfile
            import os
            
            # Очищення тимчасових файлів
            temp_dir = tempfile.gettempdir()
            cleaned_files = 0
            
            for item in os.listdir(temp_dir):
                try:
                    item_path = os.path.join(temp_dir, item)
                    if os.path.isfile(item_path) and item.endswith(('.tmp', '.temp')):
                        os.remove(item_path)
                        cleaned_files += 1
                except (OSError, PermissionError):
                    continue
            
            return {
                'success': True,
                'message': f'Очищення завершено. Видалено {cleaned_files} тимчасових файлів'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Помилка очищення: {str(e)}'}
    
    def _execute_defrag_task(self):
        """Виконання завдання дефрагментації"""
        try:
            # Симуляція дефрагментації
            # В реальності тут би був виклик системної команди дефрагментації
            
            return {
                'success': True,
                'message': 'Дефрагментація диска завершена (симуляція)'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Помилка дефрагментації: {str(e)}'}
    
    def _execute_update_task(self):
        """Виконання завдання оновлення"""
        try:
            # Симуляція перевірки оновлень
            # В реальності тут би був виклик системи оновлень
            
            return {
                'success': True,
                'message': 'Перевірка оновлень завершена (симуляція)'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Помилка перевірки оновлень: {str(e)}'}
    
    def _execute_backup_task(self):
        """Виконання завдання резервного копіювання"""
        try:
            # Симуляція резервного копіювання
            # В реальності тут би була логіка створення резервних копій
            
            return {
                'success': True,
                'message': 'Резервне копіювання завершено (симуляція)'
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Помилка резервного копіювання: {str(e)}'}
    
    def get_task_statistics(self):
        """Отримання статистики завдань"""
        try:
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            # Загальна статистика
            cursor.execute('SELECT COUNT(*) FROM scheduled_tasks')
            total_tasks = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM scheduled_tasks WHERE completed = 1')
            completed_tasks = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM scheduled_tasks WHERE scheduled_date = CURRENT_DATE')
            today_tasks = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM scheduled_tasks WHERE scheduled_date = CURRENT_DATE AND completed = 1')
            today_completed = cursor.fetchone()[0]
            
            # Статистика по категоріях
            cursor.execute('''
                SELECT category, COUNT(*) as count, SUM(completed) as completed_count
                FROM scheduled_tasks 
                GROUP BY category
            ''')
            
            category_stats = {}
            for row in cursor.fetchall():
                category, total, completed = row
                category_stats[category] = {
                    'total': total,
                    'completed': completed,
                    'completion_rate': (completed / total * 100) if total > 0 else 0
                }
            
            conn.close()
            
            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
                'today_tasks': today_tasks,
                'today_completed': today_completed,
                'today_completion_rate': (today_completed / today_tasks * 100) if today_tasks > 0 else 0,
                'category_stats': category_stats
            }
            
        except Exception as e:
            print(f"Помилка отримання статистики завдань: {e}")
            return {}
    
    def cleanup_old_tasks(self, days_old=30):
        """Очищення старих виконаних завдань"""
        try:
            conn = sqlite3.connect(self.data_manager.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.now().date() - timedelta(days=days_old)
            
            cursor.execute('''
                DELETE FROM scheduled_tasks 
                WHERE completed = 1 
                AND scheduled_date < ?
                AND auto_generated = 1
            ''', [cutoff_date])
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return deleted_count
            
        except Exception as e:
            print(f"Помилка очищення старих завдань: {e}")
            return 0
