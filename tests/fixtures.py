
import pytest

import pandas as pd


@pytest.fixture
def df_ext_partner():
    data = {"document": [1234, 4567, 7890],
            "external_id" :["abcd#i.p4", "defg#ii", "ghij"],
            "type": ["DLMF"]*3}
    return pd.DataFrame(data)


@pytest.fixture
def df_scrape():
    data = {"document": [1234, 4567, 1357],
            "external_id" :["abcd#i.p5", "defg#ii", "ftyd#iv.p5"],
            "title": ["None"]*3,
            "type": ["DLMF"]*3}
    return pd.DataFrame(data)


def mock_get_titles(df_link, partner):
    df_link["title_doc_ext_ids"] = "None"
    return df_link