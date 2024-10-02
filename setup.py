from setuptools import setup, find_packages

setup(
    name='exe_202_backend',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'bcrypt==4.1.2',
        'beanie==1.25.0',
        'fastapi==0.109.0',
        'pydantic==2.5.3',
        'PyJWT==2.8.0',
        'pymongo==4.6.1',
        'uvicorn==0.26.0',
        'umongo==3.1.0',
        'websockets==12.0'

    ],
)
