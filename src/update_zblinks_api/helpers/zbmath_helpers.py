import pandas as pd
import psycopg2

from update_zblinks_api import params_dict


def get_des_from_zbl_ids(df_scrape):
    """
    Matches the de numbers to given zbl_ids

    Parameters
    ----------
    df_scrape : DataFrame
        represents the dataframe from a partner scrape
        has "zbl_code" as a columns.

    Returns
    -------
    df_scrape_with_de : DataFrame
        has de numbers corresponding to the zbl_codes in an adjacent column.

    """

    zbl_id_tuple = tuple(df_scrape["zbl_code"].to_list())

    connection = psycopg2.connect(**params_dict)

    query_request = """
        SELECT id, zbl_id
        FROM math_documents
        WHERE zbl_id IN %(id_list)s
    """

    df_des = pd.read_sql_query(query_request,
                               connection,
                               params={"id_list": zbl_id_tuple})
    connection.close()

    df_merge = pd.merge(df_scrape, df_des,
                        left_on="zbl_code",
                        right_on="zbl_id",
                        how="inner")

    df_scrape_with_de = df_merge[["id","external_id","title"]]
    df_scrape_with_de = df_scrape_with_de.rename(
        columns=({"id":"document"})
    )

    return df_scrape_with_de
