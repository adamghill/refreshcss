import pytest
from refreshcss.html.site import DjangoSite


@pytest.fixture
def django_site():
    return DjangoSite()
