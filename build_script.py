import PyInstaller.__main__
import flet
import os

flet_path = os.path.dirname(flet.__file__)

PyInstaller.__main__.run([
    'main.py',
    '--name=bank_accounts',
    '--windowed',
    f'--add-data={flet_path};flet',
    '--additional-hooks-dir=.',
    '--clean',
])