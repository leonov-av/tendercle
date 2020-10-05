import functions_host_cards
import functions_remote_probes
import time


min_time_between_probing_ports_on_the_same_host = 30
min_time_between_doing_tasks = 10
min_time_between_updating_status_of_the_port = 12*60*60

def check_can_make_probe_of_host(card, card_id, port_id):
    # Checking that we haven't probed recently
    can_make_probe_of_host = True
    time_left_since_last_probe = -1
    if 'last_probe_time' in card:
        time_left_since_last_probe = int(time.time()) - card['last_probe_time']
        if time_left_since_last_probe < min_time_between_probing_ports_on_the_same_host:
            can_make_probe_of_host = False  # Need to wait to be tender with the host
    if not can_make_probe_of_host:
        print("Skipping " + str(card_id) + " " + str(port_id) + \
              " - Need to wait " + str(min_time_between_probing_ports_on_the_same_host - time_left_since_last_probe) + \
              "s to be tender with the host (new proposed)")
    return can_make_probe_of_host

def check_can_update_port_status(card, card_id, port_id):
    # Checking that we haven't probed recently
    can_make_probe_of_host = True
    time_left_since_last_probe = -1
    if 'last_time_telnet_probe' in card['ports'][port_id]:
        time_left_since_last_probe = int(time.time()) - card['ports'][port_id]['last_time_telnet_probe']
        if time_left_since_last_probe < min_time_between_updating_status_of_the_port:
            can_make_probe_of_host = False  # Need to wait to be tender with the host
    if not can_make_probe_of_host:
        print("Skipping " + str(card_id) + " " + str(port_id) + \
              " - Need to wait " + str(min_time_between_updating_status_of_the_port - time_left_since_last_probe) + \
              "s to be tender with the host (updating existing)")
    return can_make_probe_of_host


def get_next_task_to_do():
    # Processing new proposed ports
    # Iterating through all the host cards
    for card_id in functions_host_cards.get_host_card_ids():
        # Getting the card
        card = functions_host_cards.get_host_card(card_id)
        port_ids = list(card['ports'])
        port_ids.sort()
        for port_id in port_ids:
            if card['ports'][port_id]['status'] == 'proposed':
                if check_can_make_probe_of_host(card, card_id, port_id):
                    return({'action':'make_telnet_probe', 'card_id':card_id, 'port_id':port_id})

    # Updating status for existing ports
    # Iterating through all the host cards
    for card_id in functions_host_cards.get_host_card_ids():
        # Getting the card
        card = functions_host_cards.get_host_card(card_id)
        port_ids = list(card['ports'])
        port_ids.sort()
        for port_id in port_ids:
            if card['ports'][port_id]['status'] == 'open' or card['ports'][port_id]['status'] == 'closed':
                if check_can_update_port_status(card, card_id, port_id):
                    if check_can_make_probe_of_host(card, card_id, port_id):
                        return ({'action': 'make_telnet_probe', 'card_id': card_id, 'port_id': port_id})

    return({'action':'idle'})


def process_task(task):
    print("Processing task " + str(task))
    if task['action'] == 'make_telnet_probe':
        card_id = task['card_id']
        port_id = task['port_id']
        card = functions_host_cards.get_host_card(card_id)
        target = {'host': card_id, 'port': card['ports'][port_id]['port']}
        telnet_probe = functions_remote_probes.get_telnet_probe(target)
        probe_time = int(time.time())
        card['ports'][port_id]['status'] = telnet_probe['port_status']
        if not 'n_times_seen_open' in card['ports'][port_id]:
            card['ports'][port_id]['n_times_seen_open'] = 0
        if not 'n_times_seen_closed' in card['ports'][port_id]:
            card['ports'][port_id]['n_times_seen_closed'] = 0
        if telnet_probe['port_status'] == "open":
            card['ports'][port_id]['last_time_seen_open'] = probe_time
            card['ports'][port_id]['n_times_seen_open'] += 1
        if telnet_probe['port_status'] == "closed":
            card['ports'][port_id]['last_time_seen_closed'] = probe_time
            card['ports'][port_id]['n_times_seen_closed'] += 1
        card['ports'][port_id]['last_time_telnet_probe'] = probe_time
        card['ports'][port_id]['last_telnet_probe'] = telnet_probe
        card['last_probe_time'] = probe_time
        functions_host_cards.save_host_card(card_id, card)

def task_processing_cycle():
    while True:
        task = get_next_task_to_do()
        process_task(task)
        print("Waiting " + str(min_time_between_doing_tasks) + "s...")
        time.sleep(min_time_between_doing_tasks)