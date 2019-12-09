import re
from constants import *

def _check_if_path_is_config_file(filepath):
    return filepath in CONFIG_FILES or re.match(r"^/etc", filepath)

def get_all_possible_corrupted_processes_resources_from_process_id(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_id = int(inputs[0])
    element = inputs[1]

    ret = set()
    process_limit = 50
    resource_limit = 50
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) -[:USES *0..2]- (ELEMENT) "
        "WHERE toInteger(PROC.process_id) = $process_id "
        "RETURN DISTINCT ELEMENT.process_id AS PROCESS_ID, ELEMENT.name AS NAME "
        "ORDER BY PROCESS_ID DESC",
        process_id=process_id
    ):
        if record['PROCESS_ID'] != None and element == 'process':
            ret.add((str(record['PROCESS_ID']), str(record['NAME']), 'PROCESS'))
            process_limit -= 1
        elif element == 'resource':
            ret.add((str(record['NAME'][:40]), 'RESOURCE'))
            resource_limit -= 1

        if (process_limit <= 0 or resource_limit <= 0):
            break

    return ret

def get_count_summary(tx, raw_inputs):
    ret = list()
    for record in tx.run(
        "MATCH (PROC: PROCESS) RETURN COUNT(PROC.process_id) AS COUNT"
    ):
        ret.append(record['COUNT'])

    for record in tx.run(
        "MATCH (RES: RESOURCE) RETURN COUNT(RES.name) AS COUNT"
    ):
        ret.append(record['COUNT'])

    for record in tx.run(
        "MATCH (PROCESS) -[USE: USES]-> (RESOURCE) RETURN COUNT(USE) AS COUNT"
    ):
        ret.append(record['COUNT'])

    return [ret]

def get_possible_corrupted_processes_from_process_id(tx, raw_inputs):
    process_id = int(raw_inputs)

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) <-[USE2 :USES]- (PROC2: PROCESS) "
        "WHERE toInteger(PROC.process_id) = $process_id AND PROC2.process_id <> PROC.process_id "
        "AND (USE2.ts > USE.ts OR (USE2.ts = USE.ts AND USE2.serial > USE.serial)) "
        "RETURN DISTINCT PROC2.process_id as PROCESS_ID, PROC2.name as PROCESS_NAME",
        process_id=process_id
    ):
        ret.add((str(record['PROCESS_ID']), str(record['PROCESS_NAME'])))

    return ret

def get_possible_corrupted_processes_from_process_id_after_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_id = int(inputs[0])
    start_time = float(inputs[1])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) <-[USE2 :USES]- (PROC2: PROCESS) "
        "WHERE toInteger(PROC.process_id) = $process_id AND PROC2.process_id <> PROC.process_id "
        "AND (USE2.ts > USE.ts OR (USE2.ts = USE.ts AND USE2.serial > USE.serial)) "
        "AND toFloat(USE.ts) > $start_time "
        "RETURN DISTINCT PROC2.process_id as PROCESS_ID, PROC2.name as PROCESS_NAME",
        process_id=process_id,
        start_time=start_time
    ):
        ret.add((str(record['PROCESS_ID']), str(record['PROCESS_NAME'])))

    return ret

def get_resources_for_process_id(tx, raw_inputs):
    process_id = int(raw_inputs)

    ret = list()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE toInteger(PROC.process_id) = $process_id "
        "RETURN DISTINCT RES.name AS RESOURCE_NAME, COUNT(*) AS COUNT",
        process_id=process_id
    ):
        ret.append([str(record['RESOURCE_NAME']), str(record['COUNT'])])

    return ret

def get_resources_for_process_id_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_id = int(inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = list()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE toInteger(PROC.process_id) = $process_id "
        " AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end"
        " RETURN DISTINCT RES.name AS RESOURCE_NAME, COUNT(*) AS COUNT",
        process_id = process_id,
        ts_start = start_time,
        ts_end = end_time
    ):
        ret.append([str(record['RESOURCE_NAME']), str(record['COUNT'])])

    return ret

def get_configuration_files_for_process_id(tx, raw_inputs):
    process_id = float(raw_inputs)

    ret = list()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE toInteger(PROC.process_id) = $process_id"
        " RETURN DISTINCT RES.name AS RESOURCE_NAME, COUNT(*) AS COUNT",
        process_id = process_id
    ):
        if _check_if_path_is_config_file(record['RESOURCE_NAME']):
            ret.append([str(record['RESOURCE_NAME']), str(record['COUNT'])])

    return ret

