# -*- coding: utf-8 -*-
"""
TechCare - System Monitor Module
Модуль для моніторингу системних параметрів комп'ютера
"""

import psutil
import time
from datetime import datetime, timedelta

def get_system_data():
    """
    Отримує поточні системні дані
    Повертає словник з параметрами системи
    """
    try:
        # Отримання інформації про CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Спроба отримати температуру процесора
        cpu_temp = None
        try:
            # Перевіряємо наявність функції на Windows
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
            else:
                temps = None
            if temps:
                # Шукаємо температуру процесора в різних джерелах
                for name, entries in temps.items():
                    if 'cpu' in name.lower() or 'core' in name.lower():
                        if entries:
                            cpu_temp = entries[0].current
                            break
                # Якщо не знайшли, беремо перше доступне значення
                if cpu_temp is None and temps:
                    first_sensor = list(temps.values())[0]
                    if first_sensor:
                        cpu_temp = first_sensor[0].current
        except (AttributeError, KeyError):
            # Якщо температуру недоступна, використовуємо CPU usage як заміну
            cpu_temp = None
        
        # Час роботи системи
        boot_time = psutil.boot_time()
        current_time = time.time()
        uptime_seconds = current_time - boot_time
        
        # Форматування часу роботи
        uptime_delta = timedelta(seconds=uptime_seconds)
        days = uptime_delta.days
        hours, remainder = divmod(uptime_delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            uptime_str = f"{days}д {hours}г {minutes}хв"
        elif hours > 0:
            uptime_str = f"{hours}г {minutes}хв"
        else:
            uptime_str = f"{minutes}хв"
        
        # Використання RAM
        memory = psutil.virtual_memory()
        ram_percent = memory.percent
        
        # Використання диска
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        
        # Швидкість вентиляторів
        fan_speed = None
        try:
            fans = psutil.sensors_fans()
            if fans:
                for name, entries in fans.items():
                    if entries:
                        fan_speed = entries[0].current
                        break
        except (AttributeError, KeyError):
            fan_speed = None
        
        return {
            'cpu_temp': cpu_temp,
            'cpu_percent': cpu_percent,
            'uptime_seconds': uptime_seconds,
            'uptime_str': uptime_str,
            'ram_percent': ram_percent,
            'disk_percent': disk_percent,
            'fan_speed': fan_speed,
            'timestamp': datetime.now()
        }
        
    except Exception as e:
        print(f"Помилка при отриманні системних даних: {e}")
        return {
            'cpu_temp': None,
            'cpu_percent': 0,
            'uptime_seconds': 0,
            'uptime_str': "Н/Д",
            'ram_percent': 0,
            'disk_percent': 0,
            'fan_speed': None,
            'timestamp': datetime.now()
        }

def format_temperature(temp):
    """Форматує температуру для відображення"""
    if temp is None:
        return "Н/Д"
    return f"{int(temp)}°C"

def format_percentage(percent):
    """Форматує відсоток для відображення"""
    return f"{int(percent)}%"

def format_fan_speed(speed):
    """Форматує швидкість вентилятора для відображення"""
    if speed is None:
        return "Н/Д"
    return f"{int(speed)} RPM"

if __name__ == "__main__":
    # Тестування модуля
    data = get_system_data()
    print("Системні дані:")
    for key, value in data.items():
        print(f"{key}: {value}")
