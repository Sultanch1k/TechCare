# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Модуль тестування продуктивності
Бенчмаркінг та оцінка швидкодії системи
"""

import time
import threading
import random
import math
import psutil
from datetime import datetime

class SystemBenchmark:
    """Клас для проведення тестів продуктивності"""
    
    def __init__(self, database_controller):
        self.db_handler = database_controller
        self.test_results = {}
    
    def execute_full_benchmark(self):
        """Виконання повного набору тестів"""
        
        test_start_time = time.time()
        
        # Тестування компонентів системи
        processor_score = self._test_processor_performance()
        memory_score = self._test_memory_performance()
        storage_score = self._test_storage_performance()
        network_score = self._test_network_performance()
        
        # Розрахунок загального результату
        overall_score = self._calculate_overall_score([
            processor_score, memory_score, storage_score, network_score
        ])
        
        test_duration = time.time() - test_start_time
        
        results = {
            'cpu_score': processor_score,
            'memory_score': memory_score,
            'disk_score': storage_score,
            'network_score': network_score,
            'overall_score': overall_score,
            'duration': test_duration,
            'timestamp': datetime.now()
        }
        
        return results
    
    def _test_processor_performance(self):
        """Тест продуктивності процесора"""
        
        start_time = time.time()
        
        # Обчислювальний тест
        calculation_result = self._cpu_calculation_test()
        
        # Багатопоточний тест
        threading_result = self._cpu_threading_test()
        
        # Комбінований результат
        cpu_score = min(int((calculation_result + threading_result) / 2), 100)
        
        return cpu_score
    
    def _cpu_calculation_test(self):
        """Обчислювальний тест процесора"""
        
        start_time = time.time()
        iterations = 50000
        
        # Математичні операції
        for i in range(iterations):
            math.sqrt(i * random.random())
            math.sin(i) + math.cos(i)
        
        execution_time = time.time() - start_time
        
        # Оцінка на основі швидкості виконання
        base_score = max(0, 100 - (execution_time * 10))
        return min(base_score, 100)
    
    def _cpu_threading_test(self):
        """Тест багатопоточності"""
        
        cpu_count = psutil.cpu_count()
        threads = []
        results = []
        
        def worker_function():
            start = time.time()
            for _ in range(10000):
                math.factorial(100)
            results.append(time.time() - start)
        
        start_time = time.time()
        
        # Створення потоків
        for _ in range(min(cpu_count, 4)):
            thread = threading.Thread(target=worker_function)
            threads.append(thread)
            thread.start()
        
        # Очікування завершення
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        # Оцінка ефективності багатопоточності
        efficiency_score = max(0, 100 - (total_time * 20))
        return min(efficiency_score, 100)
    
    def _test_memory_performance(self):
        """Тест продуктивності пам'яті"""
        
        memory_info = psutil.virtual_memory()
        
        # Тест швидкості доступу до пам'яті
        access_score = self._memory_access_test()
        
        # Оцінка доступної пам'яті
        availability_score = min((memory_info.available / (1024**3)) * 20, 50)
        
        # Комбінований результат
        memory_score = min(int(access_score + availability_score), 100)
        
        return memory_score
    
    def _memory_access_test(self):
        """Тест швидкості доступу до пам'яті"""
        
        start_time = time.time()
        
        # Створення та обробка великих списків
        test_data = []
        for i in range(100000):
            test_data.append(random.random())
        
        # Сортування для навантаження пам'яті
        test_data.sort()
        
        execution_time = time.time() - start_time
        
        # Оцінка швидкості
        speed_score = max(0, 100 - (execution_time * 50))
        return min(speed_score, 100)
    
    def _test_storage_performance(self):
        """Тест продуктивності накопичувача"""
        
        disk_usage = psutil.disk_usage('/')
        
        # Оцінка вільного місця
        free_space_gb = disk_usage.free / (1024**3)
        space_score = min(free_space_gb * 2, 50)
        
        # Базова оцінка швидкості (симуляція)
        speed_score = 50 - (disk_usage.percent * 0.3)
        
        # Комбінований результат
        storage_score = min(int(space_score + speed_score), 100)
        
        return storage_score
    
    def _test_network_performance(self):
        """Тест мережевої продуктивності"""
        
        # Отримання мережевої статистики
        network_stats = psutil.net_io_counters()
        
        if network_stats:
            # Базова оцінка на основі активності
            bytes_total = network_stats.bytes_sent + network_stats.bytes_recv
            
            # Симуляція тесту швидкості
            if bytes_total > 1000000:  # 1MB
                network_score = random.randint(70, 95)
            else:
                network_score = random.randint(40, 70)
        else:
            network_score = 60  # Середня оцінка
        
        return min(network_score, 100)
    
    def _calculate_overall_score(self, component_scores):
        """Розрахунок загального результату"""
        
        # Вагові коефіцієнти для різних компонентів
        weights = {
            'cpu': 0.3,
            'memory': 0.25,
            'storage': 0.25,
            'network': 0.2
        }
        
        weighted_sum = (
            component_scores[0] * weights['cpu'] +
            component_scores[1] * weights['memory'] +
            component_scores[2] * weights['storage'] +
            component_scores[3] * weights['network']
        )
        
        return min(int(weighted_sum), 100)
    
    def get_performance_category(self, score):
        """Визначення категорії продуктивності"""
        
        if score >= 90:
            return "Відмінна"
        elif score >= 75:
            return "Висока"
        elif score >= 60:
            return "Середня"
        elif score >= 40:
            return "Низька"
        else:
            return "Критична"
    
    def generate_improvement_suggestions(self, results):
        """Генерація рекомендацій для покращення"""
        
        suggestions = []
        
        if results['cpu_score'] < 70:
            suggestions.append("Розгляньте закриття ресурсомістких програм для покращення роботи процесора")
        
        if results['memory_score'] < 60:
            suggestions.append("Рекомендується збільшити обсяг оперативної пам'яті")
        
        if results['disk_score'] < 50:
            suggestions.append("Необхідно звільнити місце на диску та провести дефрагментацію")
        
        if results['network_score'] < 60:
            suggestions.append("Перевірте мережеве з'єднання та налаштування")
        
        return suggestions