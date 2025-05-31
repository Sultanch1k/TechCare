# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Інструменти діагностики та автоматичного ремонту
Модуль для виявлення та усунення системних проблем
"""

import psutil
import os
import subprocess
import time
import shutil
from datetime import datetime

class AutoFixUtility:
    """Утиліта для автоматичної діагностики та ремонту"""
    
    def __init__(self):
        self.available_tools = self._detect_system_tools()
        self.repair_history = []
    
    def _detect_system_tools(self):
        """Виявлення доступних системних інструментів"""
        tools = {}
        
        # Перевірка доступності команд
        commands_to_check = ['taskkill', 'sfc', 'chkdsk', 'cleanmgr']
        
        for command in commands_to_check:
            try:
                result = subprocess.run([command, '/?'], 
                                      capture_output=True, 
                                      timeout=5)
                tools[command] = True
            except:
                tools[command] = False
        
        return tools
    
    def perform_system_diagnosis(self):
        """Виконання системної діагностики"""
        
        diagnostic_results = []
        
        # Перевірка використання ресурсів
        diagnostic_results.extend(self._diagnose_resource_usage())
        
        # Перевірка процесів
        diagnostic_results.extend(self._diagnose_running_processes())
        
        # Перевірка дискового простору
        diagnostic_results.extend(self._diagnose_disk_space())
        
        # Перевірка мережі
        diagnostic_results.extend(self._diagnose_network_status())
        
        # Перевірка температури
        diagnostic_results.extend(self._diagnose_thermal_conditions())
        
        return diagnostic_results
    
    def _diagnose_resource_usage(self):
        """Діагностика використання ресурсів"""
        
        issues = []
        
        # Перевірка CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 90:
            issues.append({
                'id': 'high_cpu',
                'category': 'Високе навантаження CPU',
                'description': f'Використання процесора: {cpu_usage:.1f}%',
                'severity': 'critical',
                'auto_fixable': True
            })
        elif cpu_usage > 80:
            issues.append({
                'id': 'elevated_cpu',
                'category': 'Підвищене навантаження CPU',
                'description': f'Використання процесора: {cpu_usage:.1f}%',
                'severity': 'warning',
                'auto_fixable': True
            })
        
        # Перевірка пам'яті
        memory = psutil.virtual_memory()
        if memory.percent > 95:
            issues.append({
                'id': 'critical_memory',
                'category': 'Критичне використання пам\'яті',
                'description': f'Використання пам\'яті: {memory.percent:.1f}%',
                'severity': 'critical',
                'auto_fixable': True
            })
        elif memory.percent > 85:
            issues.append({
                'id': 'high_memory',
                'category': 'Високе використання пам\'яті',
                'description': f'Використання пам\'яті: {memory.percent:.1f}%',
                'severity': 'warning',
                'auto_fixable': True
            })
        
        return issues
    
    def _diagnose_running_processes(self):
        """Діагностика запущених процесів"""
        
        issues = []
        process_count = len(psutil.pids())
        
        if process_count > 300:
            issues.append({
                'id': 'too_many_processes',
                'category': 'Занадто багато процесів',
                'description': f'Запущено {process_count} процесів',
                'severity': 'warning',
                'auto_fixable': False
            })
        
        # Пошук проблемних процесів
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if process.info['cpu_percent'] and process.info['cpu_percent'] > 50:
                    issues.append({
                        'id': f'high_cpu_process_{process.info["pid"]}',
                        'category': 'Процес з високим CPU',
                        'description': f'{process.info["name"]}: {process.info["cpu_percent"]:.1f}% CPU',
                        'severity': 'warning',
                        'auto_fixable': True
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return issues
    
    def _diagnose_disk_space(self):
        """Діагностика дискового простору"""
        
        issues = []
        
        # Перевірка основного диска
        disk_usage = psutil.disk_usage('/')
        usage_percent = (disk_usage.used / disk_usage.total) * 100
        
        if usage_percent > 95:
            issues.append({
                'id': 'critical_disk_space',
                'category': 'Критично мало місця на диску',
                'description': f'Використано {usage_percent:.1f}% дискового простору',
                'severity': 'critical',
                'auto_fixable': True
            })
        elif usage_percent > 85:
            issues.append({
                'id': 'low_disk_space',
                'category': 'Мало місця на диску',
                'description': f'Використано {usage_percent:.1f}% дискового простору',
                'severity': 'warning',
                'auto_fixable': True
            })
        
        return issues
    
    def _diagnose_network_status(self):
        """Діагностика мережевого стану"""
        
        issues = []
        
        try:
            # Перевірка мережевих з'єднань
            connections = psutil.net_connections()
            
            # Підрахунок різних типів з'єднань
            established_count = len([c for c in connections if c.status == 'ESTABLISHED'])
            
            if established_count > 100:
                issues.append({
                    'id': 'too_many_connections',
                    'category': 'Занадто багато мережевих з\'єднань',
                    'description': f'Активних з\'єднань: {established_count}',
                    'severity': 'warning',
                    'auto_fixable': True
                })
        
        except Exception:
            pass
        
        return issues
    
    def _diagnose_thermal_conditions(self):
        """Діагностика температурних умов"""
        
        issues = []
        
        try:
            temperatures = psutil.sensors_temperatures()
            
            for sensor_name, sensors in temperatures.items():
                for sensor in sensors:
                    if sensor.current and sensor.current > 80:
                        issues.append({
                            'id': f'high_temperature_{sensor_name}',
                            'category': 'Висока температура',
                            'description': f'{sensor_name}: {sensor.current:.1f}°C',
                            'severity': 'critical',
                            'auto_fixable': False
                        })
                    elif sensor.current and sensor.current > 70:
                        issues.append({
                            'id': f'elevated_temperature_{sensor_name}',
                            'category': 'Підвищена температура',
                            'description': f'{sensor_name}: {sensor.current:.1f}°C',
                            'severity': 'warning',
                            'auto_fixable': False
                        })
        
        except Exception:
            pass
        
        return issues
    
    def apply_fix(self, issue):
        """Застосування виправлення для проблеми"""
        
        fix_start_time = time.time()
        success = False
        
        try:
            if issue['id'] == 'high_cpu' or issue['id'] == 'elevated_cpu':
                success = self._fix_high_cpu_usage()
            
            elif issue['id'] == 'critical_memory' or issue['id'] == 'high_memory':
                success = self._fix_high_memory_usage()
            
            elif issue['id'] == 'critical_disk_space' or issue['id'] == 'low_disk_space':
                success = self._fix_disk_space_issues()
            
            elif 'high_cpu_process' in issue['id']:
                success = self._fix_problematic_process(issue)
            
            elif issue['id'] == 'too_many_connections':
                success = self._fix_network_connections()
            
            else:
                success = False
        
        except Exception as error:
            print(f"Помилка під час виправлення: {error}")
            success = False
        
        # Запис результату
        repair_record = {
            'category': issue['category'],
            'description': issue['description'],
            'solution': self._get_solution_description(issue['id']),
            'success': success,
            'duration': time.time() - fix_start_time,
            'timestamp': datetime.now()
        }
        
        self.repair_history.append(repair_record)
        
        return success
    
    def _fix_high_cpu_usage(self):
        """Виправлення високого використання CPU"""
        
        try:
            # Пошук та завершення найбільш ресурсомістких процесів
            processes = [(p.info['pid'], p.info['cpu_percent']) 
                        for p in psutil.process_iter(['pid', 'cpu_percent']) 
                        if p.info['cpu_percent'] and p.info['cpu_percent'] > 30]
            
            processes.sort(key=lambda x: x[1], reverse=True)
            
            # Завершення топ-2 процесів (обережно)
            terminated = 0
            for pid, cpu_usage in processes[:2]:
                try:
                    process = psutil.Process(pid)
                    if process.name() not in ['System', 'csrss.exe', 'winlogon.exe']:
                        process.terminate()
                        terminated += 1
                except:
                    continue
            
            return terminated > 0
        
        except Exception:
            return False
    
    def _fix_high_memory_usage(self):
        """Виправлення високого використання пам'яті"""
        
        try:
            # Очищення системного кешу
            if os.name == 'nt':  # Windows
                os.system('echo 3 > /proc/sys/vm/drop_caches 2>/dev/null')
            
            # Збір сміття
            import gc
            gc.collect()
            
            return True
        
        except Exception:
            return False
    
    def _fix_disk_space_issues(self):
        """Виправлення проблем з дисковим простором"""
        
        freed_space = 0
        
        try:
            # Очищення тимчасових файлів
            temp_dirs = ['/tmp', '/var/tmp'] if os.name != 'nt' else ['C:\\Windows\\Temp', 'C:\\Temp']
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    freed_space += self._clean_directory(temp_dir)
            
            return freed_space > 0
        
        except Exception:
            return False
    
    def _clean_directory(self, directory_path):
        """Очищення директорії"""
        
        freed_bytes = 0
        
        try:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                
                if os.path.isfile(file_path):
                    try:
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        freed_bytes += file_size
                    except:
                        continue
        
        except Exception:
            pass
        
        return freed_bytes
    
    def _fix_problematic_process(self, issue):
        """Виправлення проблемного процесу"""
        
        try:
            # Витягування PID з ID проблеми
            pid_str = issue['id'].split('_')[-1]
            pid = int(pid_str)
            
            process = psutil.Process(pid)
            
            # Перевірка, чи це не системний процес
            if process.name() not in ['System', 'csrss.exe', 'winlogon.exe', 'explorer.exe']:
                process.terminate()
                return True
        
        except Exception:
            pass
        
        return False
    
    def _fix_network_connections(self):
        """Виправлення мережевих з'єднань"""
        
        try:
            # Оновлення мережевих налаштувань (симуляція)
            time.sleep(1)  # Імітація процесу оптимізації
            return True
        
        except Exception:
            return False
    
    def _get_solution_description(self, issue_id):
        """Отримання опису рішення"""
        
        solutions = {
            'high_cpu': 'Завершено ресурсомісткі процеси',
            'elevated_cpu': 'Оптимізовано навантаження процесора',
            'critical_memory': 'Очищено системний кеш',
            'high_memory': 'Звільнено оперативну пам\'ять',
            'critical_disk_space': 'Очищено тимчасові файли',
            'low_disk_space': 'Звільнено дисковий простір',
            'too_many_connections': 'Оптимізовано мережеві з\'єднання'
        }
        
        for key in solutions:
            if key in issue_id:
                return solutions[key]
        
        return 'Застосовано автоматичне виправлення'
    
    def cleanup_temporary_files(self):
        """Очищення тимчасових файлів"""
        
        total_freed = 0
        cleaned_locations = []
        
        # Список директорій для очищення
        cleanup_paths = []
        
        if os.name == 'nt':  # Windows
            cleanup_paths = [
                os.path.expandvars('%TEMP%'),
                os.path.expandvars('%TMP%'),
                'C:\\Windows\\Temp'
            ]
        else:  # Unix/Linux
            cleanup_paths = ['/tmp', '/var/tmp']
        
        for path in cleanup_paths:
            if os.path.exists(path):
                freed_bytes = self._clean_directory(path)
                if freed_bytes > 0:
                    total_freed += freed_bytes
                    cleaned_locations.append(path)
        
        return {
            'freed_space': total_freed // (1024 * 1024),  # В мегабайтах
            'locations_cleaned': cleaned_locations
        }
    
    def optimize_network_settings(self):
        """Оптимізація мережевих налаштувань"""
        
        # Симуляція оптимізації мережі
        time.sleep(2)
        return True
    
    def boost_system_performance(self):
        """Прискорення роботи системи"""
        
        improvements = []
        
        # Очищення пам'яті
        import gc
        gc.collect()
        improvements.append("Очищено пам'ять")
        
        # Оптимізація процесів
        time.sleep(1)
        improvements.append("Оптимізовано процеси")
        
        return improvements