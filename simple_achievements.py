# -*- coding: utf-8 -*-
"""
Система досягнень як в іграх
Прості очки та рівні
"""

class SimpleAchievements:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def get_user_level(self, total_points):
        """Рахує рівень за очками"""
        level = (total_points // 100) + 1
        return min(level, 50)  # максимум 50 рівень
    
    def add_points(self, points, reason=""):
        """Додає очки користувачу"""
        try:
            self.data_manager.save_user_activity("points", points, reason)
            return True
        except:
            return False