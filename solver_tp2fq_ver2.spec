# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['solver_tp2fq_ver2.py'],
             pathex=['C:\\Users\\Lenovo\\Desktop\\-Fingerprint-Shazam_DSP2022'],
             binaries=[],
             datas=[],
             hiddenimports=['scipy.spatial.transform._rotation_groups'],
             hookspath=[],
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
          name='solver_tp2fq_ver2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
