from setuptools import setup, find_packages

setup(
    name="pyMuellerMat",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pyMuellerMat.physical_models": ["physical_model_csvs/*.csv"]
    },
)