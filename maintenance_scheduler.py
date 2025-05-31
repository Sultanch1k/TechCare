# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Планувальник технічного обслуговування
Модуль для автоматичного планування та виконання завдань
"""

import threading
import time
from datetime import datetime, timedelta, time as dt_time
import schedule

class TaskAutomation:
    """Система автоматизації завдань обслуговування"""
    
    def __init__(self, database_controller):
        self.db_handler = database_controller
        self.scheduler_thread = None
        self.is_running = False
        self.task_settings = self._load_scheduler_settings()
        
        # Ініціалізація стандартних завдань
        self._initialize_standard_tasks()
    
    def _load_scheduler_settings(self):
        """Завантаження налаштувань планувальника"""
        
        default_settings = {
            'auto_cleanup_enabled': True,
            'auto_scan_enabled': True,
            'auto_defrag_enabled': False,
            'auto_backup_enabled': False,
            'daily_maintenance_time': '02:00',
            'weekly_maintenance_day': 'Sunday',
            'notifications_enabled': True
        }
        
        # Завантаження з бази даних
        for key, default_value in default_settings.items():
            saved_value = self.db_handler.get_application_setting(key, default_value)
            default_settings[key] = saved_value
        
        return default_settings
    
    def _initialize_standard_tasks(self):
        """Ініціалізація стандартних завдань"""
        
        standard_tasks = self._generate_weekly_tasks()
        
        for task in standard_tasks:
            try:
                self.db_handler.store_maintenance_task(task)
            except Exception as error:
                print(f"Помилка ініціалізації завдання: {error}")
    
    def _generate_weekly_tasks(self):
        """Генерація завдань на тиждень"""
        
        base_date = datetime.now().date()
        tasks = []
        
        # Щоденні завдання
        daily_tasks = [
            {
                'title': 'Перевірка оновлень системи',
                'description': 'Автоматична перевірка доступних оновлень',
                'category': 'Безпека',
                'priority': 2
            },
            {
                'title': 'Сканування на загрози',
                'description': 'Швидке сканування системи на віруси',
                'category': 'Безпека',
                'priority': 3
            }
        ]
        
        # Щотижневі завдання
        weekly_tasks = [
            {
                'title': 'Очищення диска',
                'description': 'Видалення тимчасових та непотрібних файлів',
                'category': 'Оптимізація',
                'priority': 2,
                'day': 'Monday'
            },
            {
                'title': 'Дефрагментація диска',
                'description': 'Оптимізація розташування файлів на диску',
                'category': 'Оптимізація',
                'priority': 1,
                'day': 'Wednesday'
            },
            {
                'title': 'Повне системне сканування',
                'description': 'Глибоке сканування всієї системи',
                'category': 'Безпека',
                'priority': 2,
                'day': 'Friday'
            },
            {
                'title': 'Резервне копіювання',
                'description': 'Створення резервної копії важливих даних',
                'category': 'Надійність',
                'priority': 3,
                'day': 'Sunday'
            }
        ]
        
        # Створення завдань на найближчі дні
        for i in range(7):
            task_date = base_date + timedelta(days=i)
            weekday_name = task_date.strftime('%A')
            
            # Додавання щоденних завдань
            for daily_task in daily_tasks:
                task = daily_task.copy()
                task.update({
                    'date': task_date,
                    'time': dt_time(hour=8, minute=0),
                    'auto_generated': True
                })
                tasks.append(task)
            
            # Додавання щотижневих завдань
            for weekly_task in weekly_tasks:
                if weekly_task.get('day') == weekday_name:
                    task = weekly_task.copy()
                    task.update({
                        'date': task_date,
                        'time': dt_time(hour=20, minute=0),
                        'auto_generated': True
                    })
                    tasks.append(task)
        
        return tasks
    
    def get_todays_tasks(self):
        """Отримання завдань на сьогодні"""
        
        today = datetime.now().date()
        tasks = []
        
        connection = self.db_handler.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    SELECT task_id, task_name, task_description, scheduled_time, 
                           task_priority, task_category, completion_status
                    FROM maintenance_tasks 
                    WHERE scheduled_date = %s 
                    ORDER BY scheduled_time, task_priority DESC
                """, (today,))
                
                results = cursor.fetchall()
                
                for result in results:
                    tasks.append({
                        'id': result[0],
                        'title': result[1],
                        'description': result[2],
                        'time': result[3],
                        'priority': result[4],
                        'category': result[5],
                        'status': result[6]
                    })
                
                cursor.close()
                connection.close()
                
            except Exception as error:
                print(f"Помилка отримання завдань: {error}")
                if connection:
                    connection.close()
        
        return tasks
    
    def get_weekly_schedule(self):
        """Отримання розкладу на тиждень"""
        
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)
        
        weekly_tasks = {}
        
        connection = self.db_handler.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    SELECT scheduled_date, task_name, task_description, 
                           scheduled_time, task_category, completion_status
                    FROM maintenance_tasks 
                    WHERE scheduled_date BETWEEN %s AND %s 
                    ORDER BY scheduled_date, scheduled_time
                """, (start_date, end_date))
                
                results = cursor.fetchall()
                
                for result in results:
                    date_str = result[0].strftime('%Y-%m-%d')
                    
                    if date_str not in weekly_tasks:
                        weekly_tasks[date_str] = []
                    
                    weekly_tasks[date_str].append({
                        'title': result[1],
                        'description': result[2],
                        'time': result[3].strftime('%H:%M') if result[3] else '00:00',
                        'category': result[4],
                        'status': result[5]
                    })
                
                cursor.close()
                connection.close()
                
            except Exception as error:
                print(f"Помилка отримання розкладу: {error}")
                if connection:
                    connection.close()
        
        return weekly_tasks
    
    def add_custom_task(self, task_details):
        """Додавання користувацького завдання"""
        
        task_data = {
            'title': task_details.get('title', ''),
            'description': task_details.get('description', ''),
            'date': task_details.get('date'),
            'time': task_details.get('time'),
            'priority': task_details.get('priority', 1),
            'category': task_details.get('category', 'Користувацьке'),
            'auto_generated': False
        }
        
        self.db_handler.store_maintenance_task(task_data)
        return True
    
    def mark_task_completed(self, task_id):
        """Позначення завдання як виконаного"""
        
        connection = self.db_handler.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    UPDATE maintenance_tasks 
                    SET completion_status = 'completed',
                        completion_timestamp = CURRENT_TIMESTAMP
                    WHERE task_id = %s
                """, (task_id,))
                
                connection.commit()
                cursor.close()
                connection.close()
                
                return True
                
            except Exception as error:
                print(f"Помилка позначення завдання: {error}")
                if connection:
                    connection.close()
        
        return False
    
    def postpone_task(self, task_id, hours=24):
        """Відкладення завдання"""
        
        new_datetime = datetime.now() + timedelta(hours=hours)
        
        connection = self.db_handler.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    UPDATE maintenance_tasks 
                    SET scheduled_date = %s,
                        scheduled_time = %s
                    WHERE task_id = %s
                """, (new_datetime.date(), new_datetime.time(), task_id))
                
                connection.commit()
                cursor.close()
                connection.close()
                
                return True
                
            except Exception as error:
                print(f"Помилка відкладення завдання: {error}")
                if connection:
                    connection.close()
        
        return False
    
    def update_scheduler_settings(self, new_settings):
        """Оновлення налаштувань планувальника"""
        
        for key, value in new_settings.items():
            self.task_settings[key] = value
            self.db_handler.update_application_setting(key, value)
        
        # Перезапуск планувальника з новими налаштуваннями
        if self.is_running:
            self.stop_scheduler()
            self.start_scheduler()
    
    def start_scheduler(self):
        """Запуск планувальника"""
        
        if not self.is_running:
            self.is_running = True
            self.scheduler_thread = threading.Thread(target=self._scheduler_main_loop)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
    
    def stop_scheduler(self):
        """Зупинка планувальника"""
        
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
    
    def _scheduler_main_loop(self):
        """Основний цикл планувальника"""
        
        while self.is_running:
            try:
                # Перевірка завдань для виконання
                self._check_pending_tasks()
                
                # Очікування перед наступною перевіркою
                time.sleep(60)  # Перевірка кожну хвилину
                
            except Exception as error:
                print(f"Помилка в планувальнику: {error}")
                time.sleep(300)  # Очікування 5 хвилин при помилці
    
    def _check_pending_tasks(self):
        """Перевірка завдань для виконання"""
        
        current_time = datetime.now()
        
        connection = self.db_handler.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Пошук завдань для виконання
                cursor.execute("""
                    SELECT task_id, task_name, task_description, task_category
                    FROM maintenance_tasks 
                    WHERE scheduled_date = %s 
                    AND scheduled_time <= %s
                    AND completion_status = 'pending'
                """, (current_time.date(), current_time.time()))
                
                pending_tasks = cursor.fetchall()
                
                for task in pending_tasks:
                    self._execute_automatic_task(task)
                
                cursor.close()
                connection.close()
                
            except Exception as error:
                print(f"Помилка перевірки завдань: {error}")
                if connection:
                    connection.close()
    
    def _execute_automatic_task(self, task_info):
        """Виконання автоматичного завдання"""
        
        task_id, task_name, description, category = task_info
        
        try:
            # Симуляція виконання завдання
            if 'очищення' in task_name.lower():
                self._execute_cleanup_task()
            elif 'сканування' in task_name.lower():
                self._execute_scan_task()
            elif 'дефрагментація' in task_name.lower():
                self._execute_defrag_task()
            elif 'оновлення' in task_name.lower():
                self._execute_update_task()
            elif 'резервне' in task_name.lower():
                self._execute_backup_task()
            
            # Позначення як виконане
            self.mark_task_completed(task_id)
            
            print(f"Виконано завдання: {task_name}")
            
        except Exception as error:
            print(f"Помилка виконання завдання {task_name}: {error}")
    
    def _execute_cleanup_task(self):
        """Виконання завдання очищення"""
        time.sleep(2)  # Симуляція роботи
    
    def _execute_scan_task(self):
        """Виконання завдання сканування"""
        time.sleep(5)  # Симуляція роботи
    
    def _execute_defrag_task(self):
        """Виконання завдання дефрагментації"""
        time.sleep(10)  # Симуляція роботи
    
    def _execute_update_task(self):
        """Виконання завдання оновлення"""
        time.sleep(3)  # Симуляція роботи
    
    def _execute_backup_task(self):
        """Виконання завдання резервного копіювання"""
        time.sleep(8)  # Симуляція роботи
    
    def get_task_statistics(self):
        """Отримання статистики завдань"""
        
        stats = {
            'total_tasks': 0,
            'completed_tasks': 0,
            'pending_tasks': 0,
            'overdue_tasks': 0
        }
        
        connection = self.db_handler.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Загальна кількість завдань
                cursor.execute("SELECT COUNT(*) FROM maintenance_tasks")
                stats['total_tasks'] = cursor.fetchone()[0]
                
                # Виконані завдання
                cursor.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE completion_status = 'completed'")
                stats['completed_tasks'] = cursor.fetchone()[0]
                
                # Очікуючі завдання
                cursor.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE completion_status = 'pending'")
                stats['pending_tasks'] = cursor.fetchone()[0]
                
                # Прострочені завдання
                current_datetime = datetime.now()
                cursor.execute("""
                    SELECT COUNT(*) FROM maintenance_tasks 
                    WHERE completion_status = 'pending' 
                    AND (scheduled_date < %s OR 
                         (scheduled_date = %s AND scheduled_time < %s))
                """, (current_datetime.date(), current_datetime.date(), current_datetime.time()))
                stats['overdue_tasks'] = cursor.fetchone()[0]
                
                cursor.close()
                connection.close()
                
            except Exception as error:
                print(f"Помилка отримання статистики: {error}")
                if connection:
                    connection.close()
        
        return stats
    
    def cleanup_old_tasks(self, days_old=30):
        """Очищення старих виконаних завдань"""
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        connection = self.db_handler.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    DELETE FROM maintenance_tasks 
                    WHERE completion_status = 'completed' 
                    AND completion_timestamp < %s
                """, (cutoff_date,))
                
                deleted_count = cursor.rowcount
                connection.commit()
                cursor.close()
                connection.close()
                
                return deleted_count
                
            except Exception as error:
                print(f"Помилка очищення завдань: {error}")
                if connection:
                    connection.close()
        
        return 0