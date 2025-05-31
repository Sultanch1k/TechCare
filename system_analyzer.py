# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Модуль аналізу апаратного забезпечення
Збір та обробка метрик комп'ютерної системи
"""

import psutil
import platform
import socket
import time
from datetime import datetime

def collect_hardware_metrics():
    """Збір поточних метрик апаратного забезпечення"""
    
    metrics_data = {}
    
    try:
        # Інформація про процесор
        cpu_metrics = analyze_processor_state()
        metrics_data.update(cpu_metrics)
        
        # Аналіз пам'яті
        memory_metrics = examine_memory_usage()
        metrics_data.update(memory_metrics)
        
        # Стан накопичувачів
        storage_metrics = evaluate_storage_status()
        metrics_data.update(storage_metrics)
        
        # Мережева активність
        network_metrics = monitor_network_activity()
        metrics_data.update(network_metrics)
        
        # Загальна інформація про систему
        system_info = gather_system_information()
        metrics_data.update(system_info)
        
        # Часова мітка
        metrics_data['collection_timestamp'] = datetime.now()
        
    except Exception as error:
        print(f"Помилка збору метрик: {error}")
        metrics_data = get_fallback_metrics()
    
    return metrics_data

def analyze_processor_state():
    """Аналіз стану процесора"""
    cpu_data = {}
    
    try:
        # Завантаженість процесора
        cpu_data['cpu_usage'] = psutil.cpu_percent(interval=1)
        
        # Частота процесора
        cpu_frequencies = psutil.cpu_freq()
        if cpu_frequencies:
            cpu_data['cpu_frequency_current'] = cpu_frequencies.current
            cpu_data['cpu_frequency_max'] = cpu_frequencies.max
        
        # Кількість ядер
        cpu_data['cpu_cores_logical'] = psutil.cpu_count(logical=True)
        cpu_data['cpu_cores_physical'] = psutil.cpu_count(logical=False)
        
        # Завантаженість по ядрах
        cpu_data['cpu_per_core'] = psutil.cpu_percent(percpu=True, interval=1)
        
        # Температура (якщо доступна)
        try:
            thermal_sensors = psutil.sensors_temperatures()
            if thermal_sensors:
                for sensor_name, sensor_list in thermal_sensors.items():
                    if sensor_list:
                        cpu_data['thermal_reading'] = sensor_list[0].current
                        break
        except:
            cpu_data['thermal_reading'] = None
            
    except Exception as error:
        print(f"Помилка аналізу процесора: {error}")
        cpu_data = {'cpu_usage': 0, 'cpu_frequency_current': 0}
    
    return cpu_data

def examine_memory_usage():
    """Дослідження використання пам'яті"""
    memory_data = {}
    
    try:
        # Віртуальна пам'ять
        virtual_memory = psutil.virtual_memory()
        memory_data['memory_total'] = virtual_memory.total
        memory_data['memory_available'] = virtual_memory.available
        memory_data['memory_used'] = virtual_memory.used
        memory_data['memory_usage'] = virtual_memory.percent
        memory_data['memory_free'] = virtual_memory.free
        
        # Файл підкачки
        swap_memory = psutil.swap_memory()
        memory_data['swap_total'] = swap_memory.total
        memory_data['swap_used'] = swap_memory.used
        memory_data['swap_usage'] = swap_memory.percent
        
    except Exception as error:
        print(f"Помилка аналізу пам'яті: {error}")
        memory_data = {'memory_usage': 0, 'swap_usage': 0}
    
    return memory_data

