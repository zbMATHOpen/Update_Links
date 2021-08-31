## Update package for the zbMATH Links API

The purpose of this package is to populate and update the database used by another package produced at [zbMATH](https://zbmath.org/), namely the zbMATH Links API `zbmath-links-api`, available [here](https://github.com/zbMATHOpen/linksApi). 
The usage of the present package is mainly described in the README file of the `zbmath-links-api` package.

Here we provide some simple instructions to install and use this package.

1) Install the requirements and set the environment variables.
On a first install:

    ```
    python3 -m venv env
    source env/bin/activate
    pip install -e .
    ```

    This will install the package, `update-zblinks-api`, in the [virtual environment](https://docs.python.org/3/tutorial/venv.html). 
    

2) Fill in the `config_template.ini` and save it as `config.ini`.

    (i) The URL should be the endpoint for link items, e.g.,
    http://my_host/links_api/link/item

    (ii) Fill in database information.

    (iii) The API-KEY is the one used by the API package `zbmath-links-api`.


3) The package has two entry points:

    (i) To scrape (i.e., to obtain all links) all zbMATH partners and update the database used by the package `zbmath-links-api` use the command

    ```
    update-api
    ```
    
    This will automatically add new links, delete links that no longer exist, and edit links that have been modified. 
    
    **Remark 1.** The present version of the package works with the [Digital Library of Mathematical Functions](https://dlmf.nist.gov/) (DLMF) as zbMATH partner. 
    Therefore, one can use the command
    
    ```
    update-api -p DLMF
    ```
    
    to update the DLMF dataset managed by `zbmath-links-api`.
    In the next future, some scraping scripts for other partners will be integrated into this package, and the command
    
    ```
    update-api
    ```
    
    will do an automatic update of all links managed by `zbmath-links-api` for all partners.

    **Remark 2.** To generate CSV files (but not update the database) which can be used to manually update the database use the command
    
    ```
    update-api --file
    ```
    
    This creates three CSV files: `new_links.csv`, `to_edit.csv`, `delete.csv` with the obvious contents, contained in the `update_zblinks_api/results` folder.

    (ii) Use the command

   ```
   csv-initial -p DLMF
   ```
   
   to create two csv files with real DLMF data up to the year 2020: `DLMF_deids_table_init.csv` (to be inserted into the table `document_external_ids`) and   `DLMF_source_table_init.csv` (to be inserted into the table `source`). 
   These files are contained in the `update_zblinks_api/results` folder.


