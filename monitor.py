# -*- coding: utf-8 -*-
"""
Простий модуль для отримання даних про систему
Без складних функцій, тільки основне
"""

import psutil
import platform
import time

def get_system_data():
    """Отримуємо основні дані про систему"""
    data = {}
    
    try:
        # CPU
        data['cpu_percent'] = psutil.cpu_percent(interval=1)
        
        # RAM
        memory = psutil.virtual_memory()
        data['ram_percent'] = memory.percent
        data['ram_total'] = memory.total
        data['ram_used'] = memory.used
        
        # Диск
        disk = psutil.disk_usage('/')
        data['disk_percent'] = (disk.used / disk.total) * 100
        data['disk_total'] = disk.total
        data['disk_used'] = disk.used
        data['disk_free'] = disk.free
        
        # Температура (через датчики або заміна CPU > 80%)
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        data['temperature'] = entries[0].current
                        break
            else:
                # Заміна: якщо CPU > 80% то температура "висока"
                data['temperature'] = 85 if data['cpu_percent'] > 80 else 45
        except:
            data['temperature'] = 85 if data['cpu_percent'] > 80 else 45
        
        # Швидкість вентилятора
        try:
            fans = psutil.sensors_fans()
            if fans:
                for name, entries in fans.items():
                    if entries:
                        data['fan_speed'] = entries[0].current
                        break
            else:
                data['fan_speed'] = None
        except:
            data['fan_speed'] = None
        
        # Час роботи системи
        boot_time = psutil.boot_time()
        data['uptime_hours'] = (time.time() - boot_time) / 3600
        
        # Температура (якщо є)
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # беремо першу доступну температуру
                for name, entries in temps.items():
                    if entries:
                        data['temperature'] = entries[0].current
                        break
            else:
                data['temperature'] = None
        except:
            data['temperature'] = None
        
        # Кількість процесів
        data['process_count'] = len(psutil.pids())
        
        # Інформація про систему
        data['system_info'] = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor()
        }
        
        return data
        
    except Exception as e:
        print(f"Помилка отримання даних: {e}")
        # повертаємо базові дані щоб програма не крашилась
        return {
            'cpu_percent': 0,
            'ram_percent': 0,
            'disk_percent': 0,
            'temperature': None,
            'process_count': 0,
            'ram_total': 0,
            'ram_used': 0,
            'disk_total': 0,
            'disk_used': 0,
            'disk_free': 0,
            'system_info': {}
        }

def format_bytes(bytes_value):
    """Форматує байти в зручний вигляд"""
    if bytes_value == 0:
        return "0 B"
    
    sizes = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while bytes_value >= 1024 and i < len(sizes) - 1:
        bytes_value /= 1024.0
        i += 1
    
    return f"{bytes_value:.1f} {sizes[i]}"