# Toxic Text Classifier

This project is a machine learning toxic text classifier—it's the capstone 
project for my bachelor's degree in Computer Science at Western Governors 
University. It uses a multinomial naïve Bayes algorithm to classify text input as either toxic or not toxic.

The application runs in two Docker containers: one running PostgreSQL and
another running Python.

## Getting Started

1. Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

    * For more information, guides, and manuals on using Docker, see the 
    [Docker Documentation](https://docs.docker.com/).

2. Open a terminal and navigate to the root directory of this project (the same
level `docker-compose.yml` is on).

    * Mac example (assuming you saved the project to your downloads folder):

            cd ~/Downloads/toxic-text-clasifier

    * Windows example (again assuming the project is in your downloads folder):

            cd %USERPROFILE%\Downloads\toxic-text-classifier

3. Start the containers using Docker Compose.

        $ docker compose up

    * If you do not want to observe the application's startup logs, start in
    detatched mode:

            $ docker compose up -d

4. When you see startup has completed, open a browser and navigate to 
[http://localhost:8000](http://localhost:8000)

## Update Environment Variables

The [.env](.env) file contains placeholder variables to get started. Please
be sure to update them to unique values when you clone this repository.
