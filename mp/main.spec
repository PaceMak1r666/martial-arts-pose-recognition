# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['D:\\openpose\\test_1\\mp\\main.py',
     'D:\\openpose\\test_1\\mp\\login_window.py',
     'D:\\openpose\\test_1\\mp\\angle_calculation.py',
     'D:\\openpose\\test_1\\mp\\main_window.py',
     'D:\\openpose\\test_1\\mp\\data_processing.py',
     'D:\\openpose\\test_1\\mp\\score_calculation.py',
     'D:\\openpose\\test_1\\mp\\video_processor.py',
     'D:\\openpose\\test_1\\mp\\Ui_login.py',
     'D:\\openpose\\test_1\\mp\\Ui_main.py',
     'D:\\openpose\\test_1\\mp\\rules_1.py']
             pathex=['D:/openpose/test_1/mp'],
             binaries=[],
             datas=[],
             hiddenimports=['mp.source.image.pic_rc'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
