# -*- coding: utf-8 -*-
"""
TechCare AI - Auto Repair System Module
Модуль автоматичної діагностики та самовиправлення проблем
"""

import psutil
import subprocess
import platform
import os
import tempfile
import shutil
from datetime import datetime
import time

class AutoRepairSystem:
    def __init__(self):
        """Ініціалізація системи автоматичного ремонту"""
        self.os_type = platform.system()
        self.auto_fix_enabled = True
        self.repair_history = []
        
        # Визначення доступних інструментів ремонту
        self.available_tools = self.detect_available_tools()
    
    def detect_available_tools(self):
        """Виявлення доступних інструментів для ремонту"""
        tools = {
            'disk_cleanup': False,
            'memory_cleanup': True,  # Завжди доступно через psutil
            'process_manager': True,  # Завжди доступно через psutil
            'network_reset': False,
            'registry_cleanup': False,
            'temp_cleanup': True,  # Завжди доступно
            'service_restart': False
        }
        
        try:
            if self.os_type == "Windows":
                # Перевірка Windows інструментів
                tools['disk_cleanup'] = self.check_command_available('cleanmgr')
                tools['network_reset'] = True  # netsh завжди доступний
                tools['registry_cleanup'] = True  # можна через regedit
                tools['service_restart'] = True  # sc command
                
            elif self.os_type == "Linux":
                # Перевірка Linux інструментів
                tools['disk_cleanup'] = self.check_command_available('apt-get') or self.check_command_available('yum')
                tools['network_reset'] = self.check_command_available('systemctl')
                tools['service_restart'] = self.check_command_available('systemctl')
                
            elif self.os_type == "Darwin":  # macOS
                tools['disk_cleanup'] = True
                tools['service_restart'] = self.check_command_available('launchctl')
                
        except Exception as e:
            print(f"Помилка виявлення інструментів: {e}")
        
        return tools
    
    def check_command_available(self, command):
        """Перевірка доступності команди"""
        try:
            subprocess.run([command], capture_output=True, timeout=5)
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            return False
    
    def diagnose_system(self):
        """Повна діагностика системи"""
        issues = []
        
        try:
            # Діагностика використання ресурсів
            issues.extend(self.diagnose_resource_usage())
            
            # Діагностика процесів
            issues.extend(self.diagnose_processes())
            
            # Діагностика дисків
            issues.extend(self.diagnose_disk_issues())
            
            # Діагностика мережі
            issues.extend(self.diagnose_network_issues())
            
            # Діагностика температури
            issues.extend(self.diagnose_thermal_issues())
            
            # Діагностика служб і процесів
            issues.extend(self.diagnose_services())
            
        except Exception as e:
            print(f"Помилка діагностики: {e}")
            issues.append({
                'id': 'diagnostic_error',
                'type': 'Помилка діагностики',
                'description': f'Виникла помилка під час діагностики: {str(e)}',
                'severity': 'medium',
                'auto_fixable': False
            })
        
        return issues
    
    def diagnose_resource_usage(self):
        """Діагностика використання ресурсів"""
        issues = []
        
        try:
            # Перевірка CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 90:
                issues.append({
                    'id': 'high_cpu_usage',
                    'type': 'Високе використання CPU',
                    'description': f'CPU використовується на {cpu_percent:.1f}%',
                    'severity': 'high',
                    'auto_fixable': True
                })
            
            # Перевірка RAM
            memory = psutil.virtual_memory()
            if memory.percent > 95:
                issues.append({
                    'id': 'high_memory_usage',
                    'type': 'Критичне використання RAM',
                    'description': f'RAM використовується на {memory.percent:.1f}%',
                    'severity': 'high',
                    'auto_fixable': True
                })
            elif memory.percent > 85:
                issues.append({
                    'id': 'moderate_memory_usage',
                    'type': 'Високе використання RAM',
                    'description': f'RAM використовується на {memory.percent:.1f}%',
                    'severity': 'medium',
                    'auto_fixable': True
                })
            
            # Перевірка дисків
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    usage_percent = (usage.used / usage.total) * 100
                    
                    if usage_percent > 95:
                        issues.append({
                            'id': f'disk_full_{partition.device}',
                            'type': 'Диск майже повний',
                            'description': f'Диск {partition.device} заповнений на {usage_percent:.1f}%',
                            'severity': 'high',
                            'auto_fixable': True
                        })
                    elif usage_percent > 85:
                        issues.append({
                            'id': f'disk_low_space_{partition.device}',
                            'type': 'Мало місця на диску',
                            'description': f'Диск {partition.device} заповнений на {usage_percent:.1f}%',
                            'severity': 'medium',
                            'auto_fixable': True
                        })
                except PermissionError:
                    continue
                    
        except Exception as e:
            print(f"Помилка діагностики ресурсів: {e}")
        
        return issues
    
    def diagnose_processes(self):
        """Діагностика проблемних процесів"""
        issues = []
        
        try:
            # Пошук процесів з високим споживанням ресурсів
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    
                    # Процеси з високим CPU
                    if pinfo['cpu_percent'] > 80:
                        issues.append({
                            'id': f'high_cpu_process_{pinfo["pid"]}',
                            'type': 'Процес навантажує CPU',
                            'description': f'Процес {pinfo["name"]} (PID: {pinfo["pid"]}) використовує {pinfo["cpu_percent"]:.1f}% CPU',
                            'severity': 'medium',
                            'auto_fixable': True,
                            'process_info': pinfo
                        })
                    
                    # Процеси з високим споживанням пам'яті
                    if pinfo['memory_percent'] > 20:  # Більше 20% RAM
                        issues.append({
                            'id': f'high_memory_process_{pinfo["pid"]}',
                            'type': 'Процес споживає багато пам\'яті',
                            'description': f'Процес {pinfo["name"]} (PID: {pinfo["pid"]}) використовує {pinfo["memory_percent"]:.1f}% RAM',
                            'severity': 'medium',
                            'auto_fixable': True,
                            'process_info': pinfo
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                    
            # Пошук зависших процесів
            zombie_count = len([p for p in psutil.process_iter() if p.status() == psutil.STATUS_ZOMBIE])
            if zombie_count > 0:
                issues.append({
                    'id': 'zombie_processes',
                    'type': 'Зависші процеси',
                    'description': f'Виявлено {zombie_count} зависших процесів',
                    'severity': 'medium',
                    'auto_fixable': True
                })
                
        except Exception as e:
            print(f"Помилка діагностики процесів: {e}")
        
        return issues
    
    def diagnose_disk_issues(self):
        """Діагностика проблем з дисками"""
        issues = []
        
        try:
            # Перевірка тимчасових файлів
            temp_size = self.calculate_temp_files_size()
            if temp_size > 1024 * 1024 * 1024:  # Більше 1GB
                issues.append({
                    'id': 'large_temp_files',
                    'type': 'Багато тимчасових файлів',
                    'description': f'Тимчасові файли займають {temp_size / (1024**3):.1f} GB',
                    'severity': 'medium',
                    'auto_fixable': True
                })
            
            # Перевірка I/O статистики дисків
            try:
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    # Перевірка на високу активність дисків
                    read_mb = disk_io.read_bytes / (1024**2)
                    write_mb = disk_io.write_bytes / (1024**2)
                    
                    # Це спрощена перевірка - в реальності потрібен аналіз динаміки
                    if disk_io.read_time > 10000 or disk_io.write_time > 10000:  # Високий час очікування
                        issues.append({
                            'id': 'slow_disk_io',
                            'type': 'Повільна робота диска',
                            'description': 'Виявлено повільну роботу диска',
                            'severity': 'medium',
                            'auto_fixable': False  # Потребує ручного втручання
                        })
            except:
                pass
                
        except Exception as e:
            print(f"Помилка діагностики дисків: {e}")
        
        return issues
    
    def diagnose_network_issues(self):
        """Діагностика мережевих проблем"""
        issues = []
        
        try:
            # Перевірка мережевих з'єднань
            connections = psutil.net_connections()
            
            # Підрахунок різних типів з'єднань
            connection_stats = {}
            for conn in connections:
                status = conn.status
                connection_stats[status] = connection_stats.get(status, 0) + 1
            
            # Перевірка на занадто багато з'єднань
            total_connections = len(connections)
            if total_connections > 200:
                issues.append({
                    'id': 'too_many_connections',
                    'type': 'Занадто багато мережевих з\'єднань',
                    'description': f'Активно {total_connections} мережевих з\'єднань',
                    'severity': 'medium',
                    'auto_fixable': True
                })
            
            # Перевірка мережевих помилок
            net_io = psutil.net_io_counters()
            if net_io:
                total_errors = net_io.errin + net_io.errout
                if total_errors > 100:
                    issues.append({
                        'id': 'network_errors',
                        'type': 'Мережеві помилки',
                        'description': f'Виявлено {total_errors} мережевих помилок',
                        'severity': 'medium',
                        'auto_fixable': True
                    })
                    
        except Exception as e:
            print(f"Помилка діагностики мережі: {e}")
        
        return issues
    
    def diagnose_thermal_issues(self):
        """Діагностика температурних проблем"""
        issues = []
        
        try:
            # Перевірка температури
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                if temps:
                    max_temp = 0
                    for name, entries in temps.items():
                        for entry in entries:
                            max_temp = max(max_temp, entry.current)
                    
                    if max_temp > 85:
                        issues.append({
                            'id': 'high_temperature',
                            'type': 'Критична температура',
                            'description': f'Температура досягла {max_temp:.1f}°C',
                            'severity': 'high',
                            'auto_fixable': True
                        })
                    elif max_temp > 75:
                        issues.append({
                            'id': 'moderate_temperature',
                            'type': 'Підвищена температура',
                            'description': f'Температура досягла {max_temp:.1f}°C',
                            'severity': 'medium',
                            'auto_fixable': True
                        })
                        
        except Exception as e:
            print(f"Помилка діагностики температури: {e}")
        
        return issues
    
    def diagnose_services(self):
        """Діагностика служб та сервісів"""
        issues = []
        
        try:
            # Перевірка кількості запущених процесів
            process_count = len(list(psutil.process_iter()))
            
            if process_count > 300:
                issues.append({
                    'id': 'too_many_processes',
                    'type': 'Занадто багато процесів',
                    'description': f'Запущено {process_count} процесів',
                    'severity': 'medium',
                    'auto_fixable': True
                })
            
            # Перевірка часу роботи системи
            uptime_seconds = time.time() - psutil.boot_time()
            uptime_days = uptime_seconds / (24 * 3600)
            
            if uptime_days > 7:  # Більше тижня
                issues.append({
                    'id': 'long_uptime',
                    'type': 'Довгий час роботи без перезапуску',
                    'description': f'Система працює {uptime_days:.1f} днів без перезапуску',
                    'severity': 'low',
                    'auto_fixable': False  # Перезапуск потребує підтвердження користувача
                })
                
        except Exception as e:
            print(f"Помилка діагностики служб: {e}")
        
        return issues
    
    def auto_fix_issue(self, issue):
        """Автоматичне виправлення проблеми"""
        if not self.auto_fix_enabled:
            return {'success': False, 'message': 'Автоматичне виправлення вимкнено'}
        
        try:
            issue_id = issue.get('id', '')
            issue_type = issue.get('type', '')
            
            # Запис спроби ремонту
            repair_record = {
                'timestamp': datetime.now(),
                'issue_type': issue_type,
                'description': issue.get('description', ''),
                'action_taken': '',
                'success': False,
                'result': ''
            }
            
            result = {'success': False, 'message': 'Невідома проблема'}
            
            # Виправлення конкретних проблем
            if 'high_cpu_usage' in issue_id:
                result = self.fix_high_cpu_usage()
            elif 'high_memory_usage' in issue_id or 'moderate_memory_usage' in issue_id:
                result = self.fix_high_memory_usage()
            elif 'disk_full' in issue_id or 'disk_low_space' in issue_id:
                result = self.fix_disk_space_issues()
            elif 'high_cpu_process' in issue_id or 'high_memory_process' in issue_id:
                result = self.fix_problematic_process(issue.get('process_info'))
            elif 'zombie_processes' in issue_id:
                result = self.fix_zombie_processes()
            elif 'large_temp_files' in issue_id:
                result = self.fix_temp_files()
            elif 'too_many_connections' in issue_id:
                result = self.fix_network_connections()
            elif 'network_errors' in issue_id:
                result = self.fix_network_errors()
            elif 'high_temperature' in issue_id or 'moderate_temperature' in issue_id:
                result = self.fix_temperature_issues()
            elif 'too_many_processes' in issue_id:
                result = self.fix_too_many_processes()
            else:
                result = {'success': False, 'message': f'Автоматичне виправлення для "{issue_type}" не реалізовано'}
            
            # Оновлення запису ремонту
            repair_record['action_taken'] = result.get('action', 'Невідома дія')
            repair_record['success'] = result['success']
            repair_record['result'] = result['message']
            
            self.repair_history.append(repair_record)
            
            return result
            
        except Exception as e:
            return {'success': False, 'message': f'Помилка при автоматичному виправленні: {str(e)}'}
    
    def fix_high_cpu_usage(self):
        """Виправлення високого використання CPU"""
        try:
            # Пошук і завершення процесів з найвищим споживанням CPU
            processes = sorted(
                psutil.process_iter(['pid', 'name', 'cpu_percent']),
                key=lambda p: p.info['cpu_percent'],
                reverse=True
            )
            
            terminated_count = 0
            for proc in processes[:3]:  # Топ 3 процеси
                try:
                    if proc.info['cpu_percent'] > 50 and proc.info['name'] not in ['System', 'kernel', 'init']:
                        proc.terminate()
                        terminated_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if terminated_count > 0:
                return {
                    'success': True,
                    'message': f'Завершено {terminated_count} ресурсомістких процесів',
                    'action': 'Завершення процесів з високим споживанням CPU'
                }
            else:
                return {
                    'success': False,
                    'message': 'Не вдалося завершити жоден процес',
                    'action': 'Спроба завершення ресурсомістких процесів'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка виправлення CPU: {str(e)}',
                'action': 'Виправлення високого використання CPU'
            }
    
    def fix_high_memory_usage(self):
        """Виправлення високого використання пам'яті"""
        try:
            # Спроба звільнення пам'яті
            freed_memory = 0
            
            # Завершення процесів з високим споживанням пам'яті
            processes = sorted(
                psutil.process_iter(['pid', 'name', 'memory_percent', 'memory_info']),
                key=lambda p: p.info['memory_percent'],
                reverse=True
            )
            
            for proc in processes[:5]:  # Топ 5 процесів
                try:
                    if (proc.info['memory_percent'] > 10 and 
                        proc.info['name'] not in ['System', 'kernel', 'init', 'python', 'techcare']):
                        
                        memory_before = proc.info['memory_info'].rss
                        proc.terminate()
                        time.sleep(1)  # Дати час на завершення
                        freed_memory += memory_before
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Очищення кешу (платформо-залежне)
            cache_cleared = self.clear_system_cache()
            
            freed_mb = freed_memory / (1024 * 1024)
            
            if freed_mb > 100 or cache_cleared:
                return {
                    'success': True,
                    'message': f'Звільнено {freed_mb:.1f} MB пам\'яті',
                    'action': 'Завершення ресурсомістких процесів та очищення кешу'
                }
            else:
                return {
                    'success': False,
                    'message': 'Не вдалося значно звільнити пам\'ять',
                    'action': 'Спроба звільнення пам\'яті'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка виправлення пам\'яті: {str(e)}',
                'action': 'Виправлення високого використання пам\'яті'
            }
    
    def fix_disk_space_issues(self):
        """Виправлення проблем з дисковим простором"""
        try:
            freed_space = 0
            
            # Очищення тимчасових файлів
            temp_freed = self.clean_temp_files()
            freed_space += temp_freed
            
            # Очищення кешу браузерів (базове)
            cache_freed = self.clean_browser_cache()
            freed_space += cache_freed
            
            # Очищення системних логів (обережно)
            log_freed = self.clean_system_logs()
            freed_space += log_freed
            
            freed_gb = freed_space / (1024**3)
            
            if freed_gb > 0.1:  # Більше 100MB
                return {
                    'success': True,
                    'message': f'Звільнено {freed_gb:.2f} GB дискового простору',
                    'action': 'Очищення тимчасових файлів та кешу'
                }
            else:
                return {
                    'success': False,
                    'message': 'Не вдалося значно звільнити дисковий простір',
                    'action': 'Спроба очищення дискового простору'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка очищення диска: {str(e)}',
                'action': 'Очищення дискового простору'
            }
    
    def fix_problematic_process(self, process_info):
        """Виправлення проблемного процесу"""
        try:
            if not process_info:
                return {'success': False, 'message': 'Інформація про процес недоступна'}
            
            pid = process_info.get('pid')
            name = process_info.get('name', 'Unknown')
            
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                
                # Очікування завершення
                try:
                    proc.wait(timeout=5)
                except psutil.TimeoutExpired:
                    proc.kill()  # Примусове завершення
                
                return {
                    'success': True,
                    'message': f'Процес {name} (PID: {pid}) успішно завершено',
                    'action': f'Завершення процесу {name}'
                }
                
            except psutil.NoSuchProcess:
                return {
                    'success': True,
                    'message': f'Процес {name} вже завершений',
                    'action': f'Перевірка процесу {name}'
                }
            except psutil.AccessDenied:
                return {
                    'success': False,
                    'message': f'Недостатньо прав для завершення процесу {name}',
                    'action': f'Спроба завершення процесу {name}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка завершення процесу: {str(e)}',
                'action': 'Завершення проблемного процесу'
            }
    
    def fix_zombie_processes(self):
        """Виправлення зависших процесів"""
        try:
            # Пошук і очищення zombie процесів
            zombie_count = 0
            
            for proc in psutil.process_iter():
                try:
                    if proc.status() == psutil.STATUS_ZOMBIE:
                        parent = proc.parent()
                        if parent:
                            parent.send_signal(17)  # SIGCHLD
                        zombie_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if zombie_count > 0:
                return {
                    'success': True,
                    'message': f'Очищено {zombie_count} зависших процесів',
                    'action': 'Очищення zombie процесів'
                }
            else:
                return {
                    'success': True,
                    'message': 'Зависших процесів не знайдено',
                    'action': 'Перевірка zombie процесів'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка очищення зависших процесів: {str(e)}',
                'action': 'Очищення zombie процесів'
            }
    
    def fix_temp_files(self):
        """Очищення тимчасових файлів"""
        try:
            freed_space = self.clean_temp_files()
            freed_gb = freed_space / (1024**3)
            
            return {
                'success': True,
                'message': f'Очищено {freed_gb:.2f} GB тимчасових файлів',
                'action': 'Очищення тимчасових файлів'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка очищення тимчасових файлів: {str(e)}',
                'action': 'Очищення тимчасових файлів'
            }
    
    def fix_network_connections(self):
        """Виправлення проблем з мережевими з'єднаннями"""
        try:
            # Закриття неактивних з'єднань (обмежено можливостями Python)
            connections_before = len(psutil.net_connections())
            
            # Перезапуск мережевих служб (якщо доступно)
            if self.available_tools.get('network_reset'):
                if self.os_type == "Windows":
                    subprocess.run(['netsh', 'winsock', 'reset'], capture_output=True)
                elif self.os_type == "Linux":
                    subprocess.run(['sudo', 'systemctl', 'restart', 'networking'], capture_output=True)
            
            time.sleep(2)  # Дати час на застосування змін
            connections_after = len(psutil.net_connections())
            
            return {
                'success': True,
                'message': f'Кількість з\'єднань: {connections_before} → {connections_after}',
                'action': 'Оптимізація мережевих з\'єднань'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка оптимізації мережі: {str(e)}',
                'action': 'Оптимізація мережевих з\'єднань'
            }
    
    def fix_network_errors(self):
        """Виправлення мережевих помилок"""
        try:
            # Скидання мережевих налаштувань
            if self.os_type == "Windows":
                commands = [
                    ['netsh', 'int', 'ip', 'reset'],
                    ['netsh', 'winsock', 'reset'],
                    ['ipconfig', '/flushdns']
                ]
            elif self.os_type == "Linux":
                commands = [
                    ['sudo', 'systemctl', 'restart', 'networking']
                ]
            else:
                return {
                    'success': False,
                    'message': 'Автоматичне виправлення мережі не підтримується на цій ОС',
                    'action': 'Спроба виправлення мережевих помилок'
                }
            
            executed_commands = 0
            for cmd in commands:
                try:
                    subprocess.run(cmd, capture_output=True, timeout=30)
                    executed_commands += 1
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    continue
            
            if executed_commands > 0:
                return {
                    'success': True,
                    'message': f'Виконано {executed_commands} команд скидання мережі',
                    'action': 'Скидання мережевих налаштувань'
                }
            else:
                return {
                    'success': False,
                    'message': 'Не вдалося виконати команди скидання мережі',
                    'action': 'Спроба скидання мережевих налаштувань'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка виправлення мережевих помилок: {str(e)}',
                'action': 'Виправлення мережевих помилок'
            }
    
    def fix_temperature_issues(self):
        """Виправлення температурних проблем"""
        try:
            actions_taken = []
            
            # Завершення ресурсомістких процесів
            cpu_result = self.fix_high_cpu_usage()
            if cpu_result['success']:
                actions_taken.append('Завершено ресурсомістки процеси')
            
            # Очищення системи для зменшення навантаження
            temp_result = self.fix_temp_files()
            if temp_result['success']:
                actions_taken.append('Очищено тимчасові файли')
            
            if actions_taken:
                return {
                    'success': True,
                    'message': f'Виконано дії для зниження температури: {", ".join(actions_taken)}',
                    'action': 'Зниження температури системи'
                }
            else:
                return {
                    'success': False,
                    'message': 'Рекомендується перевірити систему охолодження вручну',
                    'action': 'Спроба зниження температури'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка виправлення температурних проблем: {str(e)}',
                'action': 'Виправлення температурних проблем'
            }
    
    def fix_too_many_processes(self):
        """Виправлення занадто великої кількості процесів"""
        try:
            # Завершення непотрібних процесів
            terminated_count = 0
            
            # Список процесів, які можна безпечно завершити
            safe_to_terminate = [
                'notepad.exe', 'calc.exe', 'mspaint.exe',  # Windows
                'gedit', 'calculator', 'simple-scan'       # Linux
            ]
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() in [p.lower() for p in safe_to_terminate]:
                        proc.terminate()
                        terminated_count += 1
                        
                        if terminated_count >= 5:  # Обмеження на безпеку
                            break
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if terminated_count > 0:
                return {
                    'success': True,
                    'message': f'Завершено {terminated_count} непотрібних процесів',
                    'action': 'Оптимізація кількості процесів'
                }
            else:
                return {
                    'success': False,
                    'message': 'Не знайдено безпечних для завершення процесів',
                    'action': 'Спроба оптимізації процесів'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка оптимізації процесів: {str(e)}',
                'action': 'Оптимізація кількості процесів'
            }
    
    # Допоміжні методи
    def calculate_temp_files_size(self):
        """Розрахунок розміру тимчасових файлів"""
        try:
            temp_dirs = [tempfile.gettempdir()]
            
            # Додавання інших тимчасових директорій
            if self.os_type == "Windows":
                temp_dirs.extend([
                    os.path.expandvars('%TEMP%'),
                    os.path.expandvars('%TMP%'),
                    os.path.expandvars('%LOCALAPPDATA%\\Temp')
                ])
            
            total_size = 0
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    total_size += self.get_directory_size(temp_dir)
            
            return total_size
        except Exception as e:
            print(f"Помилка розрахунку розміру тимчасових файлів: {e}")
            return 0
    
    def get_directory_size(self, directory):
        """Отримання розміру директорії"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    try:
                        filepath = os.path.join(dirpath, filename)
                        total_size += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        continue
        except Exception as e:
            print(f"Помилка розрахунку розміру директорії {directory}: {e}")
        
        return total_size
    
    def clean_temp_files(self):
        """Очищення тимчасових файлів"""
        try:
            freed_space = 0
            temp_dirs = [tempfile.gettempdir()]
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isfile(item_path):
                                size = os.path.getsize(item_path)
                                os.remove(item_path)
                                freed_space += size
                            elif os.path.isdir(item_path):
                                size = self.get_directory_size(item_path)
                                shutil.rmtree(item_path)
                                freed_space += size
                        except (OSError, PermissionError):
                            continue
            
            return freed_space
        except Exception as e:
            print(f"Помилка очищення тимчасових файлів: {e}")
            return 0
    
    def clear_system_cache(self):
        """Очищення системного кешу"""
        try:
            if self.os_type == "Linux":
                # Очищення кешу на Linux
                subprocess.run(['sync'], capture_output=True)
                with open('/proc/sys/vm/drop_caches', 'w') as f:
                    f.write('3')
                return True
            elif self.os_type == "Windows":
                # На Windows це складніше - можна спробувати очистити DNS кеш
                subprocess.run(['ipconfig', '/flushdns'], capture_output=True)
                return True
        except Exception as e:
            print(f"Помилка очищення кешу: {e}")
        
        return False
    
    def clean_browser_cache(self):
        """Очищення кешу браузерів (базове)"""
        # Спрощена реалізація - в реальності потрібен більш детальний підхід
        try:
            freed_space = 0
            
            # Можливі директорії кешу браузерів
            cache_paths = []
            
            if self.os_type == "Windows":
                user_profile = os.path.expanduser('~')
                cache_paths.extend([
                    os.path.join(user_profile, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
                    os.path.join(user_profile, 'AppData', 'Local', 'Mozilla', 'Firefox', 'Profiles'),
                ])
            elif self.os_type == "Linux":
                user_home = os.path.expanduser('~')
                cache_paths.extend([
                    os.path.join(user_home, '.cache', 'google-chrome'),
                    os.path.join(user_home, '.cache', 'mozilla'),
                ])
            
            for cache_path in cache_paths:
                if os.path.exists(cache_path):
                    try:
                        size_before = self.get_directory_size(cache_path)
                        # Обережне очищення - тільки файли кешу
                        for root, dirs, files in os.walk(cache_path):
                            for file in files:
                                if any(file.endswith(ext) for ext in ['.cache', '.tmp', '.temp']):
                                    try:
                                        file_path = os.path.join(root, file)
                                        os.remove(file_path)
                                    except (OSError, PermissionError):
                                        continue
                        
                        size_after = self.get_directory_size(cache_path)
                        freed_space += (size_before - size_after)
                    except Exception:
                        continue
            
            return freed_space
        except Exception as e:
            print(f"Помилка очищення кешу браузерів: {e}")
            return 0
    
    def clean_system_logs(self):
        """Очищення системних логів (обережно)"""
        try:
            freed_space = 0
            
            if self.os_type == "Linux":
                log_dirs = ['/var/log', '/tmp']
                for log_dir in log_dirs:
                    if os.path.exists(log_dir):
                        try:
                            # Очищення тільки старих log файлів
                            for root, dirs, files in os.walk(log_dir):
                                for file in files:
                                    if file.endswith('.log') or file.endswith('.log.1'):
                                        try:
                                            file_path = os.path.join(root, file)
                                            # Перевірка віку файлу
                                            file_age = time.time() - os.path.getmtime(file_path)
                                            if file_age > 7 * 24 * 3600:  # Старший за тиждень
                                                size = os.path.getsize(file_path)
                                                os.remove(file_path)
                                                freed_space += size
                                        except (OSError, PermissionError):
                                            continue
                        except Exception:
                            continue
            
            return freed_space
        except Exception as e:
            print(f"Помилка очищення системних логів: {e}")
            return 0
    
    def get_repair_history(self):
        """Отримання історії ремонтів"""
        return self.repair_history
    
    def set_auto_fix_enabled(self, enabled):
        """Встановлення статусу автоматичного виправлення"""
        self.auto_fix_enabled = enabled
    
    def apply_recommendation(self, recommendation):
        """Застосування рекомендації"""
        try:
            # Створення фейкової проблеми на основі рекомендації
            fake_issue = {
                'id': 'recommendation_' + recommendation.get('title', '').lower().replace(' ', '_'),
                'type': recommendation.get('title', 'Рекомендація'),
                'description': recommendation.get('description', ''),
                'severity': recommendation.get('priority', 'medium'),
                'auto_fixable': recommendation.get('auto_applicable', False)
            }
            
            return self.auto_fix_issue(fake_issue)
        except Exception as e:
            return {
                'success': False,
                'message': f'Помилка застосування рекомендації: {str(e)}'
            }
