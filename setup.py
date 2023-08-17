from setuptools import setup, find_packages

setup(
    name='Solar-Control-Program',
    version='1.0.0',
    description='Python Package that Communicates with Pylontech US2000B Plus Batteries and Controls Schneider Conext Components',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'pyModbusTCP',
        'pyserial',
        'configparser'
    ],
    author='Dr. Alexander Pollak',
    author_email='Alexander.Pollak.87@gmail.com',
    keywords=['Pylontech','US2000B','Schneider','Conext'],
    url='https://github.com/AlexanderPollak/Solar-Control-Program',
    entry_points={'console_scripts': ['SolarControl = SCP.main:main']},
)
