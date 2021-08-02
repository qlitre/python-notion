from __future__ import annotations

from typing import Literal, Dict, Any
import attr
from _base import APIClientBase
from requests import Response
import schemas
from database import DatabaseAPI
from page import PageAPI
from block import BlockAPI


@attr.s(auto_attribs=True)
class NotionClient:
    """
    基本クラス
    """
    api_key: str = attr.ib(repr=False)
    database: DatabaseAPI = attr.ib(init=False, repr=False)
    page: PageAPI = attr.ib(init=False, repr=False)
    block: BlockAPI = attr.ib(init=False, repr=False)

    def __attrs_post_init__(self):
        self.raw: APIClientBase = APIClientBase(
            api_key=self.api_key
        )
        self.database: DatabaseAPI = DatabaseAPI(self.raw)
        self.page: PageAPI = PageAPI(self.raw)
        self.block: BlockAPI = BlockAPI(self.raw)

    def list_databases(self) -> Response:
        """
        データベース情報を返します
        """
        return self.database.list_databases()

    def get_database_id(self,
                        database_name: str
                        ) -> str:
        """
        データベースの名前からデータベースIDを特定します
        """
        json_data = self.database.list_databases().json()
        for data in json_data['results']:
            if database_name == data['title'][0]['text']['content']:
                return data['id']

    def property_name_of_title(self,
                               database_id: str
                               ) -> str:
        """
        データベースのtitleプロパティ名を取得します
        """
        json_data = self.database.retrieve_databases(database_id).json()
        for name, value in json_data['properties'].items():
            if value.get('type') == 'title':
                return name

    def database_properties(self,
                            database_id: str
                            ) -> dict:
        """
        データベースのプロパティ名とプロパティのタイプを辞書にして返します
        """
        name_and_types = {}
        json_data = self.database.retrieve_databases(database_id).json()
        for name, value in json_data['properties'].items():
            name_and_types[name] = value.get('type')

        return name_and_types

    def list_titles(self,
                    database_id: str
                    ) -> list:
        """
        データベースのタイトルの値をリストにして返します
        """
        property_name_of_title = self.property_name_of_title(database_id)
        name_and_types = self.database_properties(database_id)
        property_type = name_and_types.get(property_name_of_title)

        schema = schemas.FilterObject(name=property_name_of_title,
                                      property_type=property_type)
        body = schema.text_filter_body(method='is_not_empty', value=True)
        titles = []
        next_cur = None
        while True:
            if next_cur:
                body['start_cursor'] = next_cur

            json_data = self.database.filter_database(database_id=database_id,
                                                      body=body).json()
            for data in json_data['results']:
                titles.append(data['properties'][property_name_of_title]['title'][0]['text']['content'])

            if json_data['has_more']:
                next_cur = json_data['next_cursor']
            else:
                break

        return titles

    def list_property_values(self,
                             database_id: str,
                             property_name: str
                             ) -> list:

        """
        データベースのプロパティの値のリストを返します
        """
        name_and_types = self.database_properties(database_id)
        property_type = name_and_types.get(property_name)
        approved = ["title", "rich_text", "url", "email", "phone"]

        if property_type not in approved:
            raise ValueError(f'Invalid property type you specified :{property_type}.\n '
                             f'Allowed type is only "title" or "rich_text" or "url" or "email" or "phone"')

        schema = schemas.FilterObject(name=property_name, property_type=property_type)
        body = schema.text_filter_body(method='is_not_empty', value=True)
        next_cur = None
        values = []
        while True:
            if next_cur:
                body['start_cursor'] = next_cur

            json_data = self.database.filter_database(database_id=database_id,
                                                      body=body).json()
            for data in json_data['results']:
                values.append(data['properties'][property_name][property_type][0]['text']['content'])

            if json_data['has_more']:
                next_cur = json_data['next_cursor']
            else:
                break

        return values

    def date_filter(self,
                    database_id: str,
                    property_name: str,
                    method: schemas.DateFilterMethod,
                    value: [str, bool] = None,
                    start_cursor=None
                    ) -> Response:

        name_and_types = self.database_properties(database_id)
        property_type = name_and_types.get(property_name)
        if property_type != 'date':
            raise ValueError(f'Invalid property type you specified :{property_type}.\n '
                             f'Allowed type is only "date"')
        schema = schemas.FilterObject(name=property_name, property_type=property_type)
        body = schema.date_filter_body(method=method, value=value, start_cursor=start_cursor)
        return self.database.filter_database(database_id, body)

    def create_database(self, title_of_database: str,
                        page_id: str,
                        properties: Dict[str, schemas.PropertyType]
                        ) -> Response:

        """
        ページ内にデータベースを作成します。
        Parameters
        ----------
        title_of_database:作成するデータベースのタイトル
        page_id:データベースを作成するページのid
        properties:{プロパティ名：プロパティタイプ}の辞書で指定します。
            ex. {'タイトル':'title', '詳細':'rich_text', 'tags':'multi_select', '期限':'date', 'done!':'checkbox'}
        """

        body: Dict[str, Any] = {
            "parent": {
                "type": "page_id",
                "page_id": page_id
            },
            "title": [{
                "type": "text",
                "text": {"content": title_of_database,
                         "link": None}
            }],
            "properties": {},
        }

        for prop_name, prop_type in properties.items():
            body["properties"].setdefault(prop_name, {prop_type: {}})

        return self.database.create_database(body=body)

    def retrieve_a_page(self,
                        page_id: str
                        ) -> Response:

        return self.page.retrieve_page(page_id=page_id)

    def add_page_to_database(self,
                             database_id: str,
                             prop_name_and_value: dict
                             ) -> Response:

        """
        データベースにページを追加します

        Parameters
        ----------
        database_id:データベースのid
        prop_name_and_value:
            {プロパティ名：value,プロパティ名2:value2...}の辞書形式で指定します。
            valueが複数ある時は、カンマで区切ります。日付のvalueはyyyy-mm-dd形式。
            ex {'category':'Programing', 'tag':'Python,basic','due':'2021-08-01,2021-08-02'}
        """

        body: Dict[str, Any] = {
            "parent": {
                "database_id": database_id},
            "properties": {
            }
        }

        name_and_types = self.database_properties(database_id)

        for name, value in prop_name_and_value.items():
            prop_type = name_and_types.get(name)
            obj = schemas.PropertyValueObject(name=name, property_type=prop_type)
            body['properties'].update(obj.property_value(value))

        return self.page.create_page(body)

    def retrieve_block_children(self,
                                page_id: str
                                ) -> Response:
        """
        ページ内のblock情報を返します
        """
        return self.block.retrieve_block_children(page_id)

    def add_heading_to_page(self,
                            page_id: str,
                            heading_type: Literal['heading_1', 'heading_2', 'heading_3'],
                            content: str) -> Response:
        """
        ページ内にヘディングを書きこみます
        """
        body = {
            "children": [schemas.BlockObjects(heading_type).item_block(content)]
        }

        return self.block.append_block_children(page_id, body)

    def add_paragraph_to_page(self,
                              page_id: str,
                              content: str
                              ) -> Response:
        """
        ページ内にパラグラフを書きこみます
        """

        body = {
            "children": [schemas.BlockObjects('paragraph').item_block(content)]
        }

        return self.block.append_block_children(page_id, body)

    def add_todolist_to_page(self,
                             page_id: str,
                             list_content: list,
                             checked: bool = False
                             ) -> Response:
        """
        ページ内にtodolistブロックを書きこみます。
        デフォルトは未チェックです。
        """

        block_object = schemas.BlockObjects('to_do')
        obj_list = [block_object.item_block(content, checked) for content in list_content]
        body = {
            "children": obj_list
        }
        return self.block.append_block_children(page_id, body)

    def add_numbered_list_item_to_page(self,
                                       page_id: str,
                                       list_content: list
                                       ) -> Response:
        """
        ページ内にナンバーリストを書きこみます
        """

        block_object = schemas.BlockObjects('numbered_list_item')
        obj_list = [block_object.item_block(content) for content in list_content]
        body = {
            "children": obj_list
        }

        return self.block.append_block_children(page_id, body)

    def add_bulleted_list_item_to_page(self,
                                       page_id: str,
                                       list_content: list
                                       ) -> Response:
        """
        ページ内にバレットリストを書きこみます。
        """

        block_object = schemas.BlockObjects('bulleted_list_item')
        obj_list = [block_object.item_block(content) for content in list_content]
        body = {
            "children": obj_list
        }

        return self.block.append_block_children(page_id, body)

    def add_toggle_block_to_page(self,
                                 page_id: str,
                                 parent_content: str,
                                 children_type: schemas.BlockObjectType = None,
                                 children_content: list = None
                                 ) -> Response:
        """
        ページ内にトグルブロックを作成します
        """

        parent_object = schemas.BlockObjects('toggle')
        body = {
            "children": [parent_object.item_block(parent_content)]
        }

        if not children_type or not children_content:
            return self.block.append_block_children(page_id, body)

        children_object = schemas.BlockObjects(children_type)
        obj_list = [children_object.item_block(content) for content in children_content]
        body['children'][0]['toggle']['children'] = obj_list

        return self.block.append_block_children(page_id, body)
