import click
import requests
import os
import pandas as pd
import psycopg2
from urllib.parse import urlencode

import importlib

from update_zblinks_api import arg_names, params_dict, partners, link_url
from update_zblinks_api.helpers import dlmf_helpers, source_helpers

scrape_dict = {}
for partner in partners:
    partner = partner.lower()
    mod_name = f"update_zblinks_api.{partner}_scraping.scrape_{partner}"
    imported_module = importlib.import_module(mod_name)
    scrape_dict[partner] = getattr(imported_module, f"get_df_{partner}_current")


def get_doc_ext_id_links():
    """
    reads from the document_external_ids table relevant
    link partner data

    Returns
    -------
    df_zblinks_ext_id : pandas DataFrame
        DataFrame representation of external links from
        document_external_ids which only include entries whose
        type is a listed zblinks API partner.

    """
    connection = psycopg2.connect(**params_dict)

    column_request = """
        SELECT document, external_id, type
        FROM document_external_ids
    """
    SQL_QUERY = pd.read_sql_query(column_request, connection)

    file_columns = ["document", "external_id", "type"]
    df_ext_id = pd.DataFrame(SQL_QUERY, columns=file_columns)
    df_ext_id = df_ext_id.fillna("")

    # filter out only entries for zblinks
    df_zblinks_ext_id = df_ext_id[df_ext_id["type"].isin(partners)]

    return df_zblinks_ext_id


def post_request(input_data, partner):
    """
    submits a link post request to the linksApi.

    Parameters
    ----------
    input_data : pandas row
        contains: [document_id, external_id, title]
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.

    """

    dict_input = {arg_names["document"]: input_data[0],
                  arg_names["link_ext_id"]: input_data[1],
                  arg_names["link_partner"]: partner,
                  "title": input_data[2]}
    dict_input = {k: v for k, v in dict_input.items() if v}
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}

    post_url = link_url + "/?" + urlencode(dict_input)
    requests.post(post_url, headers=headers)


def update_request(input_data, partner):
    """
    submits a link patch request to the linksApi.

    Parameters
    ----------
    input_data : pandas row
        contains: [
        document_id, previous_ext_id, external_id, title (possibly null)
        ].
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.

    """

    dict_input = {arg_names["document"]: input_data[0],
                  arg_names["link_ext_id"]: input_data[1],
                  arg_names["link_partner"]: partner,
                  arg_names["edit_link_ext_id"]: input_data[2],
                  "title": input_data[3]}
    dict_input = {k: v for k, v in dict_input.items() if v}
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}

    update_url = link_url + "/?" + urlencode(dict_input)
    requests.patch(update_url, headers=headers)


def delete_request(input_data, partner):
    """
    submits a link delete request to the linksApi.

    Parameters
    ----------
    input_data : pandas row
        contains: [document_id, external_id].
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.

    """

    dict_input = {arg_names["document"]: input_data[0],
                  arg_names["link_ext_id"]: input_data[1],
                  arg_names["link_partner"]: partner}
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}

    delete_url = link_url + "/?" + urlencode(dict_input)
    requests.delete(delete_url, headers=headers)


