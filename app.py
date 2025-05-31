# -*- coding: utf-8 -*-
"""
TechCare AI - Інтелектуальна система моніторингу та прогнозування
Головний Streamlit додаток з AI функціональністю
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import threading
import numpy as np

# Імпорт модулів
from monitor import get_system_data
from ai_engine import AIEngine
from data_manager import DataManager
from gamification import GamificationSystem
from benchmarking import BenchmarkingSystem
from auto_repair import AutoRepairSystem
from scheduler import MaintenanceScheduler
from advanced_monitor import AdvancedSystemMonitor
from adaptive_components import AdaptiveLayout, apply_mobile_styles, responsive_dataframe

# Ініціалізація сесійного стану
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.data_manager = DataManager()
    st.session_state.ai_engine = AIEngine(st.session_state.data_manager)
    st.session_state.gamification = GamificationSystem(st.session_state.data_manager)
    st.session_state.benchmarking = BenchmarkingSystem(st.session_state.data_manager)
    st.session_state.auto_repair = AutoRepairSystem()
    st.session_state.scheduler = MaintenanceScheduler(st.session_state.data_manager)
    st.session_state.advanced_monitor = AdvancedSystemMonitor()
    st.session_state.last_update = 0

def main():
    """Головна функція додатка"""
    st.set_page_config(
        page_title="TechCare AI",
        page_icon="🖥️",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    # Адаптивні CSS стилі
    st.markdown("""
    <style>
    /* Адаптивність для мобільних пристроїв */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .stMetric {
            background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 100%);
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin: 0.25rem 0;
            border: 1px solid #e6e9ef;
        }
        
        .sidebar .sidebar-content {
            width: 100% !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.25rem !important;
        }
        
        h3 {
            font-size: 1.1rem !important;
        }
    }
    
    /* Адаптивність для планшетів */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .stMetric {
            padding: 0.75rem;
            margin: 0.375rem 0;
        }
    }
    
    /* Стилі для покращеного вигляду */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stMetric > div {
        color: white !important;
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600;
    }
    
    .stMetric [data-testid="metric-value"] {
        color: white !important;
        font-size: 1.5rem !important;
        font-weight: 700;
    }
    
    /* Адаптивна сітка */
    .metric-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    /* Стилі для карток */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    /* Адаптивні кнопки */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Адаптивні таби */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        min-width: auto;
        padding: 0.5rem 1rem;
        white-space: nowrap;
    }
    
    /* Респонсивні графіки */
    .js-plotly-plot {
        width: 100% !important;
    }
    
    .plotly {
        width: 100% !important;
    }
    
    /* Мобільна навігація */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
            overflow-x: auto;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 0.9rem;
            padding: 0.4rem 0.8rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Заголовок
    st.title("🖥️ TechCare AI")
    st.markdown("**Інтелектуальна система моніторингу та прогнозування здоров'я ПК**")
    
    # Адаптивна навігація
    # Визначення розміру екрану
    screen_size = st.selectbox(
        "📱 Розмір екрану:",
        ["🖥️ Десктоп", "📱 Мобільний", "📱 Планшет"],
        index=0,
        help="Оберіть для оптимального відображення"
    )
    
    mobile_mode = screen_size in ["📱 Мобільний", "📱 Планшет"]
    st.session_state['mobile_mode'] = mobile_mode
    
    if mobile_mode:
        # Мобільна навігація у вигляді табів
        st.markdown("### 🎯 Навігація")
        page = st.radio(
            "Оберіть розділ:",
            [
                "📊 Дашборд",
                "🤖 AI Аналітика", 
                "🔧 Авто-ремонт",
                "🏆 Геймифікація",
                "📈 Бенчмаркінг",
                "📅 Розклад",
                "📋 Детальний аналіз"
            ],
            horizontal=True if screen_size == "📱 Планшет" else False
        )
    else:
        # Десктопна навігація
        with st.sidebar:
            st.header("🎯 Навігація")
            page = st.selectbox(
                "Оберіть розділ:",
                [
                    "📊 Дашборд",
                    "🤖 AI Аналітика", 
                    "🔧 Авто-ремонт",
                    "🏆 Геймифікація",
                    "📈 Бенчмаркінг",
                    "📅 Розклад",
                    "📋 Детальний аналіз"
                ]
            )
        
        # Автоматичне оновлення
        auto_refresh = st.checkbox("Авто-оновлення (30с)", value=False)
        if auto_refresh:
            # Використовуємо st.empty() для оновлення без блокування
            placeholder = st.empty()
            with placeholder.container():
                st.info("🔄 Авто-оновлення увімкнено")
                
        # Кнопка ручного оновлення
        if st.button("🔄 Оновити дані"):
            st.rerun()
    
    # Маршрутизація сторінок
    if page == "📊 Дашборд":
        show_dashboard()
    elif page == "🤖 AI Аналітика":
        show_ai_analytics()
    elif page == "🔧 Авто-ремонт":
        show_auto_repair()
    elif page == "🏆 Геймифікація":
        show_gamification()
    elif page == "📈 Бенчмаркінг":
        show_benchmarking()
    elif page == "📅 Розклад":
        show_scheduler()
    elif page == "📋 Детальний аналіз":
        show_detailed_analysis()

