import click
import pandas as pd

import importlib

from update_zblinks_api import partners
from update_zblinks_api.helpers.zbmath_helpers import get_des_from_zbl_ids

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
        partner from which the initial datasets are to come.
    df_hist : dataframe
        contains columns: "document" (or "zbl_code"), "external_id",
        "date" (as int year).

    """

    df_hist = df_hist.rename(columns={"date": "matched_at"})

    df_hist["type"] = partner.lower()

    df_hist["matched_at"] = pd.to_datetime(df_hist["matched_at"], format="%Y")
    df_hist["matched_at"] = (
        df_hist["matched_at"].dt.tz_localize("CET").dt.tz_convert(
            "Europe/Berlin"
        )
    )

    df_hist["matched_by"] = "zbmath-links-api"
    df_hist["matched_by_version"] = "1.0.0"

    if "zbl_code" in df_hist.columns:
        df_hist = get_des_from_zbl_ids(df_hist)

    column_order = ["document", "external_id", "type", "matched_at",
                    "matched_by", "matched_by_version"]
    df_hist = df_hist.reindex(columns=column_order)

    df_hist.to_csv(f"results/{partner}_deids_table_init.csv", index=False)


@click.command()
@click.option('--partner', '-p',
              help="partner from which the initial datasets are to come",
              required=True
              )
def create_matrix_table_datasets(partner):
    """
    creates the initial csv files for matrix table insertions
    (for the document_external_ids and zb_links.source tables)
    for the particular partner

    Parameters
    ----------
    partner : str
        partner from which the initial datasets are to come.

    """

    # this also creates the initial dataset for the zb_links.source table
    df_init_partner = hist_scrape_dict[partner.lower()]()

    create_deids_table_dataset(partner, df_init_partner)
