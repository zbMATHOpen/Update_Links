
import pandas as pd


def get_permalinks(ext_id):
    """
    gets the permalink under which an external_id is located;
    the permalink is custom defined (overlaps in most cases with
    the DLMF defined permalinks)

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
    ext_id_parts = ext_id.split("#")
    if len(ext_id_parts) == 1:
        return ext_id

    if "about/bio/" in ext_id:
        return ext_id_parts[0]

    prefix = ext_id_parts[0]
    suffix = ext_id_parts[1]
    if suffix.lower().startswith("p"):
        return prefix

    suffix_remove_two_dots = suffix.rsplit(".", 2)
    suffix_remove_two_dots = suffix_remove_two_dots[0]
    # remove possible Itemized sections
    suffix_remove_another = suffix_remove_two_dots.rsplit(".", 1)
    if len(suffix_remove_another) == 1:
        return prefix + "#" + suffix_remove_two_dots

    if suffix_remove_another[1].startswith("I"):
        return prefix + "#" + suffix_remove_another[0]

    return prefix + "#" + suffix_remove_two_dots


def update(df_ext_partner, df_new, df_delete):
    """
    determines links which are to be grouped as to be added, edited, or
    deleted; specific to DLMF: a link will not be edited if the only
    change is a change in location, but under the same permalink.

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

    df_same_permalink = pd.merge(df_same_permalink, df_delete,
                                 left_on=["document", "external_id_x"],
                                 right_on=["document", "external_id"],
                                 how="inner")
    df_same_permalink = df_same_permalink.drop_duplicates(
        subset=["document","external_id_x"],keep='first'
    )

    df_same_permalink = df_same_permalink.drop_duplicates(
        subset=["document","external_id_y"],keep='first'
    )
    # note this could mix up the order of the link changes
    # but in the end all the new links are included

    df_remove_from_delete = df_same_permalink[
        ["document","external_id_x"]
    ].rename(columns={"external_id_x": "external_id"})
    df_edit = df_same_permalink[
        ["document", "external_id_x", "external_id_y","title_x"]
    ]
    df_edit = df_edit.rename(
        columns={
            "external_id_x": "previous_ext_id",
            "external_id_y": "external_id",
            "title_x": "title"
        }
    )

    df_delete = pd.concat(
        [df_delete,df_remove_from_delete,df_remove_from_delete]
    ).drop_duplicates(subset=["document","external_id"],keep=False)

    df_new = pd.concat(
        [df_new,df_edit,df_edit]
    ).drop_duplicates(subset=["document","external_id"],keep=False)

    df_new = df_new[["document","external_id","title"]]

    return df_new, df_edit, df_delete
