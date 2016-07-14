## Log Monitor
This is a  log monitor for an HTTP access.log file that receives data from multiple servers for a web application.  The program that is invoked with the following arguments:

```
logmonitor <access.log> <traffic_threshold>
```

where *access.log* is the path to a file that is being **actively** written-to and *traffic_threshold* is an integer parameter described in the requirements below. The task of this tool is to monitor the specified log file for HTTP traffic with log lines like these:

```
194.179.0.18, 10.16.1.2, 10.129.0.10 [13/02/2016 16:45:01] "GET /some/path?param1=x&param2=y HTTP/1.1" 200 0.006065388
213.1.20.7 [13/02/2016 16:45:02] "POST /some/other/path HTTP/1.0" 201 0.012901348
```

Conformant log lines contain US ASCII characters, and the fields are as follows, from left to right, always separated by one or more space or non-printable characters:
  * IPv4 addresses, from left to right, are the client's IP address, followed
    by optional additional addresses with the list of proxies forwarding the
    request to each other until the last one reaches us (the proxy chain).
    Addresses are separated by commas (`,`) and any amount of space or
    non-printable characters.
  * The date and the time of the request in UTC as recorded by the server that
    processed it, enclosed in brackets, and separated by a single space
    character.
  * The request information enclosed in double quotes, with the method, the
    path including any URL parameters, and the protocol and its version, each
    separated by one space character.
  * The status code of the response.
  * The seconds it took the server to process and respond to the request.

## Application Requirements

### Task 1 - Stats and alerts
* Once started the program must run continuously. Every 10 seconds *and* when
  terminated it should display:
  * The number of GET and POST methods hits, as well as the total number of hits.
  * The number of requests that have been proxied.
  * The proxy that forwarded most requests and number of forwarded requests.
  * The 95 percentile request time.

### Task 2 - Traffic threshold violations
* Whenever total traffic for the past minute *crosses* the traffic threshold
  *traffic_threshold*, it should show an alert saying `Traffic is [above/below]
  {threshold} requests/min at {current value}, [alert triggered/back to normal]
  at {current time}`. *Past minute* is defined as the previous 60 seconds at **any**
  given time.

### Task 3 - Efficient proxy chains
  * Add another alert to your program. Whenever an inefficient proxy chain is
    seen, based on proxy chains already observed, print a message saying:
    `Request originating at {client IP address} used inefficient proxy chain:
     {proxy chain}; there are N known efficient proxy chains: {list of
    efficient proxy chains}`.

    An *inefficient proxy chain* is one that contains *at least one* proxy common
    to other observed chains and a number of proxies after the common proxy
    larger than needed to reach the server.

    An *efficient proxy chain* is one for which *all* proxies are followed by the
    minimum amount of proxies possible to reach the server as per other observed
    proxy chains.

    Example:

    ```
    100.1.10.11, 89.2.1.13, 64.200.1.20, 10.1.10.16 * OK *
    80.139.20.2, 190.9.11.1, 89.2.1.13, 64.200.1.20, 10.1.10.15 * OK *
    193.176.1.4, 64.200.1.20, 10.1.10.15 * OK *
    77.8.100.30, 109.1.20.3, 64.200.1.20, 68.35.10.101, 10.1.10.13 * ALERT *!
    ```

    This would have displayed:

    ```
    Request originating at 77.8.100.30 used inefficient proxy chain:
      109.1.20.3, 64.200.1.20, 68.35.10.101, 10.1.10.13
    There are 2 known efficient proxy chains:
      1. 109.1.20.3, 64.200.1.20, 10.1.10.16
      2. 109.1.20.3, 64.200.1.20, 10.1.10.15
    ```

## Architecture description

##### Logmonitor

This is the executable file that is responsible of detecting when a new line is written in to the log file and perform the required tasks. It also implements signal handlers for program termination.

##### Logmonitor.conf
External configuration files so there is no need to modify the code if parameters change in the future. It is possible to modify the following variables:
- Stats_interval: 10 -> time interval for displaying stats (default: 10 secs)
- Percentile: 95 -> percentile request time (default: 95)
- Traffic_threshold_time: 60 -> past time for traffic threshold alerts (default: 60 secs)

##### Logline

This class represents a log line. The fields corresponds to the ones described in the EXERCISE.md

##### Loguilts

This file contains useful methods for parsing lines, converting strings and validate IPs. It makes use of regular expressions and an exception is thrown when a log line is not well formatted.

##### Logstats
This class keeps track of the number/type of requests and proxies written into the log file.
Since no external libraries are allowed, the percentile function has been reimplemented (it could be replace by the percentile() function of the numpy package).

##### Logalerts

This class is able to detect when an alert needs to be raised due to constraint violations (traffic threshold). It uses a circular buffer (deque) in order to keep always stored only the number of requests arrived in the last N  seconds (N= 60 since *Past minute* is defined as the previous 60 seconds at **any** given time).

##### Proxymanager
This class is responsible of detecting inefficient proxy chains.
The chains are represented as a linked list where a proxy points to its next one in the chain. This is implemented with a dictionary where the key is the proxy and the value is a Proxyitem element representing the next proxy in the chain.

A **recursive** function (print_chain(…) ) takes care of printing the efficient proxy chains.

##### Proxyitem
The fields of this class are:
- hops: the number of the following proxies in the chain
- next_items: a list of the following proxies (since the same proxy can has different following proxies)
- num_of_chain: the number of chains for this proxy


# Implementation task 1
The number of requests/proxies, etc... are stored in variables that every 10 seconds are refreshed.
When a new request arrive, they are updated.
If a termination signal is received the last values are display before exiting.

# Implementation task 2
A circular buffer is updated every second.
Insertion are appended to the right size and the rest of the elements are automatically left-shifted.
Each second the total number of requests in the buffer is updated: sum of the new appended value (if any) and subtraction of the oldest one (if any).
This allows to have at any second the total number of requests of the last minute and no need to re-count it each time.

Although we need to create an buffer of fixed size at the beginning, performance is improved a lot: we don't need to sum each second the total number of requests but we always keep the total and we just subtract the first value of the buffer before removing it that corresponds to the -61 second.

# Implementation task 3
Inefficient proxies detection has been implemented as a linked list where each proxy in the chain point to the next one. A part from this, the length of the chain is stored for each proxy so we don't need to walk to the map to count the length of th current "best chain".
Printing the efficient chains has been implemented using a recursive functions

# Optimization
1. Instead of opening the log file each seconds and check the requests I use an implementation that each time that a line is written in the file, it is processed by the program (as the unix command tail -f).
This avoids a lot of file open/close operations that can slow down the process.
2. For detecting threshold violations I use a circular buffer that keep stored the number of requests for each seconds in last n seconds(60 in this case).
3. The data structures used for proxy chains are dictionary (which has an average time complexity of is O(1)) and a sort of linked list to keep track of the relationship between proxies.
4. CPU and memory usage is not high
