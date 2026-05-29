import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget, \
    QStackedWidget, QLineEdit
from PyQt6.QtCore import Qt, QSize, QTimer, QSettings
from PyQt6.QtGui import QIcon, QPalette, QBrush, QMovie
from Tabs.tab_cleanup import CleanupPage

from assets_loader import Assets
from Tabs.tab_main import MainMenuPage
from Tabs.tab_tasks import TasksPage
from Tabs.tab_antivirus import AntivirusPage
from Tabs.tab_devices import DevicesPage
from Tabs.tab_network import NetworkPage
from Tabs.tab_users import UsersPage
from Tabs.top_bar import AeroTopBar

MAIN_STYLE = "QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #cceeff, stop:1 #66ccff); }"
SIDEBAR_BTN_STYLE = "QPushButton { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255,255,255,0.7), stop:0.49 rgba(255,255,255,0.3), stop:0.50 rgba(0,200,100,0.3), stop:1 rgba(0,150,50,0.5)); color: #113355; font-weight: bold; font-size: 13px; border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 10px; text-align: left; padding-left: 15px; } QPushButton:hover { border: 1px solid #00AA00; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255,255,255,0.9), stop:1 rgba(0,220,120,0.5)); }"
TOP_BTN_STYLE = "QPushButton { background: rgba(255, 255, 255, 0.5); border: 1px solid rgba(0, 50, 100, 0.2); border-radius: 5px; color: #113355; font-size: 11px; font-weight: bold; } QPushButton:hover { background: rgba(255, 255, 255, 0.8); border: 1px solid #0088ff; }"


class FrutigerAeroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        settings = QSettings("AeroCyberArtel", "AeroControlPanel")
        Assets.current_lang = settings.value("language", "ru")
        self.current_bg_name = settings.value("wallpaper", "bg2")
        self.resize(1050, 700)
        self.update_bg()

        main_widget = QWidget()
        self.main_layout = QVBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(main_widget)

        self.top_bar = AeroTopBar(self)
        self.main_layout.addWidget(self.top_bar)

        self.line_separator = QWidget()
        self.line_separator.setFixedHeight(2)
        self.line_separator.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255,255,255,0), stop:0.5 rgba(255,255,255,0.8), stop:1 rgba(255,255,255,0));")
        self.main_layout.addWidget(self.line_separator)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        self.main_layout.addLayout(content_layout)

        sidebar = QWidget()
        sidebar.setFixedWidth(180)
        sidebar.setStyleSheet(
            "QWidget { background-color: rgba(255, 255, 255, 0.25); border-right: 1px solid rgba(255, 255, 255, 0.4); }")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)

        self.btn_tab_main = QPushButton()
        self.btn_tab_tasks = QPushButton()
        self.btn_tab_anti = QPushButton()
        self.btn_tab_devices = QPushButton()
        self.btn_tab_network = QPushButton()
        self.btn_tab_users = QPushButton()

        sidebar_layout.addWidget(self.btn_tab_main)
        sidebar_layout.addWidget(self.btn_tab_tasks)
        sidebar_layout.addWidget(self.btn_tab_anti)
        sidebar_layout.addWidget(self.btn_tab_devices)
        sidebar_layout.addWidget(self.btn_tab_network)
        sidebar_layout.addWidget(self.btn_tab_users)
        sidebar_layout.addStretch()

        self.version_lbl = QLabel()
        self.version_lbl.setStyleSheet(
            "font-size: 11px; color: rgba(17,51,85,0.6); background: transparent; padding-left: 5px;")
        sidebar_layout.addWidget(self.version_lbl)
        content_layout.addWidget(sidebar)

        self.pages = QStackedWidget()
        self.pages.setStyleSheet("background: transparent;")
        content_layout.addWidget(self.pages)

        self.loading_page = QWidget()
        loading_layout = QVBoxLayout(self.loading_page)
        self.gif_label = QLabel()
        self.movie = QMovie("Assets/loading-windows.gif")
        if self.movie.isValid():
            self.gif_label.setMovie(self.movie)
            self.movie.setScaledSize(QSize(64, 64))
        loading_layout.addWidget(self.gif_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Подключаем страницы
        self.page_main = MainMenuPage(self)
        self.page_tasks = TasksPage()
        self.page_anti = AntivirusPage(self)
        self.page_devices = DevicesPage()
        self.page_network = NetworkPage()
        self.page_users = UsersPage()
        self.page_cleanup = CleanupPage()  # 💥 ДОБАВИЛИ ТУТ

        self.pages.addWidget(self.page_main)  # 0
        self.pages.addWidget(self.page_tasks)  # 1
        self.pages.addWidget(self.page_anti)  # 2
        self.pages.addWidget(self.page_devices)  # 3
        self.pages.addWidget(self.page_network)  # 4
        self.pages.addWidget(self.page_users)  # 5
        self.pages.addWidget(self.page_cleanup)  # 6 💥 ТЕПЕРЬ ТУТ ОЧИСТКА
        self.pages.addWidget(self.loading_page)  # 7 💥 ГИФКА СДВИНУЛАСЬ НА ИНДЕКС 7

        self.btn_tab_main.clicked.connect(lambda: self.switch_page(0))
        self.btn_tab_tasks.clicked.connect(lambda: self.switch_page(1))
        self.btn_tab_anti.clicked.connect(lambda: self.switch_page(2))
        self.btn_tab_devices.clicked.connect(lambda: self.switch_page(3))
        self.btn_tab_network.clicked.connect(lambda: self.switch_page(4))
        self.btn_tab_users.clicked.connect(lambda: self.switch_page(5))

        self.load_timer = QTimer()
        self.load_timer.timeout.connect(self.show_real_page)
        self.pending_page_index = 0
        self.reload_language_ui()

    def switch_page(self, index):
        def switch_page(self, index):
            # 💥 ИСПРАВЛЕНО: Издаем сочный звук клика XP при нажатии на любую вкладку!
            Assets.play_click()

            self.pending_page_index = index
            self.pages.setCurrentIndex(6)
            if self.movie.isValid(): self.movie.start()
            self.load_timer.start(600)

        self.pending_page_index = index
        self.pages.setCurrentIndex(7)  # 💥 ИСПРАВЛЕНО НА 7 (Показываем GIF)
        if self.movie.isValid(): self.movie.start()
        self.load_timer.start(600)

    def show_real_page(self):
        self.load_timer.stop()
        if self.movie.isValid(): self.movie.stop()
        idx = self.pending_page_index
        self.pages.setCurrentIndex(idx)

        # Добавь "tab_clean" в список ключей для названия разделов в шапке
        keys = ["default_panel_title", "tab_tasks", "tab_anti", "tab_devices", "tab_network", "tab_users", "tab_clean"]
        if idx < len(keys):
            self.top_bar.panel_title.setText(Assets.text(keys[idx]))

        if idx == 3:
            self.page_devices.update_devices()
        elif idx == 1:
            self.page_tasks.refresh_processes()
        elif idx == 4:
            self.page_network.check_internet()
        elif idx == 6:
            self.page_cleanup.update_ui_text()  # 💥 ДОБАВИЛИ ТУТ

    def reload_language_ui(self):
        self.version_lbl.setText(Assets.text("version"))
        self.top_bar.update_texts()
        idx = self.pages.currentIndex()
        keys = ["default_panel_title", "tab_tasks", "tab_anti", "tab_devices", "tab_network", "tab_users",
                "default_panel_title"]
        self.top_bar.panel_title.setText(Assets.text(keys[idx if idx < 6 else 0]))

        self.btn_tab_main.setText(Assets.text("tab_main"))
        self.btn_tab_tasks.setText(Assets.text("tab_tasks"))
        self.btn_tab_anti.setText(Assets.text("tab_anti"))
        self.btn_tab_devices.setText(Assets.text("tab_devices"))
        self.btn_tab_network.setText(Assets.text("tab_network"))
        self.btn_tab_users.setText(Assets.text("tab_users"))

        self.style_sidebar_button(self.btn_tab_main, "Help")
        self.style_sidebar_button(self.btn_tab_tasks, "Performance")
        self.style_sidebar_button(self.btn_tab_anti, "Safe_Shield")
        self.style_sidebar_button(self.btn_tab_devices, "objects_26")
        self.style_sidebar_button(self.btn_tab_network, "Cable_Network")
        self.style_sidebar_button(self.btn_tab_users, "Windows_Live_Messenger")

        if hasattr(self, 'page_main') and hasattr(self.page_main, 'update_ui_text'): self.page_main.update_ui_text()
        if hasattr(self, 'page_anti') and hasattr(self.page_anti, 'update_ui_text'): self.page_anti.update_ui_text()
        if hasattr(self, 'page_tasks') and hasattr(self.page_tasks, 'update_ui_text'): self.page_tasks.update_ui_text()
        if hasattr(self, 'page_devices') and hasattr(self.page_devices,
                                                     'update_devices'): self.page_devices.update_devices()
        if hasattr(self, 'page_users') and hasattr(self.page_users, 'update_text'): self.page_users.update_text()
        if hasattr(self, 'page_cleanup'): self.page_cleanup.update_ui_text()

    def update_bg(self):
        """💥 Метод мгновенно обновляет и растягивает выбранные обои на весь экран"""
        bg_pixmap = Assets.get(self.current_bg_name)

        if not bg_pixmap.isNull():
            # Гладкое растягивание картинки под текущий размер окна
            scaled_bg = bg_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                         Qt.TransformationMode.SmoothTransformation)
            palette = QPalette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_bg))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
            # Принудительно заставляем окно перерисоваться прямо сейчас
            self.update()
        else:
            # Сейв-мод градиент, если файлы обоев вдруг потерялись
            self.setStyleSheet(
                "QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #cceeff, stop:1 #66ccff); }")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_bg()

    def style_sidebar_button(self, button, icon_name):
        button.setFixedSize(160, 40)
        pix = Assets.get(icon_name)
        if not pix.isNull():
            button.setIcon(QIcon(pix))
            button.setIconSize(QSize(22, 22))
        if self.current_bg_name == "bg1":
            stop_color, hover_border, hover_stop = "0, 200, 100, 0.3", "#00AA00", "0, 220, 120, 0.5"
        elif self.current_bg_name == "bg3":
            stop_color, hover_border, hover_stop = "240, 120, 0, 0.3", "#FF6600", "255, 160, 50, 0.5"
        else:
            stop_color, hover_border, hover_stop = "0, 150, 255, 0.3", "#0088ff", "50, 180, 255, 0.5"
        dyn_style = f"QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255,255,255,0.7), stop:0.49 rgba(255,255,255,0.3), stop:0.50 rgba({stop_color}), stop:1 rgba(50,140,240,0.4)); color: #113355; font-weight: bold; font-size: 13px; border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 10px; text-align: left; padding-left: 15px; }} QPushButton:hover {{ border: 1px solid {hover_border}; background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255,255,255,0.9), stop:0.49 rgba(255,255,255,0.5), stop:0.50 rgba({hover_stop}), stop:1 rgba(0,120,240,0.6)); }}"
        button.setStyleSheet(dyn_style)

# 🚀 СТАРТ СИСТЕМЫ (Строго с самого левого края!)
app = QApplication(sys.argv)
Assets.load_all()
window = FrutigerAeroApp()
window.show()
sys.exit(app.exec())
