import tkinter as tk
from tkinter import ttk
from monitor import get_system_data, get_network_data
from tests import SimpleTests

class AITab:
    def __init__(self, parent, app_ref):
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        self.app_ref = app_ref  # посилання на головний додаток з ai_engine
        self.build_ui()
        self.init_ai_engine()

    def build_ui(self):
        # Заголовок з неоновим ефектом
        title = tk.Label(self.frame, text="🤖 AI Аналітика",
                         font=('Roboto', 16, 'bold'),
                         fg='#00DDEB', bg='#0F0F0F')
        title.pack(pady=(15, 10), fill='x')

        # Статус здоров'я AI
        self.health_label = tk.Label(self.frame, text="🧠 Індекс здоров'я: --%",
                                     font=('Roboto', 12), fg='#00FF66', bg='#0F0F0F')
        self.health_label.pack(pady=(0, 10))

        # Статус індикатор
        self.status_indicator = tk.Canvas(self.frame, width=20, height=20,
                                          bg='#0F0F0F', highlightthickness=0)
        self.status_indicator.pack(pady=(0, 10))

        # Текстове поле з неоновим фоном
        self.predictions_text = tk.Text(self.frame, height=15,
                                        bg='#1A1A1A', fg='#00FF66',
                                        font=('Consolas', 12),
                                        insertbackground='#00FF66',
                                        relief='flat', bd=2,
                                        highlightbackground='#00DDEB',
                                        highlightcolor='#00DDEB',
                                        highlightthickness=2)
        self.predictions_text.pack(fill='both', expand=True, padx=15, pady=10)

        # Теги для стилізації тексту
        self.predictions_text.tag_configure('bold', font=('Consolas', 12, 'bold'))
        self.predictions_text.tag_configure('warning', foreground='#FFA500')
        self.predictions_text.tag_configure('prediction', foreground='#00FFFF')
        self.predictions_text.tag_configure('error', foreground='#FF4444')
        self.predictions_text.tag_configure('success', foreground='#00FF00')

        # Кнопка оновлення
        button_frame = tk.Frame(self.frame, bg='#0F0F0F')
        button_frame.pack(pady=15)

        refresh_btn = tk.Button(button_frame, text="🔄 Оновити AI аналіз",
                                font=('Roboto', 12, 'bold'),
                                bg='#2D2D2D', fg='#FFFFFF',
                                activebackground='#00DDEB',
                                activeforeground='#000000',
                                relief='solid', bd=2,
                                highlightbackground='#00DDEB',
                                highlightthickness=2,
                                command=self.run_ai_analysis,
                                padx=30, pady=10,
                                cursor='hand2')
        refresh_btn.pack()

        def on_enter(e):
            refresh_btn.config(bg='#00AACC', fg='#FFFFFF', highlightbackground='#00FF66')
        def on_leave(e):
            refresh_btn.config(bg='#2D2D2D', fg='#FFFFFF', highlightbackground='#00DDEB')

        refresh_btn.bind("<Enter>", on_enter)
        refresh_btn.bind("<Leave>", on_leave)

    def update_status_indicator(self, score):
        # Змінюємо колір індикатора залежно від оцінки
        color = '#00FF00' if score >= 70 else '#FFFF00' if score >= 40 else '#FF4444'
        self.status_indicator.delete("all")
        self.status_indicator.create_oval(2, 2, 18, 18, fill=color)

    def run_ai_analysis(self):
        self.predictions_text.delete(1.0, tk.END)
        self.predictions_text.insert(tk.END, "🧠 Збір даних...\n", 'bold')

        try:
            data = get_system_data()

            if not hasattr(self.app_ref, 'ai_engine') or self.app_ref.ai_engine is None:
                raise Exception("AI engine не ініціалізований")

            result = self.app_ref.ai_engine.predict_system_health(data)

            score = result.get('health_score', 0)
            self.health_label.config(text=f"🧠 Індекс здоров'я: {score}%")
            self.update_status_indicator(score)

            # Метрики мережі
            net = get_network_data()
            recv, sent = net.get('net_recv_mb_s', 0), net.get('net_sent_mb_s', 0)
            if recv > 0 or sent > 0:
                self.predictions_text.insert(tk.END, "\n📡 Метрики мережі:\n", 'bold')
                self.predictions_text.insert(tk.END, f" • Отримано: {recv:.2f} МБ/с\n")
                self.predictions_text.insert(tk.END, f" • Відправлено: {sent:.2f} МБ/с\n")
            else:
                self.predictions_text.insert(tk.END, "\n📡 Трафік наразі нульовий\n", 'bold')

            # Disk Test
            disk_score = SimpleTests(self.app_ref.data_manager).run_disk_test().get('disk_score', 0)
            self.predictions_text.insert(tk.END, f"\n💽 Disk Test: {disk_score:.1f}%\n", 'bold')

            if result.get('warnings'):
                self.predictions_text.insert(tk.END, "\n⚠️ Попередження:\n", 'warning')
                for w in result['warnings']:
                    self.predictions_text.insert(tk.END, f" • {w}\n")

            if result.get('predictions'):
                self.predictions_text.insert(tk.END, "\n🔮 Прогнози:\n", 'prediction')
                for p in result['predictions']:
                    self.predictions_text.insert(tk.END, f" • {p}\n")

            # Рекомендації
            self.predictions_text.insert(tk.END, "\n💡 Рекомендації:\n", 'success')
            if score < 70:
                self.predictions_text.insert(tk.END, " • Перезапуск системи\n")
            if disk_score < 75:
                self.predictions_text.insert(tk.END, " • Дефрагментація: defrag C:\\n")

        except Exception as e:
            self.predictions_text.insert(tk.END, f"❌ Помилка AI аналізу: {e}\n", 'error')
        finally:
            try:
                self.app_ref.gui.status_label.config(text="✅ AI аналіз завершено")
            except:
                pass

    def init_ai_engine(self):
        if self.app_ref and hasattr(self.app_ref, 'ai_engine'):
            self.ai_engine = self.app_ref.ai_engine
        else:
            self.ai_engine = None

    def set_app_ref(self, app_ref):
        self.app_ref = app_ref
        self.init_ai_engine()
