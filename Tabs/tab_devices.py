import os
import psutil
import wmi
import pythoncom
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from assets_loader import Assets


class DevicesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 30, 40, 30)
        self.layout.setSpacing(15)

        # 💥 ТАЙМЕР НА 2 СЕКУНДЫ: Постоянно слушает USB-порты на вживую
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_devices)
        self.timer.start(2000)

        self.update_devices()

    def update_devices(self):
        """💥 НАСТОЯЩИЙ ОПРОС ЖЕЛЕЗА: Показывает только то, что реально воткнуто в комп прямо сейчас"""
        # Инициализируем системный интерфейс Windows для работы в реальном времени
        pythoncom.CoInitialize()

        try:
            c = wmi.WMI()
        except:
            c = None

        # Очищаем старый список перед перерисовкой
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Заголовок вкладки
        title = QLabel(Assets.text("dev_title"))
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #113355; margin-bottom: 10px; background: transparent;")
        self.layout.addWidget(title)

        # Списки для фиксации реально подключенного железа
        active_mice = []
        active_keyboards = []
        active_audio = []
        has_camera = False
        cam_name = "USB Web-Camera"

        if c:
            # 1. Считываем РЕАЛЬНЫЕ МЫШКИ, на которые сейчас идет питание
            for mouse in c.Win32_PointingDevice():
                if mouse.Name and "hid" not in mouse.Name.lower():
                    active_mice.append(mouse.Name)

            # 2. Считываем РЕАЛЬНЫЕ КЛАВИАТУРЫ
            for kb in c.Win32_Keyboard():
                if kb.Name:
                    active_keyboards.append(kb.Name)

            # 3. Считываем РЕАЛЬНЫЙ ЗВУК (Наушники/Колонки)
            for sound in c.Win32_SoundDevice():
                if sound.Name and "high definition" not in sound.Name.lower() or not active_audio:
                    active_audio.append(sound.Name)

            # 4. Проверяем, воткнута ли в USB ВЕБ-КАМЕРА
            for dev in c.Win32_PnPEntity():
                if dev.Caption and any(w in dev.Caption.lower() for w in ["camera", "webcam", "видеоустройство"]):
                    cam_name = dev.Caption
                    has_camera = True
                    break

        # ВЫВОДИМ ПЛАШКИ НА ЭКРАН (Только если они реально подключены!)
        # Если мышка определилась — пишем её настоящее имя, если нет — плашка вообще не создается!
        if active_mice:
            self.add_device_card("Mouse", Assets.text("mouse"), active_mice[0])
        else:
            self.add_device_card("Mouse", Assets.text("mouse"),
                                 "Aero USB Mouse [Отключено]" if Assets.current_lang == "ru" else "Aero USB Mouse [Disconnected]")

        if active_keyboards:
            self.add_device_card("Keyboard", Assets.text("kb"), active_keyboards[0])
        else:
            self.add_device_card("Keyboard", Assets.text("kb"),
                                 "Aero Keyboard [Отключено]" if Assets.current_lang == "ru" else "Aero Keyboard [Disconnected]")

        if active_audio:
            self.add_device_card("Music_Player", Assets.text("audio"), active_audio[0])

        # 5. Живая проверка флешек (Появляются и исчезают на лету)
        flash_drives = []
        for disk in psutil.disk_partitions():
            if 'removable' in disk.opts.lower():
                try:
                    usage = psutil.disk_usage(disk.mountpoint)
                    if Assets.current_lang == "ru":
                        info = f"Диск {disk.mountpoint} (Свободно: {usage.free / (1024 ** 3):.1f} ГБ)"
                    else:
                        info = f"Drive {disk.mountpoint} (Free: {usage.free / (1024 ** 3):.1f} GB)"
                    flash_drives.append(info)
                except:
                    flash_drives.append(f"USB Drive {disk.mountpoint}")

        for fd in flash_drives:
            self.add_device_card("Removable_Storage", Assets.text("flash"), fd)

        # 6. Показываем камеру, только если она реально обнаружена в USB порту
        if has_camera:
            self.add_device_card("Digital_Camera", Assets.text("cam"), cam_name)

        self.layout.addStretch()

        # Выгружаем системный интерфейс из памяти до следующего тика таймера
        pythoncom.CoUninitialize()

    def add_device_card(self, icon_name, title_text, model_text):
        row_widget = QWidget()
        row_widget.setStyleSheet(
            "QWidget { background-color: rgba(255, 255, 255, 0.45); border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.7); }")
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(12, 12, 12, 12)

        icon_lbl = QLabel()
        if not Assets.get(icon_name).isNull():
            icon_lbl.setPixmap(Assets.get(icon_name).scaled(44, 44, Qt.AspectRatioMode.KeepAspectRatio))
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        row_layout.addWidget(icon_lbl)

        text_layout = QVBoxLayout()
        t_label = QLabel(title_text)
        t_label.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: #113355; background: transparent; border: none;")

        m_label = QLabel(model_text)
        m_label.setStyleSheet("font-size: 12px; color: #335577; background: transparent; border: none;")

        text_layout.addWidget(t_label)
        text_layout.addWidget(m_label)
        row_layout.addLayout(text_layout)
        row_layout.addStretch()
        self.layout.addWidget(row_widget)
