# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Моя дипломна програма
Написав сам для контролю комп'ютера
TODO: додати більше функцій коли буде час
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# мої модулі
from simple_monitor import get_system_data
from data_manager import DataManager
from simple_ai import SimpleAI
from simple_achievements import SimpleAchievements
from simple_tests import SimpleTests
from simple_repair import SimpleRepair

# мої іконки
from icons import *
from student_style import *

def init_my_app():
    """Ініціалізація моєї програми"""
    # TODO: покращити це пізніше
    if 'data_manager' not in st.session_state:
        st.session_state.data_manager = DataManager()
        st.session_state.ai_engine = SimpleAI(st.session_state.data_manager)
        st.session_state.achievements = SimpleAchievements(st.session_state.data_manager)
        st.session_state.tests = SimpleTests(st.session_state.data_manager)
        st.session_state.repair = SimpleRepair()

def show_main_page():
    """Головна сторінка"""
    st.markdown("## Головна панель")
    st.markdown("*Тут показуються основні дані про комп'ютер*")
    
    # отримуємо дані
    data = get_system_data()
    
    # простий спосіб показати метрики
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(get_simple_metric("CPU", f"{data['cpu_percent']:.1f}%", get_cpu_icon()), unsafe_allow_html=True)
    
    with col2:
        st.markdown(get_simple_metric("RAM", f"{data['ram_percent']:.1f}%", get_ram_icon()), unsafe_allow_html=True)
    
    with col3:
        st.markdown(get_simple_metric("Диск", f"{data['disk_percent']:.1f}%", get_disk_icon()), unsafe_allow_html=True)
    
    # AI аналіз
    st.markdown("### AI аналіз")
    warnings = st.session_state.ai_engine.predict_system_health(data)
    
    if warnings.get('warnings', []):
        st.warning("Знайдені проблеми:")
        for warning in warnings['warnings']:
            st.write(f"• {warning}")
    else:
        st.success("Все працює нормально!")
    
    # зберігаємо дані в базу
    st.session_state.data_manager.save_system_data(data)
    
    # TODO: додати графіки

def show_ai_page():
    """Сторінка AI"""
    st.markdown("## AI Аналітика")
    st.markdown("*Тут штучний інтелект аналізує систему*")
    
    data = get_system_data()
    prediction = st.session_state.ai_engine.predict_system_health(data)
    
    # показуємо скор здоров'я
    health_score = prediction.get('health_score', 85)
    st.metric("Індекс здоров'я системи", f"{health_score}%")
    
    # прогнози
    if prediction.get('predictions'):
        st.subheader("Прогнози")
        for pred in prediction['predictions']:
            st.info(f"📊 {pred}")

def show_repair_page():
    """Сторінка ремонту"""
    st.markdown("## Автоматичний ремонт")
    st.markdown("*Програма сама знаходить та виправляє проблеми*")
    
    if st.button("Діагностувати систему"):
        with st.spinner("Шукаю проблеми..."):
            issues = st.session_state.repair.diagnose_system()
        
        if issues:
            st.warning(f"Знайдено {len(issues)} проблем:")
            for i, issue in enumerate(issues, 1):
                st.write(f"{i}. {issue['description']}")
                if issue.get('fixable') and st.button(f"Виправити #{i}"):
                    result = st.session_state.repair.auto_fix_issue(issue)
                    if result:
                        st.success("Виправлено!")
                    else:
                        st.error("Не вдалося виправити")
        else:
            st.success("Проблем не знайдено!")

def show_achievements_page():
    """Сторінка досягнень"""
    st.markdown("## Досягнення")
    st.markdown("*Як в іграх - набираєш очки за використання програми*")
    
    # статистика користувача
    stats = st.session_state.data_manager.get_user_stats()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Рівень", stats.get('level', 1))
    with col2:
        st.metric("Очки", stats.get('total_points', 0))
    
    # прогрес бар
    current_points = stats.get('total_points', 0)
    points_to_next = ((stats.get('level', 1)) * 100) - current_points
    progress = min(current_points % 100 / 100, 1.0)
    st.progress(progress)
    st.write(f"До наступного рівня: {max(0, points_to_next)} очок")

def show_tests_page():
    """Сторінка тестів"""
    st.markdown("## Тести швидкості")
    st.markdown("*Перевіряє наскільки швидкий твій комп'ютер*")
    
    if st.button("Запустити тест"):
        with st.spinner("Тестую..."):
            results = st.session_state.tests.run_benchmark()
        
        st.success("Тест завершено!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CPU", f"{results.get('cpu_score', 0):.0f}/100")
        with col2:
            st.metric("RAM", f"{results.get('ram_score', 0):.0f}/100")
        with col3:
            st.metric("Загальний", f"{results.get('overall_score', 0):.0f}/100")

def main():
    """Головна функція моєї програми"""
    st.set_page_config(
        page_title="SystemWatch Pro",
        layout="wide"
    )
    
    # ініціалізація
    init_my_app()
    
    # заголовок
    col1, col2 = st.columns([1, 10])
    with col1:
        st.markdown(get_dashboard_icon(), unsafe_allow_html=True)
    with col2:
        st.title("SystemWatch Pro")
        st.markdown("### Моя програма для моніторингу комп'ютера")
    
    # навігація (без емоджі)
    with st.sidebar:
        st.header("Меню")
        
        # простий список сторінок
        page = st.selectbox(
            "Оберіть розділ:",
            [
                "Головна",
                "AI Аналітика", 
                "Ремонт",
                "Досягнення",
                "Тести"
            ]
        )
        
        # кнопка оновлення
        if st.button("Оновити дані"):
            st.rerun()
    
    # показуємо вибрану сторінку
    if page == "Головна":
        show_main_page()
    elif page == "AI Аналітика":
        show_ai_page()
    elif page == "Ремонт":
        show_repair_page()
    elif page == "Досягнення":
        show_achievements_page()
    elif page == "Тести":
        show_tests_page()

if __name__ == "__main__":
    main()