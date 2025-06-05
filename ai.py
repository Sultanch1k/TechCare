# -*- coding: utf-8 -*-
"""
мій простий штучний інтелект для аналізу
зробив сам без готових бібліотек машинного навчання
"""

class SimpleAI:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        # Стан для лічильників часу
        self.state = {
            'high_temp_start': None,
            'high_ram_start': None,
            'last_check': None
        }
    
    def predict_system_health(self, data):
        """Прогнозує здоров'я системи з часовими лічильниками"""
        import time
        warnings = []
        current_time = time.time()
        
        # Температура > 85°C або CPU > 80% протягом 30 хвилин
        temperature = data.get('temperature', 45)
        if temperature is None:
            temperature = 45
        temp_high = temperature > 85 or data['cpu_percent'] > 80
        if temp_high:
            if self.state['high_temp_start'] is None:
                self.state['high_temp_start'] = current_time
            elif (current_time - self.state['high_temp_start']) > 1800:  # 30 хвилин
                warnings.append("Охолодіть систему! Висока температура більше 30 хвилин")
        else:
            self.state['high_temp_start'] = None
        
        # RAM > 90% протягом 15 хвилин
        if data['ram_percent'] > 90:
            if self.state['high_ram_start'] is None:
                self.state['high_ram_start'] = current_time
            elif (current_time - self.state['high_ram_start']) > 900:  # 15 хвилин
                warnings.append("Закрийте програми або перезапустіть! Пам'ять переповнена")
        else:
            self.state['high_ram_start'] = None
        
        # Диск > 90%
        if data['disk_percent'] > 90:
            warnings.append("Очистіть файли! Диск майже заповнений")
        
        # Час роботи > 24 години
        if data.get('uptime_hours', 0) > 24:
            warnings.append("Перезапустіть для стабільності! Система працює більше доби")
        
        # Звичайні перевірки
        if data['cpu_percent'] > 80:
            warnings.append("Процесор сильно навантажений")
        
        if data['ram_percent'] > 85:
            warnings.append("Мало вільної пам'яті")
        
        # Прагматичний розрахунок індексу здоров'я системи
        health_score = 100
        
        # CPU: більш м'які пороги
        cpu_usage = data['cpu_percent']
        if cpu_usage < 20:
            cpu_penalty = 0
        elif cpu_usage < 50:
            cpu_penalty = (cpu_usage - 20) * 0.1  # невелика зниження
        elif cpu_usage < 80:
            cpu_penalty = 3 + (cpu_usage - 50) * 0.2  # помірне зниження
        else:
            cpu_penalty = 9 + (cpu_usage - 80) * 0.4  # значне зниження
        
        # RAM: враховуємо що 70-80% це нормально
        ram_usage = data['ram_percent']
        if ram_usage < 50:
            ram_penalty = 0
        elif ram_usage < 75:
            ram_penalty = (ram_usage - 50) * 0.08
        elif ram_usage < 90:
            ram_penalty = 2 + (ram_usage - 75) * 0.3
        else:
            ram_penalty = 6.5 + (ram_usage - 90) * 0.5
        
        # Диск: менше критично ніж RAM/CPU
        disk_usage = data['disk_percent']
        if disk_usage < 60:
            disk_penalty = 0
        elif disk_usage < 85:
            disk_penalty = (disk_usage - 60) * 0.05
        else:
            disk_penalty = 1.25 + (disk_usage - 85) * 0.2
        
        # Температура: реалістичніші пороги
        temp = data.get('temperature', 45)
        if temp is None:
            temp = 45
        if temp > 85:
            temp_penalty = 15  # критично
        elif temp > 75:
            temp_penalty = 8   # високо
        elif temp > 65:
            temp_penalty = 3   # тепло
        else:
            temp_penalty = 0   # нормально
        
        health_score -= cpu_penalty + ram_penalty + disk_penalty + temp_penalty
        health_score = max(15, min(100, int(health_score)))  # мінімум 15%, максимум 100%
        
        # Прогнозування майбутніх проблем на основі історії
        predictions = self._predict_future_issues(data)
        
        return {
            'warnings': warnings,
            'health_score': health_score,
            'predictions': predictions
        }
    
    def _predict_future_issues(self, current_data):
        """Прогнозування майбутніх проблем на основі поточних тенденцій"""
        predictions = []
        
        # Отримуємо історичні дані для аналізу тенденцій
        try:
            historical_data = self.data_manager.get_historical_data(days=3)
            
            if len(historical_data) >= 5:
                # Аналізуємо тренди CPU
                cpu_values = [float(d.get('cpu_percent', 0)) for d in historical_data[-5:]]
                cpu_trend = sum(cpu_values[-3:]) / 3 - sum(cpu_values[:2]) / 2
                
                if cpu_trend > 10:
                    predictions.append("📈 CPU навантаження зростає - можливі проблеми через 2-3 години")
                
                # Аналізуємо тренди RAM
                ram_values = [float(d.get('ram_percent', 0)) for d in historical_data[-5:]]
                ram_trend = sum(ram_values[-3:]) / 3 - sum(ram_values[:2]) / 2
                
                if ram_trend > 15:
                    predictions.append("📈 Пам'ять заповнюється - рекомендується перезавантаження протягом дня")
                
                # Аналізуємо температуру
                temp_values = [float(d.get('temperature', 40)) for d in historical_data[-5:]]
                avg_temp = sum(temp_values) / len(temp_values)
                
                if avg_temp > 60:
                    predictions.append("🌡️ Температура підвищена останні дні - перевірте охолодження")
        except:
            pass
        
        # Базові прогнози на основі поточного стану
        current_cpu = current_data['cpu_percent']
        current_ram = current_data['ram_percent']
        current_disk = current_data['disk_percent']
        
        if current_cpu > 70 and current_ram > 70:
            predictions.append("⚠️ Високе навантаження системи - можливі зависання")
        
        if current_disk > 95:
            predictions.append("💾 Диск майже заповнений - система може стати нестабільною")
        
        if current_ram > 90:
            predictions.append("🔄 Пам'ять критично мало - рекомендується перезавантаження")
        
        # Прогноз на майбутнє
        uptime = current_data.get('uptime_hours', 0)
        if uptime > 48:
            predictions.append("⏰ Система працює довго - рекомендується перезавантаження для стабільності")
        
        if not predictions:
            health_score = 100 - (current_cpu * 0.2 + current_ram * 0.3 + current_disk * 0.2)
            if health_score > 80:
                predictions.append("✅ Система працює стабільно - проблеми не прогнозуються")
            else:
                predictions.append("📊 Рекомендується моніторинг показників")
        
        return predictions