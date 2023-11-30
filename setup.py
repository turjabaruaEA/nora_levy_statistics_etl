from setuptools import setup, find_packages

setup(
    name='nora_levy_statistics',
    version='2.0.4',
    description='Script to scrape India Oil Data from the PPAC website',
    url='https://github.com/energyaspects/india_oil_data',
    author='EA Data Engineering Team',
    author_email='data-engineering@energyaspects.com',
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'shooju',
        'requests',
        'python-dotenv',
        'xlrd',
        'beautifulsoup4',
    ],
    package_data={
        "": ["*"]
    },
    entry_points={
        'console_scripts': [
            'nora_levy_statistics = nora_levy_statistics.nora_levy_statistics_etl:main',
        ],
    },
    extras_require={
        "test": ["pytest"]
    },
    zip_safe=False,
)
