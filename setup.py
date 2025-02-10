from setuptools import setup, find_packages

setup(
    name="not_hyprland",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'python-xlib>=0.31',
        'cairocffi>=1.4.0',
        'xcffib>=1.2.0',
        'pywayland>=0.4.14',
        'pycairo>=1.23.0',
        'dbus-python>=1.3.2',
    ],
    entry_points={
        'console_scripts': [
            'not-hyprland=src:main',
        ],
    },
)