def show_dashboard():
    """Головний дашборд з системними показниками"""
    st.header("📊 Системний дашборд")
    
    # Отримання поточних даних
    current_time = time.time()
    if current_time - st.session_state.last_update > 10:  # Оновлення кожні 10 секунд
        system_data = get_system_data()
        st.session_state.data_manager.save_system_data(system_data)
        st.session_state.last_update = current_time
        
        # AI прогнозування
        predictions = st.session_state.ai_engine.predict_system_health(system_data)
        st.session_state.predictions = predictions
    else:
        system_data = get_system_data()
        predictions = getattr(st.session_state, 'predictions', {})
    
    # Основні метрики - адаптивна сітка
    # На мобільних пристроях буде 2 колонки, на планшетах - 3, на десктопі - 4
    is_mobile = st.session_state.get('is_mobile', False)
    
    # Адаптивна сітка метрик на основі режиму екрану
    mobile_mode = st.session_state.get('mobile_mode', False)
    
    # Застосування мобільних стилів при потребі
    if mobile_mode:
        apply_mobile_styles()
    
    # Створення адаптивного макету
    adaptive_layout = AdaptiveLayout(mobile_mode)
    
    # Підготовка даних для метрик
    metrics_data = [
        {
            'label': '🌡️ Температура/CPU',
            'value': f"{float(system_data.get('cpu_temp') or system_data.get('cpu_percent') or 0):.1f}{'°C' if system_data.get('cpu_temp') else '%'}",
            'delta': predictions.get('temp_trend', 0)
        },
        {
            'label': '💾 RAM',
            'value': f"{float(system_data.get('ram_percent', 0)):.1f}%",
            'delta': predictions.get('ram_trend', 0)
        },
        {
            'label': '💿 Диск',
            'value': f"{float(system_data.get('disk_percent', 0)):.1f}%",
            'delta': predictions.get('disk_trend', 0)
        },
        {
            'label': '❤️ Здоров\'я ПК',
            'value': f"{predictions.get('health_score', 85)}/100",
            'delta': predictions.get('health_trend', 0)
        }
    ]
    
    # Відображення метрик через адаптивний компонент
    adaptive_layout.create_metric_grid(metrics_data)
    
    # AI Попередження
    if predictions.get('warnings'):
        st.warning("⚠️ AI виявив потенційні проблеми:")
        for warning in predictions['warnings']:
            st.error(f"• {warning}")
    
    # Графіки трендів
    st.subheader("📈 Тренди продуктивності")
    
    # Отримання історичних даних
    historical_data = st.session_state.data_manager.get_historical_data(hours=24)
    
    if not historical_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Графік температури/CPU
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=historical_data['timestamp'],
                y=historical_data['cpu_temp'].fillna(historical_data['cpu_percent']),
                mode='lines+markers',
                name='Температура/CPU',
                line=dict(color='#FF6B6B')
            ))
            fig_temp.update_layout(
                title="Температура/CPU за 24 години",
                xaxis_title="Час",
                yaxis_title="Значення",
                height=300
            )
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col2:
            # Графік RAM
            fig_ram = go.Figure()
            fig_ram.add_trace(go.Scatter(
                x=historical_data['timestamp'],
                y=historical_data['ram_percent'],
                mode='lines+markers',
                name='RAM',
                line=dict(color='#4ECDC4')
            ))
            fig_ram.update_layout(
                title="Використання RAM за 24 години",
                xaxis_title="Час",
                yaxis_title="Відсоток (%)",
                height=300
            )
            st.plotly_chart(fig_ram, use_container_width=True)
    
    # Час роботи системи
    uptime_hours = system_data['uptime_seconds'] / 3600
    st.info(f"⏰ Час роботи системи: {system_data['uptime_str']}")
    
    if uptime_hours > 24:
        st.warning("💡 Рекомендуємо перезапустити систему для оптимальної продуктивності")

