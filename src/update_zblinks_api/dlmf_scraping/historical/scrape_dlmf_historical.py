
import pandas as pd
import string
from helpers import historical_helpers


def get_df_dlmf(year):
    external_id = []
    zbl_code = []

    upper_list = list(string.ascii_uppercase)
    for each_letter in upper_list:
        if year == 2008:
            historical_helpers.scrape_page_2008(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2009:
            historical_helpers.scrape_page_2009(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2011:
            historical_helpers.scrape_page_2011(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2012:
            historical_helpers.scrape_page_2012(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2013:
            historical_helpers.scrape_page_2013(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2014:
            historical_helpers.scrape_page_2014(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2015:
            historical_helpers.scrape_page_2015(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2016:
            historical_helpers.scrape_page_2016(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2017:
            historical_helpers.scrape_page_2017(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2018:
            historical_helpers.scrape_page_2018(
                letter=each_letter,
                external_id=external_id,
                zbl_code=zbl_code
            )
        if year == 2019:
            historical_helpers.scrape_page_2019(
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


get_df_dlmf(2020)