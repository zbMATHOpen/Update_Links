
import pandas as pd

import pytest
from fixtures import df_ext_partner, df_scrape

from update_zblinks_api.update_with_api import separate_links
from update_zblinks_api.helpers.source_helpers import get_titles


def test_separation(df_ext_partner, df_scrape):
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


def test_title_change_on_edit(df_ext_partner, df_scrape):
    partner = "DLMF"

    df_scrape.loc[
        df_scrape["document"] == 4567, "title"
    ] = "newly scraped title"

    df_new, df_edit, df_delete = separate_links(
        partner, df_ext_partner, df_scrape
    )

    assert 4567 in df_edit["document"].to_list()


@pytest.mark.skip(reason='uses get_title fcn without patch')
def test_get_titles(df_scrape):
    df_res = get_titles(df_scrape,"DLMF")
    assert len(df_res.index) == 0


def test_two_in_same_permalink_one_changed(df_ext_partner, df_scrape):
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


def test_two_added_in_same_permalink_one_exits(df_ext_partner, df_scrape):
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


def test_two_links_with_same_permalink_one_changed(df_ext_partner, df_scrape):
    partner = "DLMF"

    data = {"document": [4567]*2,
            "external_id" :["abcd#i.p4", "abcd#i.p7"],
            "type": ["DLMF"]*2}
    df_same_ext_id_doc =  pd.DataFrame(data)
    df_ext_partner = pd.concat([df_ext_partner, df_same_ext_id_doc])

    data_scrape = {"document": [4567]*2,
                   "external_id" :["abcd#i.p4", "abcd#i.p8"],
                   "type": ["DLMF"]*2}
    df_change_scrape = pd.DataFrame(data_scrape)
    df_scrape = pd.concat([df_scrape, df_change_scrape])
    df_scrape.loc[
        df_scrape["document"] == 4567, "title"
    ] = "None"

    df_new, df_edit, df_delete = separate_links(
        partner, df_ext_partner, df_scrape
    )

    df_edit_doc = df_edit.loc[
        df_edit["document"] == 4567, "previous_ext_id"
    ]

    assert "abcd#i.p4" not in df_edit_doc.to_list()
