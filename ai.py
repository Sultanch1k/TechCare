# -*- coding: utf-8 -*-
"""
Простий AI для аналізу системи
Написав сам, без складних алгоритмів
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
        
        # Температура > 70°C або CPU > 80% протягом 30 хвилин
        temperature = data.get('temperature', 45)
        if temperature is None:
            temperature = 45
        temp_high = temperature > 70 or data['cpu_percent'] > 80
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
        
        # рахуємо індекс здоров'я з температурою
        health_score = 100
        health_score -= data['cpu_percent'] * 0.2
        health_score -= data['ram_percent'] * 0.3  
        health_score -= data['disk_percent'] * 0.2
        # Враховуємо температуру
        temp = data.get('temperature', 45)
        if temp is None:
            temp = 45
        if temp > 70:
            health_score -= 20
        elif temp > 60:
            health_score -= 10
        health_score = max(0, int(health_score))
        
        predictions = []
        if health_score < 50:
            predictions.append("Система потребує уваги")
        elif health_score < 70:
            predictions.append("Можливі проблеми в майбутньому")
        else:
            predictions.append("Система працює добре")
        
        return {
            'warnings': warnings,
            'health_score': health_score,
            'predictions': predictions
        }