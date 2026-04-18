from setuptools import setup, find_packages

setup(
    name="artha",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ollama>=0.1.0",
        "python-dotenv>=1.0.0"
    ],
)
