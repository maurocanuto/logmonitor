#!/usr/bin/env python
from proxyitem import ProxyItem


class ProxyManager:
    """ This class is responsible of detecting unefficient proxy chains
    proxies_dic is a dictionary where the key is the proxy and the value is a ProxyItem object
    """

    proxies_dic = dict()

    def find_inefficient_proxies(self, logline):
        client_ip = logline.client_ip
        proxies = logline.proxies

        l = len(proxies)
        num_proxies_next_hops = l - 1

        for index, p in enumerate(proxies):
            if index == l - 1:  # last proxy
                item = ProxyItem(0, None)
                self.proxies_dic[p] = item
                break

            # Check if proxy already present
            if p in self.proxies_dic:
                dict_item = self.proxies_dic[p]
                if dict_item.hops < num_proxies_next_hops:  # Inefficient chain
                    self.print_inefficient_chain(client_ip, proxies, index, dict_item)

                elif dict_item.hops == num_proxies_next_hops:  # Add chain with same number of proxies if different
                    if proxies[index + 1] not in dict_item.next_items:
                        dict_item.add_item(proxies[index + 1])

                else:  # Update chain with the new one with less hops
                    dict_item.replace_item(num_proxies_next_hops, proxies[index + 1])

            else:  # If proxy is not present, add to dictionary
                item = ProxyItem(num_proxies_next_hops, proxies[index + 1])
                self.proxies_dic[p] = item

            # Update indexes
            index += 1
            num_proxies_next_hops -= 1

    def print_inefficient_chain(self, client_ip, proxies, index, dict_item):

        print "Request originating at " + client_ip + " used inefficient proxy chain:"
        print "  " + str(", ".join(proxies))
        print "There are " + str(len(dict_item.next_items)) + " known efficient proxy chains:"
        prefix = str(", ".join(proxies[:index]))
        self.print_chain(proxies[index], prefix, 0, True)

    def print_chain(self, item, s, i, first):
        """ Recursive function for printing efficient chains"""

        el = self.proxies_dic[item]
        if el.hops == 0:
            if i == 0:  # Chain with only 1 proxy
                s = "  1. " + str(item)
            else:
                pref = "  " + str(i) + ". "
                s = pref + s + ", " + item
            print s
            return s

        else:
            for it in el.next_items:
                if first:
                    if s:
                        s = s + ", " + item
                    else:
                        s = item
                    first = False
                i += 1
                self.print_chain(it, s, i, False)










