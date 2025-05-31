# -*- coding: utf-8 -*-
"""
TechCare AI - AI Engine Module
Модуль штучного інтелекту для прогнозування та аналізу
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import pickle
import os

class AIEngine:
    def __init__(self, data_manager):
        """Ініціалізація AI движка"""
        self.data_manager = data_manager
        self.models = {}
        self.scalers = {}
        self.is_trained = False
        
        # Ініціалізація моделей
        self.init_models()
        
        # Спроба завантажити навчені моделі
        self.load_models()
    
    def init_models(self):
        """Ініціалізація ML моделей"""
        # Модель для прогнозування збоїв
        self.models['failure_prediction'] = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        
        # Модель для виявлення аномалій
        self.models['anomaly_detection'] = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        
        # Модель для прогнозування навантаження
        self.models['load_prediction'] = LinearRegression()
        
        # Скейлери для нормалізації даних
        self.scalers['system_metrics'] = StandardScaler()
        self.scalers['time_features'] = StandardScaler()
    
    def prepare_features(self, system_data):
        """Підготовка ознак для ML"""
        features = []
        
        # Основні системні метрики
        cpu_metric = system_data.get('cpu_temp', system_data.get('cpu_percent', 0))
        features.extend([
            cpu_metric,
            system_data.get('ram_percent', 0),
            system_data.get('disk_percent', 0),
            system_data.get('uptime_seconds', 0) / 3600,  # години
        ])
        
        # Часові ознаки
        now = datetime.now()
        features.extend([
            now.hour,
            now.weekday(),
            now.day,
        ])
        
        # Додаткові обчислені ознаки
        features.extend([
            cpu_metric / 100 * system_data.get('ram_percent', 0),  # Інтеракція CPU-RAM
            system_data.get('uptime_seconds', 0) / 86400,  # дні роботи
        ])
        
        return np.array(features).reshape(1, -1)
    
    def train_models(self):
        """Навчання моделей на історичних даних"""
        # Отримання історичних даних
        historical_data = self.data_manager.get_historical_data(days=30)
        
        if historical_data.empty or len(historical_data) < 50:
            print("Недостатньо даних для навчання моделей")
            return False
        
        try:
            # Підготовка ознак
            features_list = []
            failure_labels = []
            
            for _, row in historical_data.iterrows():
                features = self.prepare_features(row.to_dict()).flatten()
                features_list.append(features)
                
                # Створення міток для класифікації збоїв
                failure_label = self.create_failure_label(row)
                failure_labels.append(failure_label)
            
            X = np.array(features_list)
            y = np.array(failure_labels)
            
            # Розділення на тренувальні та тестові дані
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Нормалізація ознак
            X_train_scaled = self.scalers['system_metrics'].fit_transform(X_train)
            X_test_scaled = self.scalers['system_metrics'].transform(X_test)
            
            # Навчання моделі прогнозування збоїв
            self.models['failure_prediction'].fit(X_train_scaled, y_train)
            
            # Навчання моделі виявлення аномалій
            normal_data = X_train_scaled[y_train == 0]  # Тільки нормальні дані
            self.models['anomaly_detection'].fit(normal_data)
            
            # Навчання моделі прогнозування навантаження
            load_target = X_train[:, 1]  # RAM як ціль
            self.models['load_prediction'].fit(X_train_scaled, load_target)
            
            self.is_trained = True
            
            # Збереження моделей
            self.save_models()
            
            print("Моделі успішно навчені")
            return True
            
        except Exception as e:
            print(f"Помилка при навчанні моделей: {e}")
            return False
    
    def create_failure_label(self, data_row):
        """Створення міток для навчання (0 - норма, 1 - проблема)"""
        cpu_metric = data_row.get('cpu_temp', data_row.get('cpu_percent', 0))
        
        # Критерії для визначення проблемного стану
        if (cpu_metric > 80 or 
            data_row.get('ram_percent', 0) > 95 or 
            data_row.get('disk_percent', 0) > 95):
            return 1
        return 0
    
    def predict_system_health(self, current_data):
        """Прогнозування здоров'я системи"""
        if not self.is_trained:
            # Спроба навчання якщо моделі не готові
            if not self.train_models():
                return self.fallback_predictions(current_data)
        
        try:
            features = self.prepare_features(current_data)
            features_scaled = self.scalers['system_metrics'].transform(features)
            
            # Прогноз ймовірності збою
            failure_prob = self.models['failure_prediction'].predict_proba(features_scaled)[0, 1]
            
            # Виявлення аномалій
            anomaly_score = self.models['anomaly_detection'].decision_function(features_scaled)[0]
            
            # Прогноз майбутнього навантаження
            predicted_load = self.models['load_prediction'].predict(features_scaled)[0]
            
            # Розрахунок загального скору здоров'я
            health_score = max(0, min(100, 100 - (failure_prob * 100)))
            
            # Створення попереджень
            warnings = []
            if failure_prob > 0.7:
                warnings.append("Високий ризик збою системи")
            if anomaly_score < -0.5:
                warnings.append("Виявлено аномальну поведінку системи")
            if predicted_load > 90:
                warnings.append("Прогнозується високе навантаження на RAM")
            
            # Трендові індикатори
            trends = self.calculate_trends(current_data)
            
            return {
                'health_score': int(health_score),
                'failure_probability': failure_prob,
                'anomaly_score': anomaly_score,
                'predicted_load': predicted_load,
                'warnings': warnings,
                'temp_trend': trends.get('temp_trend', 0),
                'ram_trend': trends.get('ram_trend', 0),
                'disk_trend': trends.get('disk_trend', 0),
                'health_trend': trends.get('health_trend', 0)
            }
            
        except Exception as e:
            print(f"Помилка при прогнозуванні: {e}")
            return self.fallback_predictions(current_data)
    
    def fallback_predictions(self, current_data):
        """Резервні прогнози без ML"""
        cpu_metric = current_data.get('cpu_temp', current_data.get('cpu_percent', 0))
        ram_percent = current_data.get('ram_percent', 0)
        disk_percent = current_data.get('disk_percent', 0)
        
        # Простий алгоритм оцінки здоров'я
        health_score = 100
        warnings = []
        
        if cpu_metric > 80:
            health_score -= 20
            warnings.append("Висока температура/навантаження CPU")
        
        if ram_percent > 90:
            health_score -= 15
            warnings.append("Критичне використання RAM")
        
        if disk_percent > 90:
            health_score -= 10
            warnings.append("Диск майже повний")
        
        return {
            'health_score': max(0, health_score),
            'failure_probability': 0.1,
            'warnings': warnings,
            'temp_trend': 0,
            'ram_trend': 0,
            'disk_trend': 0,
            'health_trend': 0
        }
    
    def calculate_trends(self, current_data):
        """Розрахунок трендів на основі історичних даних"""
        recent_data = self.data_manager.get_historical_data(hours=6)
        
        if recent_data.empty or len(recent_data) < 2:
            return {}
        
        trends = {}
        
        # Тренд температури/CPU
        cpu_values = recent_data['cpu_temp'].fillna(recent_data['cpu_percent'])
        if len(cpu_values) >= 2:
            trends['temp_trend'] = cpu_values.iloc[-1] - cpu_values.iloc[-2]
        
        # Тренд RAM
        if len(recent_data['ram_percent']) >= 2:
            trends['ram_trend'] = recent_data['ram_percent'].iloc[-1] - recent_data['ram_percent'].iloc[-2]
        
        # Тренд диска
        if len(recent_data['disk_percent']) >= 2:
            trends['disk_trend'] = recent_data['disk_percent'].iloc[-1] - recent_data['disk_percent'].iloc[-2]
        
        return trends
    
    def predict_failures(self):
        """Прогнозування конкретних типів збоїв"""
        if not self.is_trained:
            return []
        
        recent_data = self.data_manager.get_historical_data(hours=12)
        
        if recent_data.empty:
            return []
        
        predictions = []
        
        # Аналіз трендів для різних типів збоїв
        cpu_trend = recent_data['cpu_temp'].fillna(recent_data['cpu_percent']).pct_change().mean()
        ram_trend = recent_data['ram_percent'].pct_change().mean()
        
        # Прогноз перегріву
        if cpu_trend > 0.05:  # 5% зростання
            predictions.append({
                'type': 'Перегрів системи',
                'probability': min(0.9, cpu_trend * 10),
                'estimated_time': '2-4 години'
            })
        
        # Прогноз нестачі RAM
        if ram_trend > 0.03:  # 3% зростання
            predictions.append({
                'type': 'Нестача оперативної пам\'яті',
                'probability': min(0.8, ram_trend * 15),
                'estimated_time': '1-2 години'
            })
        
        # Прогноз на основі часу роботи
        latest_data = recent_data.iloc[-1] if not recent_data.empty else {}
        uptime_hours = latest_data.get('uptime_seconds', 0) / 3600
        
        if uptime_hours > 72:  # Більше 3 днів
            predictions.append({
                'type': 'Потреба в перезапуску',
                'probability': min(0.7, uptime_hours / 168),  # 168 годин = тиждень
                'estimated_time': 'Рекомендується зараз'
            })
        
        return predictions
    
    def analyze_system_patterns(self, current_data):
        """Аналіз патернів поведінки системи"""
        historical_data = self.data_manager.get_historical_data(days=7)
        
        if historical_data.empty:
            return {'patterns': []}
        
        patterns = []
        
        # Аналіз циклічності навантаження
        hourly_avg = historical_data.groupby(historical_data['timestamp'].dt.hour)['ram_percent'].mean()
        peak_hours = hourly_avg.nlargest(3).index.tolist()
        
        if len(peak_hours) > 0:
            patterns.append({
                'type': 'Піки навантаження',
                'description': f'Найвище навантаження о {peak_hours[0]}:00-{peak_hours[-1]}:00',
                'confidence': 0.8
            })
        
        # Аналіз стабільності температури
        cpu_values = historical_data['cpu_temp'].fillna(historical_data['cpu_percent'])
        temp_variance = cpu_values.var()
        
        if temp_variance < 10:
            patterns.append({
                'type': 'Стабільна температура',
                'description': 'Система працює в стабільному температурному режимі',
                'confidence': 0.9
            })
        elif temp_variance > 50:
            patterns.append({
                'type': 'Нестабільна температура',
                'description': 'Виявлені коливання температури, можлива проблема з охолодженням',
                'confidence': 0.7
            })
        
        return {'patterns': patterns}
    
    def get_personalized_recommendations(self, current_data):
        """Персоналізовані рекомендації на основі AI аналізу"""
        recommendations = []
        
        # Аналіз поточного стану
        health_prediction = self.predict_system_health(current_data)
        failure_predictions = self.predict_failures()
        
        # Рекомендації на основі прогнозів
        if health_prediction['health_score'] < 70:
            recommendations.append({
                'title': 'Термінова оптимізація системи',
                'description': 'AI виявив зниження здоров\'я системи. Рекомендується провести діагностику.',
                'priority': 'high',
                'expected_impact': 'Підвищення стабільності на 15-20%',
                'auto_applicable': True
            })
        
        # Рекомендації на основі прогнозів збоїв
        for prediction in failure_predictions:
            if prediction['probability'] > 0.6:
                recommendations.append({
                    'title': f'Попередження: {prediction["type"]}',
                    'description': f'AI прогнозує {prediction["type"]} з ймовірністю {prediction["probability"]:.1%}',
                    'priority': 'high' if prediction['probability'] > 0.8 else 'medium',
                    'expected_impact': 'Запобігання потенційного збою',
                    'auto_applicable': False
                })
        
        # Рекомендації на основі трендів
        cpu_metric = current_data.get('cpu_temp', current_data.get('cpu_percent', 0))
        
        if cpu_metric > 75:
            recommendations.append({
                'title': 'Оптимізація охолодження',
                'description': 'Висока температура може призвести до зниження продуктивності',
                'priority': 'medium',
                'expected_impact': 'Зниження температури на 5-10°C',
                'auto_applicable': True
            })
        
        if current_data.get('ram_percent', 0) > 85:
            recommendations.append({
                'title': 'Очищення оперативної пам\'яті',
                'description': 'Високе використання RAM може сповільнити систему',
                'priority': 'medium',
                'expected_impact': 'Звільнення 10-20% RAM',
                'auto_applicable': True
            })
        
        # Загальні рекомендації
        if not recommendations:
            recommendations.append({
                'title': 'Профілактичне обслуговування',
                'description': 'Система працює стабільно, рекомендується планове обслуговування',
                'priority': 'low',
                'expected_impact': 'Підтримання оптимальної продуктивності',
                'auto_applicable': True
            })
        
        return recommendations[:5]  # Максимум 5 рекомендацій
    
    def save_models(self):
        """Збереження навчених моделей"""
        try:
            models_dir = 'models'
            os.makedirs(models_dir, exist_ok=True)
            
            # Збереження моделей
            for name, model in self.models.items():
                with open(f'{models_dir}/{name}.pkl', 'wb') as f:
                    pickle.dump(model, f)
            
            # Збереження скейлерів
            for name, scaler in self.scalers.items():
                with open(f'{models_dir}/{name}_scaler.pkl', 'wb') as f:
                    pickle.dump(scaler, f)
            
            print("Моделі збережено")
            
        except Exception as e:
            print(f"Помилка збереження моделей: {e}")
    
    def load_models(self):
        """Завантаження збережених моделей"""
        try:
            models_dir = 'models'
            if not os.path.exists(models_dir):
                return False
            
            # Завантаження моделей
            for name in self.models.keys():
                model_path = f'{models_dir}/{name}.pkl'
                if os.path.exists(model_path):
                    with open(model_path, 'rb') as f:
                        self.models[name] = pickle.load(f)
            
            # Завантаження скейлерів
            for name in self.scalers.keys():
                scaler_path = f'{models_dir}/{name}_scaler.pkl'
                if os.path.exists(scaler_path):
                    with open(scaler_path, 'rb') as f:
                        self.scalers[name] = pickle.load(f)
            
            self.is_trained = True
            print("Моделі завантажено")
            return True
            
        except Exception as e:
            print(f"Помилка завантаження моделей: {e}")
            return False
