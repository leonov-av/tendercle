import json
import os
import time


def check_host_card_exists(host):
    if os.path.exists("data/hosts/" + host):
        return True
    else:
        return False


def create_new_host_card(host):
    f = open("data/hosts/" + host, "w")
    f.write(json.dumps({'created':int(time.time())}, indent=4, sort_keys=True))
    f.close()


def get_host_card_ids():
    files = os.listdir("data/hosts/")
    files.remove(".gitkeep")
    return(files)


def get_host_card(card_id):
    f = open("data/hosts/" + card_id, "r")
    card = json.loads(f.read())
    f.close()
    return(card)


def save_host_card(host,card):
    f = open("data/hosts/" + host, "w")
    f.write(json.dumps(card, indent=4, sort_keys=True))
    f.close()


def add_proposed_port_to_card_dict(card, port_id, port, type, source):
    if not 'ports' in card:
        card['ports'] = dict()
    if port_id not in card['ports']:
        card['ports'][port_id] = {'port': port,
                                  'type': type,
                                  'status': 'proposed',
                                  'proposed_source': source,
                                  'proposed_time': int(time.time())}
        status = "added new port"
    else:
        status = "already exists, ignored"
    return(card, status)