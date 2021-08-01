# python-notion

A wrapper around the Notion API written in Python.

## Example Database
![python-notion1](https://user-images.githubusercontent.com/77523162/127741332-e732a88d-d887-4e94-948d-bd4d19b2ec7e.png)

## Usage

```python
from notion import NotionClient

api_key = 'your api key'
client = NotionClient(api_key)
```

### Get Database ID

```python
database_id = client.get_database_id(database_name='ToDo List')
```

### Get Properties of database

```python
database_properties = client.database_properties(database_id=database_id)
print(database_properties)

>>>
{'Tags': 'multi_select', 'Due': 'date', 'Done!': 'checkbox', 'Name': 'title'}
```

### Add page to database

```python
add_items = {'Name': '部屋の掃除', 'Tags': '家事', 'Due': '2021-08-01', 'Done!': False}
client.add_page_to_database(database_id=database_id, prop_name_and_value=add_items)
```

if multi values:

```python
add_items = {'Name': 'Pythonブログの更新', 'Tags': '趣味,プログラミング',
             'Due': '2021-08-02,2021-08-03', 'Done!': False}
client.add_page_to_database(database_id=database_id,
                            prop_name_and_value=add_items)
```

![python-notion2](https://user-images.githubusercontent.com/77523162/127741330-a8d5064c-d827-477e-9e0e-d45e0940a2e8.png)


### add content to page


```python
add_items = {'Name': 'ページ内書き込みテスト'}
res = client.add_page_to_database(database_id=database_id,
                                  prop_name_and_value=add_items)

page_id = res.json()['id']

# heading
client.add_heading_to_page(page_id=page_id,
                           heading_type='heading_1',
                           content='This is Heading1')
client.add_heading_to_page(page_id=page_id,
                           heading_type='heading_2',
                           content='This is Heading2')
client.add_heading_to_page(page_id=page_id,
                           heading_type='heading_3',
                           content='This is Heading3')
# paragraph
paragraph = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, ' \
            'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.' \
            ' Ut enim ad minim veniam, quis ...'
client.add_paragraph_to_page(page_id=page_id,
                             content=paragraph)

# bulleted list
client.add_bulleted_list_item_to_page(page_id=page_id,
                                      list_content=['bullet1', 'bullet2', 'bullet3'])
# numbered list
client.add_numbered_list_item_to_page(page_id=page_id,
                                      list_content=['冷蔵庫を開ける', '像を入れる', '冷蔵庫を閉める'])

# todolist
client.add_todolist_to_page(page_id=page_id,
                            list_content=['トイレ掃除', '料理', 'エアコンのフィルター清掃'])

# toggle
client.add_toggle_block_to_page(page_id=page_id,
                                parent_content='秘密の質問',
                                children_type='bulleted_list_item',
                                children_content=['小学校の名前', '母親の旧姓', '初恋の人の名前'])
```

![python-notion3](https://user-images.githubusercontent.com/77523162/127741331-53249de3-3487-4709-970d-27f92c206d64.png)
