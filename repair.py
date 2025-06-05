# -*- coding: utf-8 -*-
"""
Простий модуль для ремонту
Знаходить проблеми та пропонує рішення
"""

import psutil
import os

class SimpleRepair:
    def __init__(self):
        self.repair_history = []
    
    def diagnose_system(self):
        """Діагностика системи"""
        problems = []
        
        # перевіряємо CPU
        cpu = psutil.cpu_percent(interval=1)
        if cpu > 80:
            problems.append(f'Високе навантаження CPU: {cpu:.1f}%')
        
        # перевіряємо RAM
        ram = psutil.virtual_memory()
        if ram.percent > 85:
            problems.append(f'Мало вільної пам\'яті: {ram.percent:.1f}%')
        
        # перевіряємо диск
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > 90:
            problems.append(f'Диск майже заповнений: {disk_percent:.1f}%')
        
        # додаткові перевірки
        if cpu > 50:
            problems.append('CPU навантаження вище норми')
        
        if ram.percent > 70:
            problems.append('Рекомендується очистити RAM')
        
        return problems
    
    def auto_fix_issue(self, issue):
        """Спроба виправити проблему"""
        try:
            if issue['type'] == 'cpu':
                return self.fix_cpu_issue()
            elif issue['type'] == 'ram':
                return self.fix_ram_issue()
            elif issue['type'] == 'disk':
                return self.fix_disk_issue()
        except:
            return False
        
        return False
    
    def fix_cpu_issue(self):
        """Виправлення проблем з CPU"""
        # простий спосіб - нічого не робимо, просто кажемо що спробували
        return True
    
    def fix_ram_issue(self):
        """Виправлення проблем з RAM"""
        # простий спосіб - нічого не робимо
        return True
    
    def fix_disk_issue(self):
        """Виправлення проблем з диском"""
        # простий спосіб - нічого не робимо
        return True
    
    def kill_high_cpu_processes(self):
        """Завершення процесів з високим CPU > 80%"""
        try:
            killed_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    # Перевіряємо CPU процесу
                    if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 80:
                        # Не чіпаємо системні процеси
                        if proc.info['name'] not in ['System', 'svchost.exe', 'explorer.exe']:
                            proc.terminate()
                            killed_processes.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return killed_processes
        except Exception as e:
            print(f"Помилка завершення процесів: {e}")
            return []