def get_configuration_files_for_process_id_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_id = int(inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = list()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE toInteger(PROC.process_id) = $process_id "
        " AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end"
        " RETURN RES.name AS RESOURCE_NAME, COUNT(*) AS COUNT",
        process_id = process_id,
        ts_start = start_time,
        ts_end = end_time
    ):
        if _check_if_path_is_config_file(record['RESOURCE_NAME']):
            ret.append([str(record['RESOURCE_NAME']), str(record['COUNT'])])

    return ret

def get_process_ids_for_program_name(tx, raw_inputs):
    process_name = raw_inputs

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE PROC.name = $process_name"
        " RETURN PROC.process_id AS PROCESS_ID, PROC.name AS PROCESS_NAME",
        process_name=process_name
    ):
        ret.add((str(record['PROCESS_ID']), str(record['PROCESS_NAME'])))

    return ret

def get_process_ids_for_program_name_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_name = int(inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE)"
        " WHERE PROC.name = $process_name"
        " AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end"
        " RETURN PROC.process_id AS PROCESS_ID, PROC.name AS PROCESS_NAME",
        process_name=process_name,
        ts_start=start_time,
        ts_end=end_time
    ):
        ret.add((str(record['PROCESS_ID']), str(record['PROCESS_NAME'])))

    return ret


def get_resources_for_process_name(tx, raw_inputs):
    process_name = raw_inputs

    ret = list()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        " WHERE PROC.name = $process_name"
        " RETURN DISTINCT RES.name AS RESOURCE_NAME, COUNT(*) AS COUNT",
        process_name=process_name
    ):
        ret.append([str(record['RESOURCE_NAME']), str(record['COUNT'])])

    return ret

def get_resources_for_process_name_between_ts(tx, raw_inputs):
    inputs = raw_inputs
    process_name = (inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = list()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        " WHERE PROC.name = $process_name "
        " AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end"
        " RETURN DISTINCT RES.name AS RESOURCE_NAME, COUNT(*) AS COUNT",
        process_name=process_name,
        ts_start=start_time,
        ts_end=end_time
    ):
        ret.add([str(record['RESOURCE_NAME']), str(record['COUNT'])])

    return ret

def get_process_ids_for_resource(tx, raw_inputs):
    resource_name = raw_inputs

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE RES.name = $resource_name "
        "RETURN PROC.process_id AS PROCESS_ID, PROC.name AS PROCESS_NAME",
        resource_name=resource_name
    ):
        ret.add((str(record['PROCESS_ID']), str(record['PROCESS_NAME'])))

    return ret

def get_process_ids_for_resource_between_ts(tx, raw_inputs):
    inputs = raw_inputs
    resource_name = (inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE RES.name = $resource_name "
        "AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end "
        "RETURN PROC.process_id AS PROCESS_ID, PROC.name AS PROCESS_NAME",
        resource_name=resource_name,
        ts_start=start_time,
        ts_end=end_time
    ):
        ret.add((str(record['PROCESS_ID']), str(record['PROCESS_NAME'])))

    return ret

def get_process_ids_for_config_resources(tx, raw_inputs):
    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE RES.name IN {resource_names} "
        "RETURN PROC.process_id AS PROCESS_ID, PROC.name AS PROCESS_NAME",
        resource_names=CONFIG_FILES
    ):
        ret.add((str(record['PROCESS_ID']), str(record['PROCESS_NAME'])))

    return ret

def get_process_ids_for_config_resources_between_ts(tx, raw_inputs):
    inputs = raw_inputs
    start_time = float(inputs[0])
    end_time = float(inputs[1])

    ret = set()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE RES.name IN {resource_names}"
        "AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end "
        "RETURN PROC.process_id AS PROCESS_ID, PROC.name as PROCESS_NAME",
        resource_names=CONFIG_FILES,
        start_time=ts_start,
        end_time=ts_end
    ):
        ret.add(str(record['PROCESS_ID']), str(record['PROCESS_NAME']))

    return ret

def get_most_freq_accessed_resources_by_program(tx, raw_inputs):
    process_name = raw_inputs

    ret = list()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.name = $process_name "
        "RETURN RES.name AS RESOURCE_NAME, COUNT(*) AS COUNT "
        "ORDER BY COUNT DESC",
        process_name=process_name
    ):
        ret.append((str(record['RESOURCE_NAME']), str(record['COUNT'])))

    return ret

