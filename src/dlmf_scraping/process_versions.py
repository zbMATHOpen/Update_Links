import datetime
from dateutil import relativedelta
import pandas as pd

name_dict = dict()

start_date = datetime.date(2008, 1, 1)
end_date = datetime.date(2021, 1, 1)

version_date = start_date
count = 0
while version_date < end_date:
    name_dict[count] = "dlmf_dataset_" + str(version_date.year) + ".csv"
    count += 1
    version_date += relativedelta.relativedelta(years=+1)

name_dict[count] = "dlmf_dataset_" + str(version_date.year) + ".csv"

column_names = ["zbl_code", "source_val"]

old_file_path = "csv_files/" + name_dict[0]

df_old = pd.read_csv(
    old_file_path,
    engine="python",
    names=column_names,
    index_col=False
)

df_old = df_old[["zbl_code", "source_val"]]

df_old = df_old.drop_duplicates(subset=["zbl_code", "source_val"])

df_date_added = df_old[["zbl_code", "source_val"]]

df_date_added["date_added"] = name_dict[0].split(".csv")[0][-4:]

number_versions = len(name_dict)

for i in range(number_versions - 1):
    new_file_path = "csv_files/" + name_dict[i + 1]
    df_new = pd.read_csv(
        new_file_path,
        engine="python",
        names=column_names,
        index_col=False
    )
    df_new = df_new[["zbl_code", "source_val"]]
    df_new["date_added"] = name_dict[i + 1].split(".csv")[0][-4:]
    df_new = df_new.drop_duplicates(subset=["zbl_code", "source_val"])
    df_link_insert = pd.concat([df_new, df_old, df_old]).drop_duplicates(
        subset=["zbl_code", "source_val"], keep=False)
    df_link_delete = pd.concat([df_old, df_new, df_new]).drop_duplicates(
        subset=["zbl_code", "source_val"],
        keep=False
    )
    df_date_added = pd.concat(
        [df_date_added, df_link_delete, df_link_delete]).drop_duplicates(
        subset=["zbl_code", "source_val"],
        keep=False
    )
    df_date_added = pd.concat([df_date_added, df_link_insert]).drop_duplicates(
        subset=["zbl_code", "source_val"]
    )
    df_old = df_new


def write_csv_final():
    df_date_added.to_csv(
        "csv_files/dlmf_dataset_final.csv",
        sep=",",
        mode="w",
        index=False
    )


write_csv_final()
