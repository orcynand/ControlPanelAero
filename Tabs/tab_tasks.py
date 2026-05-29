import psutil
import win32gui
import win32process
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, \
    QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon
from assets_loader import Assets


class TasksPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # ЛЕВАЯ ЧАСТЬ: Таблица
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)

        title_box = QHBoxLayout()
        perf_icon = QLabel()
        if not Assets.get("Performance").isNull():
            perf_icon.setPixmap(Assets.get("Performance").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio))
        title_box.addWidget(perf_icon)

        # Заголовок, который мы будем переводить
        self.title_lbl = QLabel()
        title_box.addWidget(self.title_lbl)
        title_box.addStretch()

        self.btn_refresh = QPushButton()
        self.btn_refresh.clicked.connect(self.refresh_processes)
        title_box.addWidget(self.btn_refresh)
        left_layout.addLayout(title_box)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget { background-color: rgba(255, 255, 255, 0.6); border: 1px solid rgba(255, 255, 255, 0.8); border-radius: 8px; color: #113355; font-size: 14px; }
            QHeaderView::section { background-color: rgba(100, 180, 240, 0.6); color: #113355; font-weight: bold; border: 1px solid rgba(255, 255, 255, 0.5); }
        """)
        left_layout.addWidget(self.table)
        main_layout.addWidget(left_container, stretch=3)

        # ПРАВАЯ ЧАСТЬ: Панель управления
        self.right_panel = QWidget()
        self.right_panel.setFixedWidth(220)
        self.right_panel.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.4); border-radius: 12px; border: 1px solid rgba(255,255,255,0.6);")
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(15, 20, 15, 20)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.panel_title = QLabel()
        self.panel_title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #113355; background: transparent; border:none;")
        right_layout.addWidget(self.panel_title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.alert_icon = QLabel()
        if not Assets.get("Alert").isNull():
            self.alert_icon.setPixmap(Assets.get("Alert").scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        right_layout.addWidget(self.alert_icon, alignment=Qt.AlignmentFlag.AlignCenter)

        self.info_text = QLabel()
        self.info_text.setWordWrap(True)
        self.info_text.setStyleSheet(
            "font-size: 12px; color: #335577; text-align: center; background: transparent; border:none;")
        right_layout.addWidget(self.info_text, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_kill = QPushButton()
        self.btn_kill.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ff9999, stop:0.5 #ff2222, stop:1 #cc0000); color: white; font-weight: bold; font-size: 14px; border: 2px solid rgba(255, 255, 255, 0.7); border-radius: 10px; padding: 8px; }
            QPushButton:hover { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffbbbb, stop:1 #ee0000); }
        """)
        self.btn_kill.clicked.connect(self.kill_selected_process)
        right_layout.addStretch()
        right_layout.addWidget(self.btn_kill)

        main_layout.addWidget(self.right_panel)

        self.row_to_pid = {}
        self.table.itemSelectionChanged.connect(self.on_item_selected)

        # Накатываем языковые строки
        self.update_ui_text()
        self.refresh_processes()

    def update_ui_text(self):
        """💥 ИСПРАВЛЕНО: Полный перевод Диспетчера задач на лету"""
        is_ru = (Assets.current_lang == "ru")

        # Перевод текстов шапки и панели
        self.title_lbl.setText("Диспетчер запущенных программ" if is_ru else "Task Manager Processes")
        self.title_lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #113355; background: transparent;")

        self.btn_refresh.setText(" Обновить" if is_ru else " Refresh")
        if not Assets.get("Good").isNull():
            self.btn_refresh.setIcon(QIcon(Assets.get("Good")))

        self.panel_title.setText("Управление" if is_ru else "Control")

        # Корректируем инфо-подпись, если ничего не выбрано
        selected_row = self.table.currentRow()
        if selected_row == -1 or selected_row not in self.row_to_pid:
            self.info_text.setText(
                "Выберите программу из списка, чтобы закрыть её." if is_ru else "Select a program from the list to close it.")

        self.btn_kill.setText(" Закрыть её" if is_ru else " Close It")
        if not Assets.get("Remove").isNull():
            self.btn_kill.setIcon(QIcon(Assets.get("Remove")))

        # Перевод колонок таблицы
        self.table.setHorizontalHeaderLabels([
            "Название программы" if is_ru else "Program Name",
            "Использует памяти" if is_ru else "Memory Usage"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def get_visible_windows_pids(self):
        pids = set()

        def enum_windows_proc(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                pids.add(pid)
            return True

        win32gui.EnumWindows(enum_windows_proc, 0)
        return pids

    def refresh_processes(self):
        self.table.itemSelectionChanged.disconnect(self.on_item_selected)  # Временно отключаем сигнал, чтобы не лагало
        self.table.setRowCount(0)
        self.row_to_pid.clear()
        visible_pids = self.get_visible_windows_pids()
        row = 0
        system_skips = ['explorer.exe', 'pycharm64.exe', 'python.exe', 'cmd.exe', 'conhost.exe', 'taskhostw.exe']

        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                if proc.info['pid'] in visible_pids and proc.info['name'].lower() not in system_skips:
                    mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    clean_name = proc.info['name'].replace('.exe', '').capitalize()

                    self.table.insertRow(row)
                    name_item = QTableWidgetItem(f" 🖥️  {clean_name}")
                    mem_item = QTableWidgetItem(
                        f"{mem_mb:.1f} МБ" if Assets.current_lang == "ru" else f"{mem_mb:.1f} MB")

                    name_item.setForeground(QColor("#113355"))
                    mem_item.setForeground(QColor("#113355"))

                    self.table.setItem(row, 0, name_item)
                    self.table.setItem(row, 1, mem_item)
                    self.row_to_pid[row] = proc.info['pid']
                    row += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        self.table.itemSelectionChanged.connect(self.on_item_selected)

    def on_item_selected(self):
        selected_row = self.table.currentRow()
        if selected_row in self.row_to_pid:
            prog_name = self.table.item(selected_row, 0).text().strip()
            if Assets.current_lang == "ru":
                self.info_text.setText(f"Выбрана программа:\n{prog_name}.\n\nНажмите кнопку ниже для закрытия.")
            else:
                self.info_text.setText(f"Selected program:\n{prog_name}.\n\nClick the button below to close it.")

    def kill_selected_process(self):
        selected_row = self.table.currentRow()
        if selected_row in self.row_to_pid:
            pid = self.row_to_pid[selected_row]
            try:
                proc = psutil.Process(pid)
                proc.terminate()
                self.refresh_processes()
                self.info_text.setText("Программа закрыта!" if Assets.current_lang == "ru" else "Program closed!")
            except:
                self.info_text.setText("Ошибка закрытия." if Assets.current_lang == "ru" else "Error closing.")
