# Toxic Text Classifier

This project is a machine learning toxic text classifier—it's the capstone 
project for my bachelor's degree in Computer Science at Western Governors 
University. It uses a multinomial naïve Bayes algorithm to classify text input as either toxic or not toxic.

The application runs in two Docker containers: one running PostgreSQL and
another running Python.

## Getting Started

1. You will need to download the data set from Kaggle for this project. See
the next section for more details.

2. Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

    * For more information, guides, and manuals on using Docker, see the 
    [Docker Documentation](https://docs.docker.com/).

3. Open a terminal and navigate to the root directory of this project (the same
level `docker-compose.yml` is on).

    * Mac example (assuming you saved the project to your downloads folder):

            cd ~/Downloads/toxic-text-clasifier

    * Windows example (again assuming the project is in your downloads folder):

            cd %USERPROFILE%\Downloads\toxic-text-classifier

4. Start the containers using Docker Compose.

        $ docker compose up

    * If you do not want to observe the application's startup logs, start in
    detatched mode:

            $ docker compose up -d

5. When you see startup has completed, open a browser and navigate to 
[http://localhost:8000](http://localhost:8000)

## Jigsaw Unintended Bias in Toxicity Classification Data Set

This data set was obtained from the *Jigsaw Unintended Bias in Toxicity
Classification* challenge on [Kaggle](https://www.kaggle.com).

The [competition terms](https://www.kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification/rules)
include a section governing the use of this data set.

### Obtaining the Data Set

Because redistribution of this data set outside of Kaggle is forbidden (§7.B.),
the data set is not included in this repository. To obtain a copy, visit the
[Kaggle competition page](https://www.kaggle.com/competitions/jigsaw-unintended-bias-in-toxicity-classification/overview)
and agree to the competition rules. You can then download the data. Once
downloaded, add the .csv files to the [data/](data/) directory.

## Update Environment Variables

The [.env](.env) file contains placeholder variables to get started. Please
be sure to update them to unique values when you clone this repository.
