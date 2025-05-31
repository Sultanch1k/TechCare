# -*- coding: utf-8 -*-
"""
TechCare AI - Adaptive Components Module
Модуль адаптивних компонентів для різних розмірів екранів
"""

import streamlit as st

class AdaptiveLayout:
    def __init__(self, mobile_mode=False):
        self.mobile_mode = mobile_mode
    
    def create_metric_grid(self, metrics_data):
        """Створення адаптивної сітки метрик"""
        if self.mobile_mode:
            # Мобільний режим: 2x2 сітка
            cols = []
            for i in range(0, len(metrics_data), 2):
                col1, col2 = st.columns(2)
                cols.extend([col1, col2])
        else:
            # Десктоп режим: всі в один ряд
            cols = st.columns(len(metrics_data))
        
        for i, (col, metric) in enumerate(zip(cols, metrics_data)):
            if i < len(metrics_data):
                with col:
                    st.metric(
                        label=metric['label'],
                        value=metric['value'],
                        delta=metric.get('delta')
                    )
    
    def create_responsive_chart(self, fig, title=""):
        """Створення адаптивного графіка"""
        if self.mobile_mode:
            # Мобільні налаштування
            fig.update_layout(
                height=300,
                font=dict(size=10),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0
                ),
                margin=dict(l=10, r=10, t=30, b=10)
            )
        else:
            # Десктопні налаштування
            fig.update_layout(
                height=400,
                font=dict(size=12),
                margin=dict(l=20, r=20, t=40, b=20)
            )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_info_cards(self, cards_data):
        """Створення адаптивних інформаційних карток"""
        if self.mobile_mode:
            # Мобільний: одна картка на ряд
            for card in cards_data:
                st.markdown(f"""
                <div class="info-card">
                    <h4>{card['title']}</h4>
                    <p>{card['content']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Десктоп: кілька карток в ряд
            cols = st.columns(min(3, len(cards_data)))
            for i, card in enumerate(cards_data):
                with cols[i % len(cols)]:
                    st.markdown(f"""
                    <div class="info-card">
                        <h4>{card['title']}</h4>
                        <p>{card['content']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    def create_tab_layout(self, tabs_data):
        """Створення адаптивного макету з табами"""
        if self.mobile_mode:
            # Мобільний: компактні таби
            return st.tabs([f"📱 {tab}" for tab in tabs_data])
        else:
            # Десктоп: повні таби
            return st.tabs(tabs_data)

def get_responsive_columns(mobile_mode, desktop_cols=4, mobile_cols=2):
    """Отримання адаптивних колонок"""
    if mobile_mode:
        return mobile_cols
    return desktop_cols

def apply_mobile_styles():
    """Застосування мобільних стилів"""
    st.markdown("""
    <style>
    /* Мобільні стилі */
    .mobile-container {
        padding: 0.5rem;
    }
    
    .mobile-metric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        text-align: center;
    }
    
    .mobile-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    
    .mobile-button {
        width: 100%;
        padding: 0.75rem;
        border-radius: 6px;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        font-weight: 600;
        margin: 0.25rem 0;
    }
    
    /* Компактні заголовки для мобільних */
    @media (max-width: 768px) {
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.1rem !important; }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 0.8rem !important;
            padding: 0.3rem 0.6rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_mobile_navigation(pages):
    """Створення мобільної навігації"""
    # Компактна горизонтальна навігація для мобільних
    return st.radio(
        "Навігація:",
        pages,
        horizontal=True,
        label_visibility="collapsed"
    )

def responsive_dataframe(df, mobile_mode=False):
    """Адаптивне відображення DataFrame"""
    if mobile_mode and not df.empty:
        # Для мобільних показуємо тільки ключові колонки
        if len(df.columns) > 3:
            # Показуємо перші 3 колонки
            display_df = df.iloc[:, :3]
            st.dataframe(display_df, use_container_width=True)
            
            # Додаємо можливість розгорнути всі дані
            if st.button("Показати всі дані"):
                st.dataframe(df, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)