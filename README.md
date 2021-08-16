# Partner scraping

1) Install requirements and set the env variables.

    On a first install:
    ```
    python3 -m venv env
    source env/bin/activate
    pip install .
    ```

    This will install the package (update-zblinks-api) in the virtual environment.

    Note: to install the package outside the virtual environment,
    deactivate your virtual environment:
    ```
    deactivate
    ```
    Navigate to root folder, and
    ```
    pip install -e .
    ```

2) Fill in the config_template.ini and save as config.ini.

    (i) The url should be the endpoint for link items, e.g.,
    http://my_host/links_api/link/item

    (ii) Fill in database information.

    (iii) The API-KEY is the one used by the zbmath_links_api.


3) Available entry points:

    (i) To scrape all partners and modify the database

    ```
    update-api
    ```

    (ii) To generate csv files (but not update the database) which can be used to
    manually update the database:
    ```
    update-api --file
    ```
    This creates three csv files: new_links.csv, to_edit.csv, delete.csv with the obvious contents,
    contained in the update_zblinks_api/results folder.

    (iii) To generate the initial csv files for matrix tables (document_external_ids
    and zb_links.source) for a particular partner:

    ```
    csv-initial -p <partner>
    ```
    This creates two csv files:
    {partner}_deids_table_init.csv, {partner}_source_table_init.csv
    contained in the update_zblinks_api/results folder.




4) Adding other partners, updating code:

    IMPORTANT: the call for the scraping functions depend on the naming of
    the folders, and files.

    scraping modules should be named according to the convention
    update_zblinks_api.{partner}_scraping.scrape_{partner}

    and the funtion in the scrape_{partner} module should be named
    get_df_{partner}_current

    similarly for any historical scraping (for instance to get initial database
    datasets) the modules should be named according to
    update_zblinks_api.{partner}_scraping.historical.scrape_{partner}_historical

    and the funtion in the scrape_{partner}_historical module should be named
    get_df_{partner}_initial

