from setuptools import setup,find_packages

setup(
    name="pyMuellerMat",
    version="0.1",
    packages=find_packages(include=["pyMuellerMat*", "physical_models*"]),
)
