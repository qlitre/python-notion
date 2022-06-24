from typing import Literal, Dict
import requests
import attr


@attr.s
class APIClientBase:
    api_key: str = attr.ib(repr=False)
    name = "notion_api_client"
    base_url: str = "https://api.notion.com/v1"

    def header(self) -> dict:

        return {"Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-02-22"}

    def make_request(self, endpoint: str,
                     method: Literal["GET", "POST", "PATCH", "DELETE", "PUT"],
                     query: Dict = None,
                     body: Dict = None,
                     raise_on_error=True,
                     ) -> requests.Response:

        allowed_methods = "GET POST PATCH DELETE PUT".split()
        if method not in allowed_methods:
            raise ValueError(
                f'Invalid method: {method}. Must be one of {", ".join(allowed_methods)}'
            )
        headers = self.header()
        url = self.base_url + endpoint
        session = requests.Session()

        r = session.request(method, url, headers=headers, params=query, json=body)

        if 200 <= r.status_code < 300:
            return r

        try:
            message = r.json()["message"]
        except KeyError:
            message = r.json()

        raise AttributeError(message)

    def get(self,
            endpoint: str,
            query: Dict = None,
            raise_on_error: bool = True
            ) -> requests.Response:

        return self.make_request(
            endpoint, method="GET", query=query, raise_on_error=raise_on_error
        )

    def post(self,
             endpoint: str,
             query: Dict = None,
             body: Dict = None,
             raise_on_error: bool = True,
             ) -> requests.Response:

        return self.make_request(endpoint,
                                 method="POST",
                                 query=query,
                                 body=body,
                                 raise_on_error=raise_on_error,
                                 )

    def patch(self,
              endpoint: str,
              query: Dict = None,
              body: Dict = None,
              raise_on_error: bool = True,
              ) -> requests.Response:

        return self.make_request(endpoint,
                                 method="PATCH",
                                 query=query,
                                 body=body,
                                 raise_on_error=raise_on_error,
                                 )
