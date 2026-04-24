
# File reader
def readNCAP(filepath):
    icmp_lines = []

    with open(filepath, "r", errors = "ignore") as file:
        for line in file:
            stripped = line.strip()

            # All summary lines start with a ID; if a line 
            # does not start with a ID or is a blank line, 
            # it will be skipped
            if not stripped or not stripped[0].isdigit():
                continue

            # Drops any summary line that isn't ICMP
            if " ICMP " not in f" {line} ":
                continue

            # Drop destination unreachable ICMP packets
            # This also drops all hexcodes
            if "Destination unreachable" in line:
                continue

            icmp_lines.append(line.rstrip("\n"))

    return icmp_lines

def test():
    pass
    # generate a test file
    # filepath = "Captures/Node1.txt"
    # icmpList = readNCAP(filepath)
    # with open ("testFile.csv", "w") as someFile:
    #     for entry in icmpList:
    #         someFile.writelines(entry + "\n")

    # Use this to view the indicies of
    # strip().split()
    # someLine = "    441 590.404752     192.168.100.1         192.168.100.2         ICMP     74     Echo (ping) request  id=0x0001, seq=91/23296, ttl=128 (reply in 442)"
    # someLine = someLine.strip().split()
    # print(someLine)


# test()
