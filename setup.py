from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

setup(
    name="multiagentbattlesim",
    version="0.0.1",
    packages=find_packages(),
    author='Shyam Sudhakaran',
    author_email='shyamsnair97@gmail.com',
    install_requires=all_reqs,
    description='Multi Agent Battle Simulation',
    include_package_data=True,
)

