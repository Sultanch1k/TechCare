# -*- coding: utf-8 -*-
"""
Простий AI для аналізу системи
Написав сам, без складних алгоритмів
"""

class SimpleAI:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def predict_system_health(self, data):
        """Прогнозує здоров'я системи"""
        warnings = []
        
        # прості перевірки
        if data['cpu_percent'] > 80:
            warnings.append("Процесор сильно навантажений")
        
        if data['ram_percent'] > 85:
            warnings.append("Мало вільної пам'яті")
        
        if data['disk_percent'] > 90:
            warnings.append("Диск майже заповнений")
        
        # рахуємо індекс здоров'я
        health_score = 100
        health_score -= data['cpu_percent'] * 0.3
        health_score -= data['ram_percent'] * 0.4  
        health_score -= data['disk_percent'] * 0.3
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