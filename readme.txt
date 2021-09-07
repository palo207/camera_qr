config.py nastaviť a nakopírovať do priečinka s programom

Spúšťanie cez python interpretter:
1. Inštalácia python interpretteru z https://www.python.org/downloads/windows/
2. Inštalácia potrebných knižníc cez cmd: 
    cd do priečinku camera_qr
    python3 -m pip install -r requirements.txt
    Vytvoriť shortcut pre cam_service dať ho do priečinku startup (win+r shell:startup) 

Vytvorenie exe:
    1. Nastaviť config
    2. cd do priečinku camera_qr
        pyinstaller --onefile cam_service.py