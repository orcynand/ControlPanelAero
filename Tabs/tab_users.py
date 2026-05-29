import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from assets_loader import Assets


class UsersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 30, 40, 30)
        self.layout.setSpacing(20)
        self.update_text()

    def update_text(self):
        """💥 ИСПРАВЛЕНО: Полное обновление текстов при смене языка на лету"""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        # Заголовок вкладки
        title = QLabel(Assets.text("tab_users"))
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #113355; background: transparent;")
        self.layout.addWidget(title)

        card = QWidget()
        card.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.45); border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.7);")
        card_layout = QHBoxLayout(card)

        icon_lbl = QLabel()
        if not Assets.get("Windows_Live_Messenger").isNull():
            icon_lbl.setPixmap(Assets.get("Windows_Live_Messenger").scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        card_layout.addWidget(icon_lbl)

        # Вытягиваем РЕАЛЬНОЕ имя текущего пользователя Windows
        username = os.getlogin().capitalize()

        text_layout = QVBoxLayout()
        u_label = QLabel(f"Профиль: {username}" if Assets.current_lang == "ru" else f"Profile: {username}")
        u_label.setStyleSheet(
            "font-weight: bold; font-size: 15px; color: #113355; background: transparent; border: none;")

        t_label = QLabel("Тип: Администратор" if Assets.current_lang == "ru" else "Type: Administrator")
        t_label.setStyleSheet("font-size: 12px; color: #445577; background: transparent; border: none;")

        text_layout.addWidget(u_label)
        text_layout.addWidget(t_label)
        card_layout.addLayout(text_layout)
        card_layout.addStretch()

        self.layout.addWidget(card)
        self.layout.addStretch()
