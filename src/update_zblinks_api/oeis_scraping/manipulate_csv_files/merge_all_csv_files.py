import shutil
import glob
import pandas as pd


# Concatenate all csv files and produce oeis_dataset.csv
path = r"../csv_datasets"
allFiles = glob.glob(path + "/*.csv")
allFiles.sort()
with open("full_dataset_oeis.csv", "wb") as outfile:
    for i, fname in enumerate(allFiles):
        with open(fname, "rb") as infile:
            shutil.copyfileobj(infile, outfile)
            print(fname + " has been imported.")


# # Convert oeis_dataset.csv into a dataframe
# df = pd.read_csv("full_dataset_oeis.csv", sep="|", header=None)
# # df["id"] = range(1, 1+len(df))
# df.index = df.index + 1
# df.columns = ["sequence_id", "sequence_name", "date_link", "de"]
# # df = pd.read_csv("../csv_datasets/data_337994_342885.csv", sep="|",
# # header=None)
# df.to_csv(r"full_dataset_oeis_after_pandas.csv",
#           sep="|",
#           header=None)

