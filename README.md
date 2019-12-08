# Database system for Linux Data Log Analysis


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

#### Download files from this OneDrive folder to your data/ directory
```
https://gtvault-my.sharepoint.com/:f:/g/personal/dbansod3_gatech_edu/Ek_MxbalghtHk4Gr5T7uyGQBT8GZtmYkar29aDmJqYgI0g?e=sreoRS
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

```bash
python main.py 127.0.0.1:7687 neo4j $PASS
```
