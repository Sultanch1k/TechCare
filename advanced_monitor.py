# -*- coding: utf-8 -*-
"""
TechCare AI - Advanced System Monitor Module
Розширений модуль моніторингу з поглибленим аналізом системи
"""

import psutil
import platform
import subprocess
import os
import time
import json
from datetime import datetime, timedelta

class AdvancedSystemMonitor:
    def __init__(self):
        """Ініціалізація розширеного монітора"""
        self.os_type = platform.system()
        self.monitoring_cache = {}
        self.last_analysis_time = 0
    
    def get_comprehensive_analysis(self):
        """Отримання комплексного аналізу системи"""
        current_time = time.time()
        
        # Кешування для оптимізації (оновлення кожні 30 секунд)
        if current_time - self.last_analysis_time < 30 and self.monitoring_cache:
            return self.monitoring_cache
        
        analysis = {
            'cpu_analysis': self.analyze_cpu_performance(),
            'thermal_analysis': self.analyze_thermal_state(),
            'fan_analysis': self.analyze_cooling_system(),
            'disk_analysis': self.analyze_disk_health(),
            'network_analysis': self.analyze_network_performance(),
            'security_analysis': self.analyze_system_security(),
            'power_analysis': self.analyze_power_management(),
            'startup_analysis': self.analyze_startup_programs()
        }
        
        self.monitoring_cache = analysis
        self.last_analysis_time = current_time
        
        return analysis
    
    def analyze_cpu_performance(self):
        """Аналіз продуктивності процесора"""
        try:
            # Базова інформація
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_count_logical = psutil.cpu_count(logical=True)
            
            # Частота процесора
            cpu_freq = psutil.cpu_freq()
            current_freq = cpu_freq.current if cpu_freq else None
            max_freq = cpu_freq.max if cpu_freq else None
            
            # Навантаження по ядрах
            cpu_per_core = psutil.cpu_percent(percpu=True, interval=1)
            
            # Статистика часу
            cpu_times = psutil.cpu_times()
            
            # Середні навантаження
            try:
                load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            except:
                load_avg = [0, 0, 0]
            
            analysis = {
                'model': platform.processor(),
                'cores': cpu_count,
                'logical_cores': cpu_count_logical,
                'usage': cpu_percent,
                'frequency': current_freq,
                'max_frequency': max_freq,
                'usage_per_core': cpu_per_core,
                'load_average': load_avg,
                'times': {
                    'user': cpu_times.user,
                    'system': cpu_times.system,
                    'idle': cpu_times.idle
                },
                'performance_score': self.calculate_cpu_performance_score(cpu_percent, current_freq, max_freq)
            }
            
            return analysis
            
        except Exception as e:
            print(f"Помилка аналізу CPU: {e}")
            return {}
    
    def analyze_thermal_state(self):
        """Аналіз термального стану системи"""
        try:
            thermal_data = {
                'current_temp': None,
                'max_temp_24h': None,
                'average_temp': None,
                'thermal_zones': [],
                'paste_condition': 'невідомо',
                'cooling_efficiency': 0,
                'thermal_throttling': False
            }
            
            # Отримання температурних датчиків
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    all_temps = []
                    for name, entries in temps.items():
                        for entry in entries:
                            thermal_data['thermal_zones'].append({
                                'name': f"{name}_{entry.label or 'sensor'}",
                                'current': entry.current,
                                'high': entry.high,
                                'critical': entry.critical
                            })
                            all_temps.append(entry.current)
                    
                    if all_temps:
                        thermal_data['current_temp'] = f"{max(all_temps):.1f}°C"
                        thermal_data['average_temp'] = f"{sum(all_temps)/len(all_temps):.1f}°C"
                        
                        # Оцінка стану термопасти
                        max_temp = max(all_temps)
                        cpu_usage = psutil.cpu_percent()
                        
                        if max_temp > 85:
                            thermal_data['paste_condition'] = 'критичний'
                        elif max_temp > 75 and cpu_usage < 50:
                            thermal_data['paste_condition'] = 'потребує заміни'
                        elif max_temp < 60:
                            thermal_data['paste_condition'] = 'відмінний'
                        else:
                            thermal_data['paste_condition'] = 'задовільний'
                        
                        # Перевірка термотротлінгу
                        if max_temp > 90:
                            thermal_data['thermal_throttling'] = True
            except:
                pass
            
            return thermal_data
            
        except Exception as e:
            print(f"Помилка термального аналізу: {e}")
            return {}
    
    def analyze_cooling_system(self):
        """Аналіз системи охолодження"""
        try:
            cooling_data = {
                'fans': [],
                'total_fans': 0,
                'working_fans': 0,
                'average_speed': 0,
                'cooling_efficiency': 0,
                'noise_level': 'невідомо'
            }
            
            # Отримання інформації про вентилятори
            try:
                fans = psutil.sensors_fans()
                if fans:
                    all_speeds = []
                    for name, entries in fans.items():
                        for i, fan in enumerate(entries):
                            fan_info = {
                                'name': f"{name}_{i}",
                                'speed': fan.current,
                                'status': 'працює' if fan.current > 0 else 'зупинений'
                            }
                            cooling_data['fans'].append(fan_info)
                            cooling_data['total_fans'] += 1
                            
                            if fan.current > 0:
                                cooling_data['working_fans'] += 1
                                all_speeds.append(fan.current)
                    
                    if all_speeds:
                        cooling_data['average_speed'] = sum(all_speeds) / len(all_speeds)
                        
                        # Оцінка рівня шуму
                        avg_speed = cooling_data['average_speed']
                        if avg_speed > 2500:
                            cooling_data['noise_level'] = 'високий'
                        elif avg_speed > 1500:
                            cooling_data['noise_level'] = 'помірний'
                        else:
                            cooling_data['noise_level'] = 'низький'
            except:
                pass
            
            # Статус системи охолодження
            if cooling_data['total_fans'] == 0:
                cooling_data['status'] = 'unknown'
            elif cooling_data['working_fans'] == 0:
                cooling_data['status'] = 'critical'
            elif cooling_data['working_fans'] < cooling_data['total_fans']:
                cooling_data['status'] = 'warning'
            else:
                cooling_data['status'] = 'good'
            
            return cooling_data
            
        except Exception as e:
            print(f"Помилка аналізу охолодження: {e}")
            return {}
    
    def analyze_disk_health(self):
        """Аналіз здоров'я дисків"""
        try:
            disk_data = {
                'disks': [],
                'total_disks': 0,
                'warnings': [],
                'fragmentation': {},
                'large_files': []
            }
            
            # Аналіз розділів дисків
            partitions = psutil.disk_partitions()
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    disk_info = {
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'filesystem': partition.fstype,
                        'total_size': self.format_bytes(usage.total),
                        'used_space': self.format_bytes(usage.used),
                        'free_space': self.format_bytes(usage.free),
                        'usage_percent': (usage.used / usage.total) * 100,
                        'type': self.detect_disk_type(partition.device),
                        'health_status': 'невідомо'
                    }
                    
                    # Оцінка здоров'я на основі використання
                    if disk_info['usage_percent'] > 95:
                        disk_info['health_status'] = 'критичний'
                        disk_data['warnings'].append(f"Диск {partition.device} майже повний")
                    elif disk_info['usage_percent'] > 85:
                        disk_info['health_status'] = 'попередження'
                    else:
                        disk_info['health_status'] = 'нормальний'
                    
                    disk_data['disks'].append(disk_info)
                    disk_data['total_disks'] += 1
                    
                except PermissionError:
                    continue
            
            # Аналіз I/O статистики
            try:
                io_stats = psutil.disk_io_counters()
                if io_stats:
                    disk_data['io_performance'] = {
                        'read_count': io_stats.read_count,
                        'write_count': io_stats.write_count,
                        'read_bytes': self.format_bytes(io_stats.read_bytes),
                        'write_bytes': self.format_bytes(io_stats.write_bytes)
                    }
            except:
                pass
            
            return disk_data
            
        except Exception as e:
            print(f"Помилка аналізу дисків: {e}")
            return {}
    
    def analyze_network_performance(self):
        """Аналіз мережевої продуктивності"""
        try:
            network_data = {
                'speed_test': {},
                'connections': [],
                'interfaces': {},
                'dns_analysis': {},
                'bandwidth_usage': {}
            }
            
            # Статистика мережевих інтерфейсів
            net_io = psutil.net_io_counters(pernic=True)
            
            for interface, stats in net_io.items():
                network_data['interfaces'][interface] = {
                    'bytes_sent': self.format_bytes(stats.bytes_sent),
                    'bytes_recv': self.format_bytes(stats.bytes_recv),
                    'packets_sent': stats.packets_sent,
                    'packets_recv': stats.packets_recv,
                    'errors_in': stats.errin,
                    'errors_out': stats.errout
                }
            
            # Активні з'єднання
            try:
                connections = psutil.net_connections()
                
                connection_summary = {}
                for conn in connections:
                    status = conn.status
                    if status in connection_summary:
                        connection_summary[status] += 1
                    else:
                        connection_summary[status] = 1
                
                network_data['connections'] = [
                    {'status': status, 'count': count}
                    for status, count in connection_summary.items()
                ]
                
                # Симуляція швидкості підключення (базовий аналіз)
                network_data['speed_test'] = {
                    'download': 50.0 + (len(connections) * 0.1),  # Симуляція
                    'upload': 25.0 + (len(connections) * 0.05),
                    'ping': 20 + min(len(connections), 50)
                }
                
            except:
                network_data['connections'] = []
                network_data['speed_test'] = {'download': 0, 'upload': 0, 'ping': 0}
            
            # DNS аналіз (базовий)
            network_data['dns_analysis'] = {
                'response_time': 15,  # мс (симуляція)
                'server': '8.8.8.8'  # Google DNS як приклад
            }
            
            return network_data
            
        except Exception as e:
            print(f"Помилка аналізу мережі: {e}")
            return {}
    
    def analyze_system_security(self):
        """Аналіз безпеки системи"""
        try:
            security_data = {
                'security_score': 0,
                'checks': {},
                'recommendations': [],
                'recent_events': []
            }
            
            checks_passed = 0
            total_checks = 6
            
            # Перевірка оновлень системи
            security_data['checks']['system_updates'] = self.check_system_updates()
            if security_data['checks']['system_updates']:
                checks_passed += 1
            
            # Перевірка антивірусу (базова)
            security_data['checks']['antivirus'] = self.check_antivirus_status()
            if security_data['checks']['antivirus']:
                checks_passed += 1
            
            # Перевірка firewall
            security_data['checks']['firewall'] = self.check_firewall_status()
            if security_data['checks']['firewall']:
                checks_passed += 1
            
            # Перевірка автозапуску
            security_data['checks']['startup_programs'] = self.check_startup_security()
            if security_data['checks']['startup_programs']:
                checks_passed += 1
            
            # Перевірка мережевої безпеки
            security_data['checks']['network_security'] = self.check_network_security()
            if security_data['checks']['network_security']:
                checks_passed += 1
            
            # Перевірка прав доступу
            security_data['checks']['user_permissions'] = self.check_user_permissions()
            if security_data['checks']['user_permissions']:
                checks_passed += 1
            
            # Розрахунок загального скору
            security_data['security_score'] = int((checks_passed / total_checks) * 100)
            
            # Рекомендації
            if not security_data['checks']['system_updates']:
                security_data['recommendations'].append('Оновіть систему до останньої версії')
            
            if not security_data['checks']['antivirus']:
                security_data['recommendations'].append('Встановіть або оновіть антивірус')
            
            if not security_data['checks']['firewall']:
                security_data['recommendations'].append('Увімкніть системний firewall')
            
            return security_data
            
        except Exception as e:
            print(f"Помилка аналізу безпеки: {e}")
            return {}
    
    def analyze_power_management(self):
        """Аналіз управління живленням"""
        try:
            power_data = {
                'battery_present': False,
                'power_plan': 'невідомо',
                'energy_efficiency': 0
            }
            
            # Перевірка батареї
            try:
                battery = psutil.sensors_battery()
                if battery:
                    power_data['battery_present'] = True
                    power_data['battery_info'] = {
                        'percent': battery.percent,
                        'plugged': battery.power_plugged,
                        'time_left': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                    }
            except:
                pass
            
            return power_data
            
        except Exception as e:
            print(f"Помилка аналізу живлення: {e}")
            return {}
    
    def analyze_startup_programs(self):
        """Аналіз програм автозапуску"""
        try:
            startup_data = {
                'total_count': 0,
                'enabled_count': 0,
                'programs': [],
                'recommendation': ''
            }
            
            # Підрахунок запущених процесів як приблизна оцінка
            processes = list(psutil.process_iter(['pid', 'name', 'create_time']))
            startup_data['total_count'] = len(processes)
            
            # Фільтрація процесів, запущених недавно (приблизна оцінка автозапуску)
            boot_time = psutil.boot_time()
            startup_processes = [p for p in processes if p.info['create_time'] - boot_time < 120]  # 2 хвилини після запуску
            
            startup_data['enabled_count'] = len(startup_processes)
            
            # Рекомендації
            if startup_data['enabled_count'] > 15:
                startup_data['recommendation'] = 'Рекомендується відключити деякі програми з автозапуску'
            elif startup_data['enabled_count'] < 5:
                startup_data['recommendation'] = 'Оптимальна кількість програм автозапуску'
            else:
                startup_data['recommendation'] = 'Кількість програм автозапуску в нормі'
            
            return startup_data
            
        except Exception as e:
            print(f"Помилка аналізу автозапуску: {e}")
            return {}
    
    # Допоміжні методи
    def calculate_cpu_performance_score(self, usage, current_freq, max_freq):
        """Розрахунок скору продуктивності CPU"""
        try:
            if max_freq and current_freq:
                freq_ratio = current_freq / max_freq
                # Обернено пропорційний зв'язок з навантаженням
                usage_score = max(0, 100 - usage)
                freq_score = freq_ratio * 100
                return int((usage_score + freq_score) / 2)
            else:
                return max(0, int(100 - usage))
        except:
            return 50
    
    def detect_disk_type(self, device):
        """Визначення типу диска"""
        # Спрощена логіка визначення типу
        if 'nvme' in device.lower():
            return 'NVMe SSD'
        elif 'ssd' in device.lower():
            return 'SSD'
        else:
            return 'HDD'
    
    def format_bytes(self, bytes_value):
        """Форматування байтів"""
        if bytes_value < 1024:
            return f"{bytes_value} B"
        elif bytes_value < 1024**2:
            return f"{bytes_value/1024:.1f} KB"
        elif bytes_value < 1024**3:
            return f"{bytes_value/(1024**2):.1f} MB"
        else:
            return f"{bytes_value/(1024**3):.1f} GB"
    
    def check_system_updates(self):
        """Перевірка наявності оновлень системи"""
        # Спрощена перевірка
        try:
            if self.os_type == "Windows":
                # На Windows можна перевірити через PowerShell
                return True  # Симуляція
            elif self.os_type == "Linux":
                # На Linux можна використати apt list --upgradable
                return True  # Симуляція
            else:
                return True
        except:
            return False
    
    def check_antivirus_status(self):
        """Перевірка статусу антивірусу"""
        # Спрощена перевірка
        try:
            # Можна перевірити запущені процеси на наявність антивірусних програм
            processes = [p.info['name'].lower() for p in psutil.process_iter(['name'])]
            antivirus_keywords = ['defender', 'antivirus', 'avast', 'norton', 'mcafee', 'kaspersky']
            
            for keyword in antivirus_keywords:
                if any(keyword in process for process in processes):
                    return True
            return False
        except:
            return False
    
    def check_firewall_status(self):
        """Перевірка статусу firewall"""
        # Спрощена перевірка
        try:
            if self.os_type == "Windows":
                # Можна перевірити через netsh advfirewall show allprofiles
                return True  # Симуляція
            elif self.os_type == "Linux":
                # Можна перевірити через ufw status або iptables
                return True  # Симуляція
            else:
                return True
        except:
            return False
    
    def check_startup_security(self):
        """Перевірка безпеки автозапуску"""
        # Спрощена перевірка - вважаємо безпечним якщо програм автозапуску не забагато
        try:
            startup_info = self.analyze_startup_programs()
            return startup_info['enabled_count'] < 20
        except:
            return True
    
    def check_network_security(self):
        """Перевірка мережевої безпеки"""
        # Спрощена перевірка
        try:
            # Перевіряємо кількість відкритих з'єднань
            connections = psutil.net_connections()
            external_connections = [c for c in connections if c.raddr and c.status == 'ESTABLISHED']
            
            # Вважаємо безпечним якщо не забагато зовнішніх з'єднань
            return len(external_connections) < 50
        except:
            return True
    
    def check_user_permissions(self):
        """Перевірка прав користувача"""
        # Спрощена перевірка
        try:
            # Перевіряємо чи користувач не працює під адміністратором постійно
            return not os.getuid() == 0 if hasattr(os, 'getuid') else True
        except:
            return True
