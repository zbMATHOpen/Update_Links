# ------------------------------------------------------------------------------
# Code to scrape the 2008-2020 DLMF bibliography and create a Pandas dataframe
# ------------------------------------------------------------------------------

import pandas as pd
import string
from helpers import historical_helpers


def get_df_dlmf(year):
    external_id = []
    zbl_code = []

    upper_list = list(string.ascii_uppercase)
    for each_letter in upper_list:
        if year == 2008 or year == 2009 or year == 2010:
            historical_helpers.scrape_page_2008_2010(
                year=year,
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2011 or year == 2012:
            historical_helpers.scrape_page_2011_2012(
                year=year,
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2013 or year == 2014 or year == 2015 \
                or year == 2016 or year == 2017 or year == 2018 or year == 2019:
            historical_helpers.scrape_page_2013_2019(
                year=year,
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2020:
            historical_helpers.scrape_page_2020(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )

    together_list = []
    together_list.append(zbl_code)
    together_list.append(external_id)
    zipped_list = list(zip(*together_list))

    df = historical_helpers.get_dataframe(zipped_list=zipped_list)
    return df