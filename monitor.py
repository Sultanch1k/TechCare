# -*- coding: utf-8 -*-
"""
TechCare AI - Enhanced System Monitor Module
Розширений модуль для моніторингу системних параметрів комп'ютера
"""

import psutil
import time
import platform
import subprocess
from datetime import datetime, timedelta

def get_system_data():
    """
    Отримує поточні системні дані з розширеним аналізом
    Повертає словник з параметрами системи
    """
    try:
        # Отримання інформації про CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        # Спроба отримати температуру процесора
        cpu_temp = None
        try:
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
        
        # Використання RAM з додатковою інформацією
        memory = psutil.virtual_memory()
        ram_percent = memory.percent
        ram_total_gb = memory.total / (1024**3)
        ram_used_gb = memory.used / (1024**3)
        ram_available_gb = memory.available / (1024**3)
        
        # Використання диска з детальною інформацією
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        disk_total_gb = disk.total / (1024**3)
        disk_used_gb = disk.used / (1024**3)
        disk_free_gb = disk.free / (1024**3)
        
        # Швидкість вентиляторів
        fan_speed = None
        fan_count = 0
        fan_speeds = []
        try:
            fans = psutil.sensors_fans()
            if fans:
                for name, entries in fans.items():
                    for fan in entries:
                        fan_speeds.append(fan.current)
                        fan_count += 1
                if fan_speeds:
                    fan_speed = sum(fan_speeds) / len(fan_speeds)  # Середня швидкість
        except (AttributeError, KeyError):
            fan_speed = None
        
        # Інформація про мережу
        network_stats = psutil.net_io_counters()
        network_sent = network_stats.bytes_sent / (1024**2)  # MB
        network_recv = network_stats.bytes_recv / (1024**2)  # MB
        
        # Кількість процесів
        process_count = len(psutil.pids())
        
        # Інформація про батарею (якщо доступна)
        battery_info = None
        try:
            battery = psutil.sensors_battery()
            if battery:
                battery_info = {
                    'percent': battery.percent,
                    'plugged': battery.power_plugged,
                    'time_left': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                }
        except (AttributeError, KeyError):
            battery_info = None
        
        # Системна інформація
        system_info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'architecture': platform.architecture()[0],
            'processor': platform.processor(),
            'hostname': platform.node()
        }
        
        return {
            'cpu_temp': cpu_temp,
            'cpu_percent': cpu_percent,
            'cpu_count': cpu_count,
            'cpu_freq': cpu_freq.current if cpu_freq else None,
            'uptime_seconds': uptime_seconds,
            'uptime_str': uptime_str,
            'ram_percent': ram_percent,
            'ram_total_gb': ram_total_gb,
            'ram_used_gb': ram_used_gb,
            'ram_available_gb': ram_available_gb,
            'disk_percent': disk_percent,
            'disk_total_gb': disk_total_gb,
            'disk_used_gb': disk_used_gb,
            'disk_free_gb': disk_free_gb,
            'fan_speed': fan_speed,
            'fan_count': fan_count,
            'fan_speeds': fan_speeds,
            'network_sent_mb': network_sent,
            'network_recv_mb': network_recv,
            'process_count': process_count,
            'battery_info': battery_info,
            'system_info': system_info,
            'timestamp': datetime.now()
        }
        
    except Exception as e:
        print(f"Помилка при отриманні системних даних: {e}")
        return {
            'cpu_temp': None,
            'cpu_percent': 0,
            'cpu_count': 0,
            'cpu_freq': None,
            'uptime_seconds': 0,
            'uptime_str': "Н/Д",
            'ram_percent': 0,
            'ram_total_gb': 0,
            'ram_used_gb': 0,
            'ram_available_gb': 0,
            'disk_percent': 0,
            'disk_total_gb': 0,
            'disk_used_gb': 0,
            'disk_free_gb': 0,
            'fan_speed': None,
            'fan_count': 0,
            'fan_speeds': [],
            'network_sent_mb': 0,
            'network_recv_mb': 0,
            'process_count': 0,
            'battery_info': None,
            'system_info': {},
            'timestamp': datetime.now()
        }

def get_detailed_cpu_info():
    """Отримання детальної інформації про процесор"""
    try:
        # Базова інформація
        cpu_percent_per_core = psutil.cpu_percent(percpu=True)
        cpu_times = psutil.cpu_times()
        
        info = {
            'usage_per_core': cpu_percent_per_core,
            'average_usage': sum(cpu_percent_per_core) / len(cpu_percent_per_core),
            'times': {
                'user': cpu_times.user,
                'system': cpu_times.system,
                'idle': cpu_times.idle
            }
        }
        
        # Частоти ядер (якщо доступно)
        try:
            cpu_freq_per_core = psutil.cpu_freq(percpu=True)
            if cpu_freq_per_core:
                info['frequencies'] = [freq.current for freq in cpu_freq_per_core]
        except:
            pass
        
        return info
        
    except Exception as e:
        print(f"Помилка отримання інформації про CPU: {e}")
        return {}

