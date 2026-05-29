# Aero Control Panel 2006 (Frutiger Aero System Suite)

A universal, lightweight, and user-friendly system configuration tool for Windows, built completely in the classic 2000s Frutiger Aero aesthetic (Windows Vista / 7 era). 

This utility simplifies system management for everyday users, filtering out complex low-level Windows data and replacing it with a clean, responsive interface.

## ⚠️ Current Project Status: BETA STAGE
This project is currently in active development (**Version 0.1.0 Beta**). Minor visual glitches, sound loading delays, or background scanner lags may occur as we continue to optimize performance. A stable release with sound fixes and disk optimization is coming soon!

## Core Modules & Features

*   **Task Manager:** Real-time process monitor that displays only recognizable user applications (e.g., browsers, games, messengers). Features a one-click process termination tool.
*   **Antivirus Shield:** Interactive file scanner supporting custom `.exe` selection and multi-stage system security analysis with dynamic progress feedback.
*   **Hardware Control:** Live USB and hardware monitor. It automatically fetches precise factory descriptions for mice, keyboards, and audio controllers via Windows APIs. It dynamically updates whenever a USB drive or web camera is plugged in or disconnected.
*   **Aero Search:** Global, interactive top-bar search utility that filters local tools and opens specific tabs instantly, complete with embedded 3D icons.
*   **Dynamic Theme Engine:** Loaded with 3 nostalgic high-quality backdrops (Bubbles, Butterfly, Autumn Leaves). Sidemenu controls and app themes automatically adapt their neon highlights and CSS gradients to match the active wallpaper.
*   **Persistent Configuration:** Automatically saves preferred UI colors and language settings across sessions using local persistent storage.

## Tech Stack & Architecture

The application is built on **Python 3** and **PyQt6**, utilizing modular architecture to prevent memory leaks and ensure rapid tab transitions. It leverages low-level Windows subsystem APIs to query device properties and process states efficiently.

*   **GUI Framework:** PyQt6
*   **System Libraries:** `winreg`, `win32gui`, `win32process`, `wmi`, `psutil`
*   **Assets:** Original high-resolution skeumorphic icons and dynamic system loading animations.

## Repository Structure

```text
AeroControlPanel/
├── Assets/          # 40+ high-quality skeuomorphic assets & animations
├── Modules/         # Back-end script mechanics & OS logic
├── Tabs/            # Modular window layouts (Main, Tasks, Network, etc.)
├── assets_loader.py # Central asset compiler and localization table
└── main.py          # Application entry point & core assembly window
```

## Setup & Local Installation

To run this project from the source code, ensure you have Python 3 installed, then clone the repository and install the dependencies:

```bash
pip install PyQt6 pywin32 wmi psutil comtypes
python main.py
```

## Project Credits
Developed by **Orcynand**, with architectural assistance from an AI collaborator.
