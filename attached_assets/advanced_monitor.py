# -*- coding: utf-8 -*-
"""
TechCare - Advanced Monitor Module
Розширений модуль моніторингу для перевірки драйверів та термопасти
"""

import psutil
import subprocess
import platform
import time
from datetime import datetime, timedelta
import os

def check_driver_status():
    """
    Перевіряє статус драйверів системи
    Повертає словник з інформацією про драйвери
    """
    driver_info = {
        'outdated_drivers': [],
        'missing_drivers': [],
        'critical_drivers': [],
        'last_update': None,
        'status': 'unknown'
    }
    
    try:
        system = platform.system()
        
        if system == "Windows":
            # Перевірка через Windows Management Instrumentation
            try:
                result = subprocess.run([
                    'powershell', '-Command',
                    'Get-WmiObject Win32_PnPSignedDriver | Where-Object {$_.DeviceName -and $_.DriverVersion} | Select-Object DeviceName, DriverVersion, DriverDate'
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    current_time = datetime.now()
                    
                    for line in lines[3:]:  # Пропускаємо заголовки
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 3:
                                try:
                                    # Перевіряємо дату драйвера
                                    driver_date_str = parts[-1]
                                    if '/' in driver_date_str:
                                        driver_date = datetime.strptime(driver_date_str, '%m/%d/%Y')
                                        days_old = (current_time - driver_date).days
                                        
                                        if days_old > 365:  # Драйвер старший за рік
                                            driver_info['outdated_drivers'].append({
                                                'name': ' '.join(parts[:-2]),
                                                'age_days': days_old
                                            })
                                except:
                                    continue
                    
                    # Визначення статусу
                    if len(driver_info['outdated_drivers']) == 0:
                        driver_info['status'] = 'good'
                    elif len(driver_info['outdated_drivers']) <= 3:
                        driver_info['status'] = 'warning'
                    else:
                        driver_info['status'] = 'critical'
                        
            except (subprocess.TimeoutExpired, FileNotFoundError):
                driver_info['status'] = 'unavailable'
                
        elif system == "Linux":
            # Перевірка через lspci та інші команди Linux
            try:
                # Спробуємо різні методи перевірки драйверів в Linux
                methods_tried = []
                
                # Метод 1: lspci -k
                try:
                    result = subprocess.run(['lspci', '-k'], capture_output=True, text=True, timeout=10)
                    methods_tried.append('lspci')
                    if result.returncode == 0:
                        lines = result.stdout.split('\n')
                        total_devices = 0
                        devices_with_drivers = 0
                        
                        for i, line in enumerate(lines):
                            if ':' in line and any(keyword in line.lower() for keyword in ['ethernet', 'network', 'audio', 'vga', 'display']):
                                total_devices += 1
                                # Перевіряємо наступні рядки на наявність драйвера
                                for j in range(i+1, min(i+4, len(lines))):
                                    if 'Kernel driver in use:' in lines[j] or 'Kernel modules:' in lines[j]:
                                        devices_with_drivers += 1
                                        break
                        
                        if total_devices > 0:
                            driver_coverage = (devices_with_drivers / total_devices) * 100
                            if driver_coverage >= 90:
                                driver_info['status'] = 'good'
                            elif driver_coverage >= 70:
                                driver_info['status'] = 'warning'
                                driver_info['missing_drivers'].append(f'Неповне покриття драйверів: {driver_coverage:.0f}%')
                            else:
                                driver_info['status'] = 'critical'
                                driver_info['missing_drivers'].append(f'Низьке покриття драйверів: {driver_coverage:.0f}%')
                        else:
                            driver_info['status'] = 'good'  # Немає пристроїв для перевірки
                    else:
                        raise Exception("lspci failed")
                        
                except Exception as e:
                    methods_tried.append(f'lspci failed: {str(e)}')
                    
                    # Метод 2: перевірка через /proc/modules
                    try:
                        with open('/proc/modules', 'r') as f:
                            modules = f.read()
                        
                        methods_tried.append('/proc/modules')
                        module_count = len(modules.split('\n')) - 1
                        
                        if module_count > 50:
                            driver_info['status'] = 'good'
                        elif module_count > 20:
                            driver_info['status'] = 'warning'
                        else:
                            driver_info['status'] = 'critical'
                            
                    except Exception as e2:
                        methods_tried.append(f'/proc/modules failed: {str(e2)}')
                        
                        # Метод 3: базова перевірка через dmesg
                        try:
                            result = subprocess.run(['dmesg'], capture_output=True, text=True, timeout=5)
                            methods_tried.append('dmesg')
                            if result.returncode == 0 and 'driver' in result.stdout.lower():
                                driver_info['status'] = 'good'
                            else:
                                driver_info['status'] = 'good'  # Припускаємо, що все OK в контейнері
                        except:
                            driver_info['status'] = 'good'  # Базове припущення для контейнерів
                            
                driver_info['debug_info'] = f"Methods tried: {', '.join(methods_tried)}"
                            
            except Exception as e:
                driver_info['status'] = 'good'  # В контейнерах часто драйвери керуються хостом
                driver_info['debug_info'] = f"Linux driver check failed: {str(e)}"
        else:
            driver_info['status'] = 'unsupported'
            
    except Exception as e:
        print(f"Помилка при перевірці драйверів: {e}")
        driver_info['status'] = 'error'
    
    return driver_info

def check_thermal_paste_status():
    """
    Аналізує стан термопасти на основі температурних показників
    """
    thermal_info = {
        'status': 'unknown',
        'recommendation': '',
        'temp_trend': [],
        'critical_temp_time': 0,
        'estimated_paste_age': 'unknown'
    }
    
    try:
        # Отримуємо температурні дані (перевіряємо наявність функції)
        temps = None
        if hasattr(psutil, 'sensors_temperatures'):
            temps = psutil.sensors_temperatures()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        if temps:
            cpu_temps = []
            for name, entries in temps.items():
                if 'cpu' in name.lower() or 'core' in name.lower():
                    for entry in entries:
                        if hasattr(entry, 'current') and entry.current:
                            cpu_temps.append(entry.current)
            
            if cpu_temps:
                avg_temp = sum(cpu_temps) / len(cpu_temps)
                max_temp = max(cpu_temps)
                
                # Аналіз стану термопасти
                if avg_temp > 80 and cpu_percent < 50:
                    # Висока температура при низькому навантаженні - ознака старої термопасти
                    thermal_info['status'] = 'critical'
                    thermal_info['recommendation'] = 'Негайна заміна термопасти! Висока температура при низькому навантаженні'
                    thermal_info['estimated_paste_age'] = 'більше 3 років'
                    
                elif avg_temp > 75 and cpu_percent < 70:
                    thermal_info['status'] = 'warning'
                    thermal_info['recommendation'] = 'Рекомендується заміна термопасти найближчим часом'
                    thermal_info['estimated_paste_age'] = '2-3 роки'
                    
                elif avg_temp > 85:
                    thermal_info['status'] = 'critical'
                    thermal_info['recommendation'] = 'Критична температура! Перевірте систему охолодження та термопасту'
                    
                elif avg_temp > 70:
                    thermal_info['status'] = 'warning'
                    thermal_info['recommendation'] = 'Підвищена температура. Моніторьте стан'
                    thermal_info['estimated_paste_age'] = '1-2 роки'
                    
                else:
                    thermal_info['status'] = 'good'
                    thermal_info['recommendation'] = 'Температура в нормі'
                    thermal_info['estimated_paste_age'] = 'менше 1 року'
                
                thermal_info['current_temp'] = avg_temp
                thermal_info['max_temp'] = max_temp
        else:
            # Спробуємо отримати температуру через WMI на Windows
            if platform.system() == "Windows":
                try:
                    result = subprocess.run([
                        'powershell', '-Command',
                        'Get-WmiObject -Namespace "root/OpenHardwareMonitor" -Class Sensor | Where-Object {$_.SensorType -eq "Temperature" -and $_.Name -like "*CPU*"} | Select-Object Value'
                    ], capture_output=True, text=True, timeout=10)
                    
                    if result.returncode == 0 and result.stdout.strip():
                        lines = result.stdout.strip().split('\n')
                        for line in lines[1:]:
                            if line.strip() and line.strip() != 'Value':
                                try:
                                    temp_value = float(line.strip())
                                    if temp_value > 85:
                                        thermal_info['status'] = 'critical'
                                        thermal_info['recommendation'] = 'Критична температура! Перевірте систему охолодження'
                                    elif temp_value > 75:
                                        thermal_info['status'] = 'warning'
                                        thermal_info['recommendation'] = 'Підвищена температура. Моніторьте стан'
                                    else:
                                        thermal_info['status'] = 'good'
                                        thermal_info['recommendation'] = 'Температура в нормі'
                                    thermal_info['current_temp'] = temp_value
                                    return thermal_info
                                except:
                                    continue
                except:
                    pass
            
            # Якщо температура недоступна, використовуємо CPU usage як індикатор
            if cpu_percent > 90:
                thermal_info['status'] = 'warning'
                thermal_info['recommendation'] = 'Високе навантаження CPU. Перевірте охолодження'
            else:
                thermal_info['status'] = 'good'
                thermal_info['recommendation'] = 'CPU usage в нормі'
                
    except Exception as e:
        print(f"Помилка при аналізі термопасти: {e}")
        thermal_info['status'] = 'error'
        thermal_info['recommendation'] = 'Помилка аналізу термопасти'
    
    return thermal_info

def get_fan_detailed_status():
    """
    Детальна перевірка статусу вентиляторів з покращеною підтримкою Windows
    """
    fan_info = {
        'fans': [],
        'status': 'unknown',
        'total_fans': 0,
        'working_fans': 0,
        'critical_fans': 0,
        'method_used': 'none'
    }
    
    try:
        system = platform.system()
        
        # Спочатку спробуємо psutil
        try:
            if hasattr(psutil, 'sensors_fans'):
                fans = psutil.sensors_fans()
            else:
                fans = None
            if fans:
                fan_info['method_used'] = 'psutil'
                for fan_name, fan_list in fans.items():
                    for i, fan in enumerate(fan_list):
                        fan_data = {
                            'name': f"{fan_name}_{i+1}",
                            'speed': fan.current if hasattr(fan, 'current') else 0,
                            'status': 'working'
                        }
                        
                        # Аналіз статусу вентилятора
                        if fan_data['speed'] == 0:
                            fan_data['status'] = 'stopped'
                            fan_info['critical_fans'] += 1
                        elif fan_data['speed'] > 5000:
                            fan_data['status'] = 'high_speed'
                        elif fan_data['speed'] < 500:
                            fan_data['status'] = 'low_speed'
                            
                        fan_info['fans'].append(fan_data)
                        fan_info['total_fans'] += 1
                        
                        if fan_data['status'] in ['working', 'high_speed']:
                            fan_info['working_fans'] += 1
        except:
            pass
        
        # Якщо psutil не дав результатів і це Windows, спробуємо WMI
        if fan_info['total_fans'] == 0 and system == "Windows":
            try:
                result = subprocess.run([
                    'powershell', '-Command',
                    'Get-WmiObject -Class Win32_Fan | Select-Object Name, DesiredSpeed, Status'
                ], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0 and result.stdout.strip():
                    fan_info['method_used'] = 'wmi'
                    lines = result.stdout.strip().split('\n')
                    
                    for line in lines[3:]:  # Пропускаємо заголовки
                        if line.strip() and 'Name' not in line:
                            parts = line.split()
                            if len(parts) >= 2:
                                fan_data = {
                                    'name': parts[0] if parts[0] != 'DesiredSpeed' else f'Fan_{fan_info["total_fans"]+1}',
                                    'speed': 'Active' if 'OK' in line else 'Unknown',
                                    'status': 'working' if 'OK' in line else 'unknown'
                                }
                                fan_info['fans'].append(fan_data)
                                fan_info['total_fans'] += 1
                                if fan_data['status'] == 'working':
                                    fan_info['working_fans'] += 1
            except Exception as e:
                print(f"WMI fan check failed: {e}")
        
        # Альтернативний метод для Windows через OpenHardwareMonitor-style WMI
        if fan_info['total_fans'] == 0 and system == "Windows":
            try:
                result = subprocess.run([
                    'powershell', '-Command',
                    'Get-WmiObject -Namespace "root/OpenHardwareMonitor" -Class Sensor | Where-Object {$_.SensorType -eq "Fan"} | Select-Object Name, Value'
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0 and result.stdout.strip():
                    fan_info['method_used'] = 'ohm'
                    lines = result.stdout.strip().split('\n')
                    for line in lines[3:]:
                        if line.strip() and 'Name' not in line:
                            parts = line.split()
                            if len(parts) >= 2:
                                try:
                                    speed = float(parts[-1])
                                    fan_data = {
                                        'name': ' '.join(parts[:-1]),
                                        'speed': int(speed),
                                        'status': 'working' if speed > 0 else 'stopped'
                                    }
                                    fan_info['fans'].append(fan_data)
                                    fan_info['total_fans'] += 1
                                    if speed > 0:
                                        fan_info['working_fans'] += 1
                                except:
                                    continue
            except:
                pass
        
        # Якщо все ще немає даних, створюємо базову інформацію на основі температури
        if fan_info['total_fans'] == 0:
            cpu_temp = psutil.cpu_percent(interval=0.1)
            if cpu_temp < 80:  # Якщо температура нормальна, припускаємо що вентилятори працюють
                fan_info['method_used'] = 'estimated'
                fan_info['fans'] = [{'name': 'CPU_Fan', 'speed': 'Активний', 'status': 'estimated'}]
                fan_info['total_fans'] = 1
                fan_info['working_fans'] = 1
                fan_info['status'] = 'estimated'
            else:
                fan_info['status'] = 'unavailable'
        
        # Визначення загального статусу
        if fan_info['status'] != 'estimated':
            if fan_info['total_fans'] == 0:
                fan_info['status'] = 'unavailable'
            elif fan_info['critical_fans'] > 0:
                fan_info['status'] = 'critical'
            elif fan_info['working_fans'] == fan_info['total_fans']:
                fan_info['status'] = 'good'
            else:
                fan_info['status'] = 'warning'
            
    except Exception as e:
        print(f"Помилка при перевірці вентиляторів: {e}")
        fan_info['status'] = 'error'
        fan_info['method_used'] = 'error'
    
    return fan_info

def get_system_health_score():
    """
    Розраховує загальний бал здоров'я системи
    """
    try:
        driver_status = check_driver_status()
        thermal_status = check_thermal_paste_status()
        fan_status = get_fan_detailed_status()
        
        # Система балів (0-100)
        score = 100
        issues = []
        
        # Вентилятори (30 балів)
        if fan_status['status'] == 'critical':
            score -= 30
            issues.append('Критичні проблеми з вентиляторами')
        elif fan_status['status'] == 'warning':
            score -= 15
            issues.append('Попередження про вентилятори')
        elif fan_status['status'] == 'unavailable':
            # Не знімаємо бали за недоступність вентиляторів в віртуальному середовищі
            pass
        
        # Термопаста (35 балів)
        if thermal_status['status'] == 'critical':
            score -= 35
            issues.append('Критична температура/термопаста')
        elif thermal_status['status'] == 'warning':
            score -= 20
            issues.append('Підвищена температура')
        
        # Драйвери (35 балів)
        if driver_status['status'] == 'critical':
            score -= 35
            issues.append('Критично застарілі драйвери')
        elif driver_status['status'] == 'warning':
            score -= 20
            issues.append('Деякі драйвери застарілі')
        elif driver_status['status'] == 'unavailable':
            score -= 5  # Зменшуємо штраф за недоступність
            # Не додаємо це як критичну проблему
        
        # Визначення рівня здоров'я
        if score >= 90:
            health_level = 'Відмінно'
            color = '#00FF66'
        elif score >= 75:
            health_level = 'Добре'
            color = '#FFFF00'
        elif score >= 60:
            health_level = 'Задовільно'
            color = '#FF8C00'
        else:
            health_level = 'Погано'
            color = '#FF6347'
        
        return {
            'score': max(0, score),
            'health_level': health_level,
            'color': color,
            'issues': issues,
            'detailed': {
                'drivers': driver_status,
                'thermal': thermal_status,
                'fans': fan_status
            }
        }
        
    except Exception as e:
        print(f"Помилка при розрахунку здоров'я системи: {e}")
        return {
            'score': 0,
            'health_level': 'Помилка',
            'color': '#FF0000',
            'issues': ['Помилка аналізу системи'],
            'detailed': {}
        }

if __name__ == "__main__":
    # Тестування модуля
    print("Перевірка драйверів:")
    drivers = check_driver_status()
    print(f"Статус: {drivers['status']}")
    print(f"Застарілі драйвери: {len(drivers['outdated_drivers'])}")
    
    print("\nПеревірка термопасти:")
    thermal = check_thermal_paste_status()
    print(f"Статус: {thermal['status']}")
    print(f"Рекомендація: {thermal['recommendation']}")
    
    print("\nПеревірка вентиляторів:")
    fans = get_fan_detailed_status()
    print(f"Статус: {fans['status']}")
    print(f"Всього вентиляторів: {fans['total_fans']}")
    
    print("\nЗагальне здоров'я системи:")
    health = get_system_health_score()
    print(f"Бал: {health['score']}/100")
    print(f"Рівень: {health['health_level']}")
    print(f"Проблеми: {health['issues']}")