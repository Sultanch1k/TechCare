# -*- coding: utf-8 -*-
"""
Система досягнень як в іграх
Прості очки та рівні
"""

class SimpleAchievements:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.achievements_list = {
            'first_start': {'name': 'Перший запуск', 'description': 'Запустили TechCare вперше', 'points': 10},
            'diagnostic_master': {'name': 'Майстер діагностики', 'description': 'Зробили 10 діагностик', 'points': 25},
            'cleanup_master': {'name': 'Майстер очищення', 'description': 'Виконали 5 ремонтів', 'points': 30},
            'speed_tester': {'name': 'Тестувальник швидкості', 'description': 'Пройшли всі тести', 'points': 20},
            'health_guardian': {'name': 'Охоронець здоров\'я', 'description': 'Підтримували здоров\'я системи на 80%+', 'points': 40}
        }
    
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
    
    def check_achievements(self, user_stats):
        """Перевіряє нові досягнення"""
        new_achievements = []
        
        # Перевірка досягнення "Майстер очищення"
        repairs_count = user_stats.get('repairs_done', 0)
        if repairs_count >= 5 and not self.is_achievement_unlocked('cleanup_master'):
            new_achievements.append('cleanup_master')
            self.unlock_achievement('cleanup_master')
        
        # Перевірка інших досягнень
        diagnostics_count = user_stats.get('diagnostics_done', 0)
        if diagnostics_count >= 10 and not self.is_achievement_unlocked('diagnostic_master'):
            new_achievements.append('diagnostic_master')
            self.unlock_achievement('diagnostic_master')
        
        return new_achievements
    
    def unlock_achievement(self, achievement_id):
        """Відкриває досягнення"""
        try:
            achievement = self.achievements_list.get(achievement_id)
            if achievement:
                self.data_manager.unlock_achievement(achievement_id)
                self.add_points(achievement['points'], f"Досягнення: {achievement['name']}")
                return True
        except:
            pass
        return False
    
    def is_achievement_unlocked(self, achievement_id):
        """Перевіряє чи відкрите досягнення"""
        try:
            # Тут має бути запит до бази даних
            return False  # Поки що повертаємо False
        except:
            return False
    
    def get_all_achievements(self):
        """Повертає всі досягнення"""
        return self.achievements_list