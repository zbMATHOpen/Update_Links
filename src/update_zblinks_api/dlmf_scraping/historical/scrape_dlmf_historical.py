# ------------------------------------------------------------------------------
# Code to scrape the 2008-2020 DLMF bibliography and create a Pandas dataframe
# ------------------------------------------------------------------------------

import pandas as pd
import string

from update_zblinks_api.dlmf_scraping.historical.helpers import \
    historical_helpers
from update_zblinks_api.update_with_api import separate_links


def get_df_dlmf(year):
    external_id = []
    document = []
    title = []

    upper_list = list(string.ascii_uppercase)
    for each_letter in upper_list:
        if year >= 2008 and year <= 2010:
            historical_helpers.scrape_page_2008_2010(
                year=year,
                letter=each_letter,
                external_id=external_id,
                title=title,
                document=document
            )
        if year == 2011 or year == 2012:
            historical_helpers.scrape_page_2011_2012(
                year=year,
                letter=each_letter,
                external_id=external_id,
                title=title,
                document=document
            )
        if year >= 2013 and year <= 2019:
            historical_helpers.scrape_page_2013_2019(
                year=year,
                letter=each_letter,
                external_id=external_id,
                title=title,
                document=document
            )
        if year == 2020:
            historical_helpers.scrape_page_2020(
                letter=each_letter,
                external_id=external_id,
                title=title,
                document=document
            )

    together_list = []
    together_list.append(document)
    together_list.append(external_id)
    together_list.append(title)
    zipped_list = list(zip(*together_list))

    df = historical_helpers.get_dataframe(zipped_list=zipped_list)
    return df


def get_df_dlmf_initial():
    """
    scrapes the DLMF website (via wayback machine) for the years
    2008-2020

    Returns
    -------
    df_main : dataframe
        contains link information: zbl_code, external_id (id on DLMF site) pairs,
        date (year in which the link was first found), and title
        (of section in which link appears; to be used in source table).

    """
    df_main = pd.DataFrame(
        columns=(["document", "external_id", "date", "title"]))
    for year in range(2008, 2021):
        df_scrape = get_df_dlmf(year)
        df_new, df_edit, df_delete = separate_links("dlmf", df_main, df_scrape)
        df_new["date"] = str(year)
        df_main = pd.concat([df_main, df_new]).drop_duplicates(keep=False)

        df_changes = pd.merge(df_main, df_edit,
                              left_on=["document", "external_id"],
                              right_on=["document", "previous_ext_id"],
                              how="inner")
        df_changes = df_changes.fillna("")
        df_changes = df_changes.drop(columns=["external_id_x", "title_x"])
        df_changes = df_changes.rename(
            columns={"external_id_y": "external_id",
                     "title_y": "title"}
        )
        df_changes = df_changes[
            ["document", "external_id", "date", "title", "previous_ext_id"]
        ]

        df_main["previous_ext_id"] = df_main["external_id"]
        df_main = pd.concat([df_main, df_changes]).drop_duplicates(
            subset=["document", "previous_ext_id"],
            keep="last"
        )
        df_main = df_main[["document", "external_id", "date", "title"]]

        df_main = pd.concat(
            [df_main, df_delete, df_delete]
        ).drop_duplicates(subset=["document", "external_id"], keep=False)

    df_main = df_main.rename(columns={"document": "zbl_code"})

    return df_main

