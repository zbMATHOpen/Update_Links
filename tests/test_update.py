
import pandas as pd

from unittest.mock import patch
from fixtures import sample_ext_id_data, sample_scrape_data, mock_get_titles

from update_zblinks_api.update_with_api import separate_links
from update_zblinks_api.helpers.source_helpers import get_titles


@patch('update_zblinks_api.helpers.source_helpers.get_titles',
       side_effect=mock_get_titles)
def test_separation(patch):
    df_scrape = sample_scrape_data()
    df_ext_partner = sample_ext_id_data()
    partner = "DLMF"

    df_new, df_edit, df_delete = separate_links(
        partner, df_ext_partner, df_scrape
    )

    assert len(df_new.index) == 1
    assert 1357 in df_new["document"].to_list()

    assert len(df_edit.index) == 1
    assert "abcd#i.p5" in df_edit["external_id"].to_list()

    assert len(df_delete.index) == 1
    assert "ghij" in df_delete["external_id"].to_list()


@patch('update_zblinks_api.helpers.source_helpers.get_titles',
       side_effect=mock_get_titles)
def test_title_change_on_edit(patch):
    df_scrape = sample_scrape_data()
    df_ext_partner = sample_ext_id_data()
    partner = "DLMF"

    df_scrape.loc[
        df_scrape["document"] == 4567, "title"
    ] = "newly scraped title"

    df_new, df_edit, df_delete = separate_links(
        partner, df_ext_partner, df_scrape
    )

    assert 4567 in df_edit["document"].to_list()


def test_get_titles():
    df_scrape = sample_scrape_data()
    df_res = get_titles(df_scrape,"DLMF")
    assert len(df_res.index) == 0


@patch('update_zblinks_api.helpers.source_helpers.get_titles',
       side_effect=mock_get_titles)
def test_two_in_same_permalink_one_changed(patch):
    df_scrape = sample_scrape_data()
    df_ext_partner = sample_ext_id_data()
    partner = "DLMF"

    data = {"document": [1235],
            "external_id" :["abcd#i.p6"],
            "type": ["DLMF"]}
    df_same_perma =  pd.DataFrame(data)
    df_scrape = pd.concat([df_scrape, df_same_perma])

    df_new, df_edit, df_delete = separate_links(
        partner, df_ext_partner, df_scrape
    )

    assert 1235 in df_new["document"].to_list()
    assert 1235 not in df_edit["document"].to_list()


@patch('update_zblinks_api.helpers.source_helpers.get_titles',
       side_effect=mock_get_titles)
def test_two_added_in_same_permalink_one_exits(patch):
    df_scrape = sample_scrape_data()
    df_ext_partner = sample_ext_id_data()
    partner = "DLMF"

    data = {"document": [1234],
            "external_id" :["abcd#i.p6"],
            "type": ["DLMF"]}
    df_same_perma_same_doc =  pd.DataFrame(data)
    df_scrape = pd.concat([df_scrape, df_same_perma_same_doc])

    df_new, df_edit, df_delete = separate_links(
        partner, df_ext_partner, df_scrape
    )

    assert 1234 in df_new["document"].to_list()
    assert 1234 in df_edit["document"].to_list()
