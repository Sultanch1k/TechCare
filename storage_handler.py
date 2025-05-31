# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Контролер зберігання даних
Модуль управління PostgreSQL базою даних
"""

import psycopg2
import pandas as pd
import os
from datetime import datetime, timedelta
import json

class DatabaseController:
    """Контролер для управління базою даних"""
    
    def __init__(self):
        self.connection_params = self._get_database_config()
        self._ensure_database_structure()
        self._initialize_default_records()
    
    def _get_database_config(self):
        """Отримання конфігурації бази даних"""
        return {
            'host': os.getenv('PGHOST', 'localhost'),
            'port': os.getenv('PGPORT', '5432'),
            'database': os.getenv('PGDATABASE', 'systemwatch'),
            'user': os.getenv('PGUSER', 'postgres'),
            'password': os.getenv('PGPASSWORD', '')
        }
    
    def establish_connection(self):
        """Встановлення з'єднання з базою даних"""
        try:
            connection = psycopg2.connect(**self.connection_params)
            return connection
        except Exception as error:
            print(f"Помилка підключення до БД: {error}")
            return None
    
    def _ensure_database_structure(self):
        """Забезпечення існування структури бази даних"""
        
        create_tables_sql = [
            # Таблиця системних метрик
            """
            CREATE TABLE IF NOT EXISTS hardware_metrics (
                metric_id SERIAL PRIMARY KEY,
                collection_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processor_load FLOAT,
                memory_utilization FLOAT,
                storage_capacity FLOAT,
                thermal_status FLOAT,
                network_throughput BIGINT,
                active_processes INTEGER,
                system_uptime FLOAT
            )
            """,
            
            # Таблиця користувацької активності
            """
            CREATE TABLE IF NOT EXISTS user_progress (
                activity_id SERIAL PRIMARY KEY,
                user_identifier VARCHAR(100) DEFAULT 'default_user',
                experience_points INTEGER DEFAULT 0,
                current_level INTEGER DEFAULT 1,
                completed_tasks INTEGER DEFAULT 0,
                activity_streak INTEGER DEFAULT 0,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            
            # Таблиця досягнень
            """
            CREATE TABLE IF NOT EXISTS user_achievements (
                achievement_id SERIAL PRIMARY KEY,
                achievement_code VARCHAR(50) UNIQUE,
                achievement_name VARCHAR(200),
                achievement_description TEXT,
                unlock_criteria TEXT,
                experience_reward INTEGER,
                is_unlocked BOOLEAN DEFAULT FALSE,
                unlock_timestamp TIMESTAMP
            )
            """,
            
            # Таблиця результатів тестування
            """
            CREATE TABLE IF NOT EXISTS performance_tests (
                test_id SERIAL PRIMARY KEY,
                test_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processor_score INTEGER,
                memory_score INTEGER,
                storage_score INTEGER,
                network_score INTEGER,
                overall_rating INTEGER,
                test_duration FLOAT,
                detailed_results JSONB
            )
            """,
            
            # Таблиця історії ремонтів
            """
            CREATE TABLE IF NOT EXISTS repair_operations (
                operation_id SERIAL PRIMARY KEY,
                operation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                problem_category VARCHAR(100),
                problem_description TEXT,
                solution_applied TEXT,
                operation_success BOOLEAN,
                execution_duration FLOAT,
                system_impact TEXT
            )
            """,
            
            # Таблиця планованих завдань
            """
            CREATE TABLE IF NOT EXISTS maintenance_tasks (
                task_id SERIAL PRIMARY KEY,
                task_name VARCHAR(200),
                task_description TEXT,
                scheduled_date DATE,
                scheduled_time TIME,
                task_priority INTEGER,
                task_category VARCHAR(100),
                is_automated BOOLEAN DEFAULT TRUE,
                completion_status VARCHAR(50) DEFAULT 'pending',
                completion_timestamp TIMESTAMP
            )
            """,
            
            # Таблиця налаштувань
            """
            CREATE TABLE IF NOT EXISTS application_settings (
                setting_id SERIAL PRIMARY KEY,
                setting_key VARCHAR(100) UNIQUE,
                setting_value TEXT,
                setting_type VARCHAR(50),
                last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                for sql_statement in create_tables_sql:
                    cursor.execute(sql_statement)
                connection.commit()
                cursor.close()
            except Exception as error:
                print(f"Помилка створення таблиць: {error}")
            finally:
                connection.close()
    
    def _initialize_default_records(self):
        """Ініціалізація базових записів"""
        
        default_achievements = [
            {
                'code': 'first_launch',
                'name': 'Перший запуск',
                'description': 'Вітаємо з першим запуском SystemWatch Pro!',
                'criteria': 'Запустити програму вперше',
                'reward': 50
            },
            {
                'code': 'system_guardian',
                'name': 'Охоронець системи',
                'description': 'Виконано 10 перевірок системи',
                'criteria': 'Провести 10 діагностик системи',
                'reward': 100
            },
            {
                'code': 'optimization_master',
                'name': 'Майстер оптимізації',
                'description': 'Успішно виправлено 25 проблем',
                'criteria': 'Виправити 25 системних проблем',
                'reward': 200
            },
            {
                'code': 'performance_expert',
                'name': 'Експерт продуктивності',
                'description': 'Проведено 5 тестів продуктивності',
                'criteria': 'Виконати 5 бенчмарків системи',
                'reward': 150
            },
            {
                'code': 'maintenance_pro',
                'name': 'Професіонал обслуговування',
                'description': 'Виконано 50 планових завдань',
                'criteria': 'Завершити 50 завдань обслуговування',
                'reward': 300
            }
        ]
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Перевірка та додавання досягнень
                for achievement in default_achievements:
                    cursor.execute("""
                        INSERT INTO user_achievements 
                        (achievement_code, achievement_name, achievement_description, unlock_criteria, experience_reward)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (achievement_code) DO NOTHING
                    """, (
                        achievement['code'],
                        achievement['name'],
                        achievement['description'],
                        achievement['criteria'],
                        achievement['reward']
                    ))
                
                # Ініціалізація користувацького прогресу
                cursor.execute("""
                    INSERT INTO user_progress (user_identifier, experience_points, current_level)
                    VALUES ('default_user', 0, 1)
                    ON CONFLICT DO NOTHING
                """)
                
                connection.commit()
                cursor.close()
                
            except Exception as error:
                print(f"Помилка ініціалізації даних: {error}")
            finally:
                connection.close()
    
    def record_system_snapshot(self, metrics_data):
        """Запис знімка системних метрик"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    INSERT INTO hardware_metrics 
                    (processor_load, memory_utilization, storage_capacity, thermal_status, 
                     network_throughput, active_processes, system_uptime)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    metrics_data.get('cpu_usage', 0),
                    metrics_data.get('memory_usage', 0),
                    metrics_data.get('storage_usage', 0),
                    metrics_data.get('thermal_reading', 0),
                    metrics_data.get('network_bytes_sent', 0),
                    metrics_data.get('running_processes', 0),
                    metrics_data.get('uptime_seconds', 0)
                ))
                
                connection.commit()
                cursor.close()
                
            except Exception as error:
                print(f"Помилка запису метрик: {error}")
            finally:
                connection.close()
    
    def get_historical_data(self, days=7, hours=None):
        """Отримання історичних даних"""
        
        connection = self.establish_connection()
        if connection:
            try:
                # Визначення часового діапазону
                if hours:
                    time_filter = datetime.now() - timedelta(hours=hours)
                else:
                    time_filter = datetime.now() - timedelta(days=days)
                
                query = """
                    SELECT collection_time, processor_load as cpu_percent, 
                           memory_utilization as ram_percent, storage_capacity as disk_percent,
                           thermal_status, network_throughput as network_speed
                    FROM hardware_metrics 
                    WHERE collection_time >= %s 
                    ORDER BY collection_time ASC
                """
                
                dataframe = pd.read_sql(query, connection, params=[time_filter])
                connection.close()
                
                return dataframe
                
            except Exception as error:
                print(f"Помилка отримання історичних даних: {error}")
                connection.close()
        
        return pd.DataFrame()
    
    def log_user_activity(self, activity_category, points_earned, activity_description=""):
        """Логування активності користувача"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Оновлення прогресу користувача
                cursor.execute("""
                    UPDATE user_progress 
                    SET experience_points = experience_points + %s,
                        completed_tasks = completed_tasks + 1,
                        last_activity = CURRENT_TIMESTAMP
                    WHERE user_identifier = 'default_user'
                """, (points_earned,))
                
                # Перерахунок рівня
                cursor.execute("""
                    UPDATE user_progress 
                    SET current_level = GREATEST(1, (experience_points / 300) + 1)
                    WHERE user_identifier = 'default_user'
                """)
                
                connection.commit()
                cursor.close()
                
            except Exception as error:
                print(f"Помилка логування активності: {error}")
            finally:
                connection.close()
    
    def get_user_statistics(self):
        """Отримання статистики користувача"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    SELECT experience_points, current_level, completed_tasks, 
                           activity_streak, last_activity
                    FROM user_progress 
                    WHERE user_identifier = 'default_user'
                """)
                
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                
                if result:
                    return {
                        'total_experience': result[0],
                        'level': result[1],
                        'tasks_completed': result[2],
                        'streak_days': result[3],
                        'last_activity': result[4]
                    }
                    
            except Exception as error:
                print(f"Помилка отримання статистики: {error}")
                if connection:
                    connection.close()
        
        return {'total_experience': 0, 'level': 1, 'tasks_completed': 0, 'streak_days': 0}
    
    def award_achievement(self, achievement_code):
        """Нагородження досягненням"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Перевірка, чи досягнення вже отримано
                cursor.execute("""
                    SELECT is_unlocked FROM user_achievements 
                    WHERE achievement_code = %s
                """, (achievement_code,))
                
                result = cursor.fetchone()
                
                if result and not result[0]:
                    # Відкриття досягнення
                    cursor.execute("""
                        UPDATE user_achievements 
                        SET is_unlocked = TRUE, unlock_timestamp = CURRENT_TIMESTAMP
                        WHERE achievement_code = %s
                    """, (achievement_code,))
                    
                    # Додавання очок досвіду
                    cursor.execute("""
                        SELECT experience_reward FROM user_achievements 
                        WHERE achievement_code = %s
                    """, (achievement_code,))
                    
                    reward = cursor.fetchone()
                    if reward:
                        cursor.execute("""
                            UPDATE user_progress 
                            SET experience_points = experience_points + %s
                            WHERE user_identifier = 'default_user'
                        """, (reward[0],))
                    
                    connection.commit()
                    cursor.close()
                    return True
                
                cursor.close()
                
            except Exception as error:
                print(f"Помилка нагородження досягненням: {error}")
            finally:
                connection.close()
        
        return False
    
    def save_benchmark_results(self, test_results):
        """Збереження результатів тестування"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    INSERT INTO performance_tests 
                    (processor_score, memory_score, storage_score, network_score, 
                     overall_rating, test_duration, detailed_results)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    test_results.get('cpu_score', 0),
                    test_results.get('memory_score', 0),
                    test_results.get('disk_score', 0),
                    test_results.get('network_score', 0),
                    test_results.get('overall_score', 0),
                    test_results.get('duration', 0),
                    json.dumps(test_results)
                ))
                
                connection.commit()
                cursor.close()
                
            except Exception as error:
                print(f"Помилка збереження результатів тестування: {error}")
            finally:
                connection.close()
    
    def get_benchmark_timeline(self):
        """Отримання історії тестувань"""
        
        connection = self.establish_connection()
        if connection:
            try:
                query = """
                    SELECT test_timestamp as timestamp, overall_rating as overall_score,
                           processor_score, memory_score, storage_score
                    FROM performance_tests 
                    ORDER BY test_timestamp DESC 
                    LIMIT 20
                """
                
                dataframe = pd.read_sql(query, connection)
                connection.close()
                
                return dataframe
                
            except Exception as error:
                print(f"Помилка отримання історії тестувань: {error}")
                connection.close()
        
        return pd.DataFrame()
    
    def log_repair_operation(self, operation_data):
        """Логування операції ремонту"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    INSERT INTO repair_operations 
                    (problem_category, problem_description, solution_applied, 
                     operation_success, execution_duration, system_impact)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    operation_data.get('category', 'Unknown'),
                    operation_data.get('description', ''),
                    operation_data.get('solution', ''),
                    operation_data.get('success', False),
                    operation_data.get('duration', 0),
                    operation_data.get('impact', '')
                ))
                
                connection.commit()
                cursor.close()
                
            except Exception as error:
                print(f"Помилка логування ремонту: {error}")
            finally:
                connection.close()
    
    def store_maintenance_task(self, task_details):
        """Збереження планового завдання"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    INSERT INTO maintenance_tasks 
                    (task_name, task_description, scheduled_date, scheduled_time, 
                     task_priority, task_category, is_automated)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    task_details.get('title', ''),
                    task_details.get('description', ''),
                    task_details.get('date'),
                    task_details.get('time'),
                    task_details.get('priority', 1),
                    task_details.get('category', ''),
                    task_details.get('auto_generated', True)
                ))
                
                connection.commit()
                cursor.close()
                
            except Exception as error:
                print(f"Помилка збереження завдання: {error}")
            finally:
                connection.close()
    
    def get_application_setting(self, setting_key, default_value=None):
        """Отримання налаштування програми"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    SELECT setting_value FROM application_settings 
                    WHERE setting_key = %s
                """, (setting_key,))
                
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                
                if result:
                    return result[0]
                    
            except Exception as error:
                print(f"Помилка отримання налаштування: {error}")
                if connection:
                    connection.close()
        
        return default_value
    
    def update_application_setting(self, setting_key, setting_value):
        """Оновлення налаштування програми"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                cursor.execute("""
                    INSERT INTO application_settings (setting_key, setting_value, setting_type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (setting_key) 
                    DO UPDATE SET setting_value = EXCLUDED.setting_value,
                                  last_modified = CURRENT_TIMESTAMP
                """, (setting_key, str(setting_value), type(setting_value).__name__))
                
                connection.commit()
                cursor.close()
                
            except Exception as error:
                print(f"Помилка оновлення налаштування: {error}")
            finally:
                connection.close()
    
    def cleanup_old_records(self):
        """Очищення старих записів"""
        
        connection = self.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Видалення старих метрик (старше 30 днів)
                cutoff_date = datetime.now() - timedelta(days=30)
                
                cursor.execute("""
                    DELETE FROM hardware_metrics 
                    WHERE collection_time < %s
                """, (cutoff_date,))
                
                # Видалення старих результатів тестування (старше 60 днів)
                test_cutoff = datetime.now() - timedelta(days=60)
                
                cursor.execute("""
                    DELETE FROM performance_tests 
                    WHERE test_timestamp < %s
                """, (test_cutoff,))
                
                connection.commit()
                cursor.close()
                
            except Exception as error:
                print(f"Помилка очищення записів: {error}")
            finally:
                connection.close()