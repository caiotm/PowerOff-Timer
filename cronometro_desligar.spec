# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Diretórios padrão do Python (ajustável se necessário)
python_dir = sys.exec_prefix
dll_path = os.path.join(python_dir, 'DLLs')
tcl_path = os.path.join(python_dir, 'tcl')

a = Analysis(
    ['cronometro_desligar.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'), 
        ('bot_telegram.py', '.'),

        # Inclui a pasta do Tcl
        (tcl_path, 'tcl'),

        # Inclui as DLLs do tkinter
        (os.path.join(dll_path, 'tk86t.dll'), '.'),
        (os.path.join(dll_path, 'tcl86t.dll'), '.'),
    ],
    hiddenimports=collect_submodules('telegram'),  # Garante que todos os módulos do Telegram sejam incluídos
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='cronometro_desligar',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # janela oculta (modo GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    manifest='admin.manifest',
)
