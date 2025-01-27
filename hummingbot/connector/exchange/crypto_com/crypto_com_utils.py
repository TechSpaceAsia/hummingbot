import math
from typing import Dict, List

from pydantic import Field, SecretStr

from hummingbot.client.config.config_data_types import BaseConnectorConfigMap, ClientFieldData
from hummingbot.core.utils.tracking_nonce import get_tracking_nonce, get_tracking_nonce_low_res

from . import crypto_com_constants as CONSTANTS

CENTRALIZED = True

EXAMPLE_PAIR = "ETH-USDT"

DEFAULT_FEES = [0.1, 0.1]

HBOT_BROKER_ID = "HBOT-"


# deeply merge two dictionaries
def merge_dicts(source: Dict, destination: Dict) -> Dict:
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value

    return destination


# join paths
def join_paths(*paths: List[str]) -> str:
    return "/".join(paths)


# get timestamp in milliseconds
def get_ms_timestamp() -> int:
    return get_tracking_nonce_low_res()


# convert milliseconds timestamp to seconds
def ms_timestamp_to_s(ms: int) -> int:
    return math.floor(ms / 1e3)


# Request ID class
class RequestId:
    """
    Generate request ids
    """
    _request_id: int = 0

    @classmethod
    def generate_request_id(cls) -> int:
        return get_tracking_nonce()


def convert_from_exchange_trading_pair(exchange_trading_pair: str) -> str:
    return exchange_trading_pair.replace("_", "-")


def convert_to_exchange_trading_pair(hb_trading_pair: str) -> str:
    return hb_trading_pair.replace("-", "_")


def get_new_client_order_id(is_buy: bool, trading_pair: str) -> str:
    side = "B" if is_buy else "S"
    return f"{HBOT_BROKER_ID}{side}-{trading_pair}-{get_tracking_nonce()}"


def get_api_reason(code: str) -> str:
    return CONSTANTS.API_REASONS.get(int(code), code)


def get_rest_url(path_url: str, api_version: str = CONSTANTS.API_VERSION) -> str:
    base_url = CONSTANTS.TRADING_REST_URL if path_url.startswith('private') else CONSTANTS.MARKET_REST_URL
        
    return f"{base_url}{api_version}{path_url}"


class CryptoComConfigMap(BaseConnectorConfigMap):
    connector: str = Field(default="crypto_com", client_data=None)
    crypto_com_api_key: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Crypto.com API key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    crypto_com_secret_key: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Crypto.com secret key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )

    class Config:
        title = "crypto_com"


KEYS = CryptoComConfigMap.construct()
