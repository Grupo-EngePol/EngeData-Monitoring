# -*- mode: python ; coding: utf-8 -*-
# This is a specification file for compiling the application into a single folder

block_cipher = None


a = Analysis(['server.py'],
             pathex=['D:\\app_ElDorado\\GUI-Dash-02-26-24\\src'],
             binaries=[],
             datas=[
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/dash_iconify','dash_iconify'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/dash_mantine_components','dash_mantine_components'), 
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/dash_bootstrap_components','dash_bootstrap_components'), 
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/dash_bootstrap_templates','dash_bootstrap_templates'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/dash_daq','dash_daq'), 
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/plotly','plotly'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/dash','dash'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/joblib','joblib'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/dash','dash'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/numpy','numpy'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/pandas','pandas'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/sklearn','sklearn'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/scipy','scipy'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/matplotlib','matplotlib'),
               ('C:/Users/nacla/anaconda3/envs/ElDotado/Lib/site-packages/openpyxl','openpyxl'),


               ('D:/app_ElDorado/GUI-Dash-02-26-24/src/assets','assets'),
               ('D:/app_ElDorado/GUI-Dash-02-26-24/src/Backend','Backend'),
               ('D:/app_ElDorado/GUI-Dash-02-26-24/src/components','components'),
               ('D:/app_ElDorado/GUI-Dash-02-26-24/src/utils','utils'),

               ('D:/app_ElDorado/GUI-Dash-02-26-24/src/redeESN.py','.'),

                  
                  ],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='launch_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          icon = 'assets/icons/icon.ico',
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')
