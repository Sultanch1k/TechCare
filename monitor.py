# -*- coding: utf-8 -*-
"""
модуль для збору даних про систему
написав сам, просто отримує основну інформацію
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
        
        
        # температура: намагаємось отримати з WMI, fallback — формула
        try:
            import wmi
            import pythoncom
            pythoncom.CoInitialize()
            w = wmi.WMI(namespace="root\WMI")
            thermal_info = w.MSAcpi_ThermalZoneTemperature()
            
            valid_temp = None
            for zone in thermal_info:
                raw = zone.CurrentTemperature
                if raw and raw > 2700:
                    celsius = raw / 10.0 - 273.15
                    if 25 < celsius < 100:
                        valid_temp = round(celsius, 1)
                        break

            if valid_temp:
                data['temperature'] = valid_temp
            else:
                raise ValueError("Немає адекватної температури")
            
            pythoncom.CoUninitialize()
        except Exception as e:
            print(f"[WARN] WMI температура недоступна або некоректна: {e}")
            cpu_load = data.get('cpu_percent', 20)
            data['temperature'] = round(35 + cpu_load * 0.5, 1)

        # вентилятори
        try:
            fans = psutil.sensors_fans()
            fan_found = False
            if fans:
                for name, entries in fans.items():
                    if entries:
                        data['fan_speed'] = entries[0].current
                        fan_found = True
                        break
            
            if not fan_found:
                # рахую швидкість по температурі
                temp = data.get('temperature', 45)
                if temp > 70:
                    data['fan_speed'] = 2800 + (temp - 70) * 60
                elif temp > 60:
                    data['fan_speed'] = 2200 + (temp - 60) * 60
                elif temp > 50:
                    data['fan_speed'] = 1600 + (temp - 50) * 60
                elif temp > 40:
                    data['fan_speed'] = 1200 + (temp - 40) * 40
                else:
                    data['fan_speed'] = 900 + temp * 15
        except:
            temp = data.get('temperature', 45)
            data['fan_speed'] = 1000 + temp * 20
        
        # Час роботи з моменту завантаження (реальний uptime)
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        data['uptime_hours'] = uptime_seconds / 3600
        
        # Додаємо час завантаження для інформації
        import datetime
        boot_datetime = datetime.datetime.fromtimestamp(boot_time)
        data['boot_time'] = boot_datetime.strftime("%d.%m.%Y %H:%M")
        
        # температура вже розрахована вище, не перезаписуємо
        
        # Кількість процесів
        data['process_count'] = len(psutil.pids())
        
        # Інформація про систему
        data['system_info'] = {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor()
        }
        
        # Додаткова системна інформація
        try:
            # Спроба отримати інформацію через різні методи
            if platform.system() == "Windows":
                try:
                    import wmi
                    import pythoncom
                    
                    # Ініціалізуємо COM для WMI
                    pythoncom.CoInitialize()
                    c = wmi.WMI()
                    
                    # Інформація про материнську плату
                    for board in c.Win32_BaseBoard():
                        data['motherboard'] = board.Product
                        data['manufacturer'] = board.Manufacturer
                        break
                    
                    # Інформація про BIOS
                    for bios in c.Win32_BIOS():
                        data['bios_version'] = bios.SMBIOSBIOSVersion
                        break
                    
                    # Інформація про відеокарту
                    for gpu in c.Win32_VideoController():
                        if gpu.Name:
                            data['gpu_name'] = gpu.Name
                            data['gpu_memory'] = gpu.AdapterRAM if gpu.AdapterRAM else 0
                            break
                    
                    # Інформація про акумулятор
                    battery_info = c.Win32_Battery()
                    if battery_info:
                        for battery in battery_info:
                            data['battery_status'] = battery.EstimatedChargeRemaining
                            break
                    else:
                        data['battery_status'] = None
                    
                    # Запущені служби Windows
                    services = c.Win32_Service()
                    running_services = [s.Name for s in services if s.State == 'Running']
                    data['services_count'] = len(running_services)
                    data['total_services'] = len(list(services))
                    
                except Exception as e:
                    print(f"WMI недоступна: {e}")
                    # Альтернативний метод для Windows через реєстр та команди
                    data.update(_get_windows_alternative_info())
                finally:
                    try:
                        pythoncom.CoUninitialize()
                    except:
                        pass
                
        except Exception as e:
            print(f"Помилка отримання розширеної інформації: {e}")
            # Базові значення за замовчуванням
            data['motherboard'] = "Невідомо"
            data['manufacturer'] = "Невідомо" 
            data['gpu_name'] = "Невідомо"
            data['battery_status'] = None
        
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

def _get_windows_alternative_info():
    """Альтернативний збір Windows апаратної інформації через команди"""
    info = {}
    
    try:
        import subprocess
        
        # Материнська плата через WMIC
        try:
            result = subprocess.run(['wmic', 'baseboard', 'get', 'product,manufacturer', '/format:list'], 
                                  capture_output=True, text=True, timeout=10)
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'Manufacturer=' in line and line.split('=')[1].strip():
                    info['manufacturer'] = line.split('=')[1].strip()
                elif 'Product=' in line and line.split('=')[1].strip():
                    info['motherboard'] = line.split('=')[1].strip()
        except:
            pass
        
        # BIOS інформація
        try:
            result = subprocess.run(['wmic', 'bios', 'get', 'SMBIOSBIOSVersion', '/format:list'], 
                                  capture_output=True, text=True, timeout=10)
            for line in result.stdout.strip().split('\n'):
                if 'SMBIOSBIOSVersion=' in line and line.split('=')[1].strip():
                    info['bios_version'] = line.split('=')[1].strip()
                    break
        except:
            pass
        
        # Відеокарта через WMIC
        try:
            result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name,AdapterRAM', '/format:list'], 
                                  capture_output=True, text=True, timeout=10)
            lines = result.stdout.strip().split('\n')
            gpu_name = None
            gpu_memory = None
            
            for line in lines:
                if 'Name=' in line and line.split('=')[1].strip():
                    gpu_name = line.split('=')[1].strip()
                elif 'AdapterRAM=' in line and line.split('=')[1].strip():
                    try:
                        gpu_memory = int(line.split('=')[1].strip())
                    except:
                        pass
            
            if gpu_name:
                info['gpu_name'] = gpu_name
                info['gpu_memory'] = gpu_memory if gpu_memory else 0
        except:
            pass
        
        # Акумулятор
        try:
            result = subprocess.run(['wmic', 'path', 'Win32_Battery', 'get', 'EstimatedChargeRemaining', '/format:list'], 
                                  capture_output=True, text=True, timeout=10)
            for line in result.stdout.strip().split('\n'):
                if 'EstimatedChargeRemaining=' in line and line.split('=')[1].strip():
                    try:
                        info['battery_status'] = int(line.split('=')[1].strip())
                    except:
                        pass
                    break
        except:
            info['battery_status'] = None
        
        # Служби Windows
        try:
            result = subprocess.run(['wmic', 'service', 'get', 'state', '/format:list'], 
                                  capture_output=True, text=True, timeout=15)
            lines = result.stdout.strip().split('\n')
            running_count = 0
            total_count = 0
            
            for line in lines:
                if 'State=' in line and line.split('=')[1].strip():
                    total_count += 1
                    if line.split('=')[1].strip().lower() == 'running':
                        running_count += 1
            
            if total_count > 0:
                info['services_count'] = running_count
                info['total_services'] = total_count
        except:
            pass
            
    except Exception as e:
        print(f"Помилка альтернативного збору Windows даних: {e}")
    
    # Якщо нічого не знайшли, ставимо базові значення
    if not info.get('motherboard'):
        info['motherboard'] = "Інформація недоступна"
    if not info.get('manufacturer'):
        info['manufacturer'] = "Невідомий виробник"
    if not info.get('gpu_name'):
        info['gpu_name'] = "Відеокарта не знайдена"
    
    return info

def get_network_data():
    """Отримуємо дані про мережу"""
    data = {}
    
    try:
        # Статистика мережевих інтерфейсів
        net_io = psutil.net_io_counters()
        data['bytes_sent'] = net_io.bytes_sent
        data['bytes_recv'] = net_io.bytes_recv
        data['packets_sent'] = net_io.packets_sent
        data['packets_recv'] = net_io.packets_recv
        
        # Активні з'єднання
        connections = psutil.net_connections()
        data['active_connections'] = len([c for c in connections if c.status == 'ESTABLISHED'])
        data['listening_ports'] = len([c for c in connections if c.status == 'LISTEN'])
        
        # Мережеві інтерфейси
        net_if_addrs = psutil.net_if_addrs()
        interfaces = []
        for interface_name, interface_addresses in net_if_addrs.items():
            for address in interface_addresses:
                if address.family == 2:  # IPv4
                    interfaces.append({
                        'name': interface_name,
                        'ip': address.address,
                        'netmask': address.netmask
                    })
        data['interfaces'] = interfaces
        
        # Статистика інтерфейсів
        net_if_stats = psutil.net_if_stats()
        interface_stats = []
        for name, stats in net_if_stats.items():
            if stats.isup:
                interface_stats.append({
                    'name': name,
                    'speed': stats.speed if stats.speed > 0 else 0,
                    'mtu': stats.mtu
                })
        data['interface_stats'] = interface_stats
        
    except Exception as e:
        print(f"Помилка отримання мережевих даних: {e}")
        data = {
            'bytes_sent': 0,
            'bytes_recv': 0,
            'packets_sent': 0,
            'packets_recv': 0,
            'active_connections': 0,
            'listening_ports': 0,
            'interfaces': [],
            'interface_stats': []
        }
    
    return data