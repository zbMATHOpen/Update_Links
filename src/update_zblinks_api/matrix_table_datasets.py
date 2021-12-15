import click
import pandas as pd
from pkg_resources import get_distribution

import importlib

from update_zblinks_api import partners
from update_zblinks_api.helpers.zbmath_helpers import get_des_from_zbl_ids
from update_zblinks_api.update_with_api import post_request

hist_scrape_dict = {}
for partner in partners:
    partner = partner.lower()
    mod_name = f"update_zblinks_api.{partner}_scraping." \
               f"historical.scrape_{partner}_historical"
    imported_module = importlib.import_module(mod_name)
    hist_scrape_dict[partner] = getattr(imported_module,
                                        f"get_df_{partner}_initial")


def create_deids_table_dataset(partner, df_hist):
    """
    Creates a csv file which can be inserted into the document_external_ids table.
    Has columns "document", "external_id", "type", "matched_at", "matched_by",
    "matched_by_version"

    Parameters
    ----------
    partner : str
        partner (in lowercase) from which the initial datasets are to come.
    df_hist : dataframe
        contains columns: "document" (or "zbl_code"), "external_id",
        "date" (as int year).

    """

    df_hist = df_hist.rename(columns={"date": "matched_at"})

    df_hist["type"] = partner

    df_hist["title"] = ""

    df_hist["matched_at"] = df_hist["matched_at"] + "-01-01"

    dist = get_distribution("update-zblinks-api")
    df_hist["matched_by"] = "zbmath-links-api"
    df_hist["matched_by_version"] = dist.project_name + ":" + dist.version

    if "zbl_code" in df_hist.columns:
        df_hist = get_des_from_zbl_ids(df_hist)

    column_order = ["document", "external_id", "type", "title",
                    "matched_at", "matched_by", "matched_by_version"]
    df_hist = df_hist.reindex(columns=column_order)

    return df_hist


@click.command()
@click.option('--partner', '-p',
              help="partner from which the initial datasets are to come",
              required=True
              )
@click.option(
    "--file", is_flag=True,
    help="Use this option to write the data to csv files"
         "instead of writing to the matrix"
)
def matrix_table_entries(partner, file):
    """
    creates the initial csv files for matrix table insertions
    (for the document_external_ids and zb_links.source tables)
    for the particular partner

    Parameters
    ----------
    partner : str
        partner from which the initial datasets are to come.

    """
    partner = partner.lower()

    df_init_partner = hist_scrape_dict[partner]()

    df_hist = create_deids_table_dataset(partner, df_init_partner)
    if file:
        df_hist.to_csv(f"results/{partner}_deids_table_init.csv", index=False)
    else:
        df_hist = df_hist[
            ["document", "external_id", "title",
             "matched_at", "matched_by_version"]
        ]
        for _, row in df_hist.iterrows():
            post_request(row, partner, df_hist.columns)
