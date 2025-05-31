# -*- coding: utf-8 -*-
"""
SystemWatch Pro - Модуль адаптивного користувацького інтерфейсу
Створення респонсивних компонентів для різних пристроїв
"""

import streamlit as st

class ResponsiveInterface:
    """Клас для створення адаптивного інтерфейсу"""
    
    def __init__(self, mobile_mode=False):
        self.is_mobile_view = mobile_mode
        self.device_type = self._detect_device_type()
    
    def _detect_device_type(self):
        """Визначення типу пристрою"""
        if self.is_mobile_view:
            return "mobile"
        else:
            return "desktop"
    
    def render_metric_dashboard(self, indicators_data):
        """Відображення панелі показників з адаптивним макетом"""
        
        if self.is_mobile_view:
            # Мобільний макет: 2x2 сітка
            for i in range(0, len(indicators_data), 2):
                col1, col2 = st.columns(2)
                
                if i < len(indicators_data):
                    with col1:
                        self._render_single_metric(indicators_data[i])
                
                if i + 1 < len(indicators_data):
                    with col2:
                        self._render_single_metric(indicators_data[i + 1])
        else:
            # Десктопний макет: всі показники в ряд
            columns = st.columns(len(indicators_data))
            for idx, metric in enumerate(indicators_data):
                with columns[idx]:
                    self._render_single_metric(metric)
    
    def _render_single_metric(self, metric_info):
        """Відображення одного показника"""
        st.metric(
            label=metric_info['label'],
            value=metric_info['value'],
            delta=metric_info.get('trend')
        )
    
    def create_adaptive_chart(self, chart_figure, chart_title=""):
        """Створення адаптивного графіка"""
        
        if self.is_mobile_view:
            # Налаштування для мобільних пристроїв
            chart_figure.update_layout(
                height=350,
                font=dict(size=10),
                title_font_size=14,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(l=15, r=15, t=40, b=15)
            )
        else:
            # Налаштування для десктопу
            chart_figure.update_layout(
                height=450,
                font=dict(size=12),
                title_font_size=16,
                margin=dict(l=25, r=25, t=50, b=25)
            )
        
        st.plotly_chart(chart_figure, use_container_width=True)
    
    def create_information_cards(self, cards_content):
        """Створення інформаційних карток"""
        
        if self.is_mobile_view:
            # Мобільний режим: по одній картці в ряд
            for card in cards_content:
                self._render_info_card(card)
        else:
            # Десктопний режим: кілька карток в ряд
            cards_per_row = min(3, len(cards_content))
            columns = st.columns(cards_per_row)
            
            for idx, card in enumerate(cards_content):
                with columns[idx % cards_per_row]:
                    self._render_info_card(card)
    
    def _render_info_card(self, card_data):
        """Відображення інформаційної картки"""
        st.markdown(f"""
        <div class="info-card-container">
            <h4>{card_data['title']}</h4>
            <p>{card_data['content']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def create_tab_navigation(self, tab_names):
        """Створення табової навігації"""
        
        if self.is_mobile_view:
            # Компактні таби для мобільних
            formatted_tabs = [f"📱 {tab}" for tab in tab_names]
        else:
            # Повні назви для десктопу
            formatted_tabs = tab_names
        
        return st.tabs(formatted_tabs)

def mobile_optimizations():
    """Застосування оптимізацій для мобільних пристроїв"""
    
    st.markdown("""
    <style>
    /* Мобільні оптимізації */
    .mobile-container {
        padding: 0.75rem;
        max-width: 100%;
    }
    
    .mobile-metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .info-card-container {
        background: white;
        padding: 1.25rem;
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        margin: 0.75rem 0;
        border-left: 4px solid #667eea;
    }
    
    .mobile-action-button {
        width: 100%;
        padding: 0.875rem;
        border-radius: 8px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        font-weight: 600;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .mobile-action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Адаптивні заголовки */
    @media (max-width: 768px) {
        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.15rem !important; }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem !important;
            padding: 0.4rem 0.7rem !important;
        }
        
        .stMetric {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin: 0.5rem 0;
        }
    }
    
    /* Анімації для покращення UX */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hover-effect:hover {
        transform: scale(1.02);
        transition: transform 0.2s ease;
    }
    </style>
    """, unsafe_allow_html=True)

def create_compact_navigation(page_options):
    """Створення компактної навігації"""
    
    return st.radio(
        "Навігація:",
        page_options,
        horizontal=True,
        label_visibility="collapsed"
    )

def adaptive_tables(dataframe, mobile_view=False):
    """Адаптивне відображення таблиць даних"""
    
    if mobile_view and not dataframe.empty:
        # Обмеження колонок для мобільних пристроїв
        if len(dataframe.columns) > 4:
            # Показ основних колонок
            main_columns = dataframe.iloc[:, :4]
            st.dataframe(main_columns, use_container_width=True)
            
            # Кнопка для розгортання всіх даних
            if st.button("📋 Показати всі колонки"):
                st.dataframe(dataframe, use_container_width=True)
        else:
            st.dataframe(dataframe, use_container_width=True)
    else:
        st.dataframe(dataframe, use_container_width=True)

def render_status_indicator(status_value, status_type="performance"):
    """Відображення індикатора статусу"""
    
    if status_type == "performance":
        if status_value >= 90:
            icon = "🟢"
            label = "Відмінно"
            color = "#4CAF50"
        elif status_value >= 70:
            icon = "🟡"
            label = "Добре"
            color = "#FF9800"
        elif status_value >= 50:
            icon = "🟠"
            label = "Задовільно"
            color = "#FF5722"
        else:
            icon = "🔴"
            label = "Потребує уваги"
            color = "#F44336"
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; padding: 0.5rem;">
        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
        <span style="color: {color}; font-weight: bold;">{label} ({status_value}%)</span>
    </div>
    """, unsafe_allow_html=True)

