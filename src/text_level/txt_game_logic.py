from text_level.news_txt import newstext
from text_level.dialogue_txt import dialoguetext
from text_level.options_txt import optionstext

class txt_Node:
    def __init__(self, node_type, content):
        self.node_type = node_type
        self.content = content
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, node_type, content):
        new_node = txt_Node(node_type, content)
        if self.head == None:
            self.head = new_node
            return

        curent = self.head
        while curent.next != None:
            curent = curent.next
        curent.next = new_node


def populate_list():
    linked_list = LinkedList()
    news = newstext()
    dialogue = dialoguetext()
    options = optionstext()

    linked_list.append("NEWS", news)
    linked_list.append("DIALOGUE", dialogue[0])
    linked_list.append("OPTIONS", options)
    linked_list.append("DIALOGUE", dialogue[1])
    linked_list.append("OPTIONS", options)

    return linked_list