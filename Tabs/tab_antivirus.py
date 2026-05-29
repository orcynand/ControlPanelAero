import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from assets_loader import Assets


class AntivirusPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  # Ссылка на главное окно для проверки цвета обоев
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.shield_icon = QLabel()
        self.shield_icon.setPixmap(Assets.get("Safe_Shield").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(self.shield_icon, alignment=Qt.AlignmentFlag.AlignCenter)

        self.status = QLabel()
        layout.addWidget(self.status, alignment=Qt.AlignmentFlag.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setFixedSize(400, 25)
        self.progress.hide()
        self.progress.setStyleSheet(
            "QProgressBar { border: 2px solid rgba(255, 255, 255, 0.6); border-radius: 8px; background: rgba(255, 255, 255, 0.3); text-align: center; color: black; font-weight: bold; } QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #77dd22, stop:1 #339900); border-radius: 6px; }")
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_file_scan = QPushButton()
        self.btn_full_scan = QPushButton()

        btn_layout.addWidget(self.btn_file_scan)
        btn_layout.addWidget(self.btn_full_scan)
        layout.addLayout(btn_layout)

        self.btn_file_scan.clicked.connect(self.scan_single_file)
        self.btn_full_scan.clicked.connect(self.start_full_scan)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_full_scan)
        self.scan_val = 0
        self.update_ui_text()

    def update_ui_text(self):
        """💥 ИСПРАВЛЕНО: Убрали ошибки anti_active, подгружаем нормальный перевод"""
        self.status.setText(Assets.text("anti_active"))
        self.status.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #113355; margin: 10px; background: transparent;")

        self.btn_file_scan.setText(Assets.text("anti_exe"))
        self.btn_full_scan.setText(Assets.text("anti_full"))

        self.style_aero_btn(self.btn_file_scan, "Folder")
        self.style_aero_btn(self.btn_full_scan, "Danger_Shield")

    def style_aero_btn(self, button, icon_name):
        button.setFixedSize(220, 45)
        if not Assets.get(icon_name).isNull():
            button.setIcon(QIcon(Assets.get(icon_name)))

        # 💥 ИСПРАВЛЕНО: Кнопки антивируса теперь ТОЖЕ меняют цвет под тему обоев!
        bg = self.main_app.current_bg_name
        if bg == "bg1":  # Зелёный (Бабочка)
            stop_c, border_c = "#bbee22", "#77aa00"
        elif bg == "bg3":  # Оранжевый (Листья)
            stop_c, border_c = "#ff9933", "#cc5500"
        else:  # Синий (Пузыри)
            stop_c, border_c = "#99ccff", "#3388ff"

        button.setStyleSheet(
            f"QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 {stop_c}); border: 1px solid {border_c}; border-radius: 8px; color: #113355; font-weight: bold; font-size: 13px; }} QPushButton:hover {{ background: #ffffff; }}")

    def scan_single_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                   "Выберите файл" if Assets.current_lang == "ru" else "Select File",
                                                   "", "Исполняемые файлы (*.exe)")
        if file_path:
            filename = os.path.basename(file_path)
            if "virus" in filename.lower() or "crack" in filename.lower():
                self.shield_icon.setPixmap(
                    Assets.get("Danger_Shield").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
                self.status.setText(
                    f"Внимание! Файл {filename} подозрителен!" if Assets.current_lang == "ru" else f"Warning! File {filename} is dangerous!")
                self.status.setStyleSheet(
                    "font-size: 16px; font-weight: bold; color: #cc0000; background: transparent;")
            else:
                self.shield_icon.setPixmap(
                    Assets.get("Safe_Shield").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
                self.status.setText(
                    f"Файл {filename} проверен. Всё чисто." if Assets.current_lang == "ru" else f"File {filename} checked. System secure.")
                self.status.setStyleSheet(
                    "font-size: 16px; font-weight: bold; color: #115511; background: transparent;")

    def start_full_scan(self):
        self.btn_file_scan.setEnabled(False)
        self.btn_full_scan.setEnabled(False)
        self.progress.show()
        self.scan_val = 0
        self.status.setText(
            "Сканирование системных файлов..." if Assets.current_lang == "ru" else "Scanning core Windows files...")
        self.timer.start(40)

    def update_full_scan(self):
        self.scan_val += 1
        self.progress.setValue(self.scan_val)
        if self.scan_val >= 100:
            self.timer.stop()
            self.progress.hide()
            self.btn_file_scan.setEnabled(True)
            self.btn_full_scan.setEnabled(True)
            self.shield_icon.setPixmap(Assets.get("Safe_Shield").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            self.status.setText(
                "Проверка завершена! Всё чисто 🎉" if Assets.current_lang == "ru" else "Scan finished! System is secure 🎉")
            self.status.setStyleSheet("font-size: 18px; font-weight: bold; color: #115511; background: transparent;")
