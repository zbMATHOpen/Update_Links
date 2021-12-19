
import pandas as pd
from pandas.testing import assert_frame_equal

from update_zblinks_api.helpers.dlmf_helpers import update


def test_dlmf_update():
    df_dlmf = pd.DataFrame(
        {
            "document": 3439409,
            "external_id": "not/#AA.n27",
            "title": "None"
        },
    index=[0])

    df_new = pd.DataFrame(
        {
            "document": 3439409,
            "external_id": "not/#AA.n28",
            "title": "None"
        },
    index=[0])

    df_delete = df_dlmf.copy()

    df_new, df_edit, df_delete = update(
        df_dlmf, df_new, df_delete
    )

    assert len(df_new.index) == 0
    assert len(df_delete.index) == 0
    assert_frame_equal(
        df_edit,
        pd.DataFrame(
            {
                "document": 3439409,
                "previous_ext_id": "not/#AA.n27",
                "external_id": "not/#AA.n28",
                "title": "None"
            },
            index=df_edit.index
        ),
        check_like=True
    )
