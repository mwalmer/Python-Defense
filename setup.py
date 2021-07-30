import sys
from cx_Freeze import setup, Executable

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name='PythonDefense',
    version='2.0.0',
    description='Tower defense game written in python',
    author='Alex Skladanek, Amer  Khalifa, Benjamin Coretese, Eric Weisfeld, Maxwell Walmer',
    url='https://github.com/mwalmer/Python-Defense',
    packages=['PythonDefense'],
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'play_PythonDefense=PythonDefense.main:main',
        ],
    },
    install_requires=[
        'pygame~=2.0.1',
        'numpy~=1.21.0',
        'cx-Freeze~=6.7',
    ],
    include_package_data=True,
    executables=[Executable("PythonDefense/main.py", base=base)]
)
