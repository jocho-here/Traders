# Backend

## Technologies
|                       |                             |
| :--                   | :--                         |
| **Language**          | Python 3.x (preferably 3.7) |
| **Package Manager**   | Pipenv                      |
| **Framework**         | Flask                       |
| **Database**          | MySQL 5.7                   |
| **Containerization**  | Docker                      |

## Installation
1. Install `pipenv` and set up the virtual environment
    - `python3 -m pip install pipenv`
        - Installing `pipenv` on Python 3.x
    - `pipenv shell`
        - This boots up a virtual environment shell
    - `pipenv install pip==18.0`
        - This downgrades the pip, fixing a bug with the version 18.1
    - `pipenv install --dev -e .`
        - Installing all the requirements by `Pipfile`
        - This also packagerizes `traders_back`
2. Install `docker` and `docker-compose`
    - Google :)

## Starting the backend
1. Boot up MySQL DB from the `docker-compose.yml`
    - `docker-compose up` in the directory with `docker-compose.yml`
2. Run the Flask backend
    - `pipenv shell`
    - `python app.py`


## Feed Exchange Rates (Important)
1. source tests/download_cmd.sh
2. python tests/upload_rates.py
    - Thses two might take long, interrupt the processing if needed, but keep in mind create position will be based on any conversion to "USD". If testing with buying currency A to currency B, it is important that there is conversion of currency A and B to USD.
