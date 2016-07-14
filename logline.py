#!/usr/bin/env python
class LogLine:
    """ This class represent a log line (list of proxies is optional) """

    def __init__(self, client_ip, date_time, method, path, protocol, status_code, time_process, proxies=None, written_time=None):
        self.client_ip = client_ip
        self.date_time = date_time
        self.method = method
        self.path = path
        self.protocol = protocol
        self.status_code = status_code
        self.time_process = time_process
        self.proxies = proxies
        self.written_time = written_time

    def __str__(self):
        return "Client: " + str(self.client_ip) + "\n" \
                "Proxies: " + str(self.proxies) + "\n" \
                "Date (timestamp): " + str(self.date_time) + "\n" \
                "Method: " + str(self.method) + "\n" \
                "Path: " + str(self.path) + "\n" \
                "Protocol: " + str(self.protocol) + "\n" \
                "Status: " + str(self.status_code) + "\n" \
                "Time to process: " + str(self.time_process) + "\n" \
                "Timestamp for log file: " + str(self.written_time)



