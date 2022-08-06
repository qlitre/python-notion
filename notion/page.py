from __future__ import annotations

import attr
from notion.base import APIClientBase
from requests import Response


@attr.s
class PageAPI:
    _client: APIClientBase = attr.ib(repr=False)

    def retrieve_page(self,
                      page_id: str
                      ) -> Response:
        end_point = f'/pages/{page_id}'

        return self._client.get(end_point)

    def retrieve_page_property_item(self,
                                    page_id: str,
                                    property_id: str
                                    ) -> Response:
        end_pont = f'/pages/{page_id}/properties/{property_id}'
        return self._client.get(end_pont)

    def create_page(self,
                    body: dict
                    ) -> Response:
        end_point = '/pages'

        return self._client.post(end_point, body=body)

    def update_page(self, page_id: str,
                    body: dict
                    ) -> Response:
        end_point = f'/pages/{page_id}'

        return self._client.patch(endpoint=end_point, body=body)
