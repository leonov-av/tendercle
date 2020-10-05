import telnetlib
import json
import hashlib

def get_telnet_probe(target):
    """
    This function will make active testing of remote service using telnet
    :param target: {'host': <host_ip>, 'port': <service_port>}
    :return: {"messages": messages, "response": response, "result_id": hash from other params}
    """
    tn = telnetlib.Telnet()
    messages = list()
    response = ""
    try:
        tn.open(target['host'], port=target['port'], timeout=20)
        messages.append("Telnet Connection Established")
        port_status = "open"
        try:
            tn.write("123".encode('ascii') + b"\n")
            response = tn.read_all().decode('ascii')
            messages.append("Telnet Interactive Output Collected")
        except:
            messages.append("Telnet Non-Interactive Service")
    except:
        messages.append("Can't Establish Telnet Connection")
        port_status = "closed"
    tn.close()
    result = {"messages": messages, "response": response, "port_status": port_status}
    result['result_id'] = hashlib.sha1(json.dumps(result, sort_keys=True).encode('ascii')).hexdigest()
    return result
