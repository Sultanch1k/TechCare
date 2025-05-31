# -*- coding: utf-8 -*-
"""
TechCare - Additional Features Module
Додаткові функції для розширення можливостей TechCare
"""

import psutil
import subprocess
import platform
import time
import json
import os
from datetime import datetime, timedelta

def check_startup_programs():
    """
    Перевіряє програми в автозапуску та їх вплив на продуктивність
    """
    startup_info = {
        'programs': [],
        'total_count': 0,
        'heavy_programs': [],
        'recommendation': '',
        'startup_time_estimate': 'unknown'
    }
    
    try:
        system = platform.system()
        
        if system == "Windows":
            # Перевірка через реєстр Windows
            try:
                result = subprocess.run([
                    'powershell', '-Command',
                    'Get-WmiObject -Class Win32_StartupCommand | Select-Object Name, Command, Location'
                ], capture_output=True, text=True, timeout=15)
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[3:]:
                        if line.strip() and 'Name' not in line:
                            parts = line.split(None, 2)
                            if len(parts) >= 2:
                                program_name = parts[0]
                                startup_info['programs'].append({
                                    'name': program_name,
                                    'path': parts[1] if len(parts) > 1 else 'Unknown',
                                    'impact': 'medium'
                                })
                                startup_info['total_count'] += 1
                                
                                # Визначення "важких" програм
                                heavy_keywords = ['adobe', 'office', 'skype', 'steam', 'discord', 'zoom']
                                if any(keyword in program_name.lower() for keyword in heavy_keywords):
                                    startup_info['heavy_programs'].append(program_name)
            except:
                pass
        
        elif system == "Linux":
            # Перевірка автозапуску в Linux
            try:
                autostart_dirs = [
                    os.path.expanduser('~/.config/autostart/'),
                    '/etc/xdg/autostart/'
                ]
                
                for directory in autostart_dirs:
                    if os.path.exists(directory):
                        for file in os.listdir(directory):
                            if file.endswith('.desktop'):
                                startup_info['programs'].append({
                                    'name': file.replace('.desktop', ''),
                                    'path': os.path.join(directory, file),
                                    'impact': 'low'
                                })
                                startup_info['total_count'] += 1
            except:
                pass
        
        # Генерація рекомендацій
        if startup_info['total_count'] > 15:
            startup_info['recommendation'] = 'Забагато програм в автозапуску! Рекомендується відключити непотрібні'
        elif startup_info['total_count'] > 10:
            startup_info['recommendation'] = 'Середня кількість програм в автозапуску. Перевірте необхідність'
        else:
            startup_info['recommendation'] = 'Кількість програм в автозапуску в нормі'
        
        # Оцінка часу завантаження
        if startup_info['total_count'] > 20:
            startup_info['startup_time_estimate'] = 'повільний (>2 хв)'
        elif startup_info['total_count'] > 10:
            startup_info['startup_time_estimate'] = 'середній (1-2 хв)'
        else:
            startup_info['startup_time_estimate'] = 'швидкий (<1 хв)'
            
    except Exception as e:
        startup_info['recommendation'] = f'Помилка перевірки автозапуску: {str(e)}'
    
    return startup_info

def check_disk_health():
    """
    Перевіряє здоров'я дисків та фрагментацію
    """
    disk_health = {
        'disks': [],
        'total_disks': 0,
        'healthy_disks': 0,
        'warnings': [],
        'fragmentation_level': 'unknown'
    }
    
    try:
        # Отримання інформації про всі диски
        disk_partitions = psutil.disk_partitions()
        
        for partition in disk_partitions:
            try:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                disk_info = {
                    'drive': partition.device,
                    'filesystem': partition.fstype,
                    'total_gb': round(disk_usage.total / (1024**3), 2),
                    'used_gb': round(disk_usage.used / (1024**3), 2),
                    'free_gb': round(disk_usage.free / (1024**3), 2),
                    'usage_percent': round((disk_usage.used / disk_usage.total) * 100, 1),
                    'health': 'good'
                }
                
                # Аналіз здоров'я диска
                if disk_info['usage_percent'] > 95:
                    disk_info['health'] = 'critical'
                    disk_health['warnings'].append(f"Диск {partition.device} майже повний!")
                elif disk_info['usage_percent'] > 85:
                    disk_info['health'] = 'warning'
                    disk_health['warnings'].append(f"Диск {partition.device} заповнений на {disk_info['usage_percent']}%")
                else:
                    disk_health['healthy_disks'] += 1
                
                disk_health['disks'].append(disk_info)
                disk_health['total_disks'] += 1
                
            except PermissionError:
                continue
        
        # Перевірка фрагментації для Windows
        if platform.system() == "Windows":
            try:
                result = subprocess.run([
                    'powershell', '-Command',
                    'Get-WmiObject -Class Win32_Volume | Where-Object {$_.DriveLetter -ne $null} | Select-Object DriveLetter, @{Name="FragmentationPercentage";Expression={$_.BlockSize}}'
                ], capture_output=True, text=True, timeout=20)
                
                if result.returncode == 0:
                    # Спрощена оцінка фрагментації
                    if 'C:' in result.stdout:
                        disk_health['fragmentation_level'] = 'низька (рекомендується дефрагментація раз на місяць)'
                    else:
                        disk_health['fragmentation_level'] = 'невідома'
            except:
                disk_health['fragmentation_level'] = 'перевірка недоступна'
        
    except Exception as e:
        disk_health['warnings'].append(f'Помилка аналізу дисків: {str(e)}')
    
    return disk_health

