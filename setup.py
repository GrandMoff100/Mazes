from setuptools import setup


setup(
    name="Mazes",
    version="0.2.1",
    url="https://github.com/GrandMoff100/Mazes",
    author="GrandMoff100",
    author_email="nlarsen23.student@gmail.com",
    install_requires=["colorama", "termcolor"],
    packages=["mazes"],
    long_description=open('README.md', 'r').read(),
    long_description_content_type="text/markdown",
    description="Generates and solves rectangular mazes in the terminal. Comes with Python API.",
    entry_points={
        'console_scripts': [
            'mazes = mazes.cli:cli',
        ],
    }
)