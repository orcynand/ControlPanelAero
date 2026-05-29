import os
from PyQt6.QtGui import QPixmap


class Assets:
    icons = {}
    current_lang = "ru"

    STRINGS = {
        "ru": {
            "title": "Aero Панель Управления 2006",
            "search_placeholder": "Поиск...",
            "default_panel_title": "Панель Управления Aero",
            "settings": " Настройки",
            "support": " Поддержка",
            "tab_main": " Главная",
            "tab_tasks": " Диспетчер",
            "tab_anti": " Антивирус",
            "tab_devices": " Устройства",
            "tab_network": " Соединение",
            "tab_users": " Пользователи",
            "version": "2026 ver 1",
            "tile_tasks_title": "Диспетчер Задач",
            "tile_tasks_desc": "Контроль процессов",
            "tile_anti_title": "Антивирус",
            "tile_anti_desc": "Поиск Вирусов",
            "tile_devices_title": "Устройства",
            "tile_devices_desc": "Мышь, принтер, диски...",
            "tile_clean_title": "Очистка диска",
            "tile_clean_desc": "Удаление мусора",
            "tile_net_title": "Соединение",
            "tile_net_desc": "Ваше подключение к сети и Интернету",
            "tile_users_title": "Пользователи",
            "tile_users_desc": "Текущий пользователь и пользователи компьютера",
            "anti_active": "Защита компьютера активна",
            "anti_exe": " Проверить .EXE файл",
            "anti_full": " Полная проверка ПК",
            # 💥 УБРАЛИ ПРИСТАВКУ dev_
            "dev_title": "Подключенные устройства компьютера",
            "mouse": "Основное устройство ввода",
            "kb": "Стандартная клавиатура",
            "mic": "Звуковой микрофон",
            "audio": "Аудиосистема / Плеер",
            "flash": "Съемный накопитель (Флешка)",
            "cam": "Веб-камера / Видеоустройство"
        },
        "en": {
            "title": "Aero Control Panel 2006",
            "search_placeholder": "Search...",
            "default_panel_title": "Aero Control Panel",
            "settings": " Settings",
            "support": " Support",
            "tab_main": " Main Menu",
            "tab_tasks": " Task Manager",
            "tab_anti": " Antivirus",
            "tab_devices": " Devices",
            "tab_network": " Connection",
            "tab_users": " Users",
            "version": "2026 ver 1",
            "tile_tasks_title": "Task Manager",
            "tile_tasks_desc": "Process Control",
            "tile_anti_title": "Antivirus",
            "tile_anti_desc": "Virus Scan",
            "tile_devices_title": "Devices",
            "tile_devices_desc": "Mouse, printer, drives...",
            "tile_clean_title": "Disk Cleanup",
            "tile_clean_desc": "Garbage Removal",
            "tile_net_title": "Connection",
            "tile_net_desc": "Your connection to network and Internet",
            "tile_users_title": "User Accounts",
            "tile_users_desc": "Current user and computer accounts",
            "anti_active": "Computer protection is active",
            "anti_exe": " Scan .EXE File",
            "anti_full": " Full PC Scan",
            # 💥 УБРАЛИ ПРИСТАВКУ dev_
            "dev_title": "Connected Computer Devices",
            "mouse": "Primary Input Device",
            "kb": "Standard Keyboard",
            "mic": "Audio Microphone",
            "audio": "Audio System / Speakers",
            "flash": "Removable Storage (USB Drive)",
            "cam": "Web Camera / Video Device"
        }
    }


    @classmethod
    def load_all(cls):
        assets_dir = os.path.join(os.path.dirname(__file__), "Assets")
        if not os.path.exists(assets_dir):
            return
        for filename in os.listdir(assets_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_path = os.path.join(assets_dir, filename)
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    icon_name = os.path.splitext(filename)[0]
                    cls.icons[icon_name] = pixmap

    @classmethod
    def get(cls, name):
        return cls.icons.get(name, QPixmap())

    @classmethod
    def text(cls, key):
        return cls.STRINGS[cls.current_lang].get(key, key)
    @classmethod
    def get(cls, name):
        return cls.icons.get(name, QPixmap())

    @classmethod
    def text(cls, key):
        return cls.STRINGS[cls.current_lang].get(key, key)

    # 💥 ДОБАВЛЯЕМ СЮДА: Скрипт мгновенного воспроизведения звука XP
    @classmethod
    def play_click(cls):
        try:
            import winsound
            import os
            # Строим абсолютный путь с учётом структуры папок проекта
            base_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(base_dir, "Assets", "click.wav")

            if os.path.exists(sound_path):
                # Флаг SND_NODEFAULT запрещает Windows включать звук ошибки, если что-то пойдёт не так
                winsound.PlaySound(sound_path,
                                   winsound.SND_FILENAME | wintypes.SND_ASYNC if 'wintypes' in locals() else winsound.SND_FILENAME | winsound.SND_ASYNC | 0x0002)
            else:
                print(f"⚠️ Файл звука не найден по пути: {sound_path}")
        except Exception as e:
            print(f"Ошибка воспроизведения звука: {e}")
