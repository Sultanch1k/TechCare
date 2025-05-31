# -*- coding: utf-8 -*-
"""
TechCare AI - Benchmarking System Module
Модуль для порівняння продуктивності системи з іншими
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import psutil
from monitor import get_system_data

class BenchmarkingSystem:
    def __init__(self, data_manager):
        """Ініціалізація системи бенчмаркінгу"""
        self.data_manager = data_manager
        self.benchmark_weights = {
            'cpu': 0.25,
            'ram': 0.20,
            'disk': 0.20,
            'network': 0.15,
            'stability': 0.10,
            'efficiency': 0.10
        }
        
        # Еталонні значення для порівняння (базуються на середніх показниках)
        self.reference_values = {
            'cpu_score': 75,
            'ram_score': 70,
            'disk_score': 65,
            'network_score': 60,
            'stability_score': 80,
            'efficiency_score': 75
        }
    
    def run_benchmark(self):
        """Запуск повного бенчмарку системи"""
        try:
            benchmark_results = {
                'timestamp': datetime.now(),
                'cpu_score': self.benchmark_cpu(),
                'ram_score': self.benchmark_ram(),
                'disk_score': self.benchmark_disk(),
                'network_score': self.benchmark_network(),
                'stability_score': self.benchmark_stability(),
                'efficiency_score': self.benchmark_efficiency()
            }
            
            # Розрахунок загального скору
            overall_score = self.calculate_overall_score(benchmark_results)
            benchmark_results['overall_score'] = overall_score
            
            # Детальні результати
            detailed_results = self.generate_detailed_analysis(benchmark_results)
            benchmark_results['detailed_results'] = detailed_results
            
            # Збереження результатів
            self.data_manager.save_benchmark_result(benchmark_results)
            
            # Нарахування досвіду
            if hasattr(self.data_manager, 'save_user_activity'):
                self.data_manager.save_user_activity('benchmark', 50, 'Виконано бенчмарк системи')
            
            return benchmark_results
            
        except Exception as e:
            print(f"Помилка виконання бенчмарку: {e}")
            return self.get_fallback_results()
    
    def benchmark_cpu(self):
        """Бенчмарк процесора"""
        try:
            # Отримання базової інформації
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Тест навантаження CPU
            start_time = time.time()
            cpu_usage_samples = []
            
            # Збір зразків використання CPU протягом 5 секунд
            for _ in range(5):
                cpu_usage = psutil.cpu_percent(interval=1)
                cpu_usage_samples.append(cpu_usage)
            
            avg_cpu_usage = sum(cpu_usage_samples) / len(cpu_usage_samples)
            
            # Розрахунок скору на основі кількості ядер, частоти та ефективності
            base_score = 50
            
            # Бонус за кількість ядер
            if cpu_count >= 8:
                base_score += 20
            elif cpu_count >= 4:
                base_score += 10
            
            # Бонус за частоту
            if cpu_freq and cpu_freq.current:
                if cpu_freq.current >= 3000:  # 3+ GHz
                    base_score += 15
                elif cpu_freq.current >= 2500:  # 2.5+ GHz
                    base_score += 10
            
            # Штраф за високе навантаження (система перевантажена)
            if avg_cpu_usage > 80:
                base_score -= 15
            elif avg_cpu_usage > 60:
                base_score -= 5
            
            return min(100, max(0, base_score))
            
        except Exception as e:
            print(f"Помилка бенчмарку CPU: {e}")
            return 50
    
    def benchmark_ram(self):
        """Бенчмарк оперативної пам'яті"""
        try:
            memory = psutil.virtual_memory()
            
            base_score = 50
            
            # Бонус за об'єм RAM
            ram_gb = memory.total / (1024**3)
            if ram_gb >= 32:
                base_score += 25
            elif ram_gb >= 16:
                base_score += 20
            elif ram_gb >= 8:
                base_score += 10
            elif ram_gb >= 4:
                base_score += 5
            
            # Штраф за високе використання
            if memory.percent > 90:
                base_score -= 20
            elif memory.percent > 75:
                base_score -= 10
            elif memory.percent > 60:
                base_score -= 5
            
            # Бонус за доступну пам'ять
            available_gb = memory.available / (1024**3)
            if available_gb >= 8:
                base_score += 10
            elif available_gb >= 4:
                base_score += 5
            
            return min(100, max(0, base_score))
            
        except Exception as e:
            print(f"Помилка бенчмарку RAM: {e}")
            return 50
    
    def benchmark_disk(self):
        """Бенчмарк дисків"""
        try:
            # Аналіз основного диска
            disk_usage = psutil.disk_usage('/')
            
            base_score = 50
            
            # Бонус за об'єм диска
            disk_gb = disk_usage.total / (1024**3)
            if disk_gb >= 1000:  # 1TB+
                base_score += 15
            elif disk_gb >= 500:  # 500GB+
                base_score += 10
            elif disk_gb >= 250:  # 250GB+
                base_score += 5
            
            # Штраф за заповненість
            usage_percent = (disk_usage.used / disk_usage.total) * 100
            if usage_percent > 90:
                base_score -= 25
            elif usage_percent > 80:
                base_score -= 15
            elif usage_percent > 70:
                base_score -= 5
            
            # Бонус за вільне місце
            free_gb = disk_usage.free / (1024**3)
            if free_gb >= 100:
                base_score += 10
            elif free_gb >= 50:
                base_score += 5
            
            # Спроба визначити тип диска через I/O тест
            try:
                io_before = psutil.disk_io_counters()
                time.sleep(1)
                io_after = psutil.disk_io_counters()
                
                if io_before and io_after:
                    read_speed = (io_after.read_bytes - io_before.read_bytes) / (1024**2)  # MB/s
                    write_speed = (io_after.write_bytes - io_before.write_bytes) / (1024**2)  # MB/s
                    
                    # Бонус за швидкість (припущення що SSD швидший)
                    avg_speed = (read_speed + write_speed) / 2
                    if avg_speed > 100:  # Швидко (можливо SSD)
                        base_score += 15
                    elif avg_speed > 50:
                        base_score += 10
            except:
                pass
            
            return min(100, max(0, base_score))
            
        except Exception as e:
            print(f"Помилка бенчмарку диска: {e}")
            return 50
    
    def benchmark_network(self):
        """Бенчмарк мережі"""
        try:
            # Базова мережева статистика
            net_io = psutil.net_io_counters()
            connections = psutil.net_connections()
            
            base_score = 50
            
            # Аналіз кількості активних з'єднань
            active_connections = len([c for c in connections if c.status == 'ESTABLISHED'])
            
            if active_connections < 10:
                base_score += 10  # Мало з'єднань - добре для продуктивності
            elif active_connections > 50:
                base_score -= 10  # Багато з'єднань - може впливати на продуктивність
            
            # Симуляція швидкості мережі на основі активності
            if net_io:
                # Перевірка загального обсягу переданих даних
                total_data = (net_io.bytes_sent + net_io.bytes_recv) / (1024**3)  # GB
                
                if total_data > 10:  # Активне використання мережі
                    base_score += 10
                
                # Перевірка помилок
                total_errors = net_io.errin + net_io.errout
                if total_errors == 0:
                    base_score += 15
                elif total_errors < 10:
                    base_score += 5
                else:
                    base_score -= 10
            
            # Симуляція пінгу на основі кількості з'єднань
            estimated_ping = 20 + min(active_connections, 50)
            if estimated_ping < 30:
                base_score += 15
            elif estimated_ping < 50:
                base_score += 10
            elif estimated_ping < 100:
                base_score += 5
            else:
                base_score -= 5
            
            return min(100, max(0, base_score))
            
        except Exception as e:
            print(f"Помилка бенчмарку мережі: {e}")
            return 50
    
    def benchmark_stability(self):
        """Бенчмарк стабільності системи"""
        try:
            base_score = 50
            
            # Час роботи системи
            uptime_seconds = time.time() - psutil.boot_time()
            uptime_hours = uptime_seconds / 3600
            
            # Бонус за стабільність, але штраф за занадто довгу роботу
            if 24 <= uptime_hours <= 168:  # 1-7 днів
                base_score += 20
            elif 12 <= uptime_hours < 24:  # 12-24 години
                base_score += 15
            elif 6 <= uptime_hours < 12:  # 6-12 годин
                base_score += 10
            elif uptime_hours > 168:  # Більше тижня
                base_score -= 5  # Потрібен перезапуск
            
            # Аналіз процесів
            try:
                processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))
                
                # Перевірка наявності зависших процесів
                high_cpu_processes = [p for p in processes if p.info['cpu_percent'] > 90]
                if len(high_cpu_processes) == 0:
                    base_score += 10
                else:
                    base_score -= len(high_cpu_processes) * 5
                
                # Загальна кількість процесів
                process_count = len(processes)
                if process_count < 100:
                    base_score += 10
                elif process_count > 200:
                    base_score -= 5
                
            except:
                pass
            
            # Аналіз історичних даних про стабільність
            try:
                historical_data = self.data_manager.get_historical_data(days=7)
                if not historical_data.empty:
                    # Перевірка варіації в даних (стабільність)
                    cpu_variance = historical_data['cpu_percent'].var() if 'cpu_percent' in historical_data else 0
                    ram_variance = historical_data['ram_percent'].var() if 'ram_percent' in historical_data else 0
                    
                    # Менша варіація = більша стабільність
                    if cpu_variance < 100 and ram_variance < 100:
                        base_score += 15
                    elif cpu_variance < 200 and ram_variance < 200:
                        base_score += 10
            except:
                pass
            
            return min(100, max(0, base_score))
            
        except Exception as e:
            print(f"Помилка бенчмарку стабільності: {e}")
            return 50
    
    def benchmark_efficiency(self):
        """Бенчмарк ефективності системи"""
        try:
            base_score = 50
            
            # Отримання поточних системних даних
            system_data = get_system_data()
            
            # Ефективність використання ресурсів
            cpu_percent = system_data.get('cpu_percent', 0)
            ram_percent = system_data.get('ram_percent', 0)
            
            # Оптимальне використання ресурсів (не занадто мало, не занадто багато)
            if 20 <= cpu_percent <= 60:
                base_score += 10
            elif cpu_percent < 20:
                base_score += 5  # Недовикористання
            else:
                base_score -= 5  # Перевикористання
            
            if 30 <= ram_percent <= 70:
                base_score += 10
            elif ram_percent < 30:
                base_score += 5
            else:
                base_score -= 5
            
            # Енергоефективність (якщо доступна інформація про батарею)
            battery_info = system_data.get('battery_info')
            if battery_info:
                if battery_info['plugged']:
                    base_score += 5  # Підключено до мережі
                else:
                    # Оцінка на основі рівня заряду
                    if battery_info['percent'] > 50:
                        base_score += 10
                    elif battery_info['percent'] > 20:
                        base_score += 5
                    else:
                        base_score -= 5
            
            # Ефективність використання мережі
            try:
                net_io = psutil.net_io_counters()
                if net_io:
                    # Співвідношення помилок до загальних пакетів
                    total_packets = net_io.packets_sent + net_io.packets_recv
                    total_errors = net_io.errin + net_io.errout
                    
                    if total_packets > 0:
                        error_rate = total_errors / total_packets
                        if error_rate < 0.001:  # Менше 0.1% помилок
                            base_score += 15
                        elif error_rate < 0.01:  # Менше 1% помилок
                            base_score += 10
                        else:
                            base_score -= 5
            except:
                pass
            
            # Температурна ефективність
            cpu_temp = system_data.get('cpu_temp')
            if cpu_temp:
                if cpu_temp < 60:
                    base_score += 15  # Холодна система
                elif cpu_temp < 70:
                    base_score += 10
                elif cpu_temp < 80:
                    base_score += 5
                else:
                    base_score -= 10  # Гаряча система
            
            return min(100, max(0, base_score))
            
        except Exception as e:
            print(f"Помилка бенчмарку ефективності: {e}")
            return 50
    
    def calculate_overall_score(self, results):
        """Розрахунок загального скору"""
        try:
            weighted_sum = 0
            for category, weight in self.benchmark_weights.items():
                score_key = f"{category}_score"
                if score_key in results:
                    weighted_sum += results[score_key] * weight
            
            return int(weighted_sum)
        except Exception as e:
            print(f"Помилка розрахунку загального скору: {e}")
            return 50
    
    def generate_detailed_analysis(self, results):
        """Генерація детального аналізу"""
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'recommendations': []
        }
        
        try:
            # Аналіз сильних сторін
            for category in ['cpu', 'ram', 'disk', 'network', 'stability', 'efficiency']:
                score_key = f"{category}_score"
                if results.get(score_key, 0) >= 80:
                    analysis['strengths'].append({
                        'category': category.upper(),
                        'score': results[score_key],
                        'description': self.get_category_description(category, 'strength')
                    })
            
            # Аналіз слабких сторін
            for category in ['cpu', 'ram', 'disk', 'network', 'stability', 'efficiency']:
                score_key = f"{category}_score"
                if results.get(score_key, 0) < 60:
                    analysis['weaknesses'].append({
                        'category': category.upper(),
                        'score': results[score_key],
                        'description': self.get_category_description(category, 'weakness')
                    })
            
            # Генерація рекомендацій
            analysis['recommendations'] = self.generate_recommendations(results)
            
        except Exception as e:
            print(f"Помилка генерації аналізу: {e}")
        
        return analysis
    
    def get_category_description(self, category, type_desc):
        """Отримання опису категорії"""
        descriptions = {
            'cpu': {
                'strength': 'Відмінна продуктивність процесора',
                'weakness': 'Процесор може бути перевантажений або застарілий'
            },
            'ram': {
                'strength': 'Достатньо оперативної пам\'яті для комфортної роботи',
                'weakness': 'Недостатньо RAM або високе використання пам\'яті'
            },
            'disk': {
                'strength': 'Диски працюють ефективно з достатнім вільним місцем',
                'weakness': 'Диски заповнені або працюють повільно'
            },
            'network': {
                'strength': 'Стабільне та швидке мережеве підключення',
                'weakness': 'Проблеми з мережею або повільне підключення'
            },
            'stability': {
                'strength': 'Система працює стабільно без збоїв',
                'weakness': 'Виявлені проблеми зі стабільністю системи'
            },
            'efficiency': {
                'strength': 'Ефективне використання ресурсів системи',
                'weakness': 'Неефективне використання ресурсів'
            }
        }
        
        return descriptions.get(category, {}).get(type_desc, 'Опис недоступний')
    
    def generate_recommendations(self, results):
        """Генерація рекомендацій на основі результатів"""
        recommendations = []
        
        try:
            if results.get('cpu_score', 0) < 60:
                recommendations.append('Розгляньте можливість оновлення процесора або зменшення навантаження')
            
            if results.get('ram_score', 0) < 60:
                recommendations.append('Додайте більше оперативної пам\'яті або закрийте непотрібні програми')
            
            if results.get('disk_score', 0) < 60:
                recommendations.append('Очистіть диск від непотрібних файлів або розгляньте оновлення до SSD')
            
            if results.get('network_score', 0) < 60:
                recommendations.append('Перевірте мережеве підключення та налаштування')
            
            if results.get('stability_score', 0) < 60:
                recommendations.append('Перезапустіть систему та перевірте на наявність проблемних програм')
            
            if results.get('efficiency_score', 0) < 60:
                recommendations.append('Оптимізуйте автозапуск програм та налаштування енергоспоживання')
            
            if results.get('overall_score', 0) >= 80:
                recommendations.append('Відмінні результати! Система працює на високому рівні')
            
        except Exception as e:
            print(f"Помилка генерації рекомендацій: {e}")
        
        return recommendations
    
    def get_current_benchmark(self):
        """Отримання поточних результатів бенчмарку"""
        try:
            # Отримання останнього бенчмарку
            history = self.data_manager.get_benchmark_history()
            
            if not history.empty:
                latest = history.iloc[0]
                previous = history.iloc[1] if len(history) > 1 else latest
                
                return {
                    'overall_score': latest['overall_score'],
                    'score_change': latest['overall_score'] - previous['overall_score'],
                    'rank': self.calculate_rank(latest['overall_score']),
                    'rank_change': 0,  # Спрощено
                    'percentile': self.calculate_percentile(latest['overall_score']),
                    'percentile_change': 0  # Спрощено
                }
            else:
                # Якщо немає історії, запускаємо перший бенчмарк
                results = self.run_benchmark()
                return {
                    'overall_score': results['overall_score'],
                    'score_change': 0,
                    'rank': self.calculate_rank(results['overall_score']),
                    'rank_change': 0,
                    'percentile': self.calculate_percentile(results['overall_score']),
                    'percentile_change': 0
                }
        except Exception as e:
            print(f"Помилка отримання поточного бенчмарку: {e}")
            return self.get_fallback_results()
    
    def get_detailed_results(self):
        """Отримання детальних результатів"""
        try:
            history = self.data_manager.get_benchmark_history()
            
            if not history.empty:
                latest = history.iloc[0]
                
                return {
                    'cpu': {
                        'your_score': latest['cpu_score'],
                        'average_score': self.reference_values['cpu_score']
                    },
                    'ram': {
                        'your_score': latest['ram_score'],
                        'average_score': self.reference_values['ram_score']
                    },
                    'disk': {
                        'your_score': latest['disk_score'],
                        'average_score': self.reference_values['disk_score']
                    },
                    'network': {
                        'your_score': latest['network_score'],
                        'average_score': self.reference_values['network_score']
                    },
                    'stability': {
                        'your_score': latest['stability_score'],
                        'average_score': self.reference_values['stability_score']
                    },
                    'efficiency': {
                        'your_score': latest['efficiency_score'],
                        'average_score': self.reference_values['efficiency_score']
                    }
                }
            else:
                # Повернення еталонних значень
                return {category: {'your_score': 50, 'average_score': score} 
                       for category, score in self.reference_values.items()}
        except Exception as e:
            print(f"Помилка отримання детальних результатів: {e}")
            return {}
    
    def get_strengths(self):
        """Отримання сильних сторін системи"""
        try:
            detailed_results = self.get_detailed_results()
            strengths = []
            
            for category, scores in detailed_results.items():
                if scores['your_score'] > scores['average_score'] + 10:
                    strengths.append({
                        'category': category.upper(),
                        'description': f"На {scores['your_score'] - scores['average_score']:.0f} балів вище середнього"
                    })
            
            if not strengths:
                strengths.append({
                    'category': 'Загальна',
                    'description': 'Система працює в межах середніх показників'
                })
            
            return strengths
        except Exception as e:
            print(f"Помилка отримання сильних сторін: {e}")
            return []
    
    def get_improvement_areas(self):
        """Отримання областей для покращення"""
        try:
            detailed_results = self.get_detailed_results()
            improvements = []
            
            for category, scores in detailed_results.items():
                if scores['your_score'] < scores['average_score'] - 10:
                    improvements.append({
                        'category': category.upper(),
                        'suggestion': self.get_improvement_suggestion(category)
                    })
            
            if not improvements:
                improvements.append({
                    'category': 'Загальна',
                    'suggestion': 'Система працює добре, розгляньте профілактичне обслуговування'
                })
            
            return improvements
        except Exception as e:
            print(f"Помилка отримання областей покращення: {e}")
            return []
    
    def get_improvement_suggestion(self, category):
        """Отримання пропозиції покращення для категорії"""
        suggestions = {
            'cpu': 'Розгляньте оновлення процесора або оптимізацію запущених програм',
            'ram': 'Додайте більше оперативної пам\'яті або закрийте непотрібні додатки',
            'disk': 'Очистіть диск або замініть на SSD для кращої продуктивності',
            'network': 'Перевірте мережеві налаштування та якість підключення',
            'stability': 'Виконайте діагностику системи та оновіть драйвери',
            'efficiency': 'Оптимізуйте налаштування енергоспоживання та автозапуск'
        }
        
        return suggestions.get(category, 'Виконайте загальну оптимізацію системи')
    
    def get_history(self):
        """Отримання історії бенчмарків"""
        return self.data_manager.get_benchmark_history()
    
    def calculate_rank(self, score):
        """Розрахунок рангу на основі скору (симуляція)"""
        # Спрощена логіка рангування
        if score >= 90:
            return 1
        elif score >= 80:
            return 2
        elif score >= 70:
            return 3
        elif score >= 60:
            return 4
        else:
            return 5
    
    def calculate_percentile(self, score):
        """Розрахунок процентилю (симуляція)"""
        # Спрощена логіка: лінейне відображення скору на процентиль
        return min(99, max(1, score))
    
    def get_fallback_results(self):
        """Резервні результати при помилках"""
        return {
            'overall_score': 50,
            'score_change': 0,
            'rank': 5,
            'rank_change': 0,
            'percentile': 50,
            'percentile_change': 0
        }
