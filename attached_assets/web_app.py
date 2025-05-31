# -*- coding: utf-8 -*-
"""
TechCare - Web Application
Веб-версія застосунку для моніторингу здоров'я комп'ютера
"""

from flask import Flask, render_template, jsonify, request
import json
import time
from datetime import datetime
from monitor import get_system_data, format_temperature, format_percentage, format_fan_speed
from reminder import (
    check_thresholds, clear_state, postpone_reminders, 
    get_status_summary, get_detailed_history
)
from advanced_monitor import (
    check_driver_status, check_thermal_paste_status, 
    get_fan_detailed_status, get_system_health_score
)
from additional_features import (
    check_startup_programs, check_disk_health, 
    check_network_performance, check_system_security,
    get_performance_recommendations
)

app = Flask(__name__)

# Глобальні налаштування
thresholds = {
    'cpu_temp': 70,
    'cpu_usage': 80,
    'ram_usage': 90,
    'disk_usage': 90,
    'uptime_restart': 86400
}

state = {
    'high_temp_time': 0,
    'high_ram_time': 0,
    'delay_until': 0
}

@app.route('/')
def index():
    """Головна сторінка"""
    return render_template('index.html')

@app.route('/api/system-data')
def get_system_status():
    """API для отримання системних даних"""
    try:
        data = get_system_data()
        warnings = check_thresholds(data, thresholds, state)
        
        # Отримання розширених даних
        health_score = get_system_health_score()
        fan_details = get_fan_detailed_status()
        thermal_status = check_thermal_paste_status()
        driver_status = check_driver_status()
        
        # Форматування даних для відображення
        cpu_temp = data.get('cpu_temp')
        cpu_percent = data.get('cpu_percent', 0)
        
        formatted_data = {
            'temperature': {
                'value': format_temperature(cpu_temp) if cpu_temp is not None else f"{int(cpu_percent)}%",
                'color': thermal_status['status'] == 'critical' and '#FF0000' or (thermal_status['status'] == 'warning' and '#FF6347' or '#00FF66'),
                'raw': cpu_temp if cpu_temp is not None else cpu_percent,
                'thermal_recommendation': thermal_status.get('recommendation', ''),
                'paste_age': thermal_status.get('estimated_paste_age', 'невідомо')
            },
            'uptime': {
                'value': data['uptime_str'],
                'color': '#FF6347' if data['uptime_seconds'] > 86400 else '#00FF66',
                'raw': data['uptime_seconds']
            },
            'ram': {
                'value': format_percentage(data['ram_percent']),
                'color': '#FF6347' if data['ram_percent'] > 90 else '#00FF66',
                'raw': data['ram_percent']
            },
            'disk': {
                'value': format_percentage(data['disk_percent']),
                'color': '#FF6347' if data['disk_percent'] > 90 else '#00FF66',
                'raw': data['disk_percent']
            },
            'fan': {
                'value': f"{fan_details['working_fans']}/{fan_details['total_fans']}" if fan_details['total_fans'] > 0 else "Н/Д",
                'color': fan_details['status'] == 'critical' and '#FF0000' or (fan_details['status'] == 'warning' and '#FF6347' or (fan_details['status'] == 'good' and '#00FF66' or '#BBBBBB')),
                'raw': fan_details,
                'details': fan_details['fans']
            },
            'drivers': {
                'value': "Недоступно" if driver_status['status'] == 'unavailable' else f"Застарілих: {len(driver_status.get('outdated_drivers', []))}",
                'color': driver_status['status'] == 'critical' and '#FF0000' or (driver_status['status'] == 'warning' and '#FF6347' or (driver_status['status'] == 'unavailable' and '#BBBBBB' or '#00FF66')),
                'status': driver_status['status'],
                'outdated_count': len(driver_status.get('outdated_drivers', []))
            },
            'health_score': {
                'value': f"{health_score['score']}/100",
                'color': health_score['color'],
                'level': health_score['health_level'],
                'issues': health_score['issues']
            }
        }
        
        return jsonify({
            'success': True,
            'data': formatted_data,
            'status': {
                'text': f"{health_score['health_level']} ({health_score['score']}/100)",
                'color': health_score['color']
            },
            'warnings': warnings + health_score['issues'],
            'timestamp': data['timestamp'].strftime('%H:%M:%S'),
            'detailed_analysis': {
                'thermal': thermal_status,
                'drivers': driver_status,
                'fans': fan_details
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/clear-state', methods=['POST'])
def clear_system_state():
    """API для очищення стану"""
    try:
        result = clear_state(state)
        return jsonify({
            'success': True,
            'message': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/postpone', methods=['POST'])
def postpone_notifications():
    """API для відкладення нагадувань"""
    try:
        minutes = request.json.get('minutes', 30) if request.json else 30
        result = postpone_reminders(state, minutes)
        return jsonify({
            'success': True,
            'message': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history')
def get_history():
    """API для отримання історії"""
    try:
        history = get_detailed_history(state)
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/advanced-analysis')
def get_advanced_analysis():
    """API для розширеного аналізу системи"""
    try:
        startup_info = check_startup_programs()
        disk_health = check_disk_health()
        network_info = check_network_performance()
        security_info = check_system_security()
        recommendations = get_performance_recommendations()
        
        return jsonify({
            'success': True,
            'startup': startup_info,
            'disk_health': disk_health,
            'network': network_info,
            'security': security_info,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/performance-tips')
def get_performance_tips():
    """API для отримання порад з оптимізації"""
    try:
        recommendations = get_performance_recommendations()
        return jsonify({
            'success': True,
            'tips': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 50)
    print("TechCare - Веб-версія")
    print("Запуск сервера на http://0.0.0.0:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)