from query_functions import *

QUERIES = [
    {
        'text': "Get a list of resources accessed by a process",
        'follow_up': 'Enter the process ID (ex. 1234): ',
        'query': get_resources_for_process_id,
        'column_labels': ['Resource name', 'Count']
    },
    {
        'text': "Get a list of processes that accessed a resource",
        'follow_up': 'Enter the resource name (ex. /etc/auditd.rules): ',
        'query': get_process_ids_for_resource,
        'column_labels': ['Process ID', 'Process name']
    },
    {
        'text': "Get count summary",
        'query': get_count_summary,
        'column_labels': ['PROCESS count', 'RESOURCE count', 'USES count']
    },
    {
        'text': "Get a list of possibly corrupted processes given a corrupt process",
        'follow_up': 'Enter the process ID (ex. 1234): ',
        'query': get_possible_corrupted_processes_from_process_id,
        'column_labels': ['Process ID', 'Process name']
    },
    {
        'text': "Get a list of possibly corrupted processes and resources given a corrupt process",
        'follow_up': 'Enter the process ID and type required (ex. 1234 process OR 1234 resource): ',
        'query': get_all_possible_corrupted_processes_resources_from_process_id,
        'column_labels': ['Name', 'Type']
    },
    {
        'text': "Get the list of top resource-utilizing processes",
        'query': get_top_resource_utilizing_processes,
        'column_labels': ['Process ID', 'Process name', 'Count']
    },
    {
        'text': "Get the list of most commonly used resources",
        'query': get_top_used_resources,
        'column_labels': ['Resource name', 'Count']
    },
    {
        'text': "Get the approximate read write ratio of a process",
        'follow_up': 'Enter the process ID (ex. 1234): ',
        'query': get_read_write_ratio_of_process,
        'column_labels': ['Read count', 'Write count', 'Read/write ratio']
    },
    {
        'text': "Get the approximate read write ratio of a program",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',
        'query': get_read_write_ratio_of_program,
        'column_labels': ['Read count', 'Write count', 'Read/write ratio']
    },
    {
        'text': "Get a list of configuration files accessed by a process",
        'follow_up': 'Enter the process ID (ex. 1234): ',
        'query': get_configuration_files_for_process_id,
        'column_labels': ['Configuration resource name', 'Count']
    },
    {
        'text': "Get a list of all process instances for a program name",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',
        'query': get_process_ids_for_program_name,
        'column_labels': ['Process ID', 'Process name']
    },
    {
        'text': "Get a list of processes that accessed a configuration resource",
        'query': get_process_ids_for_config_resources,
        'column_labels': ['Process ID', 'Process name']
    },
    {
        'text': "Get an aggregated list of resources accessed by all instances for a program name",
        'follow_up': 'Enter the program name (ex. /bin/vi): ',        
        'query': get_most_freq_accessed_resources_by_program,
        'column_labels': ['Resource name', 'Count']
    },
    {
        'text': "Get a list of possibly corrupted processes given a corrupt process after a given timestamp",
        'follow_up': 'Enter the process ID and start_time (ex. 1234 1541873682.803): ',
        'query': get_possible_corrupted_processes_from_process_id_after_ts,
        'column_labels': ['Process ID', 'Process name']
    },
    {
        'text': "Get a list of resources accessed by a process between start time and end time",
        'follow_up': 'Enter the process ID, start_time and end_time (space separated) (ex. 1234 1541873682.803 1641873682.803): ',
        'query': get_resources_for_process_id_between_ts,
        'column_labels': ['Resource name', 'Count']
    },
    {
        'text': "Get a list of configuration files accessed by a process between start time and end time",
        'follow_up': 'Enter the process ID, start_time and end_time (space separated) (ex. 1234 1541873682.803 1641873682.803): ',
        'query': get_configuration_files_for_process_id_between_ts,
        'column_labels': ['Configuration resource name', 'Count']
    },
    {
        'text': "Get a list of all process instances for a program name between start time and end time",
        'follow_up': 'Enter the program name, start_time and end_time (space separated) (ex. /bin/vi 1541873682.803 1641873682.803): ',
        'query': get_process_ids_for_program_name_between_ts,
        'column_labels': ['Process ID', 'Process name']
    },
    {
        'text': "Get an aggregated list of resources accessed by all processes of a program name between start time and end time",
        'follow_up': 'Enter the program name, start_time and end_time (space separated) (ex. /bin/vi 1541873682.803 1641873682.803): ',
        'query': get_resources_for_process_name_between_ts,
        'column_labels': ['Resource name', 'Count']
    },
    {
        'text': "Get a list of processes that accessed a resource between start time and end time",
        'follow_up': 'Enter the resource name, start_time and end_time (space separated) (ex. /etc/auditd.rules 1541873682.803 1641873682.803): ',
        'query': get_process_ids_for_resource_between_ts,
        'column_labels': ['Process ID', 'Process name']
    },
    {
        'text': "Get a list of processes that accessed a configuration resource between start time and end time",
        'follow_up': 'Enter the start_time and end_time (space separated) (ex. 1541873682.803 1641873682.803): ',
        'query': get_process_ids_for_config_resources_between_ts,
        'column_labels': ['Process ID', 'Process name']
    },
    {
        'text': "Get the approximate read write ratio of a process between start time and end time",
        'follow_up': 'Enter the process ID, start_time and end_time (space separated) (ex. 1234 1541873682.803 1641873682.803): ',
        'query': get_read_write_ratio_of_process_between_ts,
        'column_labels': ['Read count', 'Write count', 'Read/write ratio']
    }
]
