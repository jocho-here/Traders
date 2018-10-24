from setuptools import setup, find_packages

requires = [
    'flask>=0.1',
    'flask-cors>=0.1',
    'pymysql>=0.1'
]

setup(
    name='traders_back',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
