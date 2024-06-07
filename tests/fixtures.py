import pytest
from refreshcss.html.site import Site


@pytest.fixture
def site():
    return Site()
