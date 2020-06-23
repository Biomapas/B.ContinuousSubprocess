from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='biomapas_continuous_subprocess',
    version='1.0.0',
    license='Apache License 2.0',
    packages=find_packages(exclude=[
        # Exclude virtual environment.
        'venv',
        # Exclude test source files.
        'biomapas_continuous_subprocess_test'
    ]),
    description=(
        'Allows to execute subprocess commands and get their output in real-time.'
    ),
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@biomapas.com',
    keywords='Subprocess',
    url='https://github.com/biomapas/BiomapasContinuousSubprocess.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
