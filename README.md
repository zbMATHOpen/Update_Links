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

2) Entry points:

   To scrape the current 2021 DLMF and generate the csv file:
    
      ```
    dlmf-csv-2021
    ```
   
   To scrape the old DLMFs (2008-2020) and generate the csv files:
    
      ```
    dlmf-csv-older
    ```
   
   To generate the final csv files with dates:
    
      ```
    dlmf-csv-final
    ```
    
    The csv file has three columns:
    
    column 1: zbl_id (that is math_documents.zbl_id)
    
    column 2: external_id (that is zb_links.source.id and document_external_ids.external_id)
    
    column 3: title (that is zb_links.source.title)
   
    column 4: created_at (that is document_external_ids.created_at)