import csv
import string
from natsort import natsorted
from collections import defaultdict, OrderedDict

COLS = {
    'ts': 0,
    'src': 1,
    'src_name': 2,
    'type': 3,
    'dst': 4
}

def compareTo(time1, time2):
    # returns true if time1 <= time2
    start_1_second, start_1_milli, start_1_serial = time1
    start_2_second, start_2_milli, start_2_serial = time2

    return ((start_1_second < start_2_second) or (start_1_second == start_2_second and start_1_milli < start_2_milli) or (start_1_second == start_2_second and start_1_milli == start_2_milli and start_1_serial <= start_2_serial))

def read_csv(filename):
    file = open(filename, 'rb')
    f_reader = csv.reader(file, delimiter=',')

    for row in f_reader:
        yield row

def parse(forward_file, backward_file):
    parents = defaultdict(list)
    children = defaultdict(list)
    parents_id = defaultdict(list)
    children_id = defaultdict(list)
    events = defaultdict(tuple) # make an ordereddict to maintain the order to avoid sorting.
    meta = defaultdict(tuple)
    time = dict()

    id = 0

    f = read_csv(forward_file)
    b = read_csv(backward_file)

    f_row = next(f, "DONE")
    b_row = next(b, "DONE")

    while f_row is not "DONE" or b_row is not "DONE":
        if f_row is not "DONE":
            f_milli_ind = f_row[COLS['ts']].rfind(".")
            f_serial_ind = f_row[COLS['ts']].rfind(":")

            f_start_serial = float(f_row[COLS['ts']][f_serial_ind + 1:])
            f_start_milli = float(f_row[COLS['ts']][f_milli_ind + 1 : f_serial_ind])
            f_start_second = float(f_row[COLS['ts']][:f_milli_ind])

        if b_row is not "DONE":
            b_milli_ind = b_row[COLS['ts']].rfind(".")
            b_serial_ind = b_row[COLS['ts']].rfind(":")

            b_start_serial = float(b_row[COLS['ts']][b_serial_ind + 1:])
            b_start_second = float(b_row[COLS['ts']][:b_milli_ind])
            b_start_milli = float(b_row[COLS['ts']][b_milli_ind + 1 : b_serial_ind])

        if b_row is "DONE" or  (f_row is not "DONE" and compareTo((f_start_second, f_start_milli, f_start_serial), (b_start_second, b_start_milli, b_start_serial))):
            v = f_row[COLS['dst']]
            u = f_row[COLS['src']]
            sys_call = f_row[COLS['type']]
            time_start = (f_start_second, f_start_milli, f_start_serial)
            metaData = (f_row[COLS['ts']], f_row[COLS['src_name']], f_row[COLS['type']], "FORWARD")
            f_row = next(f, "DONE")

        else:
            v = b_row[COLS['dst']]
            u = b_row[COLS['src']]
            sys_call = b_row[COLS['type']]
            time_start = (b_start_second, b_start_milli, b_start_serial)
            metaData = (b_row[COLS['ts']], b_row[COLS['src_name']], b_row[COLS['type']], "BACKWARD")
            b_row = next(b, "DONE")

        parents[v].append((u, sys_call, id))
        parents_id[v].append(id)
        children[u].append((v, sys_call, id))
        children_id[u].append(id)
        events[(u, v, sys_call, id)] = (time_start, time_start)
    	meta[id] = metaData
        id += 1

    # print "ID:", id
    return parents, children, events, meta, parents_id, children_id
