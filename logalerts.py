#!/usr/bin/env python
import collections
import time


class LogAlerts:
    """ This class is responsible of raising alerts due to violations """

    def __init__(self, time_back):
        self.time_back = time_back
        self.traffic_queue = collections.deque(maxlen=time_back)
        self.total_traffic = 0
        self.last_arrival = int(time.time())

    def initialize_traffic_queue(self):
        for i in range(0, self.time_back):
            self.traffic_queue.append(0)
        self.total_traffic = 0

    def traffic_alert(self, threshold, current_time, past_status_alert=False):
        if self.total_traffic > threshold:
            print "Traffic is above " + str(threshold) + " requests/min at " + str(self.total_traffic) + ", alert triggered at " + str(current_time)
            past_status_alert = True
        elif past_status_alert:
            print "Traffic is below " + str(threshold) + " requests/min at " + str(self.total_traffic) + ", back to normal at " + str(current_time)
            past_status_alert = False
        return past_status_alert

    def add_request_to_traffic_threshold(self, arrival_time, request):
        """
        Sum values if there are multiple requests arriving at the same time and append to the last element of the buffer
        :param arrival_time: timestamp of when a line is written into the log file
        :param request: if True a request has been detected, else append 0
        """
        # print arrival_time, self.last_arrival, request
        if request:
            val = self.traffic_queue[self.time_back - 1]
            val_updated = val + 1

            if arrival_time == self.last_arrival:
                self.traffic_queue[self.time_back - 1] = val_updated
                self.total_traffic = self.total_traffic - self.traffic_queue[0] - val + val_updated
            else:
                self.traffic_queue.append(val_updated)
                self.total_traffic = self.total_traffic - self.traffic_queue[0] + val_updated
        else:
            val_updated = 0
            self.total_traffic = self.total_traffic - self.traffic_queue[0] + val_updated
            self.traffic_queue.append(val_updated)

        # Update last time
        self.last_arrival = arrival_time

