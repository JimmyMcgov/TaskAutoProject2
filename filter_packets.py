
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