import sys
import time
from decimal import Decimal
from neo4j import GraphDatabase
from cli import queries
from tabulate import tabulate

def print_commands():
    """
    Print the input commands table with task descriptions
    """
    print "* Select a query option OR Enter 0 to exit *\n"
    labels = ['input', 'command']
    commands = [[ind + 1, x['text']] for ind, x in enumerate(queries)]

    print(tabulate(commands, headers=labels, tablefmt='psql'))

def pretty_print(result, column_labels):
    """
    Pretty print the results in a tabular manner
    """
    print(tabulate(result, headers=column_labels, tablefmt='psql'))

def main():
    if (len(sys.argv) <= 3):
        print('*** ERROR ***' + '\nUsage: python main.py <server_host>:<port> <username> <password>')
        return

    driver = GraphDatabase.driver("bolt://" + sys.argv[1], auth=(sys.argv[2], sys.argv[3]))
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
            command_index = input_command - 1
            if 'follow_up' in queries[command_index]:
                raw_inputs = raw_input(queries[command_index]['follow_up'])

            start_time = time.time()
            result = session.read_transaction(queries[command_index]['query'], raw_inputs)
            exec_time = time.time() - start_time

            pretty_print(result, queries[command_index]['column_labels'])
            print("\n--- Query took %s seconds ---\n" % ('{0:.3f}'.format(exec_time)))

if __name__ == '__main__':
    main()
