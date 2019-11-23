from neo4j import GraphDatabase
import time

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "deven123"))

CONFIG_FILES = [ '/proc/filesystems' ]
READ_SYSCALLS = [ 'read', ]
WRITE_SYSCALLS = [ 'write', 'open' ]

def get_resources_for_process_id(tx, raw_inputs):
    process_id = int(raw_inputs)

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE toInteger(PROC.process_id) = $process_id "
        "RETURN RES.name AS RESOURCE_NAME",
        process_id=process_id
    ):
        ret.add(str(record['RESOURCE_NAME']))

    return ret

def get_resources_for_process_id_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_id = int(inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE toInteger(PROC.process_id) = $process_id AND toFloat(USE.ts) < $ts_start AND toFloat(USE.ts) > $ts_end"
        " RETURN RES.name AS RESOURCE_NAME",
        process_id = process_id,
        ts_start = start_time,
        ts_end = end_time
    ):
        ret.add(record['RESOURCE_NAME'])

    return ret

def check_if_path_is_config_file(filepath):
    return filepath in CONFIG_FILES

def get_configuration_files_for_process_id(tx, raw_inputs):
    process_id = float(raw_inputs)

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE toInteger(PROC.process_id) = $process_id"
        " RETURN RES.name AS RESOURCE_NAME",
        process_id = process_id
    ):
        if check_if_path_is_config_file(record['RESOURCE_NAME']):
            ret.add(record['RESOURCE_NAME'])

    return ret

def get_configuration_files_for_process_id_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_id = int(inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE toInteger(PROC.process_id) = $process_id AND toFloat(USE.ts) <= $ts_start AND toFloat(USE.ts) >= $ts_end"
        " RETURN RES.name AS RESOURCE_NAME",
        process_id = process_id,
        ts_start = start_time,
        ts_end = end_time
    ):
        if check_if_path_is_config_file(record['RESOURCE_NAME']):
            ret.add(record['RESOURCE_NAME'])

    return ret

def get_process_ids_for_program_name(tx, raw_inputs):
    process_name = raw_inputs

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE PROC.name = $process_name"
        " RETURN PROC.process_id AS PROCESS_ID",
        process_name=process_name
    ):
        ret.add(record['PROCESS_ID'])

    return ret

def get_process_ids_for_program_name_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_name = int(inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE PROC.name = $process_name AND AND toFloat(USE.ts) <= $ts_start AND toFloat(USE.ts) >= $ts_end"
        " RETURN PROC.process_id AS PROCESS_ID",
        process_name=process_name,
        ts_start=start_time,
        ts_end=end_time
    ):
        ret.add(record['PROCESS_ID'])

    return ret


def get_resources_for_process_name(tx, raw_inputs):
    process_name = raw_inputs

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        " WHERE PROC.name = $process_name"
        " RETURN RES.name AS RESOURCE_NAME",
        process_name=process_name
    ):
        ret.add(str(record['RESOURCE_NAME']))

    return ret

def get_resources_for_process_name_between_ts(tx, raw_inputs):
    inputs = raw_inputs
    process_name = (inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        " WHERE PROC.name = $process_name AND toFloat(USE.ts) < $ts_start AND toFloat(USE.ts) > $ts_end"
        " RETURN RES.name AS RESOURCE_NAME",
        process_name=process_name,
        ts_start=start_time,
        ts_end=end_time
    ):
        ret.add(str(record['RESOURCE_NAME']))

    return ret

def get_process_ids_for_resource(tx, raw_inputs):
    resource_name = int(raw_inputs)

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE RES.name = $resource_name "
        "RETURN PROC.process_id AS PROCESS_ID",
        resource_name=resource_name
    ):
        ret.add(str(record['PROCESS_ID']))

    return ret

def get_process_ids_for_resource_between_ts(tx, raw_inputs):
    inputs = raw_inputs
    resource_name = (inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE RES.name = $resource_name AND toFloat(USE.ts) < $ts_start AND toFloat(USE.ts) > $ts_end "
        "RETURN PROC.process_id AS PROCESS_ID",
        resource_name=resource_name,
        ts_start=start_time,
        ts_end=end_time
    ):
        ret.add(str(record['PROCESS_ID']))

    return ret

def get_process_ids_for_config_resources(tx, raw_inputs):
    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE RES.name IN {resource_names} "
        "RETURN PROC.process_id AS PROCESS_ID",
        resource_names=CONFIG_FILES
    ):
        ret.add(str(record['PROCESS_ID']))

    return ret

