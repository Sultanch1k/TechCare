# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Система мотивації користувачів
Модуль досягнень та геймифікації
"""

class UserMotivation:
    """Система мотивації та досягнень користувачів"""
    
    def __init__(self, database_controller):
        self.db_handler = database_controller
        self.achievement_rules = self._define_achievement_rules()
    
    def _define_achievement_rules(self):
        """Визначення правил для досягнень"""
        return {
            'first_launch': {
                'title': 'Початківець',
                'description': 'Перший запуск SystemWatch Pro',
                'condition': lambda stats: True,
                'reward': 50
            },
            'system_guardian': {
                'title': 'Охоронець системи',
                'description': 'Виконано 15 перевірок системи',
                'condition': lambda stats: stats.get('tasks_completed', 0) >= 15,
                'reward': 120
            },
            'optimization_master': {
                'title': 'Майстер оптимізації',
                'description': 'Виправлено 30 системних проблем',
                'condition': lambda stats: stats.get('problems_fixed', 0) >= 30,
                'reward': 250
            },
            'performance_expert': {
                'title': 'Експерт продуктивності',
                'description': 'Проведено 7 тестів швидкості',
                'condition': lambda stats: stats.get('benchmarks_run', 0) >= 7,
                'reward': 180
            },
            'maintenance_pro': {
                'title': 'Професіонал обслуговування',
                'description': 'Виконано 60 планових завдань',
                'condition': lambda stats: stats.get('maintenance_tasks', 0) >= 60,
                'reward': 350
            }
        }
    
    def track_user_activity(self, activity_type, points_earned, description=""):
        """Відстеження активності користувача"""
        self.db_handler.log_user_activity(activity_type, points_earned, description)
        self._check_achievement_unlocks()
    
    def _check_achievement_unlocks(self):
        """Перевірка можливості отримання нових досягнень"""
        user_stats = self.get_user_statistics()
        
        for achievement_code, rules in self.achievement_rules.items():
            if rules['condition'](user_stats):
                self.db_handler.award_achievement(achievement_code)
    
    def get_user_statistics(self):
        """Отримання статистики користувача"""
        return self.db_handler.get_user_statistics()
    
    def get_available_achievements(self):
        """Отримання списку всіх досягнень"""
        achievements = []
        
        connection = self.db_handler.establish_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT achievement_code, achievement_name, achievement_description, 
                           is_unlocked, unlock_timestamp, experience_reward
                    FROM user_achievements
                """)
                
                results = cursor.fetchall()
                
                for result in results:
                    achievements.append({
                        'code': result[0],
                        'title': result[1],
                        'description': result[2],
                        'unlocked': result[3],
                        'unlock_date': result[4],
                        'reward': result[5]
                    })
                
                cursor.close()
                connection.close()
                
            except Exception as error:
                print(f"Помилка отримання досягнень: {error}")
                if connection:
                    connection.close()
        
        return achievements