from setuptools import setup

APP = ['main.py']  # entry point of your app
DATA_FILES = ['assets']  # include your images folder
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PIL'],
    'includes': ['tkinter']
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
)