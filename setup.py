from typing import List
from setuptools import setup, find_packages


HYPEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    # Read dependency names so setuptools can install them with the package.
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        # Editable installation is useful during development but is not a package dependency.
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    # Package metadata used when this project is installed with pip.
    name= "ml_project_practice",
    author= "Mohammed Hamid",
    author_email= "mohammadhamid8554@gmail.com",
    version= "0.1.0",
    packages= find_packages(),
    install_requires=  get_requirements("requirements.txt"),
    description= "Machine learning practice project",
    python_requires = ">3.8"
)

