from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from assets_loader import Assets


class MainMenuPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 25, 35, 25)
        layout.setSpacing(20)

        grid = QGridLayout()
        grid.setSpacing(25)

        # 💥 Фиксируем единые имена для всех 6 кнопок-плиток
        self.btn_tasks = QPushButton()
        self.btn_anti = QPushButton()
        self.btn_devices = QPushButton()
        self.btn_clean = QPushButton()
        self.btn_network = QPushButton()
        self.btn_users = QPushButton()

        # Навешиваем иконки и ключи перевода
        self.setup_tile(self.btn_tasks, "Performance", "tile_tasks_title", "tile_tasks_desc")
        self.setup_tile(self.btn_anti, "Danger_Shield", "tile_anti_title", "tile_anti_desc")
        self.setup_tile(self.btn_devices, "objects_26", "tile_devices_title", "tile_devices_desc")
        self.setup_tile(self.btn_clean, "Disk_Cleanup", "tile_clean_title", "tile_clean_desc")
        self.setup_tile(self.btn_network, "Cable_Network", "tile_net_title", "tile_net_desc")
        self.setup_tile(self.btn_users, "Windows_Live_Messenger", "tile_users_title", "tile_users_desc")

        # Раскладываем строго по сетке 2х3 из Paint
        grid.addWidget(self.btn_tasks, 0, 0)
        grid.addWidget(self.btn_anti, 0, 1)
        grid.addWidget(self.btn_devices, 1, 0)
        grid.addWidget(self.btn_clean, 1, 1)
        grid.addWidget(self.btn_network, 2, 0)
        grid.addWidget(self.btn_users, 2, 1)

        layout.addLayout(grid)
        layout.addStretch()

        # Привязываем клики к переключению страниц в QStackedWidget
        self.btn_tasks.clicked.connect(lambda: self.main_app.switch_page(1))
        self.btn_anti.clicked.connect(lambda: self.main_app.switch_page(2))
        self.btn_devices.clicked.connect(lambda: self.main_app.switch_page(3))
        self.btn_network.clicked.connect(lambda: self.main_app.switch_page(4))
        self.btn_users.clicked.connect(lambda: self.main_app.switch_page(5))
        self.btn_clean.clicked.connect(
            lambda: self.main_app.switch_page(6))  # 💥 ТЕПЕРЬ СТРОГО ТУТ ЖЕЛЕЗНО ИДЕТ НА ВЕНИК

        self.update_ui_text()

    def setup_tile(self, button, icon_name, title_key, desc_key):
        button.setFixedSize(390, 100)
        pix = Assets.get(icon_name)
        if not pix.isNull():
            button.setIcon(QIcon(pix))
            button.setIconSize(QSize(54, 54))

        button.title_key = title_key
        button.desc_key = desc_key

        # 💥 ДОБАВЛЯЕМ СЮДА: Каждая плитка теперь автоматически издает щелчок при нажатии
        button.clicked.connect(Assets.play_click)

        button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                            stop:0 rgba(255, 255, 255, 0.55), 
                                            stop:0.45 rgba(240, 248, 255, 0.35), 
                                            stop:0.50 rgba(160, 210, 255, 0.25), 
                                            stop:1 rgba(130, 180, 240, 0.45));
                border: 1px solid rgba(255, 255, 255, 0.7);
                border-radius: 10px;
                text-align: left;
                padding-left: 20px;
            }
            QPushButton:hover {
                border: 1px solid #00aaff;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                            stop:0 rgba(255, 255, 255, 0.75), 
                                            stop:1 rgba(100, 180, 255, 0.65));
            }
        """)

    def update_ui_text(self):
        """Обновляет текст внутри плиток при смене языка"""
        for btn in [self.btn_tasks, self.btn_anti, self.btn_devices, self.btn_clean, self.btn_network, self.btn_users]:
            title = Assets.text(btn.title_key)
            desc = Assets.text(btn.desc_key)
            btn.setText(f"{title}\n{desc}")
            btn.setStyleSheet(
                btn.styleSheet() + "color: #113355; font-family: 'Segoe UI'; font-weight: bold; font-size: 13px;")
