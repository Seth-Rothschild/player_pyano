from setuptools import setup, find_packages
import io
import os


def read(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with io.open(filepath, mode="r", encoding="utf-8") as f:
        return f.read().splitlines()


setup(
    name="player_pyano",
    packages=find_packages(),
    version="0.0.1",
    entry_points={"console_scripts": ["player_pyano = player_pyano.__main__:main"]},
    author="Seth Rothschild",
    author_email="seth.j.rothschild@gmail.com",
    description="A web application to select and send midi",
    install_requires=read("requirements.txt"),
    tests_require=["pytest"],
    test_suite="pytest",
)
