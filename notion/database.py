from __future__ import annotations

import attr
from notion.base import APIClientBase
from requests import Response


@attr.s
class DatabaseAPI:
    _client: APIClientBase = attr.ib(repr=False)

    def retrieve_databases(self,
                           database_id: str
                           ) -> Response:
        end_point = f'/databases/{database_id}'

        return self._client.get(endpoint=end_point)

    def filter_database(self,
                        database_id: str,
                        body: dict
                        ) -> Response:
        end_point = f'/databases/{database_id}/query'

        return self._client.post(endpoint=end_point, body=body)

    def create_database(self,
                        body: dict
                        ) -> Response:
        end_point = '/databases'

        return self._client.post(endpoint=end_point, body=body)
