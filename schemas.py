from typing import Literal, Dict, Any, Union
from dataclasses import dataclass

"""DatabaseProperty"""
PropertyType = Literal["title", "rich_text", "number", "select",
                       "multi_select", "date", "people", "files",
                       "checkbox", "url", "email", "phone_number",
                       "created_time", "created_by", "last_edited_time", "last_edited_by"]

"""FilterMethod"""
TextFilterMethod = Literal['equals', 'does_not_equal', 'contains', 'does_not_contain',
                           'starts_with', 'ends_with', 'is_empty', 'is_not_empty']

DateFilterMethod = Literal['equals', 'before', 'after', 'on_or_before', 'is_empty', 'is_not_empty',
                           'on_or_after', 'past_week', 'past_month', 'past_year', 'next_week',
                           'next_month', 'next_year']

NumberFilterMethod = Literal['equals', 'does_not_equal', 'greater_than',
                             'less_than', 'greater_than_or_equal_to', 'less_than_or_equal_to',
                             'is_empty', 'is_not_empty']

CheckBoxFilterMethod = Literal['equals', 'does_not_equal']

SelectFilterMethod = Literal['equals', 'does_not_equal', 'is_empty', 'is_not_empty']

MultiSelectFilterMethod = Literal['contains', 'does_not_contain', 'is_empty', 'is_not_empty']

"""Block"""
BlockObjectType = Literal['heading_1', 'heading_2', 'heading_3', 'paragraph',
                          'to_do', 'numbered_list_item', 'bulleted_list_item', 'toggle']


@dataclass
class DatabasePropertyFilter:
    name: str
    property_type: PropertyType

    def base_body(self, filter_type: str,
                  method: str,
                  value: Any,
                  start_cursor: str = None):

        body = {
            "filter": {
                "property": self.name,
                filter_type: {method: value},
            }
        }

        if start_cursor:
            body['start_cursor'] = start_cursor

        return body

    def text_filter_body(self,
                         method: TextFilterMethod,
                         value: Union[str, bool],
                         start_cursor: str = None):
        return self.base_body('text', method, value, start_cursor)

    def number_filter_body(self,
                           method: NumberFilterMethod,
                           value: Union[int, str],
                           start_cursor: str = None):
        return self.base_body('number', method, value, start_cursor)

    def checkbox_filter_body(self,
                             method: CheckBoxFilterMethod,
                             start_cursor: str = None):
        return self.base_body('checkbox', method, True, start_cursor)

    def select_filter_body(self,
                           method: SelectFilterMethod,
                           value: Union[str, bool],
                           start_cursor: str = None):
        return self.base_body('select', method, value, start_cursor)

    def multi_select_filter_body(self,
                                 method: MultiSelectFilterMethod,
                                 value: Union[str, bool],
                                 start_cursor: str = None):
        return self.base_body('multi_select', method, value, start_cursor)

    def date_filter_body(self,
                         method: DateFilterMethod,
                         value: Union[str, bool] = None,
                         start_cursor: str = None):

        empty_methods = ['past_week', 'past_month', 'past_year', 'next_week', 'next_month', 'next_year']
        if method in empty_methods:
            value = {}
        return self.base_body('date', method, value, start_cursor)


@dataclass
class BlockObjects:
    type: BlockObjectType

    def item_block(self,
                   content: str,
                   checked: bool = False):
        obj_block: Dict[str, Any] = {
            "object": "block",
            "type": self.type,
            self.type: {
                "text": [
                    {"type": "text", "text": {"content": content}}
                ]
            }
        }
        if self.type == 'to_do':
            obj_block[self.type].setdefault('checked', checked)

        return obj_block
