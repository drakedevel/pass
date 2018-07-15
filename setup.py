from setuptools import setup


setup(
    name='passgen',
    version='0.0.1',

    url='https://github.com/drakedevel/pass',
    author='Andrew Drake',
    author_email='adrake@adrake.org',

    packages=['passgen'],
    install_requires=['docopt~=0.6.2'],

    package_data={
        'passgen': ['words.txt'],
    },
    entry_points={
        'console_scripts': [
            'passgen=passgen:main',
        ],
    },
)