def get_process_ids_for_config_resources_between_ts(tx, raw_inputs):
    inputs = raw_inputs
    start_time = float(inputs[0])
    end_time = float(inputs[1])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE RES.name IN {resource_names} AND toFloat(USE.ts) < $ts_start AND toFloat(USE.ts) > $ts_end "
        "RETURN PROC.process_id AS PROCESS_ID",
        resource_names=CONFIG_FILES,
        start_time=ts_start,
        end_time=ts_end
    ):
        ret.add(str(record['PROCESS_ID']))

    return ret

def get_most_freq_accessed_resources_by_program(tx, raw_inputs):
    process_name = raw_inputs

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.name = $process_name "
        "RETURN RES.name AS RESOURCE_NAME, COUNT(*) AS COUNT "
        "ORDER BY COUNT DESC",
        process_name=process_name
    ):
        ret.add((str(record['RESOURCE_NAME']), str(record['COUNT'])))

    return ret

def get_read_write_ratio_of_process(tx, raw_inputs):
    process_id = int(raw_inputs)

    read_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.process_id = $process_id AND USE.type IN {call_types} "
        "RETURN COUNT(*) AS COUNT ",
        process_id=process_id,
        call_types=READ_SYSCALLS
    ):
        read_count = record['COUNT']
        break

    write_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.process_id = $process_id AND USE.type IN {call_types} "
        "RETURN COUNT(*) AS COUNT ",
        process_id=process_id,
        call_types=WRITE_SYSCALLS
    ):
        write_count = record['COUNT']
        break

    print('Number of reads:' , read_count)
    print('Number of writes:' , write_count)

    if (write_count > 0):
        return float(read_count) / float(write_count)
    else:
        return None

def get_read_write_ratio_of_process_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_id = int(inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    read_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.process_id = $process_id AND USE.type IN {call_types} AND toFloat(USE.ts) <= $ts_start AND toFloat(USE.ts) >= $ts_end "
        "RETURN COUNT(*) AS COUNT ",
        process_id=process_id,
        call_types=READ_SYSCALLS,
        ts_start=start_time,
        ts_end=end_time
    ):
        read_count = record['COUNT']
        break

    write_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.process_id = $process_id AND USE.type IN {call_types} AND toFloat(USE.ts) <= $ts_start AND toFloat(USE.ts) >= $ts_end "
        "RETURN COUNT(*) AS COUNT ",
        process_id=process_id,
        call_types=WRITE_SYSCALLS,
        ts_start=start_time,
        ts_end=end_time
    ):
        write_count = record['COUNT']
        break

    print('Number of reads:' , read_count)
    print('Number of writes:' , write_count)

    if (write_count > 0):
        return float(read_count) / float(write_count)
    else:
        return None

def get_read_write_ratio_of_program(tx, raw_inputs):
    process_name = raw_inputs

    read_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.name = $program_name AND USE.type IN {call_types}"
        "RETURN COUNT(*) AS COUNT ",
        program_name=process_name,
        call_types=READ_SYSCALLS
    ):
        read_count = record['COUNT']
        break

    write_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.name = $program_name AND USE.type IN {call_types}"
        "RETURN COUNT(*) AS COUNT ",
        program_name=process_name,
        call_types=WRITE_SYSCALLS
    ):
        write_count = record['COUNT']
        break

    print('Number of reads:' , read_count)
    print('Number of writes:' , write_count)

    if (write_count > 0):
        return float(read_count) / float(write_count)
    else:
        return None

def get_read_write_ratio_of_program_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_name = inputs[0]
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    read_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.name = $program_name AND USE.type IN {call_types} AND toFloat(USE.ts) <= $ts_start AND toFloat(USE.ts) >= $ts_end "
        "RETURN COUNT(*) AS COUNT ",
        program_name=process_name,
        call_types=READ_SYSCALLS,
        ts_start=start_time,
        ts_end=end_time
    ):
        read_count = record['COUNT']
        break

    write_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.name = $program_name AND USE.type IN {call_types} AND toFloat(USE.ts) <= $ts_start AND toFloat(USE.ts) >= $ts_end "
        "RETURN COUNT(*) AS COUNT ",
        program_name=process_name,
        call_types=WRITE_SYSCALLS,
        ts_start=start_time,
        ts_end=end_time
    ):
        write_count = record['COUNT']
        break

    print('Number of reads:' , read_count)
    print('Number of writes:' , write_count)

    if (write_count > 0):
        return float(read_count) / float(write_count)
    else:
        return None

def get_top_resource_utilizing_processes(tx, raw_inputs):
    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "RETURN PROC.process_id AS PROCESS_ID, count(*) as COUNT "
        "ORDER BY COUNT DESC"
    ):
        ret.add((str(record['PROCESS_ID']), str(record['COUNT'])))

    return ret

def get_top_used_resources(tx, raw_inputs):
    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "RETURN RES.name AS RESOURCE_NAME, count(*) as COUNT "
        "ORDER BY COUNT DESC"
    ):
        ret.add((str(record['RESOURCE_NAME']), str(record['COUNT'])))

    return ret

