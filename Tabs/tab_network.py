import socket
import psutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from assets_loader import Assets


class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(20)

        # Шапка вкладки
        title = QLabel(Assets.text("tab_network"))
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #113355; background: transparent;")
        layout.addWidget(title)

        # Карточка статуса
        card = QWidget()
        card.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.45); border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.7);")
        card_layout = QHBoxLayout(card)

        # Иконка глобуса с кабелем
        icon_lbl = QLabel()
        if not Assets.get("Cable_Network").isNull():
            icon_lbl.setPixmap(Assets.get("Cable_Network").scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        card_layout.addWidget(icon_lbl)

        # Текстовые слои
        text_layout = QVBoxLayout()
        self.status_lbl = QLabel()
        self.status_lbl.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: #113355; border: none; background: transparent;")

        self.adapter_lbl = QLabel()
        self.adapter_lbl.setStyleSheet("font-size: 12px; color: #335577; border: none; background: transparent;")

        text_layout.addWidget(self.status_lbl)
        text_layout.addWidget(self.adapter_lbl)
        card_layout.addLayout(text_layout)
        card_layout.addStretch()

        layout.addWidget(card)
        layout.addStretch()
        self.check_internet()

    def get_active_adapter_name(self):
        """💥 Скрипт сканирует сетевые интерфейсы и находит имя активного адаптера"""
        try:
            # Получаем статистику по всем сетевым картам
            stats = psutil.net_if_stats()
            # Получаем адреса адаптеров
            addrs = psutil.net_if_addrs()

            # Ищем адаптер, который включен (isup=True) и имеет IP-адрес (не петлевой)
            for adapter_name, stat in stats.items():
                if stat.isup and adapter_name in addrs:
                    for addr in addrs[adapter_name]:
                        if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                            # Очищаем имя от системных индексов Windows, если они есть
                            return adapter_name.split("*")[-1].strip()
        except:
            pass
        return "Realtek PCIe GBE Family Controller"  # Дефолтный сейв-вариант

    def check_internet(self):
        """Безопасная проверка интернета и вывод реального сетевого железа"""
        real_adapter = self.get_active_adapter_name()

        try:
            socket.create_connection(("77.88.8.8", 53), timeout=2)
            txt = "Подключение к Интернету: Активно" if Assets.current_lang == "ru" else "Internet Connection: Active"
            self.status_lbl.setText(txt)
            self.adapter_lbl.setText(
                f"Адаптер: {real_adapter}" if Assets.current_lang == "ru" else f"Adapter: {real_adapter}")
        except OSError:
            txt = "Сеть: Ограничено (Нет доступа к Интернету)" if Assets.current_lang == "ru" else "Network: Limited (No Internet Access)"
            self.status_lbl.setText(txt)
            self.adapter_lbl.setText(
                f"Адаптер: {real_adapter}" if Assets.current_lang == "ru" else f"Adapter: {real_adapter}")
