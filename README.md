# Installation Guide

To install the necessary packages and set up the project, follow these steps:

1. Install library pack:
    ```sh
    py -m pip install -r requirements.txt
    ```
2. Create ".env" inside folder :
    ```sh
    JWT_SECRET = "String"
    JWT_ALGORITHM = "HS256"

    CONNECTION_STRING = "mongodb://localhost:27017/"
    ```

3. start up the project:
    ```sh
    py run.py
    ```

Good luck!


