from setuptools import setup


setup(
    name="Mazes",
    version="0.1.0",
    install_requires=["colorama"],
    packages=["mazes"],
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    description="Generates and solves rectangular mazes in the terminal. Comes with Python API.",
    entry_points={
        'console_scripts': [
            'mazes = mazes.cli:cli',
        ],
    },
)