queries = [
    {
        'text': "Get list of resources accessed by a process",
        'follow_up': 'Enter the process ID (ex. 1234): ',
        'query': get_resources_for_process_id
    },
    {
        'text': "Get list of resources accessed by a process between start time and end time",
        'follow_up': 'Enter the process ID, start_time and end_time (space separated) (ex. 1234 1541873682.803 1641873682.803): ',
        'query': get_resources_for_process_id_between_ts
    },
    {
        'text': "Get list of configuration files accessed by a process",
        'follow_up': 'Enter the process ID (ex. 1234): ',
        'query': get_configuration_files_for_process_id
    },
    {
        'text': "Get list of configuration files accessed by a process between start time and end time",
        'follow_up': 'Enter the process ID, start_time and end_time (space separated) (ex. 1234 1541873682.803 1641873682.803): ',
        'query': get_configuration_files_for_process_id_between_ts
    },
    {
        'text': "Get a list of all process instances for a program name",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',
        'query': get_process_ids_for_program_name
    },
    {
        'text': "Get a list of all process instances for a program name between start time and end time",
        'follow_up': 'Enter the program name, start_time and end_time (space separated) (ex. /bin/vi 1541873682.803 1641873682.803): ',
        'query': get_process_ids_for_program_name_between_ts
    },
    {
        'text': "Get an aggregated list of resources accessed by all processes of a program name",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',
        'query': get_resources_for_process_name
    },
    {
        'text': "Get an aggregated list of resources accessed by all processes of a program name between start time and end time",
        'follow_up': 'Enter the program name, start_time and end_time (space separated) (ex. /bin/vi 1541873682.803 1641873682.803): ',
        'query': get_resources_for_process_name_between_ts
    },
    {
        'text': "Get a list of processes that accessed a resource",
        'follow_up': 'Enter the resource name (ex. /etc/auditd.rules): ',
        'query': get_process_ids_for_resource
    },
    {
        'text': "Get a list of processes that accessed a resource between start time and end time",
        'follow_up': 'Enter the resource name, start_time and end_time (space separated) (ex. /etc/auditd.rules 1541873682.803 1641873682.803): ',
        'query': get_process_ids_for_resource_between_ts
    },
    {
        'text': "Get a list of processes that accessed a configuration resource",
        'query': get_process_ids_for_config_resources
    },
    {
        'text': "Get a list of processes that accessed a configuration resource between start time and end time",
        'follow_up': 'Enter the start_time and end_time (space separated) (ex. 1541873682.803 1641873682.803): ',
        'query': get_process_ids_for_config_resources_between_ts
    },
    {
        'text': "Get an aggregated list of most frequently accessed resources by all instances for a program name",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',        
        'query': get_most_freq_accessed_resources_by_program
    },
    {
        'text': "Get the approximate read write ratio of a process",
        'follow_up': 'Enter the process ID (ex. 1234): ',
        'query': get_read_write_ratio_of_process
    },
    {
        'text': "Get the approximate read write ratio of a program",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',
        'query': get_read_write_ratio_of_program
    },
    {
        'text': "Get the approximate read write ratio of a process between start time and end time",
        'follow_up': 'Enter the process ID, start_time and end_time (space separated) (ex. 1234 1541873682.803 1641873682.803): ',
        'query': get_read_write_ratio_of_process_between_ts
    },
    {
        'text': "Get the approximate read write ratio of a process between start time and end time",
        'follow_up': 'Enter the program name, start_time and end_time (space separated) (ex. 1234 1541873682.803 1641873682.803): ',
        'query': get_read_write_ratio_of_program_between_ts
    },
    {
        'text': "Get the list of top resource-utilizing processes",
        'query': get_top_resource_utilizing_processes
    },
    {
        'text': "Get the list of most commonly used resources",
        'query': get_top_used_resources
    }
]

def print_commands():
    print "* Select a query option OR Enter 0 to exit *\n"
    for index, query in enumerate(queries):
        print index + 1, ":", query['text']

with driver.session() as session:
    print("*** Database connection success ***\n")

    while (True):
        print_commands()
        input_command = input('> ')

        if (input_command <= 0):
            print ('\nExiting...')
            break
        if (input_command > len(queries)):
            print ('Invalid input.')
            continue

        raw_inputs = None
        if 'follow_up' in queries[input_command - 1]:
            raw_inputs = raw_input(queries[input_command - 1]['follow_up'])

        start_time = time.time()
        result = session.read_transaction(queries[input_command - 1]['query'], raw_inputs)
        exec_time = time.time() - start_time

        print(result)
        print("\n--- Query took %s seconds ---\n" % (exec_time))
