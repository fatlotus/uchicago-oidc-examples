from setuptools import setup, find_packages
setup(
    name="uchicago-oidc-examples",
    description="Contains several example applications that use UChicago-OIDC."
    author="Jeremy Archer <open-source@fatlotus.com>",
    version="1.0",

    packages=find_packages(),
    install_requires=open("requirements.txt").readlines()
)