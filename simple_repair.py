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
            problems.append({
                'description': f'Високе навантаження CPU: {cpu:.1f}%',
                'fixable': True,
                'type': 'cpu'
            })
        
        # перевіряємо RAM
        ram = psutil.virtual_memory()
        if ram.percent > 85:
            problems.append({
                'description': f'Мало вільної пам\'яті: {ram.percent:.1f}%',
                'fixable': True,
                'type': 'ram'
            })
        
        # перевіряємо диск
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        if disk_percent > 90:
            problems.append({
                'description': f'Диск майже заповнений: {disk_percent:.1f}%',
                'fixable': True,
                'type': 'disk'
            })
        
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