import requests
from ape.api.providers import UpstreamProvider
from ape.exceptions import ProviderError
from ape.logging import logger
from web3.beacon import Beacon
from yarl import URL

from ape_beacon.providers import BeaconProvider


DEFAULT_SETTINGS = {"uri": "http://localhost:5052"}


# SEE: https://github.com/ApeWorX/ape/blob/main/src/ape_geth/provider.py#L147
class Lighthouse(BeaconProvider, UpstreamProvider):
    name: str = "lighthouse"

    @property
    def uri(self) -> str:
        if "uri" in self.provider_settings:
            # Use adhoc, scripted value
            return self.provider_settings["uri"]

        config = self.config.dict().get(self.network.ecosystem.name, None)
        if config is None:
            return DEFAULT_SETTINGS["uri"]

        # Use value from config file
        network_config = config.get(self.network.name)
        return network_config.get("uri", DEFAULT_SETTINGS["uri"])

    @property
    def _clean_uri(self) -> str:
        return str(URL(self.uri).with_user(None).with_password(None))

    @property
    def connection_str(self) -> str:
        return self.uri

    def connect(self):
        self._client_version = None  # Clear cached version when connecting to another URI.
        self._beacon = Beacon(self.uri)

        if not self.is_connected:
            # TODO: "ephemeral" lighthouse?
            raise ProviderError(f"No node found on '{self._clean_uri}'")
        elif "lighthouse" in self.client_version.lower():
            self._log_connection("Lighthouse")
            # TODO: self.concurrency = ...
            # TODO: self.block_page_size = ...
        elif "prysm" in self.client_version.lower():
            self._log_connection("Prysm")
            # TODO: self.concurrency = ...
            # TODO: self.block_page_size = ...
        elif "lodestar" in self.client_version.lower():
            self._log_connection("Lodestar")
            # TODO: self.concurrency = ...
            # TODO: self.block_page_size = ...
        elif "nimbus" in self.client_version.lower():
            self._log_connection("Nimbus")
            # TODO: self.concurrency = ...
            # TODO: self.block_page_size = ...
        elif "teku" in self.client_version.lower():
            self._log_connection("Teku")
            # TODO: self.concurrency = ...
            # TODO: self.block_page_size = ...
        else:
            client_name = self.client_version.split("/")[0]
            logger.warning(
                f"Connecting Lighthouse plugin to non-Lighthouse client '{client_name}'."
            )

        # Check for chain errors, including syncing
        try:
            # use deposit contract endpoint for chain ID
            resp = self._beacon.get_deposit_contract()
            chain_id = int(resp["data"]["chain_id"])
        except (requests.exceptions.HTTPError, KeyError) as err:
            raise ProviderError(
                err.args[0].get("message")
                if all((hasattr(err, "args"), err.args, isinstance(err.args[0], dict)))
                else "Error getting chain id."
            )

        self.network.verify_chain_id(chain_id)

    def disconnect(self):
        self._beacon = None
        self._client_version = None

    def _log_connection(self, client_name: str):
        logger.info(f"Connecting to existing {client_name} node at '{self._clean_uri}'.")