def create_progress_visualization(current_value, max_value, label="Прогрес"):
    """Створення візуалізації прогресу"""
    
    progress_percentage = min(current_value / max_value, 1.0) if max_value > 0 else 0
    
    st.markdown(f"**{label}**")
    st.progress(progress_percentage)
    st.caption(f"{current_value} / {max_value} ({progress_percentage*100:.1f}%)")

def apply_theme_customization(theme_name="default"):
    """Застосування кастомної теми"""
    
    theme_styles = {
        "default": {
            "primary_color": "#667eea",
            "secondary_color": "#764ba2",
            "background_color": "#f8f9fa",
            "text_color": "#333333"
        },
        "dark": {
            "primary_color": "#6c5ce7",
            "secondary_color": "#a29bfe",
            "background_color": "#2d3436",
            "text_color": "#ddd"
        },
        "nature": {
            "primary_color": "#00b894",
            "secondary_color": "#00cec9",
            "background_color": "#f1f2f6",
            "text_color": "#2d3436"
        }
    }
    
    selected_theme = theme_styles.get(theme_name, theme_styles["default"])
    
    st.markdown(f"""
    <style>
    .custom-theme {{
        --primary-color: {selected_theme['primary_color']};
        --secondary-color: {selected_theme['secondary_color']};
        --background-color: {selected_theme['background_color']};
        --text-color: {selected_theme['text_color']};
    }}
    
    .themed-container {{
        background: var(--background-color);
        color: var(--text-color);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--primary-color);
    }}
    </style>
    """, unsafe_allow_html=True)

def create_notification_banner(message, notification_type="info"):
    """Створення банера сповіщень"""
    
    type_config = {
        "info": {"icon": "ℹ️", "color": "#2196F3"},
        "success": {"icon": "✅", "color": "#4CAF50"},
        "warning": {"icon": "⚠️", "color": "#FF9800"},
        "error": {"icon": "❌", "color": "#F44336"}
    }
    
    config = type_config.get(notification_type, type_config["info"])
    
    st.markdown(f"""
    <div style="
        background: {config['color']}15;
        border-left: 4px solid {config['color']};
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        display: flex;
        align-items: center;
    ">
        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{config['icon']}</span>
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)