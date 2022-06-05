from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

with open('VERSION') as file:
    VERSION = file.read()
    VERSION = ''.join(VERSION.split())

setup(
    name='b_continuous_subprocess',
    version=VERSION,
    license='Apache License 2.0',
    packages=find_packages(
        exclude=[
            '.github',
            'venv',
            'b_continuous_subprocess_test',
        ]
    ),
    description=(
        'Allows to execute subprocess commands and get their output in real-time.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@biomapas.com',
    keywords='Subprocess',
    url='https://github.com/biomapas/B.ContinuousSubprocess.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
