# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['interface.py'],
    pathex=[],
    binaries=[],
     datas=[
        ('../images/logo.jpg', 'images'),
        ('../.venv/Lib/site-packages/gradio', 'gradio'),
        ('../.venv/Lib/site-packages/gradio_client', 'gradio_client'),
        ('../.venv/Lib/site-packages/safehttpx', 'safehttpx'),
        ('../.venv/Lib/site-packages/groovy', 'groovy'),
        ('../.venv/Lib/site-packages/faster_whisper/assets/silero_encoder_v5.onnx', 'faster_whisper/assets')

    ],
    hiddenimports=[
        'gradio', 'gradio_client', 'safehttpx', 'groovy'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='interface',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Để hiện log lỗi. Đổi thành False nếu muốn không hiện console
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='interface'
)
