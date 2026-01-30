from setuptools import setup

setup(
    name='prmscan',
    version='1.0',
    scripts=['prmscan.py'],  # Point to the main script
    install_requires=[
        'watchdog>=2.1.0',
    ],
    entry_points={
        'console_scripts': [
            'prmscan=prmscan:main',  # The function to run from prmscan.py
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
