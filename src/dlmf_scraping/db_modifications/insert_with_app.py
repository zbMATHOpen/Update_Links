import requests
import os

import configparser
config = configparser.ConfigParser()
config.read('config.ini')


def _get_url():
    """

    Returns
    -------
    str
        url of the post link route.

    """
    return config['zblinks']['post_link']


def post_request(input_data):
    """

    Parameters
    ----------
    input_data : pandas row
        contains: [document_id, external_id, parter (type)].

    Posts
    -------
    submits a link post request to the linksApi.

    """

    url = _get_url()
    dict_input = {"DE number": input_data[0],
                  "external id": input_data[1],
                  "partner": input_data[2]}
    headers = {"X-API-KEY": os.getenv("ZBMATH_API_KEY")}

    response = requests.post(url, json=dict_input, headers=headers)


def bulk_data_requests(df_input_data):
    """

    Parameters
    ----------
    df_input_data : pandas Dataframe
        contains 3 columns: document_id (de number),
            external_id
            partner (type in document_external_ids).

    Runs
    -------
    goes through each row in the dataframe, and sends a post
    request based on the row data.

    """

    for _, row in df_input_data:
        post_request(row)