def evaluate_storage_status():
    """Оцінка стану накопичувачів"""
    storage_data = {}
    
    try:
        # Основний диск
        disk_usage = psutil.disk_usage('/')
        storage_data['storage_total'] = disk_usage.total
        storage_data['storage_used'] = disk_usage.used
        storage_data['storage_free'] = disk_usage.free
        storage_data['storage_usage'] = (disk_usage.used / disk_usage.total) * 100
        
        # Статистика вводу/виводу
        disk_io = psutil.disk_io_counters()
        if disk_io:
            storage_data['disk_read_bytes'] = disk_io.read_bytes
            storage_data['disk_write_bytes'] = disk_io.write_bytes
            storage_data['disk_read_count'] = disk_io.read_count
            storage_data['disk_write_count'] = disk_io.write_count
        
        # Список всіх дисків
        storage_data['disk_partitions'] = []
        for partition in psutil.disk_partitions():
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                storage_data['disk_partitions'].append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total': partition_usage.total,
                    'used': partition_usage.used,
                    'free': partition_usage.free,
                    'percentage': (partition_usage.used / partition_usage.total) * 100
                })
            except PermissionError:
                continue
                
    except Exception as error:
        print(f"Помилка аналізу накопичувачів: {error}")
        storage_data = {'storage_usage': 0}
    
    return storage_data

def monitor_network_activity():
    """Моніторинг мережевої активності"""
    network_data = {}
    
    try:
        # Статистика мережі
        network_io = psutil.net_io_counters()
        if network_io:
            network_data['network_bytes_sent'] = network_io.bytes_sent
            network_data['network_bytes_recv'] = network_io.bytes_recv
            network_data['network_packets_sent'] = network_io.packets_sent
            network_data['network_packets_recv'] = network_io.packets_recv
            network_data['network_errors_in'] = network_io.errin
            network_data['network_errors_out'] = network_io.errout
        
        # Активні з'єднання
        network_connections = psutil.net_connections()
        network_data['active_connections'] = len(network_connections)
        
        # Мережеві інтерфейси
        network_interfaces = psutil.net_if_addrs()
        network_data['network_interfaces'] = list(network_interfaces.keys())
        
    except Exception as error:
        print(f"Помилка моніторингу мережі: {error}")
        network_data = {'network_bytes_sent': 0, 'network_bytes_recv': 0}
    
    return network_data

def gather_system_information():
    """Збір загальної інформації про систему"""
    system_data = {}
    
    try:
        # Інформація про операційну систему
        system_data['os_name'] = platform.system()
        system_data['os_release'] = platform.release()
        system_data['os_version'] = platform.version()
        system_data['machine_type'] = platform.machine()
        system_data['processor_name'] = platform.processor()
        
        # Час роботи системи
        boot_time = psutil.boot_time()
        system_data['boot_timestamp'] = datetime.fromtimestamp(boot_time)
        system_data['uptime_seconds'] = time.time() - boot_time
        
        # Інформація про користувачів
        users = psutil.users()
        system_data['logged_users'] = len(users)
        
        # Процеси
        system_data['running_processes'] = len(psutil.pids())
        
        # Мережеве ім'я
        try:
            system_data['hostname'] = socket.gethostname()
        except:
            system_data['hostname'] = "Unknown"
            
    except Exception as error:
        print(f"Помилка збору системної інформації: {error}")
        system_data = {'os_name': 'Unknown', 'running_processes': 0}
    
    return system_data

def get_fallback_metrics():
    """Резервні метрики при помилках"""
    return {
        'cpu_usage': 0,
        'memory_usage': 0,
        'storage_usage': 0,
        'network_bytes_sent': 0,
        'network_bytes_recv': 0,
        'running_processes': 0,
        'collection_timestamp': datetime.now()
    }

def calculate_system_load_average():
    """Розрахунок середнього навантаження системи"""
    try:
        # На Unix системах
        if hasattr(psutil, 'getloadavg'):
            return psutil.getloadavg()
        else:
            # Альтернативний розрахунок для Windows
            cpu_usage = psutil.cpu_percent(interval=1)
            return [cpu_usage / 100, cpu_usage / 100, cpu_usage / 100]
    except:
        return [0, 0, 0]

def get_process_list():
    """Отримання списку запущених процесів"""
    processes = []
    
    try:
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                process_info = process.info
                if process_info['cpu_percent'] is None:
                    process_info['cpu_percent'] = 0
                if process_info['memory_percent'] is None:
                    process_info['memory_percent'] = 0
                processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as error:
        print(f"Помилка отримання процесів: {error}")
    
    return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:10]

def format_bytes_to_human(bytes_value):
    """Форматування байтів у зручний для читання вигляд"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"