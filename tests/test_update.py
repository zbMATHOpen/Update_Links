
from fixtures import sample_ext_id_data, sample_scrape_data

from update_zblinks_api.update_with_api import separate_links


def test_separation():
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


def test_title_change_on_edit():
    df_scrape = sample_scrape_data()
    df_ext_partner = sample_ext_id_data()
    partner = "DLMF"

    df_scrape.loc[
        df_scrape["document"] == 1234, "title"
    ] = "newly scraped title"

    df_new, df_edit, df_delete = separate_links(
        partner, df_ext_partner, df_scrape
    )

    assert False

