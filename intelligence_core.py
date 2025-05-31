# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Ядро штучного інтелекту
Модуль прогнозного аналізу та машинного навчання
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

class PredictiveEngine:
    """Основний клас для прогнозного аналізу системи"""
    
    def __init__(self, database_controller):
        self.db_handler = database_controller
        self.anomaly_detector = None
        self.failure_classifier = None
        self.trend_predictor = None
        self.data_scaler = StandardScaler()
        self.is_trained = False
        
        # Ініціалізація моделей
        self._initialize_ml_models()
        
        # Спроба завантаження збережених моделей
        self._load_existing_models()
    
    def _initialize_ml_models(self):
        """Ініціалізація моделей машинного навчання"""
        
        # Детектор аномалій
        self.anomaly_detector = IsolationForest(
            contamination=0.15,
            random_state=42,
            n_estimators=150
        )
        
        # Класифікатор збоїв
        self.failure_classifier = RandomForestClassifier(
            n_estimators=120,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        # Прогнозувач трендів
        self.trend_predictor = LinearRegression()
    
    def analyze_system_state(self, current_metrics):
        """Аналіз поточного стану системи"""
        
        analysis_results = {
            'health_index': 85,
            'alert_messages': [],
            'thermal_forecast': 0,
            'memory_forecast': 0,
            'storage_forecast': 0,
            'health_forecast': 0
        }
        
        try:
            # Підготовка даних для аналізу
            feature_vector = self._prepare_feature_vector(current_metrics)
            
            if self.is_trained and len(feature_vector) > 0:
                # Виявлення аномалій
                anomaly_score = self._detect_anomalies(feature_vector)
                
                # Прогнозування збоїв
                failure_probability = self._predict_failures(feature_vector)
                
                # Розрахунок індексу здоров'я
                health_score = self._calculate_health_index(current_metrics, anomaly_score)
                
                analysis_results.update({
                    'health_index': health_score,
                    'anomaly_score': anomaly_score,
                    'failure_probability': failure_probability
                })
                
                # Генерація попереджень
                warnings = self._generate_system_warnings(current_metrics, analysis_results)
                analysis_results['alert_messages'] = warnings
                
            else:
                # Базовий аналіз без ML
                analysis_results = self._basic_analysis(current_metrics)
                
        except Exception as error:
            print(f"Помилка аналізу системи: {error}")
            analysis_results = self._get_fallback_analysis()
        
        return analysis_results
    
    def _prepare_feature_vector(self, metrics):
        """Підготовка вектора ознак для ML моделей"""
        
        features = []
        
        try:
            # Основні метрики
            features.extend([
                metrics.get('cpu_usage', 0),
                metrics.get('memory_usage', 0),
                metrics.get('storage_usage', 0),
                metrics.get('running_processes', 0),
                metrics.get('active_connections', 0)
            ])
            
            # Мережеві метрики (нормалізовані)
            bytes_sent = metrics.get('network_bytes_sent', 0)
            bytes_recv = metrics.get('network_bytes_recv', 0)
            
            features.extend([
                min(bytes_sent / 1000000, 1000),  # Нормалізація до MB
                min(bytes_recv / 1000000, 1000)
            ])
            
            # Температурні дані
            thermal_reading = metrics.get('thermal_reading', 45)
            if thermal_reading is None:
                thermal_reading = 45
            features.append(min(thermal_reading, 100))
            
            # Час доби (циклічна ознака)
            current_hour = datetime.now().hour
            features.extend([
                np.sin(2 * np.pi * current_hour / 24),
                np.cos(2 * np.pi * current_hour / 24)
            ])
            
        except Exception as error:
            print(f"Помилка підготовки ознак: {error}")
            features = [0] * 10  # Базовий вектор
        
        return np.array(features).reshape(1, -1)
    
    def _detect_anomalies(self, feature_vector):
        """Виявлення аномалій в системних даних"""
        
        try:
            if self.anomaly_detector and len(feature_vector) > 0:
                # Нормалізація даних
                normalized_features = self.data_scaler.transform(feature_vector)
                
                # Виявлення аномалій
                anomaly_prediction = self.anomaly_detector.predict(normalized_features)
                anomaly_score = self.anomaly_detector.decision_function(normalized_features)[0]
                
                # Конвертація в зрозумілий формат
                is_anomaly = anomaly_prediction[0] == -1
                confidence = abs(anomaly_score)
                
                return {
                    'is_anomaly': is_anomaly,
                    'confidence': min(confidence, 1.0),
                    'severity': 'high' if confidence > 0.7 else 'medium' if confidence > 0.3 else 'low'
                }
        except Exception as error:
            print(f"Помилка виявлення аномалій: {error}")
        
        return {'is_anomaly': False, 'confidence': 0, 'severity': 'low'}
    
    def _predict_failures(self, feature_vector):
        """Прогнозування ймовірності збоїв"""
        
        try:
            if self.failure_classifier and len(feature_vector) > 0:
                # Нормалізація ознак
                normalized_features = self.data_scaler.transform(feature_vector)
                
                # Прогнозування
                failure_probability = self.failure_classifier.predict_proba(normalized_features)
                
                if len(failure_probability[0]) > 1:
                    return failure_probability[0][1]  # Ймовірність збою
        except Exception as error:
            print(f"Помилка прогнозування збоїв: {error}")
        
        return 0.1  # Базова ймовірність
    
    def _calculate_health_index(self, metrics, anomaly_data):
        """Розрахунок індексу здоров'я системи"""
        
        base_score = 100
        
        # Зниження за високе використання ресурсів
        cpu_usage = metrics.get('cpu_usage', 0)
        memory_usage = metrics.get('memory_usage', 0)
        storage_usage = metrics.get('storage_usage', 0)
        
        if cpu_usage > 80:
            base_score -= (cpu_usage - 80) * 0.5
        if memory_usage > 85:
            base_score -= (memory_usage - 85) * 0.7
        if storage_usage > 90:
            base_score -= (storage_usage - 90) * 1.0
        
        # Зниження за температуру
        thermal_reading = metrics.get('thermal_reading', 45)
        if thermal_reading and thermal_reading > 70:
            base_score -= (thermal_reading - 70) * 0.3
        
        # Зниження за аномалії
        if anomaly_data.get('is_anomaly'):
            confidence = anomaly_data.get('confidence', 0)
            base_score -= confidence * 20
        
        return max(int(base_score), 0)
    
    def _generate_system_warnings(self, metrics, analysis):
        """Генерація попереджень про стан системи"""
        
        warnings = []
        
        # Перевірка критичних показників
        cpu_usage = metrics.get('cpu_usage', 0)
        memory_usage = metrics.get('memory_usage', 0)
        storage_usage = metrics.get('storage_usage', 0)
        
        if cpu_usage > 90:
            warnings.append(f"Критично високе навантаження процесора: {cpu_usage:.1f}%")
        
        if memory_usage > 95:
            warnings.append(f"Критично мало вільної пам'яті: {100-memory_usage:.1f}%")
        
        if storage_usage > 95:
            warnings.append(f"Критично мало місця на диску: {100-storage_usage:.1f}%")
        
        # Температурні попередження
        thermal_reading = metrics.get('thermal_reading')
        if thermal_reading and thermal_reading > 80:
            warnings.append(f"Висока температура системи: {thermal_reading:.1f}°C")
        
        # Попередження про аномалії
        if analysis.get('anomaly_score', {}).get('is_anomaly'):
            warnings.append("Виявлено аномальну поведінку системи")
        
        # Попередження про ймовірність збоїв
        failure_prob = analysis.get('failure_probability', 0)
        if failure_prob > 0.7:
            warnings.append(f"Висока ймовірність збою: {failure_prob*100:.1f}%")
        
        return warnings
    
    def generate_forecasts(self):
        """Генерація прогнозів для системи"""
        
        forecasts = {
            'failure_risk': 15,
            'risk_trend': -2,
            'performance_trend': 'stable',
            'recommendations': []
        }
        
        try:
            # Отримання історичних даних
            historical_data = self.db_handler.get_historical_data(days=7)
            
            if not historical_data.empty and len(historical_data) > 10:
                # Аналіз трендів
                trends = self._analyze_performance_trends(historical_data)
                forecasts.update(trends)
                
        except Exception as error:
            print(f"Помилка генерації прогнозів: {error}")
        
        return forecasts
    
    def _analyze_performance_trends(self, historical_data):
        """Аналіз трендів продуктивності"""
        
        trends = {}
        
        try:
            # Тренд використання CPU
            cpu_trend = self._calculate_linear_trend(historical_data['cpu_percent'])
            trends['cpu_trend'] = cpu_trend
            
            # Тренд використання пам'яті
            memory_trend = self._calculate_linear_trend(historical_data['ram_percent'])
            trends['memory_trend'] = memory_trend
            
            # Загальний тренд продуктивності
            if cpu_trend > 5 or memory_trend > 5:
                trends['performance_trend'] = 'degrading'
            elif cpu_trend < -2 and memory_trend < -2:
                trends['performance_trend'] = 'improving'
            else:
                trends['performance_trend'] = 'stable'
                
        except Exception as error:
            print(f"Помилка аналізу трендів: {error}")
            trends = {'performance_trend': 'stable'}
        
        return trends
    
    def _calculate_linear_trend(self, data_series):
        """Розрахунок лінійного тренду"""
        
        try:
            if len(data_series) < 3:
                return 0
            
            x = np.arange(len(data_series))
            y = data_series.values
            
            # Лінійна регресія
            coefficients = np.polyfit(x, y, 1)
            trend_slope = coefficients[0]
            
            return float(trend_slope)
        except:
            return 0
    
    def get_optimization_suggestions(self, current_metrics):
        """Генерація рекомендацій для оптимізації"""
        
        suggestions = []
        
        cpu_usage = current_metrics.get('cpu_usage', 0)
        memory_usage = current_metrics.get('memory_usage', 0)
        storage_usage = current_metrics.get('storage_usage', 0)
        
        # Рекомендації по CPU
        if cpu_usage > 80:
            suggestions.append("Розгляньте закриття непотрібних програм для зменшення навантаження на процесор")
        
        # Рекомендації по пам'яті
        if memory_usage > 85:
            suggestions.append("Рекомендується перезапустити програми що споживають багато пам'яті")
        
        # Рекомендації по диску
        if storage_usage > 90:
            suggestions.append("Виконайте очищення диска та видаліть непотрібні файли")
        
        # Загальні рекомендації
        if len(suggestions) == 0:
            suggestions.extend([
                "Система працює в оптимальному режимі",
                "Рекомендується регулярно проводити профілактичне обслуговування",
                "Перевіряйте наявність оновлень системи та драйверів"
            ])
        
        return suggestions[:3]  # Максимум 3 рекомендації
    
    def retrain_models(self):
        """Перенавчання моделей на нових даних"""
        
        try:
            # Отримання даних для навчання
            training_data = self.db_handler.get_historical_data(days=30)
            
            if len(training_data) > 50:  # Мінімальна кількість даних
                # Підготовка навчальних даних
                X, y = self._prepare_training_data(training_data)
                
                if len(X) > 10:
                    # Навчання моделей
                    self._train_anomaly_detector(X)
                    self._train_failure_classifier(X, y)
                    
                    # Збереження моделей
                    self._save_trained_models()
                    
                    self.is_trained = True
                    return True
        except Exception as error:
            print(f"Помилка навчання моделей: {error}")
        
        return False
    
    def _prepare_training_data(self, historical_data):
        """Підготовка даних для навчання"""
        
        X = []
        y = []
        
        for _, row in historical_data.iterrows():
            # Створення вектора ознак
            features = [
                row.get('cpu_percent', 0),
                row.get('ram_percent', 0),
                row.get('disk_percent', 0),
                row.get('network_speed', 0),
                45  # Стандартна температура
            ]
            
            # Створення мітки (спрощена логіка)
            is_problem = (
                row.get('cpu_percent', 0) > 95 or 
                row.get('ram_percent', 0) > 98 or 
                row.get('disk_percent', 0) > 98
            )
            
            X.append(features)
            y.append(1 if is_problem else 0)
        
        return np.array(X), np.array(y)
    
    def _train_anomaly_detector(self, X):
        """Навчання детектора аномалій"""
        
        try:
            # Нормалізація даних
            X_scaled = self.data_scaler.fit_transform(X)
            
            # Навчання моделі
            self.anomaly_detector.fit(X_scaled)
        except Exception as error:
            print(f"Помилка навчання детектора аномалій: {error}")
    
    def _train_failure_classifier(self, X, y):
        """Навчання класифікатора збоїв"""
        
        try:
            # Перевірка наявності обох класів
            if len(set(y)) < 2:
                return
            
            # Нормалізація даних
            X_scaled = self.data_scaler.transform(X)
            
            # Навчання моделі
            self.failure_classifier.fit(X_scaled, y)
        except Exception as error:
            print(f"Помилка навчання класифікатора: {error}")
    
    def _save_trained_models(self):
        """Збереження навчених моделей"""
        
        try:
            models_dir = "ml_models"
            if not os.path.exists(models_dir):
                os.makedirs(models_dir)
            
            # Збереження моделей
            with open(f"{models_dir}/anomaly_detector.pkl", 'wb') as f:
                pickle.dump(self.anomaly_detector, f)
            
            with open(f"{models_dir}/failure_classifier.pkl", 'wb') as f:
                pickle.dump(self.failure_classifier, f)
            
            with open(f"{models_dir}/data_scaler.pkl", 'wb') as f:
                pickle.dump(self.data_scaler, f)
                
        except Exception as error:
            print(f"Помилка збереження моделей: {error}")
    
    def _load_existing_models(self):
        """Завантаження існуючих моделей"""
        
        try:
            models_dir = "ml_models"
            
            if os.path.exists(f"{models_dir}/anomaly_detector.pkl"):
                with open(f"{models_dir}/anomaly_detector.pkl", 'rb') as f:
                    self.anomaly_detector = pickle.load(f)
            
            if os.path.exists(f"{models_dir}/failure_classifier.pkl"):
                with open(f"{models_dir}/failure_classifier.pkl", 'rb') as f:
                    self.failure_classifier = pickle.load(f)
            
            if os.path.exists(f"{models_dir}/data_scaler.pkl"):
                with open(f"{models_dir}/data_scaler.pkl", 'rb') as f:
                    self.data_scaler = pickle.load(f)
                
                self.is_trained = True
                
        except Exception as error:
            print(f"Помилка завантаження моделей: {error}")
    
    def _basic_analysis(self, metrics):
        """Базовий аналіз без машинного навчання"""
        
        health_score = 100
        warnings = []
        
        # Простий розрахунок на основі порогів
        cpu_usage = metrics.get('cpu_usage', 0)
        memory_usage = metrics.get('memory_usage', 0)
        storage_usage = metrics.get('storage_usage', 0)
        
        if cpu_usage > 85:
            health_score -= 15
            warnings.append("Високе навантаження процесора")
        
        if memory_usage > 90:
            health_score -= 20
            warnings.append("Високе використання пам'яті")
        
        if storage_usage > 95:
            health_score -= 25
            warnings.append("Мало вільного місця на диску")
        
        return {
            'health_index': max(health_score, 0),
            'alert_messages': warnings,
            'thermal_forecast': 0,
            'memory_forecast': 0,
            'storage_forecast': 0,
            'health_forecast': 0
        }
    
    def _get_fallback_analysis(self):
        """Резервний аналіз при помилках"""
        
        return {
            'health_index': 75,
            'alert_messages': ["Система працює в штатному режимі"],
            'thermal_forecast': 0,
            'memory_forecast': 0,
            'storage_forecast': 0,
            'health_forecast': 0
        }