def get_detailed_memory_info():
    """Отримання детальної інформації про пам'ять"""
    try:
        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()
        
        return {
            'virtual': {
                'total': virtual_mem.total,
                'available': virtual_mem.available,
                'used': virtual_mem.used,
                'percent': virtual_mem.percent,
                'free': virtual_mem.free,
                'buffers': getattr(virtual_mem, 'buffers', 0),
                'cached': getattr(virtual_mem, 'cached', 0)
            },
            'swap': {
                'total': swap_mem.total,
                'used': swap_mem.used,
                'free': swap_mem.free,
                'percent': swap_mem.percent
            }
        }
        
    except Exception as e:
        print(f"Помилка отримання інформації про пам'ять: {e}")
        return {}

def get_detailed_disk_info():
    """Отримання детальної інформації про диски"""
    try:
        disk_partitions = psutil.disk_partitions()
        disk_info = []
        
        for partition in disk_partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                
                disk_info.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total': partition_usage.total,
                    'used': partition_usage.used,
                    'free': partition_usage.free,
                    'percent': (partition_usage.used / partition_usage.total) * 100
                })
            except PermissionError:
                continue
        
        # I/O статистика
        try:
            disk_io = psutil.disk_io_counters()
            io_stats = {
                'read_count': disk_io.read_count,
                'write_count': disk_io.write_count,
                'read_bytes': disk_io.read_bytes,
                'write_bytes': disk_io.write_bytes,
                'read_time': disk_io.read_time,
                'write_time': disk_io.write_time
            }
        except:
            io_stats = {}
        
        return {
            'partitions': disk_info,
            'io_stats': io_stats
        }
        
    except Exception as e:
        print(f"Помилка отримання інформації про диски: {e}")
        return {'partitions': [], 'io_stats': {}}

def get_network_info():
    """Отримання детальної мережевої інформації"""
    try:
        # Загальна статистика
        net_io = psutil.net_io_counters()
        
        # Статистика по інтерфейсах
        net_io_per_nic = psutil.net_io_counters(pernic=True)
        
        # Активні з'єднання
        connections = psutil.net_connections()
        
        return {
            'total_stats': {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout
            },
            'interfaces': {name: {
                'bytes_sent': stats.bytes_sent,
                'bytes_recv': stats.bytes_recv,
                'packets_sent': stats.packets_sent,
                'packets_recv': stats.packets_recv
            } for name, stats in net_io_per_nic.items()},
            'connections_count': len(connections),
            'active_connections': len([c for c in connections if c.status == 'ESTABLISHED'])
        }
        
    except Exception as e:
        print(f"Помилка отримання мережевої інформації: {e}")
        return {}

def get_process_info(limit=10):
    """Отримання інформації про топ процеси за використанням ресурсів"""
    try:
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                pinfo = proc.info
                if pinfo['cpu_percent'] is None:
                    pinfo['cpu_percent'] = 0.0
                if pinfo['memory_percent'] is None:
                    pinfo['memory_percent'] = 0.0
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Сортування за використанням CPU
        processes_by_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:limit]
        
        # Сортування за використанням пам'яті
        processes_by_memory = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:limit]
        
        return {
            'top_cpu': processes_by_cpu,
            'top_memory': processes_by_memory,
            'total_processes': len(processes)
        }
        
    except Exception as e:
        print(f"Помилка отримання інформації про процеси: {e}")
        return {'top_cpu': [], 'top_memory': [], 'total_processes': 0}

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

def format_bytes(bytes_value):
    """Форматує байти у зручний для читання формат"""
    if bytes_value < 1024:
        return f"{bytes_value} B"
    elif bytes_value < 1024**2:
        return f"{bytes_value/1024:.1f} KB"
    elif bytes_value < 1024**3:
        return f"{bytes_value/(1024**2):.1f} MB"
    else:
        return f"{bytes_value/(1024**3):.1f} GB"

if __name__ == "__main__":
    # Тестування модуля
    data = get_system_data()
    print("Системні дані:")
    for key, value in data.items():
        print(f"{key}: {value}")
    
    print("\nДетальна інформація про CPU:")
    cpu_info = get_detailed_cpu_info()
    for key, value in cpu_info.items():
        print(f"{key}: {value}")
    
    print("\nТоп процеси:")
    proc_info = get_process_info(5)
    print("За CPU:")
    for proc in proc_info['top_cpu']:
        print(f"  {proc['name']}: {proc['cpu_percent']:.1f}%")
