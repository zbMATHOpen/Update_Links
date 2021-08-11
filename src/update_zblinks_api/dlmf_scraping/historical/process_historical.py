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

    result_csv = df_main.to_csv(f"dlmf_result.csv", index = False)

    return result_csv


if __name__ == "__main__":
    csv_all_historical()