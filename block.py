from __future__ import annotations

import attr
from _base import APIClientBase
from requests import Response


@attr.s
class BlockAPI:
    _client: APIClientBase = attr.ib(repr=False)

    def retrieve_block_children(self,
                                page_id,
                                query=None) -> Response:
        end_point = f'/blocks/{page_id}/children'

        return self._client.get(endpoint=end_point, query=query)

    def append_block_children(self,
                              page_id,
                              body) -> Response:
        end_point = f'/blocks/{page_id}/children'

        return self._client.patch(end_point, body=body)
