from setuptools import find_packages
from setuptools import setup

setup(
    name='PythonDefense',
    version='1.0.0',
    description='Tower defense game written in python',
    author='Alex Skladanek, Amer  Khalifa, Benjamin Coretese, Eric Weisfeld, Maxwell Walmer',
    url='https://github.com/mwalmer/Python-Defense',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'run=PythonDefense.main:main'
        ],
    }
)