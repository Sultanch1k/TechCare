# -*- coding: utf-8 -*-
"""
TechCare - Reminder Module
Модуль для перевірки порогових значень та генерації нагадувань
"""

import time
import schedule
from datetime import datetime, timedelta

def check_thresholds(data, thresholds, state):
    """
    Перевіряє порогові значення та генерує попередження
    
    Args:
        data: Словник з системними даними
        thresholds: Словник з пороговими значеннями
        state: Словник стану для відстеження часу
    
    Returns:
        List: Список попереджень
    """
    warnings = []
    current_time = time.time()
    
    # Перевірка відкладення
    if state.get('delay_until', 0) > current_time:
        return warnings
    
    # Перевірка температури CPU або використання CPU
    temp_threshold_exceeded = False
    if data.get('cpu_temp') is not None:
        temp_threshold_exceeded = data['cpu_temp'] > thresholds.get('cpu_temp', 70)
    else:
        # Використовуємо CPU usage як заміну температури
        temp_threshold_exceeded = data['cpu_percent'] > thresholds.get('cpu_usage', 80)
    
    if temp_threshold_exceeded:
        if state.get('high_temp_time', 0) == 0:
            state['high_temp_time'] = current_time
        elif current_time - state['high_temp_time'] >= 1800:  # 30 хвилин
            warnings.append("Охолодіть систему! Можливо, потрібна чистка пилу")
    else:
        state['high_temp_time'] = 0
    
    # Перевірка використання RAM
    if data['ram_percent'] > thresholds.get('ram_usage', 90):
        if state.get('high_ram_time', 0) == 0:
            state['high_ram_time'] = current_time
        elif current_time - state['high_ram_time'] >= 900:  # 15 хвилин
            warnings.append("Закрийте непотрібні програми або перезапустіть систему")
    else:
        state['high_ram_time'] = 0
    
    # Перевірка використання диска (миттєве попередження)
    if data['disk_percent'] > thresholds.get('disk_usage', 90):
        warnings.append("Диск майже повний! Очистіть непотрібні файли")
    
    # Перевірка часу роботи системи
    if data['uptime_seconds'] > thresholds.get('uptime_restart', 86400):  # 24 години
        warnings.append("Рекомендуємо перезапустити систему для стабільності")
    
    # Перевірка швидкості вентилятора та температури
    if data.get('fan_speed') is not None:
        # Припускаємо, що швидкість вище 4000 RPM є високою
        if data['fan_speed'] > 4000 or temp_threshold_exceeded:
            warnings.append("Перевірте охолодження!")
    elif temp_threshold_exceeded:
        warnings.append("Перевірте охолодження!")
    
    return warnings

def schedule_reminders(data_func, thresholds, callback):
    """
    Планує регулярні перевірки нагадувань
    
    Args:
        data_func: Функція для отримання системних даних
        thresholds: Порогові значення
        callback: Функція зворотного виклику для обробки попереджень
    """
    def check_and_notify():
        try:
            data = data_func()
            warnings = check_thresholds(data, thresholds, callback.state)
            if warnings:
                callback(warnings, data)
        except Exception as e:
            print(f"Помилка при перевірці нагадувань: {e}")
    
    # Планування перевірки кожні 10 секунд
    schedule.every(10).seconds.do(check_and_notify)
    
    return check_and_notify

def clear_state(state):
    """Очищає стан лічильників"""
    state['high_temp_time'] = 0
    state['high_ram_time'] = 0
    return "Лічильники очищено"

def postpone_reminders(state, minutes=30):
    """Відкладає нагадування на вказану кількість хвилин"""
    state['delay_until'] = time.time() + (minutes * 60)
    return f"Нагадування відкладено на {minutes} хвилин"

def get_status_summary(data, thresholds, state):
    """
    Повертає короткий статус системи
    
    Returns:
        tuple: (статус, колір)
    """
    current_time = time.time()
    
    # Перевірка відкладення
    if state.get('delay_until', 0) > current_time:
        remaining = int((state['delay_until'] - current_time) / 60)
        return f"Нагадування відкладено ({remaining} хв)", "#FFFF99"
    
    warnings = check_thresholds(data, thresholds, state.copy())
    
    if warnings:
        return f"Виявлено {len(warnings)} проблем(а)", "#FF6347"
    else:
        return "Усе в нормі", "#00FF66"

def get_detailed_history(state):
    """Повертає детальну історію стану системи"""
    history = []
    current_time = time.time()
    
    if state.get('high_temp_time', 0) > 0:
        duration = int((current_time - state['high_temp_time']) / 60)
        history.append(f"Температура висока протягом {duration} хвилин")
    
    if state.get('high_ram_time', 0) > 0:
        duration = int((current_time - state['high_ram_time']) / 60)
        history.append(f"RAM перевантажена протягом {duration} хвилин")
    
    if state.get('delay_until', 0) > current_time:
        remaining = int((state['delay_until'] - current_time) / 60)
        history.append(f"Нагадування відкладено ще на {remaining} хвилин")
    
    if not history:
        history.append("Немає активних проблем")
    
    return history

if __name__ == "__main__":
    # Тестування модуля
    from monitor import get_system_data
    
    thresholds = {
        'cpu_temp': 70,
        'cpu_usage': 80,
        'ram_usage': 90,
        'disk_usage': 90,
        'uptime_restart': 86400
    }
    
    state = {
        'high_temp_time': 0,
        'high_ram_time': 0,
        'delay_until': 0
    }
    
    data = get_system_data()
    warnings = check_thresholds(data, thresholds, state)
    print("Попередження:", warnings)
    print("Статус:", get_status_summary(data, thresholds, state))
