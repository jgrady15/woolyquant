from setuptools import setup, find_packages

setup(
    name='woolyquant',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'pandas>=1.5.3',
        'pandas_datareader',
        'openai',
        'yfinance',
        'pybind11',
        'cmake',
        'numpy',
        'statsmodels',
        'python-dotenv',
        'alpaca-py',
        'psycopg2',
        'pydantic',
        'pytest',
        'lean'
    ]
)