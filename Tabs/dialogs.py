from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt, QSettings
from assets_loader import Assets

D_STYLE = "QDialog { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #f0fdf4, stop:1 #e0f2fe); } QLabel { color: #000000; font-family: 'Segoe UI'; font-weight: bold; font-size: 13px; } QComboBox { background-color: #ffffff; border: 1px solid #3399ff; border-radius: 4px; padding: 4px; color: #000000; font-size: 12px; } QComboBox QAbstractItemView { background-color: #ffffff; color: #000000; selection-background-color: #3399ff; selection-color: #ffffff; }"


class SupportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aero Support")
        self.setFixedSize(320, 180)
        self.setStyleSheet(D_STYLE)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        icon_lbl = QLabel()
        if not Assets.get("Microphone_user").isNull():
            icon_lbl.setPixmap(Assets.get("Microphone_user").scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        txt = "Нашли ошибку? Напишите автору:\norcynand@gmail.com" if Assets.current_lang == "ru" else "Found a bug? Contact us:\norcynand@gmail.com"
        lbl = QLabel(txt)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        btn = QPushButton("OK")
        btn.setFixedSize(80, 28)
        btn.clicked.connect(self.accept)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)


class SettingsDialog(QDialog):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("Aero Params")
        self.setFixedSize(380, 260)
        self.setStyleSheet(D_STYLE)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Language / Язык:"))
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["Русский", "English"])
        self.combo_lang.setCurrentIndex(0 if Assets.current_lang == "ru" else 1)
        layout.addWidget(self.combo_lang)

        layout.addWidget(QLabel("Wallpaper / Обои:"))
        self.combo_bg = QComboBox()
        self.combo_bg.addItems(["Wallpaper 1 (Butterfly)", "Wallpaper 2 (Bubbles)", "Wallpaper 3 (Lines)"])
        idx = 0 if self.main_app.current_bg_name == "bg1" else (1 if self.main_app.current_bg_name == "bg2" else 2)
        self.combo_bg.setCurrentIndex(idx)
        layout.addWidget(self.combo_bg)

        layout.addStretch()
        self.btn_ok = QPushButton("Apply / Применить")
        self.btn_ok.setFixedSize(150, 30)
        self.btn_ok.clicked.connect(self.save_settings)
        layout.addWidget(self.btn_ok, alignment=Qt.AlignmentFlag.AlignCenter)

    def save_settings(self):
        # 1. Меняем и сохраняем язык
        lang = "ru" if self.combo_lang.currentIndex() == 0 else "en"
        Assets.current_lang = lang

        # 2. 💥 ИСПРАВЛЕНО: Жёстко привязываем имена файлов обоев, учитывая форматы (.jpg / .png)
        bg_choice = self.combo_bg.currentIndex()
        if bg_choice == 0:
            bg_name = "bg1"  # Для твоей бабочки
        elif bg_choice == 1:
            bg_name = "bg2"  # Для пузырей
        else:
            bg_name = "bg3"  # Для листьев

        self.main_app.current_bg_name = bg_name

        # 💾 Сохраняем в реестр Windows, чтобы не сбрасывалось при перезапуске
        settings = QSettings("AeroCyberArtel", "AeroControlPanel")
        settings.setValue("language", lang)
        settings.setValue("wallpaper", bg_name)

        self.accept()

        # 🌀 Запускаем красивый лоадинг и обновляем фон
        self.main_app.switch_page(self.main_app.pages.currentIndex())
