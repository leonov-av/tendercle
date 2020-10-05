import functions_host_cards


def get_targets_from_input_file(filename):
    f = open(filename,"r")
    target_file_content = f.read()
    f.close()
    targets = list()
    for line in target_file_content.split("\n"):
        target = dict()
        target['host'] = line.split("\t")[0].lower()
        target['type'] = line.split("\t")[1].lower()
        target['port'] = line.split("\t")[2].lower()
        targets.append(target)
    return targets


def process_target_file(filename, parameters):
    targets = get_targets_from_input_file(filename)
    for target in targets:
        host = target['host']
        card_id = host
        port = target['port']
        type = target['type']
        port_id = port + "/" + type
        source = parameters['source']
        if not functions_host_cards.check_host_card_exists(host):
            functions_host_cards.create_new_host_card(host)
        card = functions_host_cards.get_host_card(card_id)
        card, status = functions_host_cards.add_proposed_port_to_card_dict(card, port_id, port, type, source)
        print(str(target) + " - " + status)
        functions_host_cards.save_host_card(host, card)
