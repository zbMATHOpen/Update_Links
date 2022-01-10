
import pandas as pd
import psycopg2
from update_zblinks_api import get_connection_params_dict

def get_titles(df_link, this_partner):
    """
    gets the title from the zb_links.source table associated with a link source

    Parameters
    ----------
    df_link : pandas DataFrame
        contains 'document', 'external_id, 'title' as columns.
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

    params_dict = get_connection_params_dict()
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
    df_link_title = df_merge[["document","external_id","title_x","title_y"]]
    df_link_title = df_link_title.rename(
        columns=(
            {
                "title_x":"title",
                "title_y":"title_doc_ext_ids"
            }
        )
    )


    return df_link_title


def remove_lonely_sources(this_partner):
    """
    Removes entries from zb_links.source table
    which no longer correspond to any link entry

    Parameters
    ----------
    this_partner : str
        name of zbMATH partner.

    """
    params_dict = get_connection_params_dict()
    connection = psycopg2.connect(**params_dict)

    query_request = """
    SELECT src.id
    FROM zb_links.source AS src
    LEFT OUTER JOIN document_external_ids
    	ON src.id = document_external_ids.external_id
        AND src.partner = document_external_ids.type::text
    WHERE src.partner = %(partner_arg)s
    AND document_external_ids.external_id IS NULL
    """

    df_lonely_source = pd.read_sql_query(query_request,
                                         connection,
                                         params={"partner_arg": this_partner})

    lonely_id_tuple = tuple(df_lonely_source["id"].to_list())

    if len(lonely_id_tuple) > 0:
        delete_request = """
            DELETE FROM zb_links.source
            WHERE id IN %(id_list)s
            AND partner = %(partner_arg)s
        """

        data = {"id_list": lonely_id_tuple, "partner_arg": this_partner}

        with connection.cursor() as cursor:
            cursor.execute(delete_request, data)
            connection.commit()

    connection.close()
