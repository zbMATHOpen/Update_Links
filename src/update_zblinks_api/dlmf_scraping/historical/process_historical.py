import pandas as pd
from update_zblinks_api.update_with_api import separate_links
import scrape_dlmf_historical


def csv_all_historical():
    df_main = pd.DataFrame(
        columns=(["document", "external_id", "date", "title"]))
    for year in range (2008, 2012, 1):
        df_scrape = scrape_dlmf_historical.get_df_dlmf(year)
        df_new, df_edit, df_delete = separate_links("DLMF", df_main, df_scrape)
        df_new["date"] = year
        df_main = pd.concat([df_main,df_new]).drop_duplicates(keep=False)

        df_changes = pd.merge(df_main, df_edit,
                              left_on="external_id",
                              right_on="previous_ext_id",
                              how="inner")
        # df_changes = df_changes.fillna("")
        # df_changes = df_changes.drop(columns=["external_id"])
        # df_changes = df_changes.rename(columns={"external_id_y": "external_id"})
        # df_changes = df_changes[["document", "external_id", "date",
        #                          "title"]]
        #
        # df_main = pd.concat([df_main, df_changes]).drop_duplicates(
        #     subset=["external_id"], keep="last")

    result_csv = df_main.to_csv(f"dlmf_result.csv", index = False)
    edit_csv = df_edit.to_csv(f"dlmf_edit.csv", index=False)
    changes_csv = df_changes.to_csv(f"dlmf_changes.csv", index=False)



if __name__ == "__main__":
    csv_all_historical()