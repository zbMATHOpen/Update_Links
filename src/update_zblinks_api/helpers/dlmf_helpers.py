
import pandas as pd


def get_permalinks(ext_id):
    """

    Parameters
    ----------
    ext_id : str
        represents the source id for DLMF source objects.

    Returns
    -------
    permalink : str
        the permalink under which the ext_id is located; ext_id is subject to
        change, permalink remains the same.

    """
    permalink = None
    return permalink


def update(df_ext_partner, df_new, df_delete):
    """

    Parameters
    ----------
    df_ext_partner : pandas DataFrame
        DataFrame representation of external links from
        document_external_ids which only include entries whose
        type is the given (as the partner parameter) zblinks API partner.
    df_new : pandas DataFrame
        those links caught from the latest scraping which are not in the matrix.
    df_delete : pandas DataFrame
        those links from the matrix which were not seen in the latest scraping.

    Returns
    -------
    df_new : pandas DataFrame
        contains representations of links which are to be posted as new links;
        in this function, the entries which have been designated to belong to
        df_edit are removed from df_new.
    df_edit : pandas DataFrame
        contains representations of links which are to be applied as patches
        to existing links; occurs when the location of a link changes
        (and thus is listed as a new link), but in fact belongs under the
        same permalink.
    df_delete : pandas DataFrame
        contains representations of links which are to be deleted;
        in this function, the entries which no longer exist because their
        location has moved and have been designated to belong to
        df_edit are removed from df_delete.

    """

    df_ext_partner["permalink"] = df_ext_partner["external_id"].map(
        get_permalinks
    )
    df_new["permalink"] = df_new["external_id"].map(
        get_permalinks
    )
    df_same_permalink = pd.merge(
        df_ext_partner, df_new,
        on=["document","permalink"],
        how="inner"
    )
    permalinks_delete_series = df_delete["external_id"].map(
        get_permalinks
    )
    df_same_permalink = df_same_permalink[
        df_same_permalink["external_id_y"].isin(permalinks_delete_series)
    ]
    df_edit = df_same_permalink[["document_y","external_id_y","title"]]
    df_edit = df_edit.rename(
        columns={
            "document_y": "document",
            "external_id": "external_id"
        }
    )

    df_delete = pd.concat(
        [df_delete,df_edit,df_edit]
    ).drop_duplicates(subset=["document","external_id"],keep=False)

    df_new = pd.concat(
        [df_new,df_edit,df_edit]
    ).drop_duplicates(subset=["document","external_id"],keep=False)

    df_new = df_new[["document","external_id","title"]]

    return df_new, df_edit, df_delete
