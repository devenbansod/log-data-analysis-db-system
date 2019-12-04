# Database system for Linux Data Log Analysis

## Initial setup

### Set password variable
```bash
export PASS=<neo4j-password>
```

### Check initial size of graph.db
```bash
du -h /var/lib/neo4j/data/databases/graph.db/
```

### Upload initial data
```bash
sudo bash upload.sh neo4j $PASS data/1.log
```

## Online Data ingestion

### Start watching being-watched.log
```bash
when-changed being-watched.log "sudo -E bash watcher.sh"
```

### Add 10 lines from data/2.log to being-watched.log

The process should run partially but halt since new lines is less than specified number.

### Add remaining lines from data/2.log to being-watched.log

The process should run completely.

## CLI usage

```bash
python main.py 127.0.0.1:7687 neo4j $PASS
```