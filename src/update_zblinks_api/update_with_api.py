import click
import requests
import os
import pandas as pd
import psycopg2

from update_zblinks_api import params_dict, partners, link_url
from update_zblinks_api.helpers import dlmf_helpers, source_helpers
from update_zblinks_api.dlmf_scraping import scrape_dlmf


def get_doc_ext_id_links():
    """

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
    df_ext_id = df_ext_id.fillna('')

    # filter out only entries for zblinks
    df_zblinks_ext_id = df_ext_id[df_ext_id["type"].isin(partners)]

    return df_zblinks_ext_id


def post_request(input_data, partner):
    """

    Parameters
    ----------
    input_data : pandas row
        contains: [document_id, external_id, title]
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.

    Posts
    -------
    submits a link post request to the linksApi.

    """

    dict_input = {"DE number": input_data[0],
                  "external id": input_data[1],
                  "partner": partner,
                  "title": input_data[3]}
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}

    requests.post(link_url, json=dict_input, headers=headers)


def update_request(input_data, partner):
    """

    Parameters
    ----------
    input_data : pandas row
        contains: [document_id, external_id, title (possibly null)].
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.

    Patches
    -------
    submits a link patch request to the linksApi.

    """

    dict_input = {"DE number": input_data[0],
                  "external id": input_data[1],
                  "partner": partner,
                  "title": input_data[3]}
    dict_input = {k: v for k, v in dict_input.items() if v}
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}

    requests.patch(link_url, json=dict_input, headers=headers)


def delete_request(input_data, partner):
    """

    Parameters
    ----------
    input_data : pandas row
        contains: [document_id, external_id].
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.

    Patches
    -------
    submits a link delete request to the linksApi.

    """

    dict_input = {"DE number": input_data[0],
                  "external id": input_data[1],
                  "partner": partner}

    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}

    requests.delete(link_url, json=dict_input, headers=headers)


def separate_links(partner, df_ext_partner, df_scrape):
    """

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
    df_edit = pd.DataFrame(columns=(["document", "external_id", "title"]))

    # those links in df_scrape which are not in the matrix
    df_new = pd.concat(
        [df_scrape,df_ext_partner,df_ext_partner]
    ).drop_duplicates(subset=["document","external_id"], keep=False)

    # those links in the matrix which are not
    # in df_scrape, and are not one of the links to update
    df_delete = pd.concat(
        [df_ext_partner, df_scrape, df_scrape]
    ).drop_duplicates(subset=["document","external_id"], keep=False)

    # to update:
    if partner == "DLMF":
        df_new, df_edit, df_delete = dlmf_helpers.update(
            df_ext_partner, df_new, df_delete
        )

    # check if already exists in database
    df_exists = pd.merge(df_ext_partner, df_scrape,
                         on=["document", "external_id"],
                         how="inner")

    df_exists["title_doc_ext_ids"] = df_exists[
        ["document", "external_id"]
    ].apply(lambda x: source_helpers.get_titles(x, partner))
    df_exists = df_exists[df_exists["title_doc_ext_ids"] != df_exists["title"]]

    # if title is different add patch
    df_exists = pd.concat(
        [df_exists, df_ext_partner, df_ext_partner]
    ).drop_duplicates(subset=["document", "external_id"], keep=False)

    df_edit = pd.concat([df_edit, df_exists])

    df_new = pd.concat(
        [df_new, df_exists, df_exists]
    ).drop_duplicates(subset=["document", "external_id"], keep=False)

    return df_new, df_edit, df_delete


def scrape(partner):
    """

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
    # TODO: needs to be implemented
    # scrape the desired partner and return a DataFrame with the current info
    df_scrape = scrape_dlmf.get_df_dlmf_2021()
    return df_scrape


@click.command()
@click.option(
    "--file", is_flag=True,
    help="Use this option to write the data to csv files"
         " instead of writing to the matrix"
         "new_links.csv, to_edit.csv, delete_links.csv will be created"
)
def update(file):
    """

    Runs
    -------
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
            df_new.to_csv("new_links.csv", index=False)
            df_edit.to_csv("to_edit.csv", index=False)
            df_delete.to_csv("delete_links.csv", index=False)
        else:
            for _, row in df_new:
                post_request(row, partner)

            for _, row in df_edit:
                update_request(row, partner)

            for _, row in df_delete:
                delete_request(row, partner)
