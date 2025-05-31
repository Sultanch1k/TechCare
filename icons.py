# -*- coding: utf-8 -*-
"""
Простенькі іконки для програми
Зробив сам щоб не використовувати емоджі
"""

def get_dashboard_icon():
    """Іконка для головної"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <rect x="3" y="3" width="7" height="7" fill="#4CAF50" rx="1"/>
        <rect x="14" y="3" width="7" height="7" fill="#2196F3" rx="1"/>
        <rect x="3" y="14" width="7" height="7" fill="#FF9800" rx="1"/>
        <rect x="14" y="14" width="7" height="7" fill="#9C27B0" rx="1"/>
    </svg>
    """

def get_ai_icon():
    """Іконка для AI"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="8" fill="#E91E63" opacity="0.2"/>
        <circle cx="8" cy="10" r="1.5" fill="#E91E63"/>
        <circle cx="16" cy="10" r="1.5" fill="#E91E63"/>
        <path d="M8 15 Q12 18 16 15" stroke="#E91E63" stroke-width="2" fill="none"/>
    </svg>
    """

def get_repair_icon():
    """Іконка для ремонту"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <rect x="6" y="4" width="12" height="3" fill="#607D8B"/>
        <rect x="10" y="7" width="4" height="10" fill="#795548"/>
        <circle cx="12" cy="19" r="2" fill="#FF5722"/>
    </svg>
    """

def get_trophy_icon():
    """Іконка для досягнень"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <ellipse cx="12" cy="8" rx="6" ry="5" fill="#FFD700"/>
        <rect x="10" y="13" width="4" height="6" fill="#8D6E63"/>
        <rect x="8" y="19" width="8" height="2" fill="#5D4037"/>
    </svg>
    """

def get_speed_icon():
    """Іконка для тестів"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M12 4 L20 18 L4 18 Z" fill="#3F51B5"/>
        <circle cx="12" cy="14" r="2" fill="white"/>
    </svg>
    """

def get_calendar_icon():
    """Іконка для розкладу"""
    return """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <rect x="3" y="6" width="18" height="14" fill="#009688" rx="2"/>
        <rect x="7" y="2" width="2" height="6" fill="#00695C"/>
        <rect x="15" y="2" width="2" height="6" fill="#00695C"/>
        <line x1="3" y1="10" x2="21" y2="10" stroke="white" stroke-width="1"/>
    </svg>
    """

def get_cpu_icon():
    """Іконка для процесора"""
    return """
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <rect x="4" y="4" width="12" height="12" fill="#673AB7" rx="1"/>
        <rect x="6" y="6" width="8" height="8" fill="#9C27B0" rx="1"/>
        <rect x="2" y="7" width="2" height="6" fill="#673AB7"/>
        <rect x="16" y="7" width="2" height="6" fill="#673AB7"/>
    </svg>
    """

def get_ram_icon():
    """Іконка для пам'яті"""
    return """
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <rect x="2" y="6" width="16" height="8" fill="#4CAF50" rx="1"/>
        <rect x="4" y="4" width="2" height="4" fill="#2E7D32"/>
        <rect x="8" y="4" width="2" height="4" fill="#2E7D32"/>
        <rect x="12" y="4" width="2" height="4" fill="#2E7D32"/>
    </svg>
    """

def get_disk_icon():
    """Іконка для диска"""
    return """
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <rect x="3" y="4" width="14" height="12" fill="#455A64" rx="1"/>
        <circle cx="10" cy="10" r="3" fill="#78909C"/>
        <circle cx="10" cy="10" r="1" fill="#263238"/>
    </svg>
    """

def get_temp_icon():
    """Іконка для температури"""
    return """
    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <rect x="8" y="2" width="4" height="12" fill="#FF5722" rx="2"/>
        <circle cx="10" cy="16" r="3" fill="#D32F2F"/>
        <rect x="9" y="4" width="2" height="8" fill="#FFCDD2"/>
    </svg>
    """