def check_network_performance():
    """
    Перевіряє продуктивність мережі та підключення
    """
    network_info = {
        'interfaces': [],
        'active_connections': 0,
        'bytes_sent': 0,
        'bytes_received': 0,
        'packet_loss': 'unknown',
        'internet_speed': 'unknown',
        'dns_response_time': 'unknown'
    }
    
    try:
        # Інформація про мережеві інтерфейси
        net_stats = psutil.net_io_counters(pernic=True)
        
        for interface, stats in net_stats.items():
            if stats.bytes_sent > 0 or stats.bytes_received > 0:
                interface_info = {
                    'name': interface,
                    'bytes_sent_mb': round(stats.bytes_sent / (1024**2), 2),
                    'bytes_received_mb': round(stats.bytes_received / (1024**2), 2),
                    'packets_sent': stats.packets_sent,
                    'packets_received': stats.packets_recv,
                    'errors': stats.errin + stats.errout,
                    'status': 'active' if stats.bytes_sent > 1024 else 'inactive'
                }
                network_info['interfaces'].append(interface_info)
        
        # Загальна статистика
        total_stats = psutil.net_io_counters()
        network_info['bytes_sent'] = round(total_stats.bytes_sent / (1024**2), 2)
        network_info['bytes_received'] = round(total_stats.bytes_recv / (1024**2), 2)
        
        # Активні з'єднання
        connections = psutil.net_connections()
        network_info['active_connections'] = len([c for c in connections if c.status == 'ESTABLISHED'])
        
        # Тест DNS (простий ping до 8.8.8.8)
        try:
            import socket
            start_time = time.time()
            socket.gethostbyname('google.com')
            dns_time = (time.time() - start_time) * 1000
            network_info['dns_response_time'] = f"{dns_time:.0f} мс"
            
            if dns_time < 50:
                network_info['dns_status'] = 'відмінно'
            elif dns_time < 100:
                network_info['dns_status'] = 'добре'
            else:
                network_info['dns_status'] = 'повільно'
        except:
            network_info['dns_response_time'] = 'недоступно'
            network_info['dns_status'] = 'помилка'
            
    except Exception as e:
        network_info['error'] = f'Помилка аналізу мережі: {str(e)}'
    
    return network_info

