from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(file_name: str) -> List[str]:
    '''
    This function returns a list of requirements found in a file
    '''
    requirements_list = []

    with open(file_name, 'r') as file:
        requirements_list = file.readlines()
        requirements_list = [req.strip() for req in requirements_list if req.strip() != '']

    if HYPEN_E_DOT in requirements_list:
        requirements_list.remove(HYPEN_E_DOT)
    
    return requirements_list

setup(
    name="mlproject",
    version="0.0.1",
    description="Machine Learning Project",
    author="Shri Charan",
    author_email="rshricharan29@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)