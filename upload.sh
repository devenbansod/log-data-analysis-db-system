#!/bin/bash

# $1 = User, $2 = password, $3 = raw log file name stored in data/

if [[ "$#" -ne 3 ]]; then
    echo "usage: ./neo4j-load-csv.sh <username> <password> <path_to_raw_log>"
    exit 2
fi

if [[ $(id -u) -ne 0 ]] ; then
    echo "Need to be root"
    exit 1
fi

# Get the parsed logs
echo "** Started cleaning and parsing $3 **"
cd parser/
python main.py "../$3"
cd ..
echo "** Cleaning and Parsing completed **"

# Run the reducer
echo "** Started reduction **"
cd reducer
python main.py "../output/intermediate/forward.csv" "../output/intermediate/backward.csv" "../output/"
cd ..
echo "** Reduction completed **"

# Import the reduced logs

echo "** Starting data ingestion **"

IMPORT_DIR="/var/lib/neo4j/import"
CYPHER_BIN="cypher-shell"
NEO4J_SERVER="127.0.0.1:7687"
USER="$1"
CYPHER_ARGS="-a $NEO4J_SERVER -u $USER -p $2"
FORWARD_PATH="output/forward-reduced.csv"
BACKWARD_PATH="output/backward-reduced.csv"

# Add indexes
CREATE INDEX ON :Person(firstname)

# Add backward reduced logs
cp $FORWARD_PATH "$IMPORT_DIR/forward-reduced.csv"
ADD_FORWARD_EDGES_QUERY="\"
USING PERIODIC COMMIT 500
LOAD CSV FROM 'file:///forward-reduced.csv' as line
MERGE (n1:PROCESS {process_id: line[2], name: line[3]})
MERGE (n2:RESOURCE {name: line[5]})
WITH line,n1,n2
CREATE (n1)-[:USES {ts: line[0], serial: line[1], type: line[4]}]->(n2)
\""
eval "${CYPHER_BIN}" "${CYPHER_ARGS}" "${ADD_FORWARD_EDGES_QUERY}"


# Add backward reduced logs
cp $BACKWARD_PATH "$IMPORT_DIR/backward-reduced.csv"

ADD_BACKWARD_EDGES_QUERY="\"
USING PERIODIC COMMIT 500
LOAD CSV FROM 'file:///backward-reduced.csv' as line
MERGE (n1:PROCESS {process_id: line[2], name: line[3]})
MERGE (n2:RESOURCE {name: line[5]})
WITH line,n1,n2
CREATE (n1)-[:USES {ts: line[0], serial: line[1], type: line[4]}]->(n2)
\""
eval "${CYPHER_BIN}" "${CYPHER_ARGS}" "${ADD_BACKWARD_EDGES_QUERY}"


echo "** Data ingestion completed **"