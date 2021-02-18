import logging
from dataclasses import dataclass
from typing import List

from datalake_scripts import Threats
from datalake_scripts.common.base_script import BaseScripts

from src.config import OCD_DTL_API_ENV, OCD_DTL_MISP_MAX_RESULT
from src.types import DtlMispEvent


@dataclass
class ConfigArg:
    loglevel: int
    env: str


class Datalake:
    def __init__(self):
        args = ConfigArg(loglevel=logging.WARNING, env=OCD_DTL_API_ENV)
        endpoint_config, _, tokens = BaseScripts().load_config(args=args)
        self.threats_api = Threats(endpoint_config, args.env, tokens)

    def retrieve_events_from_query_hash(self, query_hash: str) -> List[DtlMispEvent]:
        res = self.threats_api.get_threats(
            query_hash,
            limit=OCD_DTL_MISP_MAX_RESULT,
            response_format='application/x-misp+json',
        )
        return res['response']
