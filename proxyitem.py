#!/usr/bin/env python


class ProxyItem:
    """ This class represent a proxy
     :param hops is the number of following proxies
     :param next_items is a list of the fnext proxies
     """
    def __init__(self, hops, item):
        self.hops = hops
        self.next_items = []
        self.next_items.append(item)
        self.num_of_chain = 1

    def add_item(self, item):
        self.next_items.append(item)
        self.num_of_chain += 1

    def replace_item(self, hops, item):
        self.hops = hops
        self.next_items = []
        self.next_items.append(item)
        self.num_of_chain = 1

    def __str__(self):
        return "Next hops: " + str(self.hops) + "\n" \
                "Next proxy: " + str(self.next_items) + "\n" \


