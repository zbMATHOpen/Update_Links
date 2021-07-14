
import pandas as pd
import psycopg2
from update_zblinks_api import params_dict

def get_titles(df_link, this_partner):
    """

    Parameters
    ----------
    df_link : pandas DataFrame
        contains 'document', 'external_id' as columns.
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.

    Returns
    -------
    df_link_title : DataFrame
        adds a column 'title_doc_ext_ids' which is the source title
        corresponding to the link_data; located in the
        zb_links.source table.

    """

    connection = psycopg2.connect(**params_dict)

    query_request = """
    SELECT id, title
    FROM zb_links.source
    WHERE partner = %(partner_arg)s
    """

    df_source = pd.read_sql_query(query_request,
                                  connection,
                                  params={"partner_arg": this_partner})
    connection.close()

    df_merge = pd.merge(df_link, df_source,
                        left_on="external_id",
                        right_on="id",
                        how="inner"
                        )

    df_link_title = df_merge[["document","external_id","title"]]

    return df_link_title