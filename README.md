# DLMF scraping

1) Install requirements and set the env variables.

    On a first install:
    ```
    python3 -m venv env
    source env/bin/activate
    pip install .
    ```

    This will install the package (dlmf_scraping) in the virtual environment.

    Note: to install the package outside the virtual environment,
    deactivate your virtual environment,
    ```
    deactivate
    ```
    Navigate to root folder, and
    ```
    pip install -e .
    ```

2) Run the code dlmf_scraping_script.py to generate the DLMF csv file.

    ```
    python3 dlmf_scraping_script.py
    ```