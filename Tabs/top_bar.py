from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, \
    QListWidgetItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from assets_loader import Assets
from Tabs.dialogs import SettingsDialog, SupportDialog

TOP_BTN_STYLE = "QPushButton { background: rgba(255, 255, 255, 0.5); border: 1px solid rgba(0, 50, 100, 0.2); border-radius: 5px; color: #113355; font-size: 11px; font-weight: bold; } QPushButton:hover { background: rgba(255, 255, 255, 0.8); border: 1px solid #0088ff; }"


class AeroTopBar(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setFixedHeight(45)
        self.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.4); border-bottom: 1px solid rgba(255, 255, 255, 0.5);")

        top_layout = QHBoxLayout(self)
        top_layout.setContentsMargins(15, 0, 15, 0)

        # Поиск со слитной стеклянной лупой
        search_widget = QWidget()
        search_widget.setStyleSheet(
            "background: rgba(255,255,255,0.4); border: 1px solid #99ccff; border-radius: 6px; padding: 1px;")
        search_box = QHBoxLayout(search_widget)
        search_box.setContentsMargins(5, 2, 5, 2)
        search_box.setSpacing(5)

        self.search_icon = QLabel()
        if not Assets.get("Search_Icon").isNull():
            self.search_icon.setPixmap(Assets.get("Search_Icon").scaled(14, 14, Qt.AspectRatioMode.KeepAspectRatio))
        self.search_icon.setStyleSheet("border: none; background: transparent;")

        self.search_input = QLineEdit()
        self.search_input.setFixedWidth(120)
        self.search_input.setStyleSheet(
            "QLineEdit { background: transparent; border: none; color: black; font-size: 12px; }")
        self.search_input.textChanged.connect(self.on_search_text_changed)

        search_box.addWidget(self.search_icon)
        search_box.addWidget(self.search_input)
        top_layout.addWidget(search_widget)
        top_layout.addStretch()

        # Название текущей вкладки по центру
        self.panel_title = QLabel()
        self.panel_title.setStyleSheet("font-weight: bold; font-size: 15px; color: #113355; background: transparent;")
        top_layout.addWidget(self.panel_title)
        top_layout.addStretch()

        # Кнопка поддержки
        self.btn_support = QPushButton()
        self.style_button(self.btn_support, "Microphone_user")
        self.btn_support.clicked.connect(self.open_support)
        top_layout.addWidget(self.btn_support)

        # Кнопка параметров
        self.btn_settings = QPushButton()
        self.style_button(self.btn_settings, "System_Configurations")
        self.btn_settings.clicked.connect(self.open_settings)
        top_layout.addWidget(self.btn_settings)

        # Выпадающее окно результатов поиска
        self.search_results = QListWidget(self.main_app)
        self.search_results.setFixedWidth(240)
        self.search_results.setFixedHeight(160)
        self.search_results.setIconSize(QSize(20, 20))  # Размер для 3D-иконок в списке
        self.search_results.move(15, 45)
        self.search_results.hide()
        self.search_results.setStyleSheet("""
            QListWidget {
                background-color: rgba(240, 248, 255, 0.96);
                border: 2px solid #3399ff;
                border-radius: 8px;
                color: #113355;
                font-family: 'Segoe UI';
                font-size: 12px;
                font-weight: bold;
            }
            QListWidget::item { padding: 6px; border-bottom: 1px solid rgba(0,0,0,0.04); }
            QListWidget::item:hover { background-color: #3399ff; color: white; border-radius: 4px; }
        """)
        self.search_results.itemClicked.connect(self.on_search_item_clicked)

        # 💥 ИСПРАВЛЕНО: Привязали имя картинки из ассетов к каждому действию вместо смайликов
        self.search_db = [
            {"keys": ["главная", "меню", "плитки", "main", "menu", "home"], "ru": "Главное меню", "en": "Main Menu",
             "icon": "Help", "action": "tab_0"},
            {"keys": ["диспетчер задач", "процессы", "память", "программы", "task", "manager", "processes"],
             "ru": "Диспетчер процессов", "en": "Task Manager", "icon": "Performance", "action": "tab_1"},
            {"keys": ["антивирус", "безопасность", "сканирование", "вирусы", "защита", "anti", "virus", "scan"],
             "ru": "Антивирусная защита", "en": "Antivirus Shield", "icon": "Safe_Shield", "action": "tab_2"},
            {"keys": ["устройства", "железо", "мышь", "клавиатура", "плеер", "флешка", "камера", "devices"],
             "ru": "Подключенные устройства", "en": "Connected Hardware", "icon": "objects_26", "action": "tab_3"},
            {"keys": ["соединение", "сеть", "интернет", "подключение", "network", "internet", "connect"],
             "ru": "Сетевые подключения", "en": "Network Connection", "icon": "Cable_Network", "action": "tab_4"},
            {"keys": ["пользователи", "профиль", "аккаунт", "имя", "users", "profile"], "ru": "Учетные записи",
             "en": "User Accounts", "icon": "Windows_Live_Messenger", "action": "tab_5"},
            {"keys": ["настройки", "язык", "обои", "фон", "тема", "параметры", "settings", "wallpaper"],
             "ru": "Изменить обои и язык", "en": "Change UI & Wallpaper", "icon": "System_Configurations",
             "action": "open_settings"},
            {"keys": ["поддержка", "почта", "ошибка", "автор", "support", "bug", "email"],
             "ru": "Связаться с поддержкой", "en": "Open Support Contact", "icon": "Microphone_user",
             "action": "open_support"}
        ]

    def style_button(self, button, icon_name):
        button.setFixedSize(110, 28)
        pix = Assets.get(icon_name)
        if not pix.isNull():
            button.setIcon(QIcon(pix))
            button.setIconSize(QSize(16, 16))
        button.setStyleSheet(TOP_BTN_STYLE)

    def open_support(self):
        from Tabs.dialogs import SupportDialog
        SupportDialog().exec()

    def open_settings(self):
        from Tabs.dialogs import SettingsDialog
        SettingsDialog(self.main_app).exec()

    def on_search_text_changed(self, text):
        search_word = text.lower().strip()
        self.search_results.clear()

        if not search_word:
            self.search_results.hide()
            return

        matches_found = 0
        for item in self.search_db:
            if any(search_word in k for k in item["keys"]):
                display_text = item["ru"] if Assets.current_lang == "ru" else item["en"]

                list_item = QListWidgetItem(display_text)
                list_item.setData(Qt.ItemDataRole.UserRole, item["action"])

                # 💥 ДОБАВЛЯЕМ ОРИГИНАЛЬНУЮ ИКОНКУ В СТРОКУ ПОИСКА
                pix = Assets.get(item["icon"])
                if not pix.isNull():
                    list_item.setIcon(QIcon(pix))

                self.search_results.addItem(list_item)
                matches_found += 1

        if matches_found > 0:
            self.search_results.show()
            self.search_results.raise_()
        else:
            self.search_results.hide()

    def on_search_item_clicked(self, item):
        action = item.data(Qt.ItemDataRole.UserRole)
        self.search_input.clear()
        self.search_results.hide()

        if action.startswith("tab_"):
            page_index = int(action.split("_")[-1])
            self.main_app.switch_page(page_index)
        elif action == "open_settings":
            self.open_settings()
        elif action == "open_support":
            self.open_support()

    def update_texts(self):
        self.search_input.setPlaceholderText(Assets.text("search_placeholder"))
        self.btn_settings.setText(Assets.text("settings"))
        self.btn_support.setText(Assets.text("support"))
