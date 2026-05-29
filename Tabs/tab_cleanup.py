import os
import shutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from assets_loader import Assets


class CleanupPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Веник из ассетов
        self.icon_lbl = QLabel()
        if not Assets.get("Disk_Cleanup").isNull():
            self.icon_lbl.setPixmap(Assets.get("Disk_Cleanup").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(self.icon_lbl, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        # Текст статуса
        self.status_lbl = QLabel()
        layout.addWidget(self.status_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        # Прогресс бар
        self.progress = QProgressBar()
        self.progress.setFixedSize(400, 25)
        self.progress.hide()
        self.progress.setStyleSheet(
            "QProgressBar { border: 2px solid rgba(255, 255, 255, 0.6); border-radius: 8px; background: rgba(255, 255, 255, 0.3); text-align: center; color: black; font-weight: bold; } QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #77dd22, stop:1 #339900); border-radius: 6px; }")
        layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)

        # Кнопка Запуска
        self.btn_start = QPushButton()
        self.btn_start.setFixedSize(220, 45)
        self.btn_start.clicked.connect(self.start_cleaning)
        layout.addWidget(self.btn_start, alignment=Qt.AlignmentFlag.AlignCenter)

        self.timer = QTimer()
        self.timer.timeout.connect(self.run_cleaning_logic)
        self.current_val = 0
        self.total_freed_mb = 0

        self.update_ui_text()

    def update_ui_text(self):
        """Перевод вкладки на лету"""
        if self.current_val == 0:
            self.status_lbl.setText(
                "Система готова к очистке от мусора" if Assets.current_lang == "ru" else "System is ready for disk cleanup")
        self.status_lbl.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #113355; margin: 15px; background: transparent;")

        self.btn_start.setText(" Запустить очистку" if Assets.current_lang == "ru" else " Start Cleanup")
        if not Assets.get("Recycle_Bin_Full").isNull():
            self.btn_start.setIcon(QIcon(Assets.get("Recycle_Bin_Full")))

    def start_cleaning(self):
        self.btn_start.setEnabled(False)
        self.progress.show()
        self.current_val = 0
        self.total_freed_mb = 0
        self.timer.start(30)

    def run_cleaning_logic(self):
        self.current_val += 1
        self.progress.setValue(self.current_val)

        # Шаг 1: Имитируем сканирование и параллельно РЕАЛЬНО чистим безопасные зоны
        if self.current_val == 20:
            self.status_lbl.setText(
                "Поиск временных файлов..." if Assets.current_lang == "ru" else "Scanning temporary files...")
            self.clean_folder(os.environ.get('TEMP'))

        # Шаг 2: Чистим логи
        elif self.current_val == 60:
            self.status_lbl.setText(
                "Очистка системного кэша..." if Assets.current_lang == "ru" else "Clearing system cache...")
            win_dir = os.environ.get('SystemRoot', 'C:\\Windows')
            self.clean_folder(os.path.join(win_dir, 'Temp'))

        # Шаг 3: Финал
        elif self.current_val >= 100:
            self.timer.stop()
            self.progress.hide()
            self.btn_start.setEnabled(True)

            # Ставим красивую пустую корзину на финал
            if not Assets.get("Recycle_Bin_Empty").isNull():
                self.icon_lbl.setPixmap(
                    Assets.get("Recycle_Bin_Empty").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))

            txt = f"Очистка завершена! Освобождено: {self.total_freed_mb:.1f} МБ 🎉" if Assets.current_lang == "ru" else f"Cleanup finished! Freed: {self.total_freed_mb:.1f} MB 🎉"
            self.status_lbl.setText(txt)
            self.status_lbl.setStyleSheet(
                "font-size: 18px; font-weight: bold; color: #115511; background: transparent;")

    def clean_folder(self, folder_path):
        """Безопасное удаление файлов с подсчетом мегабайт"""
        if not folder_path or not os.path.exists(folder_path):
            return

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Считаем размер файла перед удалением
                    self.total_freed_mb += os.path.getsize(file_path) / (1024 * 1024)
                    os.remove(file_path)
                except Exception:
                    continue  # Если файл занят системой — просто идем дальше, не падая
