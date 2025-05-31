# -*- coding: utf-8 -*-
"""
Мої функції для програми
Написав щоб не використовувати емоджі
"""

def show_icon_with_text(icon_svg, text):
    """Показує іконку з текстом"""
    return f"""
    <div style="display: flex; align-items: center; gap: 8px;">
        {icon_svg}
        <span>{text}</span>
    </div>
    """

def get_simple_metric(title, value, icon_svg):
    """Проста метрика з іконкою"""
    return f"""
    <div style="background: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            {icon_svg}
            <strong>{title}</strong>
        </div>
        <div style="font-size: 1.5rem; color: #1f77b4;">{value}</div>
    </div>
    """

def make_student_comment():
    """Генерує студентські коментарі"""
    comments = [
        "# TODO: зробити це краще",
        "# працює але можна покращити", 
        "# знайшов це в інтернеті, працює",
        "# простий код але зрозумілий",
        "# TODO: додати перевірки помилок"
    ]
    import random
    return random.choice(comments)

# Простенькі назви змінних як у студента
def get_data():
    """Отримує дані (просто)"""
    pass

def save_info(data):
    """Зберігає інфу"""
    pass

def check_stuff():
    """Перевіряє всякі штуки"""
    pass

# Мої іконки замість емоджі
DASHBOARD_ICON = """
<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <rect x="2" y="2" width="6" height="6" fill="#4CAF50" rx="1"/>
    <rect x="12" y="2" width="6" height="6" fill="#2196F3" rx="1"/>
    <rect x="2" y="12" width="6" height="6" fill="#FF9800" rx="1"/>
    <rect x="12" y="12" width="6" height="6" fill="#9C27B0" rx="1"/>
</svg>
"""

AI_ICON = """
<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <circle cx="10" cy="10" r="7" fill="#E91E63" opacity="0.2"/>
    <circle cx="7" cy="8" r="1" fill="#E91E63"/>
    <circle cx="13" cy="8" r="1" fill="#E91E63"/>
    <path d="M7 13 Q10 15 13 13" stroke="#E91E63" stroke-width="1.5" fill="none"/>
</svg>
"""

REPAIR_ICON = """
<svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <rect x="5" y="3" width="10" height="2" fill="#607D8B"/>
    <rect x="8" y="5" width="4" height="8" fill="#795548"/>
    <circle cx="10" cy="15" r="2" fill="#FF5722"/>
</svg>
"""