def show_ai_analytics():
    """Сторінка AI аналітики та прогнозів"""
    st.header("🤖 AI Аналітика та прогнозування")
    
    # Поточний AI аналіз
    system_data = get_system_data()
    ai_analysis = st.session_state.ai_engine.analyze_system_patterns(system_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔮 Прогноз проблем")
        predictions = st.session_state.ai_engine.predict_failures()
        
        if predictions:
            for prediction in predictions:
                probability = prediction['probability']
                issue_type = prediction['type']
                time_to_failure = prediction['estimated_time']
                
                # Колір на основі ймовірності
                if probability > 0.7:
                    st.error(f"⚠️ **{issue_type}**")
                    st.error(f"Ймовірність: {probability:.1%}")
                    st.error(f"Очікуваний час: {time_to_failure}")
                elif probability > 0.4:
                    st.warning(f"⚡ **{issue_type}**")
                    st.warning(f"Ймовірність: {probability:.1%}")
                    st.warning(f"Очікуваний час: {time_to_failure}")
                else:
                    st.info(f"✅ **{issue_type}**")
                    st.info(f"Ймовірність: {probability:.1%}")
        else:
            st.success("✅ AI не виявив потенційних проблем найближчим часом")
    
    with col2:
        st.subheader("📊 Аналіз патернів")
        
        # Показ виявлених патернів
        patterns = ai_analysis.get('patterns', [])
        if patterns:
            for pattern in patterns:
                st.write(f"• **{pattern['type']}**: {pattern['description']}")
                st.write(f"  Впевненість: {pattern['confidence']:.1%}")
        else:
            st.info("Збираємо дані для аналізу патернів...")
    
    # Рекомендації AI
    st.subheader("💡 AI Рекомендації")
    recommendations = st.session_state.ai_engine.get_personalized_recommendations(system_data)
    
    for i, rec in enumerate(recommendations):
        priority_icon = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
        
        with st.expander(f"{priority_icon} {rec['title']}"):
            st.write(rec['description'])
            st.write(f"**Очікуваний ефект:** {rec['expected_impact']}")
            
            if st.button(f"Застосувати", key=f"apply_rec_{i}"):
                if rec.get('auto_applicable'):
                    result = st.session_state.auto_repair.apply_recommendation(rec)
                    if result['success']:
                        st.success(f"✅ {result['message']}")
                    else:
                        st.error(f"❌ {result['message']}")
                else:
                    st.info("Ця рекомендація потребує ручного виконання")

def show_auto_repair():
    """Сторінка автоматичного ремонту"""
    st.header("🔧 Система авто-ремонту")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Поточна діагностика")
        
        if st.button("▶️ Запустити повну діагностику"):
            with st.spinner("Виконується діагностика..."):
                time.sleep(2)  # Симуляція тривалості діагностики
                issues = st.session_state.auto_repair.diagnose_system()
                
                if issues:
                    st.warning(f"Виявлено {len(issues)} проблем:")
                    for issue in issues:
                        st.write(f"• **{issue['type']}**: {issue['description']}")
                        st.write(f"  Критичність: {issue['severity']}")
                        
                        if issue.get('auto_fixable'):
                            if st.button(f"🔧 Автоматично виправити", key=f"fix_{issue['id']}"):
                                result = st.session_state.auto_repair.auto_fix_issue(issue)
                                if result['success']:
                                    st.success(f"✅ {result['message']}")
                                else:
                                    st.error(f"❌ {result['message']}")
                else:
                    st.success("✅ Проблем не виявлено!")
    
    with col2:
        st.subheader("📋 Історія ремонтів")
        
        repair_history = st.session_state.auto_repair.get_repair_history()
        
        if repair_history:
            for repair in repair_history[-5:]:  # Останні 5 ремонтів
                date = repair['timestamp'].strftime("%d.%m.%Y %H:%M")
                status_icon = "✅" if repair['success'] else "❌"
                
                with st.expander(f"{status_icon} {repair['issue_type']} - {date}"):
                    st.write(f"**Проблема:** {repair['description']}")
                    st.write(f"**Дія:** {repair['action_taken']}")
                    st.write(f"**Результат:** {repair['result']}")
        else:
            st.info("Історія ремонтів пуста")
    
    # Налаштування авто-ремонту
    st.subheader("⚙️ Налаштування")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        auto_fix_enabled = st.checkbox("Автоматичний ремонт", value=True)
        st.session_state.auto_repair.set_auto_fix_enabled(auto_fix_enabled)
    
    with col2:
        fix_severity = st.selectbox(
            "Автофікс для рівня:",
            ["Низький", "Середній", "Високий"],
            index=1
        )
    
    with col3:
        notify_repairs = st.checkbox("Сповіщення про ремонти", value=True)

def show_gamification():
    """Сторінка геймифікації"""
    st.header("🏆 Система досягнень")
    
    # Поточний статус гравця
    user_stats = st.session_state.gamification.get_user_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="⭐ Рівень",
            value=user_stats['level'],
            delta=f"+{user_stats['exp_to_next']} до наступного"
        )
    
    with col2:
        st.metric(
            label="🎯 Очки досвіду",
            value=user_stats['total_exp'],
            delta=f"+{user_stats['today_exp']} сьогодні"
        )
    
    with col3:
        st.metric(
            label="🏅 Досягнення",
            value=f"{user_stats['achievements_unlocked']}/{user_stats['total_achievements']}"
        )
    
    with col4:
        st.metric(
            label="🔥 Streak",
            value=f"{user_stats['streak']} днів",
            delta="+1" if user_stats['streak_active'] else "0"
        )
    
    # Прогрес-бар досвіду
    exp_progress = user_stats['current_level_exp'] / user_stats['exp_for_next_level']
    st.progress(exp_progress)
    st.caption(f"Прогрес до рівня {user_stats['level'] + 1}: {user_stats['current_level_exp']}/{user_stats['exp_for_next_level']} XP")
    
    # Вкладки
    tab1, tab2, tab3, tab4 = st.tabs(["🏅 Досягнення", "📊 Статистика", "🎁 Нагороди", "🏆 Таблиця лідерів"])
    
    with tab1:
        achievements = st.session_state.gamification.get_achievements()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔓 Відкриті досягнення")
            unlocked = [a for a in achievements if a['unlocked']]
            
            for achievement in unlocked:
                st.success(f"🏅 **{achievement['name']}**")
                st.write(achievement['description'])
                st.write(f"Отримано: {achievement['unlocked_date']}")
                st.write(f"Нагорода: +{achievement['exp_reward']} XP")
                st.write("---")
        
        with col2:
            st.subheader("🔒 Заблоковані досягнення")
            locked = [a for a in achievements if not a['unlocked']]
            
            for achievement in locked:
                progress = achievement.get('progress', 0)
                target = achievement.get('target', 100)
                
                st.info(f"🔒 **{achievement['name']}**")
                st.write(achievement['description'])
                st.progress(progress / target)
                st.write(f"Прогрес: {progress}/{target}")
                st.write(f"Нагорода: +{achievement['exp_reward']} XP")
                st.write("---")
    
    with tab2:
        st.subheader("📈 Ваша статистика")
        
        # Графік активності
        activity_data = st.session_state.gamification.get_activity_history()
        
        if not activity_data.empty:
            fig = px.line(
                activity_data, 
                x='date', 
                y='exp_earned',
                title="Досвід за останні 30 днів"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Статистика по категоріях
        col1, col2 = st.columns(2)
        
        with col1:
            category_stats = st.session_state.gamification.get_category_stats()
            fig_pie = px.pie(
                values=list(category_stats.values()),
                names=list(category_stats.keys()),
                title="Розподіл активності по категоріях"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("🏃‍♂️ Streak статистика")
            streak_stats = st.session_state.gamification.get_streak_stats()
            
            st.write(f"• Поточний streak: {streak_stats['current']} днів")
            st.write(f"• Найдовший streak: {streak_stats['longest']} днів") 
            st.write(f"• Середній streak: {streak_stats['average']:.1f} днів")
            st.write(f"• Загальна кількість streaks: {streak_stats['total_streaks']}")
    
    with tab3:
        st.subheader("🎁 Нагороди та винагороди")
        
        available_rewards = st.session_state.gamification.get_available_rewards()
        
        for reward in available_rewards:
            cost = reward['cost']
            user_points = user_stats.get('reward_points', 0)
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{reward['name']}**")
                st.write(reward['description'])
            
            with col2:
                st.write(f"💰 {cost} балів")
            
            with col3:
                if user_points >= cost:
                    if st.button("🛒 Купити", key=f"buy_{reward['id']}"):
                        result = st.session_state.gamification.redeem_reward(reward['id'])
                        if result['success']:
                            st.success("✅ Нагороду отримано!")
                            st.rerun()
                        else:
                            st.error(f"❌ {result['message']}")
                else:
                    st.button("🔒 Недостатньо балів", disabled=True, key=f"disabled_{reward['id']}")
    
    with tab4:
        st.subheader("🏆 Таблиця лідерів")
        
        leaderboard = st.session_state.gamification.get_leaderboard()
        
        # Фейкові дані для демонстрації (в реальному застосунку це були б дані інших користувачів)
        demo_leaderboard = [
            {"rank": 1, "username": "Ви", "level": user_stats['level'], "exp": user_stats['total_exp'], "achievements": user_stats['achievements_unlocked']},
            {"rank": 2, "username": "TechMaster", "level": 15, "exp": 45000, "achievements": 23},
            {"rank": 3, "username": "PCExpert", "level": 12, "exp": 38000, "achievements": 20},
            {"rank": 4, "username": "SystemGuru", "level": 11, "exp": 35000, "achievements": 18},
            {"rank": 5, "username": "ComputerPro", "level": 10, "exp": 32000, "achievements": 16}
        ]
        
        for player in demo_leaderboard:
            if player['username'] == "Ви":
                st.success(f"🏆 #{player['rank']} **{player['username']}** - Рівень {player['level']} ({player['exp']} XP, {player['achievements']} досягнень)")
            else:
                st.write(f"#{player['rank']} {player['username']} - Рівень {player['level']} ({player['exp']} XP, {player['achievements']} досягнень)")

def show_benchmarking():
    """Сторінка бенчмаркінга"""
    st.header("📈 Бенчмаркінг та порівняння")
    
    # Поточні результати
    current_results = st.session_state.benchmarking.get_current_benchmark()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="⚡ Загальна оцінка",
            value=f"{current_results['overall_score']}/100",
            delta=f"{current_results['score_change']:+.1f}"
        )
    
    with col2:
        st.metric(
            label="🎯 Ваш рейтинг",
            value=f"#{current_results['rank']}",
            delta=f"{current_results['rank_change']:+d}"
        )
    
    with col3:
        st.metric(
            label="📊 Процентиль",
            value=f"{current_results['percentile']:.0f}%",
            delta=f"{current_results['percentile_change']:+.1f}%"
        )
    
    # Детальні результати
    st.subheader("📋 Детальні результати бенчмарку")
    
    benchmark_data = st.session_state.benchmarking.get_detailed_results()
    
    # Радарна діаграма
    categories = ['CPU', 'RAM', 'Диск', 'Мережа', 'Стабільність', 'Ефективність']
    category_mapping = {
        'CPU': 'cpu',
        'RAM': 'ram', 
        'Диск': 'disk',
        'Мережа': 'network',
        'Стабільність': 'stability',
        'Ефективність': 'efficiency'
    }
    
    your_scores = []
    avg_scores = []
    
    for cat in categories:
        key = category_mapping[cat]
        if key in benchmark_data:
            your_scores.append(benchmark_data[key]['your_score'])
            avg_scores.append(benchmark_data[key]['average_score'])
        else:
            your_scores.append(50)  # Резервне значення
            avg_scores.append(50)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=your_scores,
        theta=categories,
        fill='toself',
        name='Ваш результат',
        line_color='#00DDEB'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=avg_scores,
        theta=categories,
        fill='toself',
        name='Середній результат',
        line_color='#FF6B6B',
        opacity=0.6
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Порівняння з іншими системами"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Таблиця з детальними показниками
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💪 Ваші сильні сторони")
        strengths = st.session_state.benchmarking.get_strengths()
        for strength in strengths:
            st.success(f"✅ **{strength['category']}**: {strength['description']}")
    
    with col2:
        st.subheader("🔧 Області для покращення")
        improvements = st.session_state.benchmarking.get_improvement_areas()
        for improvement in improvements:
            st.warning(f"⚡ **{improvement['category']}**: {improvement['suggestion']}")
    
    # Історія бенчмарків
    st.subheader("📈 Історія результатів")
    
    history_data = st.session_state.benchmarking.get_history()
    
    if not history_data.empty:
        fig_history = px.line(
            history_data,
            x='timestamp',
            y='overall_score',
            title="Зміна загального рейтингу в часі"
        )
        st.plotly_chart(fig_history, use_container_width=True)
    
    # Кнопка запуску нового бенчмарку
    if st.button("🚀 Запустити новий бенчмарк"):
        with st.spinner("Виконується бенчмарк..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.05)
                progress_bar.progress(i + 1)
            
            new_results = st.session_state.benchmarking.run_benchmark()
            st.success("✅ Бенчмарк завершено!")
            st.info(f"Ваш новий результат: {new_results['overall_score']}/100")
            st.rerun()

def show_scheduler():
    """Сторінка планувальника обслуговування"""
    st.header("📅 Розклад обслуговування")
    
    # Поточні завдання
    st.subheader("📋 Сьогоднішні завдання")
    
    today_tasks = st.session_state.scheduler.get_today_tasks()
    
    if today_tasks:
        for task in today_tasks:
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                status_icon = "✅" if task['completed'] else "⏳"
                priority_icon = "🔴" if task['priority'] == 'high' else "🟡" if task['priority'] == 'medium' else "🟢"
                st.write(f"{status_icon} {priority_icon} **{task['title']}**")
                st.write(task['description'])
            
            with col2:
                st.write(f"⏰ {task['scheduled_time']}")
                st.write(f"📊 {task['category']}")
            
            with col3:
                if not task['completed']:
                    if st.button("✅ Виконано", key=f"complete_{task['id']}"):
                        st.session_state.scheduler.mark_task_completed(task['id'])
                        st.rerun()
                
                if st.button("⏸️ Відкласти", key=f"postpone_{task['id']}"):
                    st.session_state.scheduler.postpone_task(task['id'], hours=24)
                    st.rerun()
    else:
        st.success("🎉 Всі завдання на сьогодні виконані!")
    
    # Календар завдань
    st.subheader("📅 Календар на тиждень")
    
    weekly_schedule = st.session_state.scheduler.get_weekly_schedule()
    
    # Створення календарної таблиці
    days = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя']
    
    for day in days:
        with st.expander(f"📅 {day}"):
            day_tasks = weekly_schedule.get(day, [])
            
            if day_tasks:
                for task in day_tasks:
                    priority_icon = "🔴" if task['priority'] == 'high' else "🟡" if task['priority'] == 'medium' else "🟢"
                    st.write(f"{priority_icon} **{task['time']}** - {task['title']}")
                    st.write(f"   {task['description']}")
            else:
                st.write("📴 Завдань немає")
    
    # Налаштування розкладу
    st.subheader("⚙️ Налаштування розкладу")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Автоматичні завдання:**")
        
        auto_cleanup = st.checkbox("Щоденне очищення", value=True)
        auto_defrag = st.checkbox("Тижнева дефрагментація", value=True)
        auto_updates = st.checkbox("Перевірка оновлень", value=True)
        auto_backup = st.checkbox("Резервне копіювання", value=False)
        
        # Збереження налаштувань
        settings = {
            'auto_cleanup': auto_cleanup,
            'auto_defrag': auto_defrag,
            'auto_updates': auto_updates,
            'auto_backup': auto_backup
        }
        st.session_state.scheduler.update_settings(settings)
    
    with col2:
        st.write("**Час виконання:**")
        
        cleanup_time = st.time_input("Час очищення", value=datetime.strptime("02:00", "%H:%M").time())
        defrag_day = st.selectbox("День дефрагментації", days, index=6)
        update_frequency = st.selectbox("Частота оновлень", ["Щодня", "Щотижня", "Щомісяця"], index=1)
        
        if st.button("💾 Зберегти налаштування"):
            time_settings = {
                'cleanup_time': cleanup_time.strftime("%H:%M"),
                'defrag_day': defrag_day,
                'update_frequency': update_frequency
            }
            st.session_state.scheduler.update_time_settings(time_settings)
            st.success("✅ Налаштування збережено!")
    
    # Додавання власного завдання
    st.subheader("➕ Додати власне завдання")
    
    with st.form("add_task"):
        task_title = st.text_input("Назва завдання")
        task_description = st.text_area("Опис завдання")
        task_date = st.date_input("Дата виконання")
        task_time = st.time_input("Час виконання")
        task_priority = st.selectbox("Пріоритет", ["Низький", "Середній", "Високий"])
        task_category = st.selectbox("Категорія", ["Очищення", "Оптимізація", "Резервування", "Оновлення", "Інше"])
        
        if st.form_submit_button("➕ Додати завдання"):
            task_data = {
                'title': task_title,
                'description': task_description,
                'date': task_date,
                'time': task_time,
                'priority': task_priority.lower(),
                'category': task_category
            }
            
            result = st.session_state.scheduler.add_custom_task(task_data)
            
            if result['success']:
                st.success("✅ Завдання додано до розкладу!")
                st.rerun()
            else:
                st.error(f"❌ {result['message']}")

def show_detailed_analysis():
    """Сторінка детального аналізу"""
    st.header("📋 Детальний аналіз системи")
    
    # Розширений аналіз
    advanced_data = st.session_state.advanced_monitor.get_comprehensive_analysis()
    
    # Вкладки для різних видів аналізу
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 Апаратне забезпечення", "💿 Диски та файли", "🌐 Мережа", "🔒 Безпека"])
    
    with tab1:
        st.subheader("⚙️ Аналіз апаратного забезпечення")
        
        # Інформація про процесор
        cpu_info = advanced_data.get('cpu_analysis', {})
        st.write("**🖥️ Процесор:**")
        st.write(f"• Модель: {cpu_info.get('model', 'Невідомо')}")
        st.write(f"• Ядра: {cpu_info.get('cores', 'Невідомо')}")
        st.write(f"• Частота: {cpu_info.get('frequency', 'Невідомо')} MHz")
        st.write(f"• Завантаження: {cpu_info.get('usage', 0):.1f}%")
        
        # Температурний аналіз
        thermal_analysis = advanced_data.get('thermal_analysis', {})
        st.write("**🌡️ Термальний аналіз:**")
        st.write(f"• Поточна температура: {thermal_analysis.get('current_temp', 'Н/Д')}")
        st.write(f"• Максимальна за добу: {thermal_analysis.get('max_temp_24h', 'Н/Д')}")
        st.write(f"• Стан термопасти: {thermal_analysis.get('paste_condition', 'Невідомо')}")
        
        # Вентилятори
        fan_analysis = advanced_data.get('fan_analysis', {})
        st.write("**🌪️ Система охолодження:**")
        for fan in fan_analysis.get('fans', []):
            st.write(f"• {fan['name']}: {fan['speed']} RPM ({fan['status']})")
    
    with tab2:
        st.subheader("💿 Аналіз дисків та файлової системи")
        
        disk_analysis = advanced_data.get('disk_analysis', {})
        
        # Інформація про диски
        for disk in disk_analysis.get('disks', []):
            st.write(f"**📀 Диск {disk['device']}:**")
            st.write(f"• Тип: {disk['type']}")
            st.write(f"• Розмір: {disk['total_size']}")
            st.write(f"• Використано: {disk['used_space']} ({disk['usage_percent']:.1f}%)")
            st.write(f"• Файлова система: {disk['filesystem']}")
            st.write(f"• Здоров'я: {disk['health_status']}")
            
            # Прогрес-бар використання
            st.progress(disk['usage_percent'] / 100)
            st.write("---")
        
        # Аналіз великих файлів
        large_files = disk_analysis.get('large_files', [])
        if large_files:
            st.write("**📁 Найбільші файли:**")
            for file_info in large_files[:10]:
                st.write(f"• {file_info['path']} - {file_info['size']}")
        
        # Аналіз фрагментації
        fragmentation = disk_analysis.get('fragmentation', {})
        st.write(f"**📊 Фрагментація:** {fragmentation.get('level', 'Невідомо')}")
        
        if fragmentation.get('recommendation'):
            st.info(f"💡 {fragmentation['recommendation']}")
    
    with tab3:
        st.subheader("🌐 Мережевий аналіз")
        
        network_analysis = advanced_data.get('network_analysis', {})
        
        # Швидкість підключення
        speed_test = network_analysis.get('speed_test', {})
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⬇️ Швидкість завантаження", f"{speed_test.get('download', 0):.1f} Mbps")
        
        with col2:
            st.metric("⬆️ Швидкість відвантаження", f"{speed_test.get('upload', 0):.1f} Mbps")
        
        with col3:
            st.metric("📡 Пінг", f"{speed_test.get('ping', 0):.0f} ms")
        
        # Активні з'єднання
        connections = network_analysis.get('connections', [])
        st.write(f"**🔗 Активні з'єднання:** {len(connections)}")
        
        if connections:
            connection_df = pd.DataFrame(connections)
            st.dataframe(connection_df, use_container_width=True)
        
        # DNS аналіз
        dns_analysis = network_analysis.get('dns_analysis', {})
        st.write("**🔍 DNS аналіз:**")
        st.write(f"• Час відгуку: {dns_analysis.get('response_time', 'Н/Д')} ms")
        st.write(f"• Сервер: {dns_analysis.get('server', 'Невідомо')}")
    
    with tab4:
        st.subheader("🔒 Аналіз безпеки")
        
        security_analysis = advanced_data.get('security_analysis', {})
        
        # Загальна оцінка безпеки
        security_score = security_analysis.get('security_score', 0)
        st.metric("🛡️ Рівень безпеки", f"{security_score}/100")
        
        # Перевірки безпеки
        security_checks = security_analysis.get('checks', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**✅ Пройдені перевірки:**")
            for check, status in security_checks.items():
                if status:
                    st.success(f"• {check}")
        
        with col2:
            st.write("**❌ Невдалі перевірки:**")
            for check, status in security_checks.items():
                if not status:
                    st.error(f"• {check}")
        
        # Рекомендації з безпеки
        security_recommendations = security_analysis.get('recommendations', [])
        if security_recommendations:
            st.write("**💡 Рекомендації з безпеки:**")
            for rec in security_recommendations:
                st.warning(f"• {rec}")
        
        # Останні події безпеки
        security_events = security_analysis.get('recent_events', [])
        if security_events:
            st.write("**📋 Останні події безпеки:**")
            for event in security_events[-5:]:
                event_time = event['timestamp'].strftime("%d.%m.%Y %H:%M")
                st.write(f"• {event_time}: {event['description']}")

if __name__ == "__main__":
    main()
