# author: bella andrini
# project 2, group 7
# NSSA 220

def parse_packet(line):
    """
    convert one icmp summary line into a structured dictionary
    returns None if the line is invalid or not a request/reply
    """

    parts = line.split()

    # if len(parts) < 7:
    #     return None

    # fields
    time = float(parts[1])
    src = parts[2]
    dst = parts[3]
    length = int(parts[5])

    info = " ".join(parts[6:])

    # determine packet type
    if "request" in info:
        pkt_type = "request"
    elif "reply" in info:
        pkt_type = "reply"
    else:
        return None

    # icmp id (hex → int)
    id_part = info.split("id=")[1].split(",")[0]
    icmp_id = int(id_part, 16)

    # sequence number
    seq_part = info.split("seq=")[1].split("/")[0]
    seq = int(seq_part)

    # TTL
    ttl_part = info.split("ttl=")[1].split()[0]
    ttl = int(ttl_part)

    return {
        "time": time,
        "src": src,
        "dst": dst,
        "type": pkt_type,
        "bytes": length,
        "id": icmp_id,
        "seq": seq,
        "ttl": ttl
    }


def parse_packets(icmp_summary):
    """
    takes a list of icmp summary strings (from file reader)
    returns a list of structured packet dictionaries
    """

    parsed_packets = []

    for line in icmp_summary:
        packet = parse_packet(line)

        if packet is not None:
            parsed_packets.append(packet)

    return parsed_packets
