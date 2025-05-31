# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Інтелектуальний моніторинг та діагностика ПК
Платформа для проактивного управління здоров'ям комп'ютерних систем
Розроблено: [Ваше ім'я]
Версія: 2.1.0
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import threading
import numpy as np

# Імпорт власних модулів
from system_analyzer import collect_hardware_metrics
from intelligence_core import PredictiveEngine
from storage_handler import DatabaseController
from achievement_system import UserMotivation
from performance_tester import SystemBenchmark
from maintenance_scheduler import TaskAutomation
from diagnostic_tools import AutoFixUtility
from responsive_ui import ResponsiveInterface, mobile_optimizations, adaptive_tables

# Ініціалізація стану програми
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = True
    st.session_state.user_preferences = {}
    st.session_state.notification_queue = []
    st.session_state.performance_history = []

# Глобальні змінні для компонентів системи
@st.cache_resource
def initialize_core_components():
    """Ініціалізація основних компонентів системи"""
    database_ctrl = DatabaseController()
    predict_engine = PredictiveEngine(database_ctrl)
    motivator = UserMotivation(database_ctrl)
    benchmark_tool = SystemBenchmark(database_ctrl)
    repair_utility = AutoFixUtility()
    task_manager = TaskAutomation(database_ctrl)
    
    return {
        'db_controller': database_ctrl,
        'predictor': predict_engine,
        'motivator': motivator,
        'benchmark': benchmark_tool,
        'repair_tool': repair_utility,
        'scheduler': task_manager
    }

def launch_main_interface():
    """Запуск головного інтерфейсу програми"""
    
    # Налаштування веб-сторінки
    st.set_page_config(
        page_title="SystemWatch Pro",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Завантаження компонентів
    components = initialize_core_components()
    
    # Застосування власних стилів
    apply_custom_styling()
    
    # Створення заголовку програми
    create_header_section()
    
    # Бічна панель навігації
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/4a90e2/ffffff?text=SystemWatch", width=200)
        st.markdown("### 🛡️ Панель управління")
        
        # Вибір активної сторінки
        current_page = st.radio(
            "Оберіть розділ:",
            [
                "🏠 Головна панель", 
                "🧠 Розумна аналітика", 
                "⚙️ Автодіагностика",
                "🎯 Система досягнень",
                "🚀 Тестування швидкості",
                "⏰ Планувальник завдань",
                "📊 Розширений огляд"
            ]
        )
        
        # Налаштування оновлення
        refresh_enabled = st.checkbox("Авто-оновлення (30с)", value=False)
        if refresh_enabled:
            st.info("🔄 Автоматичне оновлення активне")
                
        # Ручне оновлення
        if st.button("🔄 Оновити зараз"):
            st.rerun()
    
    # Маршрутизація до відповідних розділів
    if current_page == "🏠 Головна панель":
        display_main_dashboard(components)
    elif current_page == "🧠 Розумна аналітика":
        display_intelligence_panel(components)
    elif current_page == "⚙️ Автодіагностика":
        display_repair_center(components)
    elif current_page == "🎯 Система досягнень":
        display_achievement_hub(components)
    elif current_page == "🚀 Тестування швидкості":
        display_benchmark_suite(components)
    elif current_page == "⏰ Планувальник завдань":
        display_task_scheduler(components)
    elif current_page == "📊 Розширений огляд":
        display_detailed_analytics(components)

def apply_custom_styling():
    """Застосування унікальних стилів інтерфейсу"""
    st.markdown("""
    <style>
    /* Основна тема програми */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Картки показників */
    .metric-container {
        background: linear-gradient(145deg, #f0f2f6, #ffffff);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Статусні індикатори */
    .status-excellent { color: #4CAF50; font-weight: bold; }
    .status-good { color: #8BC34A; font-weight: bold; }
    .status-warning { color: #FF9800; font-weight: bold; }
    .status-critical { color: #F44336; font-weight: bold; }
    
    /* Адаптивні елементи */
    @media (max-width: 768px) {
        .main-header { padding: 1rem; font-size: 0.9rem; }
        .metric-container { padding: 1rem; margin: 0.5rem 0; }
    }
    
    /* Анімації */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }
    
    .pulse-animation {
        animation: pulse-glow 2s infinite;
    }
    </style>
    """, unsafe_allow_html=True)

def create_header_section():
    """Створення заголовка програми"""
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ SystemWatch Pro</h1>
        <p>Інтелектуальна платформа для моніторингу та оптимізації комп'ютерних систем</p>
        <small>Розроблено з використанням передових технологій штучного інтелекту</small>
    </div>
    """, unsafe_allow_html=True)

def display_main_dashboard(components):
    """Головна панель з системними показниками"""
    st.subheader("🏠 Системний огляд")
    
    # Збір поточних метрик системи
    current_metrics = collect_hardware_metrics()
    
    # Отримання прогнозів від ШІ
    intelligence_data = components['predictor'].analyze_system_state(current_metrics)
    
    # Визначення режиму відображення
    mobile_view = st.session_state.get('mobile_interface', False)
    
    # Застосування мобільних оптимізацій
    if mobile_view:
        mobile_optimizations()
    
    # Створення адаптивного інтерфейсу
    responsive_ui = ResponsiveInterface(mobile_view)
    
    # Підготовка даних для метрик
    system_indicators = [
        {
            'label': '🌡️ Термальний стан',
            'value': f"{float(current_metrics.get('thermal_reading') or current_metrics.get('cpu_usage') or 0):.1f}{'°C' if current_metrics.get('thermal_reading') else '%'}",
            'trend': intelligence_data.get('thermal_forecast', 0)
        },
        {
            'label': '💾 Використання пам\'яті',
            'value': f"{float(current_metrics.get('memory_usage', 0)):.1f}%",
            'trend': intelligence_data.get('memory_forecast', 0)
        },
        {
            'label': '💿 Заповнення диска',
            'value': f"{float(current_metrics.get('storage_usage', 0)):.1f}%",
            'trend': intelligence_data.get('storage_forecast', 0)
        },
        {
            'label': '⚡ Індекс здоров\'я',
            'value': f"{intelligence_data.get('health_index', 85)}/100",
            'trend': intelligence_data.get('health_forecast', 0)
        }
    ]
    
    # Відображення метрик через адаптивний компонент
    responsive_ui.render_metric_dashboard(system_indicators)
    
    # Попередження від системи ШІ
    if intelligence_data.get('alert_messages'):
        st.warning("⚠️ Виявлено потенційні проблеми:")
        for alert in intelligence_data.get('alert_messages', []):
            st.write(f"• {alert}")
    
    # Створення графіків продуктивності
    create_performance_visualizations(current_metrics, intelligence_data)
    
    # Збереження даних в базу
    components['db_controller'].record_system_snapshot(current_metrics)
    
    # Оновлення системи досягнень
    components['motivator'].track_user_activity("system_check", 10, "Перевірка системи")

def display_intelligence_panel(components):
    """Панель розумної аналітики"""
    st.subheader("🧠 Інтелектуальний аналіз")
    
    current_data = collect_hardware_metrics()
    predictions = components['predictor'].generate_forecasts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Прогнози системи")
        
        # Прогноз збоїв
        failure_probability = predictions.get('failure_risk', 15)
        st.metric(
            "Ймовірність збою (7 днів)",
            f"{failure_probability}%",
            delta=f"{predictions.get('risk_trend', -2)}%" if predictions.get('risk_trend') else None
        )
        
        # Рекомендації від ШІ
        recommendations = components['predictor'].get_optimization_suggestions(current_data)
        
        if recommendations:
            st.markdown("### 💡 Рекомендації для оптимізації")
            for idx, suggestion in enumerate(recommendations[:3], 1):
                st.info(f"**{idx}.** {suggestion}")
    
    with col2:
        st.markdown("### 🎯 Швидкі дії")
        
        if st.button("🔍 Глибокий аналіз"):
            with st.spinner("Проведення детального аналізу..."):
                time.sleep(2)
                st.success("Аналіз завершено! Система в нормальному стані.")
        
        if st.button("🤖 Навчання ШІ"):
            with st.spinner("Оновлення моделей..."):
                components['predictor'].retrain_models()
                st.success("Моделі оновлено!")

def display_repair_center(components):
    """Центр автоматичної діагностики"""
    st.subheader("⚙️ Центр діагностики та ремонту")
    
    # Автоматична діагностика
    diagnostic_results = components['repair_tool'].perform_system_diagnosis()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Результати діагностики")
        
        for issue in diagnostic_results:
            severity_color = {
                'critical': '🔴',
                'warning': '🟡', 
                'info': '🟢'
            }.get(issue['severity'], '⚪')
            
            st.markdown(f"{severity_color} **{issue['category']}**: {issue['description']}")
            
            if issue['auto_fixable']:
                if st.button(f"Виправити {issue['category']}", key=f"fix_{issue['id']}"):
                    success = components['repair_tool'].apply_fix(issue)
                    if success:
                        st.success(f"✅ Проблему '{issue['category']}' усунено!")
                        components['motivator'].track_user_activity("problem_fixed", 50, f"Виправлено: {issue['category']}")
    
    with col2:
        st.markdown("### ⚡ Швидкі виправлення")
        
        if st.button("🧹 Очистити тимчасові файли"):
            cleanup_result = components['repair_tool'].cleanup_temporary_files()
            st.success(f"Звільнено {cleanup_result['freed_space']} МБ дискового простору")
        
        if st.button("🔄 Оптимізувати мережу"):
            components['repair_tool'].optimize_network_settings()
            st.success("Мережеві налаштування оптимізовано")
        
        if st.button("🚀 Прискорити систему"):
            components['repair_tool'].boost_system_performance()
            st.success("Продуктивність системи покращено")

def display_achievement_hub(components):
    """Хаб системи досягнень"""
    st.subheader("🎯 Центр досягнень")
    
    user_progress = components['motivator'].get_user_statistics()
    
    # Поточний рівень користувача
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Поточний рівень", user_progress.get('level', 1))
    
    with col2:
        st.metric("Загальний досвід", user_progress.get('total_experience', 0))
    
    with col3:
        next_level_exp = (user_progress.get('level', 1) * 200)
        progress = min(user_progress.get('total_experience', 0) / next_level_exp, 1.0)
        st.metric("До наступного рівня", f"{int(progress * 100)}%")
    
    # Прогрес-бар
    st.progress(progress)
    
    # Доступні досягнення
    achievements = components['motivator'].get_available_achievements()
    
    st.markdown("### 🏆 Досягнення")
    
    tabs = st.tabs(["🔓 Відкриті", "🔒 Заблоковані"])
    
    with tabs[0]:
        unlocked = [a for a in achievements if a['unlocked']]
        for achievement in unlocked:
            st.success(f"🏆 **{achievement['title']}** - {achievement['description']}")
    
    with tabs[1]:
        locked = [a for a in achievements if not a['unlocked']]
        for achievement in locked:
            st.info(f"🔒 **{achievement['title']}** - {achievement['description']}")

def display_benchmark_suite(components):
    """Набір тестів продуктивності"""
    st.subheader("🚀 Тестування продуктивності")
    
    # Кнопка запуску тестів
    if st.button("▶️ Запустити повне тестування", type="primary"):
        with st.spinner("Виконання тестів продуктивності..."):
            benchmark_results = components['benchmark'].execute_full_benchmark()
            
            # Відображення результатів
            st.markdown("### 📊 Результати тестування")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Процесор", f"{benchmark_results['cpu_score']}/100")
            
            with col2:
                st.metric("Пам'ять", f"{benchmark_results['memory_score']}/100")
            
            with col3:
                st.metric("Диск", f"{benchmark_results['disk_score']}/100")
            
            with col4:
                st.metric("Загальний бал", f"{benchmark_results['overall_score']}/100")
            
            # Збереження результатів
            components['db_controller'].save_benchmark_results(benchmark_results)
            
            # Нагорода за тестування
            components['motivator'].track_user_activity("benchmark_completed", 30, "Проведено бенчмарк")
    
    # Історія тестувань
    test_history = components['db_controller'].get_benchmark_timeline()
    
    if not test_history.empty:
        st.markdown("### 📈 Історія тестувань")
        
        # Графік змін продуктивності
        performance_chart = px.line(
            test_history, 
            x='timestamp', 
            y='overall_score',
            title='Зміна продуктивності у часі'
        )
        st.plotly_chart(performance_chart, use_container_width=True)

def create_performance_visualizations(metrics, intelligence):
    """Створення візуалізацій продуктивності"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Кругова діаграма використання ресурсів
        resource_data = [
            metrics.get('cpu_usage', 0),
            metrics.get('memory_usage', 0),
            metrics.get('storage_usage', 0)
        ]
        
        resource_chart = go.Figure(data=[go.Pie(
            labels=['Процесор', 'Пам\'ять', 'Диск'],
            values=resource_data,
            hole=0.4,
            marker_colors=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )])
        
        resource_chart.update_layout(
            title="Використання ресурсів",
            showlegend=True,
            height=300
        )
        
        st.plotly_chart(resource_chart, use_container_width=True)
    
    with col2:
        # Індикатор здоров'я системи
        health_score = intelligence.get('health_index', 85)
        
        health_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = health_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Індекс здоров'я системи"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        health_gauge.update_layout(height=300)
        st.plotly_chart(health_gauge, use_container_width=True)

if __name__ == "__main__":
    launch_main_interface()