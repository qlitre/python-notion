import settings
from notion import NotionClient

api_key = 'you api key'
client = NotionClient(settings.API_KEY)

# データベースのIDを取得する
database_id = client.get_database_id('ToDo List')

page_id = '8f9f9c08-0ea7-4b00-8759-867f248906e1'

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
