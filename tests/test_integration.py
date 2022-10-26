import pytest
from ape import networks

from ape_lighthouse.provider import LighthouseProvider


@pytest.mark.parametrize(
    "ecosystem,network",
    [
        ("beacon", "mainnet"),
        ("beacon", "goerli"),
    ],
)
def test_lighthouse(ecosystem, network):
    ecosystem_cls = networks.get_ecosystem(ecosystem)
    network_cls = ecosystem_cls.get_network(network)
    with network_cls.use_provider("lighthouse") as provider:
        assert isinstance(provider, LighthouseProvider)
        assert provider.get_balance("0")  # validator index == 0
        assert provider.get_block("latest")