def get_read_write_ratio_of_process(tx, raw_inputs):
    process_id = int(raw_inputs)

    read_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE toInteger(PROC.process_id) = $process_id AND USE.type IN {call_types} "
        "RETURN COUNT(*) AS COUNT ",
        process_id=process_id,
        call_types=READ_SYSCALLS
    ):
        read_count = int(record['COUNT'])
        break

    write_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE toInteger(PROC.process_id) = $process_id AND USE.type IN {call_types} "
        "RETURN COUNT(*) AS COUNT ",
        process_id=process_id,
        call_types=WRITE_SYSCALLS
    ):
        write_count = int(record['COUNT'])
        break

    ret = [read_count, write_count]
    if (write_count > 0):
        ret.append(float(read_count) / float(write_count))
    else:
        ret.append('NA')

    return [ret]

def get_read_write_ratio_of_process_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_id = int(inputs[0])
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    read_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE toInteger(PROC.process_id) = $process_id AND USE.type IN {call_types} "
        "AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end "
        "RETURN COUNT(*) AS COUNT ",
        process_id=process_id,
        call_types=READ_SYSCALLS,
        ts_start=start_time,
        ts_end=end_time
    ):
        read_count = int(record['COUNT'])
        break

    write_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE toInteger(PROC.process_id) = $process_id AND USE.type IN {call_types} "
        "AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end "
        "RETURN COUNT(*) AS COUNT ",
        process_id=process_id,
        call_types=WRITE_SYSCALLS,
        ts_start=start_time,
        ts_end=end_time
    ):
        write_count = int(record['COUNT'])
        break

    ret = [read_count, write_count]
    if (write_count > 0):
        ret.append(float(read_count) / float(write_count))
    else:
        ret.append('NA')

    return [ret]

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
        read_count = int(record['COUNT'])
        break

    write_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.name = $program_name AND USE.type IN {call_types}"
        "RETURN COUNT(*) AS COUNT ",
        program_name=process_name,
        call_types=WRITE_SYSCALLS
    ):
        write_count = int(record['COUNT'])
        break

    ret = [read_count, write_count]
    if (write_count > 0):
        ret.append(float(read_count) / float(write_count))
    else:
        ret.append('NA')

    return [ret]

def get_read_write_ratio_of_program_between_ts(tx, raw_inputs):
    inputs = raw_inputs.split(' ')
    process_name = inputs[0]
    start_time = float(inputs[1])
    end_time = float(inputs[2])

    read_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.name = $program_name AND USE.type IN {call_types} "
        "AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end "
        "RETURN COUNT(*) AS COUNT ",
        program_name=process_name,
        call_types=READ_SYSCALLS,
        ts_start=start_time,
        ts_end=end_time
    ):
        read_count = int(record['COUNT'])
        break

    write_count = 0
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "WHERE PROC.name = $program_name AND USE.type IN {call_types} "
        "AND toFloat(USE.ts) >= $ts_start AND toFloat(USE.ts) <= $ts_end "
        "RETURN COUNT(*) AS COUNT ",
        program_name=process_name,
        call_types=WRITE_SYSCALLS,
        ts_start=start_time,
        ts_end=end_time
    ):
        write_count = int(record['COUNT'])
        break

    ret = [read_count, write_count]
    if (write_count > 0):
        ret.append(float(read_count) / float(write_count))
    else:
        ret.append('NA')

    return [ret]

def get_top_resource_utilizing_processes(tx, raw_inputs):
    ret = list()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "RETURN PROC.process_id AS PROCESS_ID, PROC.name AS PROCESS_NAME, count(*) as COUNT "
        "ORDER BY COUNT DESC LIMIT 25"
    ):
        ret.append((str(record['PROCESS_ID']), str(record['PROCESS_NAME']), str(record['COUNT'])))

    return ret

def get_top_used_resources(tx, raw_inputs):
    ret = list()
    for record in tx.run(
        "MATCH (PROC :PROCESS) -[USE :USES]-> (RES :RESOURCE) "
        "RETURN RES.name AS RESOURCE_NAME, count(*) as COUNT "
        "ORDER BY COUNT DESC LIMIT 25"
    ):
        ret.append((str(record['RESOURCE_NAME']), str(record['COUNT'])))

    return ret
