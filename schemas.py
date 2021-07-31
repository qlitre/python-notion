from typing import Literal, Dict, Any
from dataclasses import dataclass


@dataclass
class BlockObjects:
    type: Literal[
        'heading_1', 'heading_2', 'heading_3', 'paragraph',
        'to_do', 'numbered_list_item', 'bulleted_list_item', 'toggle']

    def item_block(self, content, checked: bool = False):
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
