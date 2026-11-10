from news_txt import newstext
from dialogue_txt import dialoguetext
from options_txt import optionstext

class txt_Node:
    def __init__(self, data1, data2, data3):
        self.data1 = data1
        self.data2 = data2
        self.data3 = data3
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val1, val2, val3):
        new_node = txt_Node(val1, val2, val3)
        if self.head == None:
            self.head = new_node
            return

        curent = self.head
        while curent.next != None:
            curent = curent.next
        curent.next = new_node

    def populate_list(self, news, dialogue, options):
        list = LinkedList()
        news = newstext()
        dialogue = dialoguetext()
        options = optionstext()

        list.append(news[0])
        list.append(dialogue[0])
        list.append(options[0])

        