def check_system_security():
    """
    Базова перевірка безпеки системи
    """
    security_info = {
        'antivirus_status': 'unknown',
        'firewall_status': 'unknown',
        'windows_defender': 'unknown',
        'last_update': 'unknown',
        'security_score': 0,
        'recommendations': []
    }
    
    try:
        system = platform.system()
        
        if system == "Windows":
            # Перевірка Windows Defender
            try:
                result = subprocess.run([
                    'powershell', '-Command',
                    'Get-MpComputerStatus | Select-Object AntivirusEnabled, FirewallEnabled, RealTimeProtectionEnabled'
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    output = result.stdout.lower()
                    
                    if 'true' in output:
                        if 'antivirusenabled' in output and 'true' in output:
                            security_info['antivirus_status'] = 'активний'
                            security_info['security_score'] += 30
                        
                        if 'firewallenabled' in output and 'true' in output:
                            security_info['firewall_status'] = 'активний'
                            security_info['security_score'] += 30
                        
                        if 'realtimeprotectionenabled' in output and 'true' in output:
                            security_info['windows_defender'] = 'активний'
                            security_info['security_score'] += 40
                    else:
                        security_info['recommendations'].append('Увімкніть Windows Defender')
            except:
                security_info['antivirus_status'] = 'перевірка недоступна'
            
            # Перевірка оновлень Windows
            try:
                result = subprocess.run([
                    'powershell', '-Command',
                    'Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 1 | Select-Object InstalledOn'
                ], capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0 and result.stdout.strip():
                    lines = result.stdout.strip().split('\n')
                    if len(lines) > 1:
                        date_line = lines[1].strip()
                        security_info['last_update'] = date_line if date_line else 'невідомо'
            except:
                pass
        
        # Загальна оцінка безпеки
        if security_info['security_score'] >= 80:
            security_info['overall_status'] = 'безпечно'
        elif security_info['security_score'] >= 50:
            security_info['overall_status'] = 'помірно безпечно'
        else:
            security_info['overall_status'] = 'потребує уваги'
            
        if not security_info['recommendations']:
            security_info['recommendations'].append('Базова безпека налаштована')
            
    except Exception as e:
        security_info['error'] = f'Помилка перевірки безпеки: {str(e)}'
    
    return security_info

def get_performance_recommendations():
    """
    Генерує персоналізовані рекомендації для покращення продуктивності
    """
    recommendations = []
    
    try:
        # Аналіз використання RAM
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            recommendations.append({
                'category': 'Пам\'ять',
                'issue': f'Використання RAM: {memory.percent:.1f}%',
                'recommendation': 'Закрийте непотрібні програми або розгляньте збільшення оперативної пам\'яті',
                'priority': 'high'
            })
        
        # Аналіз CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 80:
            recommendations.append({
                'category': 'Процесор',
                'issue': f'Використання CPU: {cpu_percent:.1f}%',
                'recommendation': 'Перевірте процеси в диспетчері задач, можливо потрібен перезапуск',
                'priority': 'high'
            })
        
        # Аналіз дисків
        for partition in psutil.disk_partitions():
            try:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                usage_percent = (disk_usage.used / disk_usage.total) * 100
                
                if usage_percent > 90:
                    recommendations.append({
                        'category': 'Диск',
                        'issue': f'Диск {partition.device} заповнений на {usage_percent:.1f}%',
                        'recommendation': 'Очистіть непотрібні файли або перемістіть дані на інший диск',
                        'priority': 'medium'
                    })
            except:
                continue
        
        # Аналіз автозапуску
        startup_info = check_startup_programs()
        if startup_info['total_count'] > 15:
            recommendations.append({
                'category': 'Автозапуск',
                'issue': f'Забагато програм в автозапуску: {startup_info["total_count"]}',
                'recommendation': 'Відключіть непотрібні програми з автозапуску через msconfig або налаштування',
                'priority': 'medium'
            })
        
        # Якщо немає проблем
        if not recommendations:
            recommendations.append({
                'category': 'Загальне',
                'issue': 'Система працює стабільно',
                'recommendation': 'Продовжуйте регулярне обслуговування: очищення диска, оновлення драйверів',
                'priority': 'low'
            })
            
    except Exception as e:
        recommendations.append({
            'category': 'Помилка',
            'issue': 'Не вдалося проаналізувати систему',
            'recommendation': f'Помилка аналізу: {str(e)}',
            'priority': 'low'
        })
    
    return recommendations

if __name__ == "__main__":
    # Тестування модуля
    print("Тест додаткових функцій TechCare:")
    
    print("\n1. Автозапуск:")
    startup = check_startup_programs()
    print(f"Програм: {startup['total_count']}, Рекомендація: {startup['recommendation']}")
    
    print("\n2. Здоров'я дисків:")
    disks = check_disk_health()
    print(f"Дисків: {disks['total_disks']}, Здорових: {disks['healthy_disks']}")
    
    print("\n3. Мережа:")
    network = check_network_performance()
    print(f"З'єднань: {network['active_connections']}, DNS: {network['dns_response_time']}")
    
    print("\n4. Безпека:")
    security = check_system_security()
    print(f"Бал безпеки: {security['security_score']}/100")
    
    print("\n5. Рекомендації:")
    recs = get_performance_recommendations()
    for rec in recs[:3]:
        print(f"- {rec['category']}: {rec['recommendation']}")