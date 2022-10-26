import ape
import pytest

from ape_lighthouse import LighthouseProvider


@pytest.fixture
def networks():
    return ape.networks


@pytest.fixture
def lighthouse_provider(networks) -> LighthouseProvider:
    return networks.beacon.goerli.get_provider("lighthouse")
