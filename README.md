# ScienceStr
Nostr bot that answers scientific questions by accessing decentralized repositories of available research papers and constructs and answer with the help of large language models.

## How 
Combining [nostr](https://nostr.net) with [standard template construct](https://github.com/nexus-stc/stc) which hosts vast amount of academic research and other content on ipfs.

## How to run
### Manually
```
git clone https://github.com/aljazceru/sciencestr
cd sciencestr

# install dependencies
pip install requirements-api.txt
pip install requirements-bot.txt

# configure cybrex to use openai 
cybrex - write-config -l openai --force
export OPENAI_API_KEY="<insert your key>"
docker run -d --name ipfs_host -v ./ipfs/staging/:/export -v .ipfs/data:/data/ipfs -p 4001:4001 -p 4001:4001/udp -p 127.0.0.1:8080:8080 -p 127.0.0.1:5001:5001 ipfs/kubo:latest
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
python science-bot.py
python api.py

```
### Docker-compose
(to be fixed)
```
git clone https://github.com/aljazceru/sciencestr
cd sciencestr
docker-compose up 
```

## Demo
![image](./screenshot2.jpg)
![image](./screenshot3.jpg)
