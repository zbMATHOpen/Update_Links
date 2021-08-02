
import pytest
from unittest import mock
from fixtures import mock_get_titles


@pytest.fixture(autouse=True)
def get_titles():

    with mock.patch(
            "update_zblinks_api.helpers.source_helpers.get_titles",
            side_effect=mock_get_titles
        ) as title_mock:

        yield title_mock
