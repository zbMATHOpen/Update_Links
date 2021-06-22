import pandas as pd

# Initial csv file from OEIS
input_file = "oeis_dataset.csv"

# Dataframe corresponding to the initial csv file
df_starting_csv = pd.read_csv(input_file)

# Add constant columns for target
constant_columns_target = {"id_scheme": "zbMATH scheme"}
df_initial_target = df_starting_csv.assign(**constant_columns_target)

# Target dataframe
df_target = df_initial_target[
    [
        "zbl_code",
        "id_scheme",
        "title",
        "publication_date",
        "source_of_publication",
        "authors"
    ]
].drop_duplicates()

# csv file oeis_target_table_dataset.csv
df_target.to_csv("oeis_target_table_dataset.csv", index=False)
