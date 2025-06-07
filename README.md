# TechCare Monitor

**TechCare** — десктопна програма для моніторингу системних ресурсів комп'ютера. Створена як дипломна робота.

## 🧩 Основні функції:
- Відображення навантаження на CPU, RAM і диск
- Вимірювання температури системи
- Графік історії навантаження
- Збереження показників у файл `data_history.json`
- Інтерфейс на базі Tkinter (працює у віконному режимі)
- Можливість зібрати в `.exe` за допомогою PyInstaller

## Як запустити

### 1. Запуск з вихідного коду

1. Встановіть Python (https://www.python.org)
2. Встановіть бібліотеки:
```bash
pip install -r requirements.txt
```
3. Запустіть програму:
```bash
python main.py
```

### 2. Створення .exe файлу (опціонально)
1. Встановіть PyInstaller: `pip install pyinstaller`
2. Створіть exe: ` pyinstaller --onefile --windowed --icon=gear.ico main.py `
4. Готовий exe буде в папці `dist/`


## Використані бібліотеки (`requirements.txt`)

```
altgraph==0.17.4
contourpy==1.3.2
cycler==0.12.1
fonttools==4.58.2
kiwisolver==1.4.8
matplotlib==3.10.3
numpy==2.2.6
packaging==25.0
pefile==2023.2.7
pillow==11.2.1
psutil==7.0.0
pyinstaller==6.13.0
pyinstaller-hooks-contrib==2025.4
pyparsing==3.2.3
python-dateutil==2.9.0.post0
pywin32==310
pywin32-ctypes==0.2.3
setuptools==80.9.0
six==1.17.0
WMI==1.5.1
```

> Деякі бібліотеки (наприклад `pyinstaller`, `altgraph`, `pefile`) використовуються лише для збірки .exe та не потрібні при запуску з вихідного коду.

## Структура проєкту

```
TechCare/
•	achievements.py    # логіка досягнень користувача
•	ai.py             # модель AI для оцінки стану системи
•	ai_tab.py         # вкладка AI у GUI
•	gui.py            # інтерфейс користувача на Tkinter
•	json_data.py      # збереження/завантаження історії у JSON
•	main.py           # точка входу додатку
•	monitor.py        # збір метрик через psutil, WMI, LibreHardwareMonitor
•	tests.py          # тести для основних функцій
•	requirements.txt  # залежності Python
•	README.md         # цей файл
•	Gear.iso          # лого .exe застосунку
•	LibreHardwareMonitorLib.dll  # бібліотека (файл-DLL) для роботи з датчиками комп’ютера

Примітка: Для надійного зчитування температури ЦП та швидкості вентиляторів рекомендується додати:
pip install pythonnet




##  Автор

> Костянтин, студент 4 курсу  
> Дипломна робота з комп’ютерної індженерії (2025)
