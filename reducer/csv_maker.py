import csv
import time

def get_time_tuple(time):
    f_milli_ind = time.rfind(".")
    f_serial_ind = time.rfind(":")

    return (
        float(time[:f_milli_ind]),
        float(time[f_milli_ind + 1: f_serial_ind]),
        float(time[f_serial_ind + 1:])
    )

def generate(events_final, csv_details, out_dir):
    forward_count = 0
    backward_count = 0

    forward_file_index = 0
    backward_file_index = 0

    forward_file_name = out_dir + 'forward-reduced.csv'
    backward_file_name = out_dir + 'backward-reduced.csv'

    forward_file = open(forward_file_name, mode='w')
    backward_file = open(backward_file_name, mode='w')

    forward_writer = csv.writer(forward_file, delimiter=',')
    backward_writer = csv.writer(backward_file, delimiter=',')

    for k, value in events_final.items():
        u, v, sys_call, id = k
        # print csv_details[id]
        first_col = csv_details[id][0]
        tag = csv_details[id][3]

        time_start, time_end = value
        time_tuple = get_time_tuple(csv_details[id][0])
        if tag == 'FORWARD':
            forward_count += 1
            time_tuple = get_time_tuple(first_col)
            print(time_tuple[0], time_tuple[1], float(time_tuple[0]) + float(time_tuple[1]) / 1000)
            l = [float(time_tuple[0]) + float(time_tuple[1]) / 1000, int(time_tuple[2]), u, csv_details[id][1], sys_call, v] #time_start, time_end]
            forward_writer.writerow(l)
        elif tag == 'BACKWARD':
            backward_count += 1
            print(time_tuple[0], time_tuple[1], float(time_tuple[0]) + float(time_tuple[1]) / 1000)
            l = [float(time_tuple[0]) + float(time_tuple[1]) / 1000, int(time_tuple[2]), u, csv_details[id][1], sys_call, v] # time_start, time_end]
            backward_writer.writerow(l)

    forward_file.close()
    backward_file.close()

    print "forward count --> ", forward_count
    print "backward count --> ", backward_count
