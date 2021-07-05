

def get_titles(link_data, partner):
    """

    Parameters
    ----------
    link_data : pandas Series
        contains 'document', 'external_id' as fields.
    partner : string
        zblinks API partner; listed as 'type' in the document_external_ids
        table.

    Returns
    -------
    title : str
        the source title corresponding to the link_data; located in the
        zb_links.source table.

    """
    title = None
    return title