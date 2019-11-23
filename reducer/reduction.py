import string
import time
import bisect
import copy
import glob
import os
from collections import defaultdict, OrderedDict

from parser import parse, compareTo
from csv_maker import generate
from checker import forward_check, backward_check


def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1

def find_lower_upper_limit_of_interval(e_, e, events):
    lower_limit = events[e][0]
    upper_limit = events[e_][1]

    if compareTo(events[e_][0], events[e][0]):
        lower_limit = events[e_][0]
    else:
	print "Error in the order of events!"
    if compareTo(events[e_][1], events[e][1]):
        upper_limit = events[e][1]

    return lower_limit, upper_limit


def reduce(forward_file, backward_file, out_dir):    
    parents, children, events, csv_details, parents_id, children_id = parse(forward_file, backward_file)

    parent_ids = []
    stacks = defaultdict(list)
    events = OrderedDict(sorted(events.items(), key = lambda (k, v): v[0]))
    events_final = copy.deepcopy(events)
    for event, time_interval in events.items():
        u, v, sys_call, id_ = event
        # print(u, v, sys_call, id_)
        if len(stacks[(u, v, sys_call)]) == 0:
            stacks[(u, v, sys_call)].append(event)
        else:
            candidate_event = stacks[(u, v, sys_call)].pop(-1)
            if (forward_check(candidate_event, event, v, children, events) and \
                    backward_check(candidate_event, event, u, parents, events)):
                lower_limit, upper_limit = find_lower_upper_limit_of_interval(candidate_event, event, events)
                events[candidate_event] = (lower_limit, upper_limit,) #the lower limit and upper
                #limit gets updated for the same key as of the popped event
                events_final[candidate_event] = (lower_limit, upper_limit,)
                parents_index = index(parents_id[v], id_)
                if parents_index != -1:
                    del parents[v][parents_index]
                    del parents_id[v][parents_index]
                children_index = index(children_id[u], id_)
                if children_index != -1:
                    del children[u][children_index]
                    del children_id[u][children_index]

                del events_final[event]
                stacks[(u, v, sys_call)].append(candidate_event)
            else:
                stacks[(u, v, sys_call)].append(event)

    # print events_final
    # print csv_details
    generate(events_final, csv_details, out_dir)

    # return global_list_processed_files_forward, global_list_processed_files_backward
