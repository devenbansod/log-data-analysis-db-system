# Database system for Linux Data Log Analysis

A database system for the efficient storage and querying of Linux audit logs.

_Read more about the purpose of this system and its design [here](https://docs.google.com/presentation/d/1ZWzANJ9xi8FZeIqD7K0QuEHuY6InUSNafHj6FY9x_mo/edit?usp=sharing)._ 

By [Deven Bansod](https://github.com/devenbansod), [Raghav Bhat](https://github.com/rbhat35), and [Jitin George](https://github.com/jitin17).

## Installation (Debian/Ubuntu)

This assumes `python2.7` is installed.

### Install Libraries and dependency

```bash
sudo apt-get install python-audit auditd
pip install -r requirements.txt
```

### Install Neo4j server

This requires Java to be installed. See [this](https://neo4j.com/docs/operations-manual/current/installation/linux/debian/#debian-ubuntu-prerequisites) for installing Java 8 on newer versions of Ubuntu. 

```bash
wget -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.org/repo stable/' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
sudo apt install neo4j
```

### Setup Neo4j server

```bash
sudo neo4j start
```

* Open http://localhost:7474
* Setup and remember server password (initial username and password is `neo4j`)

### Install when-changed to watch the incoming logs

```bash
git clone https://github.com/joh/when-changed
cd when-changed
sudo python setup.py install
```

## Demo

### Download Data

#### Download some sample Linux Audit Log files from this OneDrive folder to your data/ directory
```
https://gtvault-my.sharepoint.com/:f:/g/personal/dbansod3_gatech_edu/Ek_MxbalghtHk4Gr5T7uyGQBFCGxjQtsfjyu_EYdkosWnA?e=bTUJbf
```

### Initial setup

#### Set password variable
```bash
export PASS=<neo4j-password>
```

#### Check initial size of graph.db
```bash
du -h /var/lib/neo4j/data/databases/graph.db/
```

#### Upload initial data
```bash
sudo bash upload.sh neo4j $PASS data/1.log
```

Note: Running this automatically creates the Indexes that are used while querying.

#### Check size of graph.db
```bash
du -h /var/lib/neo4j/data/databases/graph.db/
```

### Online Data ingestion

#### Start watching being-watched.log
```bash
when-changed being-watched.log "sudo -E bash watcher.sh"
```

#### Add 10 lines from data/2.log to being-watched.log

The process should run partially but halt since new lines is less than specified number.

#### Add remaining lines from data/2.log to being-watched.log

The process should run completely.

#### Check size of graph.db
```bash
du -h /var/lib/neo4j/data/databases/graph.db/
```

### CLI usage

Now that the demo data has been ingested by the system, we can run queries on the data. The CLI is designed to be interactive.

```bash
python main.py 127.0.0.1:7687 neo4j $PASS
```

## Code References

### Code Components Slightly Modified By Us:
`reducer/` folder in [1]:
 * Folder contains the Causality Preserving Reduction (CPR) algorithm we use to reduce shrink the logs
 * We modified the original source code to make it compatible with our log-ingestion pipeline

### Code Components Substantially Modified By Us:
`parser/` folder in [1]:
 * Folder contains the log parser, which takes in raw system call logs, strips out irrelevant fields (e.g. register values), and deletes irrelevant system-calls (e.g. execve).
 * We modified the set of parameters that is returned and made the code compatible with our pipeline 

### Code Components Written By Us:
`cli/` and `root` directories, which include:
 * Script to ingest data into Neo4j (`upload.sh`)
 * Neo4j Queries - ~20 Queries that are relevant to system call log analysis (`cli/query_functions.py`)
 * Command-line interface (`cli/*`)
 * Git diff-based system to ingest only new logs into the database (`watcher.sh`)

[1]: https://github.com/rbhat35/log-reducer
