@echo off
echo ===================================
echo    TechCare AI - Запуск програми
echo ===================================
echo.

REM Перевірка встановлення Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ПОМИЛКА: Python не встановлено або не додано в PATH
    echo Будь ласка, встановіть Python з python.org
    pause
    exit /b 1
)

echo Python знайдено.
echo.

REM Встановлення залежностей
echo Встановлення необхідних бібліотек...
pip install streamlit plotly pandas numpy scikit-learn psutil

if errorlevel 1 (
    echo ПОМИЛКА: Не вдалося встановити бібліотеки
    pause
    exit /b 1
)

echo.
echo Бібліотеки встановлено успішно.
echo.

REM Запуск програми
echo Запуск TechCare AI...
echo Програма відкриється в браузері через кілька секунд...
echo Для зупинки натисніть Ctrl+C
echo.

streamlit run app.py

pause