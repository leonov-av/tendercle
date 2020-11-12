# Tendercle
Persistent and tender IT inventory tool
![Tendercle logo](https://raw.githubusercontent.com/leonov-av/tendercle/master/images/tendercle.png)

### Input File format for targets ###
ip + \t + tcp/udp  + \t + port 

E.g.:

```81.177.6.213	tcp	3780```

### How to Run ### 

#### From sources ####

* tendercle.py - for cli (import targets, get statistics, etc.)

```
$ python3.6 tendercle.py -h
usage: tendercle.py [-h] [--add-targets TARGETS_FILE]
                    [--targets-source TARGETS_SOURCE]
                    [--get-host-card HOST_CARD] [--get-host-card-ids]

Tendercle CLI

optional arguments:
  -h, --help            show this help message and exit
  --add-targets TARGETS_FILE
                        set the path to target file you want to import
  --targets-source TARGETS_SOURCE
                        set the source of target file you want to import
  --get-host-card HOST_CARD
                        get status of the HOST_CARD (IP address)
  --get-host-card-ids   get all available HOST_CARD ids (IP addresses)
```

#### From Docker #### 

```
docker build -t tendercle .
docker run -it --rm tendercle -h
```

Examples:

```
python3.6 tendercle.py --add-targets "input.txt" --targets-source "Nmap"
python3.6 tendercle.py --get-host-card "81.177.6.213"
python3.6 tendercle.py --get-host-card-ids
```

* tendercle_proc.py - script that tenderly validates ports in cycle. Just keep it running.
