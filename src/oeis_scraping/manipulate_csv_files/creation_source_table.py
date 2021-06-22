import pandas as pd

# Initial csv file from OEIS
input_file = "oeis_dataset.csv"
# Dataframe corresponding to the initial csv file

df_starting_csv = pd.read_csv(input_file)

# Add constant columns for source
constant_columns_source = {
    "id_scheme": "OEIS scheme",
    "partner": "OEIS",
    "type_name": "OEIS bibliographic entry"
}

df_initial_source = df_starting_csv.assign(**constant_columns_source)

df_initial_source["identifier_id"] = df_initial_source.apply(
    lambda row: f"A{row.sequence_id}", axis=1)

df_initial_source["url"] = df_initial_source.apply(
    lambda row: f"https://oeis.org/A{row.sequence_id}", axis=1)

df_initial_source["title"] = df_initial_source.apply(
    lambda row: row.sequence_name, axis=1)


# df_initial_source["source_id"] = df_initial_source.apply(
#    lambda row: int(row.sequence_id[1:]), axis=1)


# Source dataframe
df_source = df_initial_source[
    [
        "sequence_id",
        "identifier_id",
        "id_scheme",
        "type_name",
        "url",
        "title",
        "partner"
    ]
].drop_duplicates()

# csv file oeis_source_table_dataset.csv
df_source.to_csv("oeis_source_table_dataset.csv", index=False)
