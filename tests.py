# -*- coding: utf-8 -*-
"""
Прості тести швидкості системи
Без складних алгоритмів
"""

import time
import random

class SimpleTests:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def run_benchmark(self):
        """Запускає тест швидкості"""
        # CPU тест
        cpu_score = self.test_cpu()
        
        # RAM тест  
        ram_score = self.test_ram()
        
        # загальний скор
        overall_score = (cpu_score + ram_score) / 2
        
        results = {
            'cpu_score': cpu_score,
            'ram_score': ram_score,
            'overall_score': overall_score
        }
        
        return results
    
    def test_cpu(self):
        """Тест процесора"""
        start_time = time.time()
        
        # робимо складні обчислення
        result = 0
        for i in range(100000):
            result += i ** 0.5
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # рахуємо скор (чим швидше, тим краще)
        score = max(0, 100 - (execution_time * 50))
        return min(score, 100)
    
    def test_ram(self):
        """Тест пам'яті"""
        start_time = time.time()
        
        # створюємо великий список
        big_list = [random.randint(1, 1000) for _ in range(50000)]
        big_list.sort()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        score = max(0, 100 - (execution_time * 30))
        return min(score, 100)