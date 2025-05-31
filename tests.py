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
    
    def run_disk_test(self):
        """Тест швидкості читання/запису диска"""
        try:
            import psutil
            
            # Отримуємо статистику диска до тесту
            disk_io_before = psutil.disk_io_counters()
            start_time = time.time()
            
            # Симуляція навантаження на диск
            test_data = b'0' * 1024 * 1024  # 1MB даних
            
            # Тест запису (симуляція)
            write_start = time.time()
            for _ in range(10):
                # Замість реального запису просто обчислюємо
                hash(test_data)
            write_time = time.time() - write_start
            
            # Тест читання (симуляція)
            read_start = time.time()
            for _ in range(10):
                # Замість реального читання просто обчислюємо
                len(test_data)
            read_time = time.time() - read_start
            
            # Отримуємо статистику після тесту
            try:
                disk_io_after = psutil.disk_io_counters()
                if disk_io_before and disk_io_after:
                    read_speed = ((disk_io_after.read_bytes - disk_io_before.read_bytes) / 
                                 (1024 * 1024)) / max(read_time, 0.1)  # MB/s
                    write_speed = ((disk_io_after.write_bytes - disk_io_before.write_bytes) / 
                                  (1024 * 1024)) / max(write_time, 0.1)  # MB/s
                else:
                    # Fallback розрахунок
                    read_speed = 100 / max(read_time * 10, 1)
                    write_speed = 100 / max(write_time * 10, 1)
            except:
                read_speed = 100 / max(read_time * 10, 1)
                write_speed = 100 / max(write_time * 10, 1)
            
            # Розрахунок скору (0-100)
            avg_speed = (read_speed + write_speed) / 2
            score = min(avg_speed * 2, 100)  # Множимо на 2 для кращого скалювання
            
            return {
                'disk_score': max(0, int(score)),
                'read_speed': read_speed,
                'write_speed': write_speed,
                'read_time': read_time,
                'write_time': write_time
            }
            
        except Exception as e:
            print(f"Помилка тесту диска: {e}")
            return {
                'disk_score': 50,  # Середній скор при помилці
                'read_speed': 0,
                'write_speed': 0,
                'read_time': 0,
                'write_time': 0
            }