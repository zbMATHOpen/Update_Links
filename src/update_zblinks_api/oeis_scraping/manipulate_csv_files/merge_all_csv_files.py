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