def separate_links(partner, df_ext_partner, df_scrape):
    """
    determines which links should be added, resp. deleted, resp. edited

    Parameters
    ----------
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.
    df_ext_partner : pandas DataFrame
        DataFrame representation of external links from
        document_external_ids which only include entries whose
        type is the given (as the partner parameter) zblinks API partner.
    df_scrape : pandas DataFrame
        contains all entries from the current scraping of the partner's
        website; columns are 'document', 'external_id', 'title'.

    Returns
    -------
    df_new : pandas DataFrame
        those entries from df_scrape which are to be posted as new links.
    df_edit : pandas DataFrame
        entries from df_scrape which are to be applied as patches
        to existing links.
    df_delete : pandas DataFrame
        those entries from df_ext_partner which are to be deleted.

    """
    df_edit = pd.DataFrame(
        columns=(["document", "external_id", "title", "previous_ext_id"])
    )

    # those links in df_scrape which are not in the matrix
    df_new = pd.concat(
        [df_scrape, df_ext_partner, df_ext_partner]
    ).drop_duplicates(subset=["document", "external_id"], keep=False)

    # those links in the matrix which are not
    # in df_scrape, and are not one of the links to update
    df_delete = pd.concat(
        [df_ext_partner, df_scrape, df_scrape]
    ).drop_duplicates(subset=["document", "external_id"], keep=False)

    # to update:
    if partner == "dlmf":
        df_new, df_edit, df_delete = dlmf_helpers.update(
            df_ext_partner, df_new, df_delete
        )

    # check if already exists in database
    df_exists = pd.merge(df_ext_partner, df_scrape,
                         on=["document", "external_id"],
                         how="inner")
    df_exists_titles = source_helpers.get_titles(df_exists, partner)

    df_new_titles = df_exists_titles[
        df_exists_titles["title_doc_ext_ids"] != df_exists_titles["title"]
        ]

    # if title is different add patch
    df_new_titles = df_new_titles[["document", "external_id", "title"]]
    df_new_titles["previous_ext_id"] = df_new_titles["external_id"]
    df_edit = pd.concat([df_edit, df_new_titles])

    df_new = pd.concat(
        [df_new, df_new_titles, df_new_titles]
    ).drop_duplicates(subset=["document", "external_id"], keep=False)

    df_new = df_new[["document", "external_id", "title"]]

    return df_new, df_edit, df_delete


def scrape(partner):
    """
    calls the web scraping code to scrape the links partner

    Parameters
    ----------
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.

    Returns
    -------
    df_scrape : pandas DataFrame
        contains the data from sraping the partner's website;
        has columns: document, external_id, title.

    """
    df_scrape = scrape_dict[partner.lower()]()
    return df_scrape


@click.command()
@click.option(
    "--file", is_flag=True,
    help="Use this option to write the data to csv files"
         "instead of writing to the matrix"
         "new_links.csv, to_edit.csv, delete_links.csv will be created"
)
def update(file):
    """
    takes the ouput from separate_links() and applies, respectively,
    post, patch, and delete requests.

    """

    for partner in partners:

        df_scrape = scrape(partner)

        df_doc_ext_id = get_doc_ext_id_links()
        df_ext_partner = df_doc_ext_id[df_doc_ext_id["type"] == partner]

        df_new, df_edit, df_delete = separate_links(
            partner, df_ext_partner, df_scrape
        )

        if file:
            df_new.to_csv(f"results/{partner}_new_links.csv", index=False)
            df_edit.to_csv(f"results/{partner}_to_edit.csv", index=False)
            df_delete.to_csv(f"results/{partner}_delete_links.csv", index=False)
        else:
            df_new = df_new.fillna("")
            df_edit = df_edit.fillna("")
            df_delete = df_delete.fillna("")

            for _, row in df_new.iterrows():
                post_request(row, partner)

            for _, row in df_edit.iterrows():
                update_request(row, partner)

            for _, row in df_delete.iterrows():
                delete_request(row, partner)

            source_helpers.remove_lonely_sources(partner)


def use_files_to_update():
    """
    For each partner, inserts the data from the csv files:
    {partner}_new_links.csv, {partner}_to_edit.csv, {partner}_delete_links.csv
    into the database
    These files need to be located in the results folder.

    Parameters
    ----------
    partner : str
        zblinks API partner


    """
    for partner in partners:
        insert_file = f"results/{partner}_new_links.csv"
        try:
            df_insert = pd.read_csv(insert_file)
            df_insert = df_insert.fillna("")
            for _, row in df_insert.iterrows():
                post_request(row, partner)
        except FileNotFoundError:
            click.echo(f"Error: could not find {insert_file}.")

        try:
            edit_file = f"results/{partner}_to_edit.csv"
            df_edit = pd.read_csv(edit_file)
            for _, row in df_edit.iterrows():
                update_request(row, partner)
        except FileNotFoundError:
            click.echo(f"Error: could not find {edit_file}.")

        try:
            delete_file = f"results/{partner}_delete_links.csv"
            df_delete = pd.read_csv(delete_file)
            for _, row in df_delete.iterrows():
                delete_request(row, partner)
        except FileNotFoundError:
            click.echo(f"Error: could not find {delete_file}.")
