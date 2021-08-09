import pandas as pd
from update_zblinks_api.update_with_api import separate_links
import scrape_dlmf_historical


df_main = pd.DataFrame(columns=(["document", "external_id", "date", "title"]))

def get_all_historical():
    for year in range (2008, 2011, 1):
        df_scrape = scrape_dlmf_historical.get_df_dlmf(year)
        df_new, df_edit, df_delete = separate_links("DLMF", df_main, df_scrape)
        df_new["date"] = year
        csv_new = df_new.to_csv(f"dlmf_new_{year}.csv", index = False)
        csv_edit = df_edit.to_csv(f"dlmf_edit_{year}.csv", index=False)
        csv_delete = df_delete.to_csv(f"dlmf_delete_{year}.csv", index=False)

        return csv_new, csv_edit


if __name__ == "__main__":
    get_all_historical()