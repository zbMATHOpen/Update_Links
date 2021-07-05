
import pandas as pd

# Initial csv file from OEIS
input_file = "oeis_dataset.csv"
# Dataframe corresponding to the initial csv file

df_starting_csv = pd.read_csv(input_file)

# Add constant columns for source
constant_columns_source = {
    "partner_id": "2",
    "partner_name": "OEIS",
    "link_provider": "2",
    "relationship_type": "None"
}

df_initial_link = df_starting_csv.assign(**constant_columns_source)

df_initial_link["link_id"] = df_initial_link.apply(
    lambda row: row.sequence_id, axis=1)

df_initial_link["source_id"] = df_initial_link.apply(
    lambda row: row.sequence_id, axis=1)

df_initial_link["source_identifier"] = df_initial_link.apply(
    lambda row: f"A{row.sequence_id}", axis=1)

df_initial_link["link_added_date"] = pd.to_datetime("today")


# Source dataframe
df_source = df_initial_link[
    [
        "link_id",
        "source_id",
        "source_identifier",
        "zbl_code",
        "partner_id",
        "partner_name",
        "link_publication_date",
        "link_provider",
        "link_added_date",
        "relationship_type"
    ]
].drop_duplicates()

# csv file oeis_source_table_dataset.csv
df_source.to_csv("oeis_link_table_dataset.csv", index=False)
