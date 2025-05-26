# cronometro_desligar.spec
# -*- mode: python ; coding: utf-8 -*-
import os
block_cipher = None

a = Analysis(
    ['cronometro_desligar.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.ico', '.')] if os.path.exists('icon.ico') else [],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='cronometro_desligar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
