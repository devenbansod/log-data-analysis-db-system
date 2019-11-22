from neo4j import GraphDatabase
import time

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "deven123"))

def get_resources_for_process_id(tx, raw_inputs):
    process_id = int(raw_inputs)

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE toInteger(PROC.process_id) = $process_id "
        "RETURN PROC.name AS RESOURCE_NAME",
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
        " WHERE toInteger(PROC.process_id) = $process_id AND toFloat(RES.ts) < $ts_start AND toFloat(RES.ts) > $ts_end"
        " RETURN RES.name AS RESOURCE_NAME",
        process_id = process_id,
        ts_start = start_time,
        ts_end = end_time
    ):
        ret.add(record['RESOURCE_NAME'])

    return ret

def check_if_path_is_config_file(filepath):
    return True

def get_list_of_configuration_files_for_process_id(tx, raw_inputs):
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

def get_list_of_configuration_files_for_process_id_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_id = int(inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE toInteger(PROC.process_id) = $process_id AND toFloat(RES.ts) <= $ts_start AND toFloat(RES.ts) >= $ts_end"
        " RETURN RES.name AS RESOURCE_NAME",
        process_id = process_id,
        ts_start = start_time,
        ts_end = end_time
    ):
        if check_if_path_is_config_file(record['RESOURCE_NAME']):
            ret.add(record['RESOURCE_NAME'])

    return ret

def get_list_of_process_ids_for_process_name(tx, raw_inputs):
    process_name = raw_inputs

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE PROC.name = $process_name"
        " RETURN RES.name AS RESOURCE_NAME",
        process_name=process_name
    ):
            ret.add(record['RESOURCE_NAME'])

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
        'query': get_list_of_configuration_files_for_process_id
    },
    {
        'text': "Get list of configuration files accessed by a process between start time and end time",
        'follow_up': 'Enter the process ID, start_time and end_time (space separated) (ex. 1234 1541873682.803 1641873682.803): ',
        'query': get_list_of_configuration_files_for_process_id_between_ts
    },
    {
        'text': "Get a list of all process instances for a program name",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',
        'query': ""
    },
    {
        'text': "Get a list of all process instances for a program name between start time and end time",
        'follow_up': 'Enter the program name, start_time and end_time (space separated) (ex. /bin/vi 1541873682.803 1641873682.803): ',
        'query': ""
    },
    {
        'text': "Get an aggregated list of resources accessed by all processes of a program name",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',
        'query': ""
    },
    {
        'text': "Get an aggregated list of resources accessed by all processes of a program name between start time and end time",
        'follow_up': 'Enter the program name, start_time and end_time (space separated) (ex. /bin/vi 1541873682.803 1641873682.803): ',
        'query': ""
    },
    {
        'text': "Get a list of processes that accessed a resource",
        'follow_up': 'Enter the resource name (ex. /etc/auditd.rules): ',
        'query': ""
    },
    {
        'text': "Get a list of processes that accessed a resource between start time and end time",
        'follow_up': 'Enter the resource name, start_time and end_time (space separated) (ex. /etc/auditd.rules 1541873682.803 1641873682.803): ',
        'query': ""
    },
    {
        'text': "Get a list of processes that accessed a configuration resource",
        'follow_up': 'Enter the configuration resource name (ex. /etc/auditd.rules): ',
        'query': ""
    },    {
        'text': "Get a list of processes that accessed a configuration resource between start time and end time",
        'follow_up': 'Enter the configuration resource name, start_time and end_time (space separated) (ex. /etc/auditd.rules 1541873682.803 1641873682.803): ',
        'query': ""
    },
    {
        'text': "Get an aggregated list of most frequently accessed resources by all instances for a program name",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',        
        'query': ""
    },
    {
        'text': "Get the approximate read write ratio of a process",
        'follow_up': 'Enter the process ID (ex. 1234): ',
        'query': ""
    },    {
        'text': "Get the approximate read write ratio of a process between start time and end time",
        'follow_up': 'Enter the process ID, start_time and end_time (space separated) (ex. 1234 1541873682.803 1641873682.803): ',
        'query': ""
    },
    {
        'text': "Get the list of top resource-utilizing processes",
        'query': ""
    },
    {
        'text': "Get the list of most commonly used resources",
        'query': ""
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
        if (input_command >= len(queries)):
            print ('Invalid input.')
            continue

        if 'follow_up' in queries[input_command - 1]:
            raw_inputs = raw_input(queries[input_command - 1]['follow_up'])

        start_time = time.time()
        result = session.read_transaction(queries[input_command - 1]['query'], raw_inputs)
        exec_time = time.time() - start_time

        print(result)
        print("\n--- Query took %s seconds ---\n" % (exec_time))
