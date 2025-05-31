#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Стартовий файл
Просто запускає програму
"""

import sys
import os

# Додаємо поточну папку до шляху
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import main
    
    if __name__ == "__main__":
        print("🛡️ Запускаю SystemWatch Pro...")
        print("Відкрий браузер на http://localhost:5000")
        main()
        
except ImportError as e:
    print(f"Помилка: не можу знайти модуль {e}")
    print("Перевір що всі файли на місці")
except Exception as e:
    print(f"Щось пішло не так: {e}")
    print("Спробуй ще раз або подивись логи")