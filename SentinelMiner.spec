 -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('ui', 'ui'), ('pages', 'pages'), ('utils', 'utils'), ('al/dec2', 'al/dec2'), ('al/dec3', 'al/dec3'), ('al/dig1', 'al/dig1'), ('al/dig2', 'al/dig2'), ('al/dig4', 'al/dig4'), ('al/dig5', 'al/dig5'), ('pro', 'pro'), ('example', 'example'), ('outputs', 'outputs'), ('data', 'data'), ('D:/pysci/xinenv/Lib/site-packages/en_core_web_sm', 'en_core_web_sm')],
    hiddenimports=['sklearn.ensemble._forest', 'en_core_web_sm'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SentinelMiner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.txt',
    icon=['fa.ico'],
)
