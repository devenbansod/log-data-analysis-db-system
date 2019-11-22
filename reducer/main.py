#!/usr/bin/python

import csv
import sys
import string
import copy
from natsort import natsorted
from collections import defaultdict, OrderedDict


COLS = {
    'ts': 0,
    'src': 1,
    'src_name': 2,
    'type': 3,
    'dst': 4
}

def get_time_tuple(time):
    f_milli_ind = time.rfind(".")
    f_serial_ind = time.rfind(":")

    return (
        float(time[:f_milli_ind]),
        float(time[f_milli_ind + 1: f_serial_ind]),
        float(time[f_serial_ind + 1:])
    )

def compareTo(time1, time2):
    """
    returns true if time1 < time2 || (time1 == time2 && serial1 < serial2)
    """
    (start_1_second, start_1_milli, start_1_serial) = get_time_tuple(time1)
    (start_2_second, start_2_milli, start_2_serial) = get_time_tuple(time2)

    ret = ((start_1_second < start_2_second) or (start_1_second == start_2_second and start_1_milli < start_2_milli) or (start_1_second == start_2_second and start_1_milli == start_2_milli and start_1_serial < start_2_serial))

    # print start_1_second, start_2_second, ret
    
    return ret

EDGE_LIST = []

# Build adjacency list from the edge list
OUTGOING_ADJ_LIST = defaultdict(set)
INCOMING_ADJ_LIST = defaultdict(set)

with open(sys.argv[1], "r") as f:
    reader = csv.reader(f, delimiter=",")

    for i, event in enumerate(reader):
        u = event[COLS['src']]
        v = event[COLS['dst']]

        OUTGOING_ADJ_LIST[u].add(tuple(event))
        INCOMING_ADJ_LIST[v].add(tuple(event))
        EDGE_LIST.append(event)

with open(sys.argv[2], "r") as f:
    reader = csv.reader(f, delimiter=",")

    for i, event in enumerate(reader):
        u = event[COLS['src']]
        v = event[COLS['dst']]

        # for backwards.csv, reverse the edge
        OUTGOING_ADJ_LIST[v].add(tuple(event))
        INCOMING_ADJ_LIST[u].add(tuple(event))
        EDGE_LIST.append(event)

def forward_check(ep, et, v):
    for event in OUTGOING_ADJ_LIST[v]:
        t_start_ep = ep[COLS['ts']]
        t_start_et = et[COLS['ts']]

        if (compareTo(t_start_ep, event[COLS['ts']]) and compareTo(event[COLS['ts']], t_start_et)) \
            or (compareTo(t_start_et, event[COLS['ts']]) and compareTo(event[COLS['ts']], t_start_ep)):
            return False

    return True

def backward_check(ep, et, u):
    for event in INCOMING_ADJ_LIST[u]:
        t_end_ep = ep[COLS['ts']]
        t_end_et = et[COLS['ts']]

        if (compareTo(t_end_et, event[COLS['ts']]) and compareTo(event[COLS['ts']], t_end_ep)) \
            or (compareTo(t_end_ep, event[COLS['ts']]) and compareTo(event[COLS['ts']], t_end_et)):
            return False

    return True

def merge(ep, el):
    ep[COLS['ts']] = el[COLS['ts']]
    return ep

F = []
S = []

# EDGE_LIST = [
#     ['2.0:123123123', '41241', 'E', 'write', 'C'],
#     ['10.0:434426125', '25316', 'A', 'read', 'B'],
#     ['15.0:434426129', '25316', 'A', 'read', 'C'],
#     ['28.0:434426129', '25316', 'A', 'read', 'C'],
#     ['36.0:434426125', '25316', 'A', 'exec', 'D'],
#     ['40.0:434426129', '25316', 'A', 'read', 'B']
# ]

COPY = copy.deepcopy(EDGE_LIST)

for i in range(len(EDGE_LIST)):
    event = EDGE_LIST[i]

    u = event[COLS['src']]
    v = event[COLS['dst']]

    # if stack empty, push the event
    if len(S) <= 0:
        S.append(event)
    else:
        ep = S.pop()

        if ep[COLS['src']] == u and ep[COLS['dst']] == v and forward_check(ep, event, v) and backward_check(ep, event, u):
            j = COPY.index(ep)

            ep[COLS['ts']] = event[COLS['ts']]
            COPY[j] = ep
            COPY.remove(event)

            S.append(ep)
        else:
            S.append(event)

print len(EDGE_LIST) - len(COPY), "records merged"

with open(sys.argv[3], "wb") as f:
    writer = csv.writer(f)
    writer.writerows(COPY)
