import pandas as pd
from update_zblinks_api.update_with_api import separate_links
import scrape_dlmf_historical


def csv_dlmf_initial():
    df_main = pd.DataFrame(
        columns=(["document", "external_id", "date", "title"]))
    for year in range (2008, 2021):
        df_scrape = scrape_dlmf_historical.get_df_dlmf(year)
        df_new, df_edit, df_delete = separate_links("DLMF", df_main, df_scrape)
        df_new["date"] = year
        df_main = pd.concat([df_main,df_new]).drop_duplicates(keep=False)

        df_changes = pd.merge(df_main, df_edit,
                              left_on=["document","external_id"],
                              right_on=["document","previous_ext_id"],
                              how="inner")
        df_changes = df_changes.fillna("")
        df_changes = df_changes.drop(columns=["external_id_x","title_x"])
        df_changes = df_changes.rename(
            columns={"external_id_y": "external_id",
                     "title_y": "title"}
        )
        df_changes = df_changes[
            ["document", "external_id", "date", "title","previous_ext_id"]
        ]

        df_main["previous_ext_id"] = df_main["external_id"]
        df_main = pd.concat([df_main, df_changes]).drop_duplicates(
            subset=["document","previous_ext_id"],
            keep="last"
        )
        df_main = df_main[["document", "external_id", "date", "title"]]

    main_csv = df_main.to_csv(f"initial_dlmf.csv", index = False)
