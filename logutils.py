#!/usr/bin/env python
import re
import socket
from datetime import datetime

# Regex for lines
regex = '([(\d\.\,\s*)]+)[\x20-\x2F]+\[(.*?)\][\x20-\x2F]+"(.*?)"[\x20-\x2F]+(\d+)[\x20-\x2F]+(\d+\.\d+)$'


def parse_request_info(request_info):
    """
    :param request_info: string to parse
    :return: req_method, req_path, req_protocol
    """
    tokens = request_info.split()
    try:
        req_method = tokens[0]
        req_path = tokens[1]
        req_protocol = tokens[2]
    except IndexError:
        raise AttributeError("Request info format is wrong")
    return req_method, req_path, req_protocol


def check_ip_format(ips):
    for ip in ips:
        if ' ' in ip:  # inet_aton does not detect ip separated by spaces
            raise AttributeError("Invalid IP found")
        else:
            try:
                socket.inet_aton(ip)
            except socket.error:
                raise AttributeError("Invalid IP found")


def check_status_code(status):
    try:
        int(status)
    except ValueError:
        raise AttributeError("Wrong status code")


def check_request_time(time_to_process):
    try:
        float(time_to_process)
    except ValueError:
        raise AttributeError("Wrong processing time")
    return float(time_to_process)


def convert_date_to_seconds(date):
    """
    :param date: string representing the date
    :return: unix timestamp
    """
    try:
        date_object = datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
    except ValueError:
        raise AttributeError("Invalid format for data: " + date + " Accepted format: %d/%m/%Y %H:%M:%S")

    # Return unix time in seconds
    return int(date_object.strftime('%s'))


def parse_ip_addresses(addresses):
    """
    :param addresses: string of ip addresses to parse
    :return: list of ips
    """
    ip_regex = "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    ips = [x.strip() for x in addresses.split(',')]
    try:
        for ip in ips:
            re.match(ip_regex, ip).groups()
    except:
        raise AttributeError("Line does not match regular expression: ignoring line")
    return ips


def parse_string(line):
    """
    :param line: line to parse
    :return: ips, date, request_info, status_code, time_to_process
    """
    try:
        splits = re.match(regex, line).groups()
    except:
        raise AttributeError("Line does not match regular expression: ignoring line")

    ip_addresses = splits[0]
    dt = splits[1]
    request_info = splits[2]
    status_code = splits[3]
    time_to_process = splits[4]

    try:  # Check format for each field
        ips = parse_ip_addresses(ip_addresses)
        check_ip_format(ips)
        client = ips[0]
        proxies = ips[1:]
        check_status_code(status_code)
        time_process = check_request_time(time_to_process)
        date = convert_date_to_seconds(dt)
    except AttributeError as e:
        raise AttributeError(e)

    return client, proxies, date, request_info, status_code, time_process
