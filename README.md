## Update package for the zbMATH Links API

The purpose of this package is to populate and update the database used by another package produced at [zbMATH](https://zbmath.org/), namely the zbMATH Links API `zbmath-links-api`, available [here](https://github.com/zbMATHOpen/linksApi).

Here we provide some simple instructions to install and use this package.

1) Install the requirements and set the environment variables.
On a first install:

    ```
    python3 -m venv env
    source env/bin/activate
    pip install -e .
    ```

    This will install the package, `update-zblinks-api` in the [virtual environment](https://docs.python.org/3/tutorial/venv.html).


2) Fill in the `config_template.ini` and save it as `config.ini`.
Default for config file is `\etc\update_zblinks_api`.
Alternately, set the location of the config.ini file in the environment variable
`UPDATE_API_CONFIG`.

    (i) The URL should be the endpoint for link items, e.g.,
    http://my_host/links_api/link/item

    (ii) Fill in database information.

    (iii) The API-KEY is the one used by the API package `zbmath-links-api`.


3) The package has three entry points:

    (i) Use the command

   ```
   initial-entries -p <partner>
   ```

   to initialise the database with historical data for the given partner.

   **Remark.** Note that this command will populate the tables `document_external_ids` and `source` with links corresponding to documents that already exist  in the table `math_documents`.

   **Remark.**  One can use  the option --file to create a csv file with historical partner data: `{partner}_deids_table_init.csv` (to be inserted into the table `document_external_ids`).
   The file will be created in the `update_zblinks_api/results` folder.

    (ii) Use the command

    ```
    update-api
    ```

    to scrape (i.e., to obtain all links) all zbMATH partners and update the database used by the package `zbmath-links-api`.
    This will automatically add new links, delete links that no longer exist, and edit links that have been modified.
    This has to be used once the database has been already initialised with the previous command.

    **Remark.** One can use  the option --file to generate csv files (but not update the database) which can be used to manually update the database.
This creates three csv files: `{partner}_new_links.csv`, `{partner}_to_edit.csv`, `{partner}_delete.csv` with the obvious contents, contained in the `update_zblinks_api/results` folder.


   (iii) Use the command

   ```
   csv-to-db
   ```

   to export the csv files from the output of `update-api --file`  to the database.

