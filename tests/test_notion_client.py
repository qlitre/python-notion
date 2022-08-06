from notion import NotionClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')
client = NotionClient(api_key=API_KEY)
test_database_id = '0c06a2ac-f6f1-46ab-b475-b3471dfac0ed'
test_page_id = '2fe2d521-7a1f-41fe-8344-9039974e48e5'


def test_get_database_id():
    database_name = 'test_database'
    database_id = client.get_database_id(database_name)
    assert database_id == test_database_id


def test_retrieve_database():
    assert client.retrieve_database(test_database_id)


def test_property_name_of_title():
    property_name_of_title = client.property_name_of_title(test_database_id)
    assert property_name_of_title == 'test_title'


def test_database_properties():
    properties = client.database_properties(test_database_id)
    for k, v in properties.items():
        assert properties[k]
        assert v['id']
        assert v['type']


def test_list_database_page_object():
    list_database_page_object = client.list_database_page_object(test_database_id)
    assert len(list_database_page_object) > 0


def test_get_page_ids_in_database():
    page_ids = client.get_page_ids_in_database(test_database_id)
    assert len(page_ids) > 0


def test_list_titles():
    list_titles = client.list_titles(test_database_id)
    print(list_titles)
    assert len(list_titles) > 0


# todo need fix
"""
def test_list_property_values():
    target_property_names = ["test_text", "test_url", "test_email", "test_phone"]
    for property_name in target_property_names:
        list_property_values = client.list_property_values(database_id=test_database_id,
                                                           property_name=property_name)
        print(list_property_values)
        assert len(list_property_values) > 0
"""


def test_create_database():
    props = {'test_email': 'email',
             'test_number': 'number',
             'test_text': 'rich_text', 'test_date': 'date',
             'test_multi_select': 'multi_select',
             'test_checkbox': 'checkbox', 'test_url': 'url',
             'test_select': 'select', 'test_phone': 'phone_number',
             'test_title': 'title'}

    r = client.create_database(page_id=test_page_id, title_of_database='database in page', properties=props)
    assert r.status_code == 200


def test_retrieve_a_page():
    r = client.retrieve_a_page(test_page_id)
    assert r.status_code == 200


def test_add_page_to_database():
    prop_name_and_values = {'test_email': 'qlitre@example.com',
                            'test_number': 123456,
                            'test_text': 'Lorem ipsum dolor sit amet,',
                            'test_date': '2022-08-10',
                            'test_multi_select': 'programing',
                            'test_checkbox': True, 'test_url': 'https://qlitre-weblog.com/',
                            'test_select': 'dark mode', 'test_phone': '123-456-890',
                            'test_title': 'test_add_page1'}
    res = client.add_page_to_database(test_database_id, prop_name_and_values)
    assert res.status_code == 200

    prop_name_and_values = {'test_date': '2022-08-10,2022-08-12',
                            'test_multi_select': 'programing,python',
                            'test_checkbox': False,
                            'test_title': 'test_add_page2'}
    res = client.add_page_to_database(test_database_id, prop_name_and_values)
    assert res.status_code == 200


def test_update_page_property():
    prop_name_and_values = {'test_email': 'qlitre@example.com',
                            'test_number': 123456,
                            'test_text': 'Lorem ipsum dolor sit amet,',
                            'test_date': '2022-08-10',
                            'test_multi_select': 'programing',
                            'test_checkbox': True, 'test_url': 'https://qlitre-weblog.com/',
                            'test_select': 'dark mode', 'test_phone': '123-456-890',
                            'test_title': 'Updated Title'}
    res = client.update_page_property(test_page_id, prop_name_and_values)
    assert res.status_code == 200


def test_retrieve_block_children():
    res = client.retrieve_block_children(test_page_id)
    assert res.status_code == 200


def test_add_heading_to_page():
    res = client.add_heading_to_page(test_page_id, heading_type='heading_1', content='heading1')
    assert res.status_code == 200
    res = client.add_heading_to_page(test_page_id, heading_type='heading_2', content='heading2')
    assert res.status_code == 200
    res = client.add_heading_to_page(test_page_id, heading_type='heading_3', content='heading3')
    assert res.status_code == 200


def test_add_paragraph_to_page():
    paragraph = """
    Lorem ipsum dolor sit amet, 
    consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi
    ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit
    in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
    sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
    mollit anim id est laborum.
    """
    res = client.add_paragraph_to_page(test_page_id, content=paragraph)
    assert res.status_code == 200


def test_add_todolist_to_page():
    res = client.add_todolist_to_page(test_page_id, list_content=['todo1', 'todo2'], checked=True)
    assert res.status_code == 200
    res = client.add_todolist_to_page(test_page_id, list_content=['todo1', 'todo2'], checked=False)
    assert res.status_code == 200


def test_add_numbered_list_item_to_page():
    res = client.add_numbered_list_item_to_page(test_page_id, list_content=['first', 'second', 'third'])
    assert res.status_code == 200


def test_add_bulleted_list_item_to_page():
    res = client.add_bulleted_list_item_to_page(test_page_id, list_content=['bullet1', 'bullet2', 'bullet3'])
    assert res.status_code == 200


def test_add_toggle_block_to_page():
    content = """
    Lorem ipsum dolor sit amet, 
    consectetur adipiscing elit,
    """
    res = client.add_toggle_block_to_page(test_page_id, parent_content='Toggle Parent',
                                          children_type='paragraph', children_content=[content])
    assert res.status_code == 200
