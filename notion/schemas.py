from typing import Literal, Dict, Any, Union
from dataclasses import dataclass

"""
todo:
relation,files,peopleプロパティの扱い
"""

"""DatabaseProperty"""
PropertyType = Literal["title", "rich_text", "number", "select",
                       "multi_select", "date", "people", "files",
                       "checkbox", "url", "email", "phone_number",
                       "created_time", "created_by", "last_edited_time", "last_edited_by"]

"""FilterMethod"""
TextFilterMethod = Literal['equals', 'does_not_equal', 'contains', 'does_not_contain',
                           'starts_with', 'ends_with', 'is_empty', 'is_not_empty']

DateFilterMethod = Literal['equals', 'before', 'after', 'on_or_before',
                           'is_empty', 'is_not_empty', 'on_or_after', 'past_week',
                           'past_month', 'past_year', 'next_week', 'next_month',
                           'next_year']

NumberFilterMethod = Literal['equals', 'does_not_equal', 'greater_than', 'less_than',
                             'greater_than_or_equal_to', 'less_than_or_equal_to', 'is_empty', 'is_not_empty']

CheckBoxFilterMethod = Literal['equals', 'does_not_equal']

SelectFilterMethod = Literal['equals', 'does_not_equal', 'is_empty', 'is_not_empty']

MultiSelectFilterMethod = Literal['contains', 'does_not_contain', 'is_empty', 'is_not_empty']

"""Block"""
BlockObjectType = Literal['heading_1', 'heading_2', 'heading_3', 'paragraph',
                          'to_do', 'numbered_list_item', 'bulleted_list_item', 'toggle']


@dataclass
class PropertyValueObject:
    name: str
    property_type: PropertyType

    def title_property_value(self,
                             content: str
                             ) -> dict:

        return {
            self.name: {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }
                ]
            }
        }

    def rich_text_property_value(self,
                                 content: str
                                 ) -> dict:

        return {
            self.name: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }
                ]
            }
        }

    def number_property_value(self,
                              number: int
                              ) -> dict:

        return {
            self.name: {
                'number': number
            }
        }

    def select_property_value(self,
                              content: str
                              ) -> dict:

        return {
            self.name: {
                "select": {
                    "name": content
                }
            }
        }

    def multi_select_property_value(self,
                                    content_list: list
                                    ) -> dict:

        contents = [{'name': content} for content in content_list]

        return {
            self.name: {
                "multi_select": contents
            }
        }

    def date_property_value(self,
                            start_date: str,
                            end_date: str = None
                            ) -> dict:

        body = {
            self.name: {
                "date": {
                    "start": start_date
                }
            }
        }

        if end_date:
            body[self.name]['date'].update({'end': end_date})

        return body

    def relation_property_value(self,
                                relation_id: str
                                ) -> dict:

        return {
            self.name: {
                "relation": [
                    {
                        "id": relation_id
                    }
                ]
            }
        }

    def check_box_property_value(self,
                                 boolean_value: bool
                                 ) -> dict:

        return {
            self.name: {
                "checkbox": boolean_value
            }
        }

    def url_property_value(self,
                           url: str
                           ) -> dict:

        return {
            self.name: {
                "url": url
            }
        }

    def email_property_value(self,
                             email: str
                             ) -> dict:

        return {
            self.name: {
                "email": email
            }
        }

    def phone_number_property_value(self,
                                    phone_number: str
                                    ) -> dict:

        return {
            self.name: {
                "phone_number": phone_number
            }
        }

    def property_value(self,
                       content: Any
                       ) -> dict:

        if self.property_type == 'title':
            return self.title_property_value(content)

        elif self.property_type == 'rich_text':
            return self.rich_text_property_value(content)

        elif self.property_type == 'number':
            return self.number_property_value(content)

        elif self.property_type == 'select':
            return self.select_property_value(content)

        elif self.property_type == 'date':
            if ',' in content:
                start = content.split(',')[0]
                end = content.split(',')[1]
                return self.date_property_value(start_date=start, end_date=end)
            else:
                return self.date_property_value(content)

        elif self.property_type == 'multi_select':
            return self.multi_select_property_value(content.split(','))

        elif self.property_type == 'checkbox':
            return self.check_box_property_value(content)

        elif self.property_type == 'url':
            return self.url_property_value(content)

        elif self.property_type == 'email':
            return self.email_property_value(content)

        elif self.property_type == 'phone_number':
            return self.phone_number_property_value(content)


@dataclass
class FilterObject:
    name: str
    property_type: PropertyType

    def base_body(self,
                  filter_type: str,
                  method: str,
                  value: Any,
                  start_cursor: str = None
                  ) -> dict:

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
                         start_cursor: str = None
                         ) -> dict:

        return self.base_body('rich_text', method, value, start_cursor)

    def number_filter_body(self,
                           method: NumberFilterMethod,
                           value: Union[int, str],
                           start_cursor: str = None
                           ) -> dict:

        return self.base_body('number', method, value, start_cursor)

    def checkbox_filter_body(self,
                             method: CheckBoxFilterMethod,
                             start_cursor: str = None):

        return self.base_body('checkbox', method, True, start_cursor)

    def select_filter_body(self,
                           method: SelectFilterMethod,
                           value: Union[str, bool],
                           start_cursor: str = None
                           ) -> dict:

        return self.base_body('select', method, value, start_cursor)

    def multi_select_filter_body(self,
                                 method: MultiSelectFilterMethod,
                                 value: Union[str, bool],
                                 start_cursor: str = None
                                 ) -> dict:

        return self.base_body('multi_select', method, value, start_cursor)

    def date_filter_body(self,
                         method: DateFilterMethod,
                         value: Union[str, bool] = None,
                         start_cursor: str = None
                         ) -> dict:

        empty_methods = ['past_week', 'past_month', 'past_year', 'next_week', 'next_month', 'next_year']
        if method in empty_methods:
            value = {}
        return self.base_body('date', method, value, start_cursor)


@dataclass
class BlockObjects:
    type: BlockObjectType

    def item_block(self,
                   content: str,
                   checked: bool = False
                   ) -> dict:
        obj_block: Dict[str, Any] = {
            "object": "block",
            "type": self.type,
            self.type: {
                "rich_text": [
                    {"type": "text", "text": {"content": content}}
                ]
            }
        }
        if self.type == 'to_do':
            obj_block[self.type].setdefault('checked', checked)

        return obj_block
