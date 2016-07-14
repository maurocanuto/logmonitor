#!/usr/bin/env python
from __future__ import division
import math


class LogStats:
    """ This class is responsible of counting and printing stats"""
    # Variables for stats
    num_GET_10_secs = 0
    num_POST_10_secs = 0
    num_proxied_req_10_secs = 0
    proxies_req_10_sec = {}
    requests_time_10_sec = []

    def reset_stats(self):
        self.num_GET_10_secs = 0
        self.num_POST_10_secs = 0
        self.num_proxied_req_10_secs = 0
        self.proxies_req_10_sec = {}
        self.requests_time_10_sec = []

    def count_stats(self, line):
        """
        Increments counters for stats and alerts
        :param line: is a LogLine object containing the information related to the inserted line
        """
        if line.method == "GET":
            self.num_GET_10_secs += 1
        elif line.method == "POST":
            self.num_POST_10_secs += 1

        if line.proxies:
            self.num_proxied_req_10_secs += 1
            # Add proxies to dict
            for proxy in line.proxies:
                if proxy in self.proxies_req_10_sec:
                    self.proxies_req_10_sec[proxy] += 1
                else:
                    self.proxies_req_10_sec[proxy] = 1

        # Add request time for percentile calculation
        self.requests_time_10_sec.append(line.time_process)

    @staticmethod
    def __calculate_percentile(N, percent, key=lambda x: x):
        """
        Find the percentile of a list of values.

        @parameter N - is a list of values. Note N MUST BE already sorted.
        @parameter percent - a float value from 0.0 to 1.0.
        @parameter key - optional key function to compute value from each element of N.

        @return - the percentile of the values
        """
        if not N:
            return None

        k = (len(N) - 1) * percent
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return key(N[int(k)])
        d0 = key(N[int(f)]) * (c - k)
        d1 = key(N[int(c)]) * (k - f)
        return d0 + d1

    def print_stats(self, percentile):
        print "----------------"
        print "Number of GET: " + str(self.num_GET_10_secs)
        print "Number of POST: " + str(self.num_POST_10_secs)
        print "Total number of hits: " + str((self.num_GET_10_secs + self.num_POST_10_secs))
        print "Number of proxied requests: " + str(self.num_proxied_req_10_secs)

        # Check if there have been proxies
        if bool(self.proxies_req_10_sec):
            # best_proxy = max(self.proxies_req_10_sec, key=self.proxies_req_10_sec.get) # This returns only 1 proxy
            highest = max(self.proxies_req_10_sec.values())
            best_proxy = ', '.join([k for k, v in self.proxies_req_10_sec.items() if v == highest])
            print "Most used proxy: " + best_proxy + " with " + str(highest) + " requests"
        else:
            print "No proxy has been used"

        # Print percentile
        if len(self.requests_time_10_sec) > 0:
            p = self.__calculate_percentile(sorted(self.requests_time_10_sec), percentile/100)
        else:
            p = 0

        print str(percentile) + " percentile request time: " + str(p)
