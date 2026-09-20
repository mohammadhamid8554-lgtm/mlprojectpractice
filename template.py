import os
import logging
from pathlib import Path

logging.basicConfig(level= logging.INFO)

# Use one project name to build all package and module paths consistently.
project_name = "ml_project_practice"

# These are the files and folders required by the project skeleton.
list_of_files = [


    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/components/data_ingestion.py",
    f"src/{project_name}/components/data_transformation.py",
    f"src/{project_name}/components/model_trainer.py",
    f"src/{project_name}/components/model_monitoring.py",
    f"src/{project_name}/pipelines/__init__.py",
    f"src/{project_name}/pipelines/training_pipeline.py",
    f"src/{project_name}/pipelines/prediction_pipeline.py",
    f"src/{project_name}/exception.py",
    f"src/{project_name}/logger.py",
    f"src/{project_name}/utils.py",
    "requirements.txt",
    "app.py",
    "main.py",
    "README.md",
    "Dockerfile",
    "setup.py"
]

# Create missing directories and empty files without overwriting existing work.
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    # Create the parent folder before trying to create the file inside it.
    if filedir != "":
        os.makedirs(filedir, exist_ok= True)
        logging.info(f"Create Directory: {filedir}")

    # Only create a file when it is missing or completely empty.
    if (not os.path.exists(filepath) or os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f'{filename} already exists!!')