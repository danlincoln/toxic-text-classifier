# Toxic Text Classifier Jupyter Notebooks

The notebooks in this folder were used to explore the dataset and to build
early prototypes of the classifier model.

To run them, you will need the dependencies listed in 
`src/classifier_project/requirements.txt`. Using a virtual environment is
recommended.

## Set Up a Python Virtual Environment

1. Create a python virtual environment in the project root.

        $ python3.12 -m venv venv

2. Activate the virtual environment.

        $ source venv/bin/activate

3. Install project dependencies.

        (venv) $ pip install -r src/classifier_project/requirements.txt

## Start Up the Database

4. The notebooks connect to the application database inside a Docker container.
Make sure the containers are running before you run code in the notebooks.

        $ docker compose up -d

## Run the Notebooks

5. Run the notebooks. Be sure that the Python executable is set to 
`venv/bin/python` in whatever editor you use.
