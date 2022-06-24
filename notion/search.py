from __future__ import annotations
from typing import Literal
import attr
from notion.base import APIClientBase
from requests import Response


@attr.s
class SearchAPI:
    _client: APIClientBase = attr.ib(repr=False)

    def search(self, object_type: Literal['database', 'page'] = None, start_cursor: str = None) -> Response:
        end_point = f'/search'
        body = {"page_size": 100}
        if object_type:
            body.update({'filter': {'value': object_type, 'property': 'object'}})
        if start_cursor:
            body.update({'start_cursor': start_cursor})

        return self._client.post(endpoint=end_point, body=body)
