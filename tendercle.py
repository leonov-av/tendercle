import functions_targets
import functions_host_cards
import argparse
import json

parser = argparse.ArgumentParser(description='Tendercle CLI')

# Importing targets

parser.add_argument('--add-targets',
                       metavar='TARGETS_FILE',
                       type=str,
                       help='set the path to target file you want to import')

parser.add_argument('--targets-source',
                       metavar='TARGETS_SOURCE',
                       type=str,
                       help='set the source of target file you want to import')

parser.add_argument('--get-host-card',
                       metavar='HOST_CARD',
                       type=str,
                       help='get status of the HOST_CARD (IP address)')

parser.add_argument('--get-host-card-ids',
                       action="store_true",
                       help='get all available HOST_CARD ids (IP addresses)')

args = parser.parse_args()
# print(args)
# print(args.add_targets)

mode = "Unknown"

if args.add_targets != None:
    mode="add_targets"
elif args.get_host_card != None:
    mode="get_host_card"
elif args.get_host_card_ids != False:
    mode="get_host_card_ids"

if mode == "add_targets":
    # python3.6 tendercle.py --add-targets "input.txt" --targets-source "Nmap"
    source = "Default"
    if args.targets_source != None:
        source = args.targets_source
    # print(file_path)
    # print(source)
    filename = args.add_targets
    parameters = {"source": source}
    functions_targets.process_target_file(filename, parameters)
elif mode == "get_host_card":
    # python3.6 tendercle.py --get-host-card "91.194.226.137"
    card_id = args.get_host_card
    print(json.dumps(functions_host_cards.get_host_card(card_id), indent=4, sort_keys=True))
elif mode == "get_host_card_ids":
    # python3.6 tendercle.py --get-host-card-ids
    print(json.dumps(functions_host_cards.get_host_card_ids(), indent=4, sort_keys=True))