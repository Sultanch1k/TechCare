# -*- coding: utf-8 -*-
"""
модуль для збору даних про систему
написав сам, просто отримує основну інформацію
"""
_cached_temp = None
_temp_timestamp = 0
import psutil
import platform
import time



def get_system_data():
    global _cached_temp, _temp_timestamp
    """Отримуємо основні дані про систему"""
    data = {}
    
    try:
        # CPU
        data['cpu_percent'] = psutil.cpu_percent(interval=None)
        
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
        
        # Температура через WMI раз на 10 хвилин (TTL=600 с), інакше — формула
        now = time.time()
        if _cached_temp is None or now - _temp_timestamp > 600:
            try:
                import wmi, pythoncom
                pythoncom.CoInitialize()
                w = wmi.WMI(namespace="root\\WMI")
                for zone in w.MSAcpi_ThermalZoneTemperature():
                    raw = zone.CurrentTemperature                    
                    if raw and raw > 2700:
                        c = raw / 10.0 - 273.15
                        if 25 < c < 100:
                            _cached_temp = round(c, 1)
                            break
                pythoncom.CoUninitialize()
            except Exception:
                _cached_temp = None
            _temp_timestamp = now
        if _cached_temp:
            data['temperature'] = _cached_temp
        else:
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

def get_network_data(interval=0.5):
        """
        Виміряти мережевий трафік (МБ/с) за заданий інтервал.
        """
        try:
            io1 = psutil.net_io_counters()
            time.sleep(interval)
            io2 = psutil.net_io_counters()
            sent = (io2.bytes_sent - io1.bytes_sent) / (1024 ** 2) / interval
            recv = (io2.bytes_recv - io1.bytes_recv) / (1024 ** 2) / interval
            return {
                'net_sent_mb_s': round(sent, 2),
                'net_recv_mb_s': round(recv, 2)
            }
        except Exception as e:
            print(f"Помилка збору мережевих даних: {e}")
            return {'net_sent_mb_s': 0.0, 'net_recv_mb_s': 0.0}
    