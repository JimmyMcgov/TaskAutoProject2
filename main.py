import filter_packets as filter
import packet_parser as parser
import compute_metrics as compute

def main():
    filepaths = [
        "Captures/Node1.txt",
        "Captures/Node2.txt",
        "Captures/Node3.txt",
        "Captures/Node4.txt"
        ]
    
    nodeCount = 1
    for nodePath in filepaths:
        # Read valid icmp entries in a 
        # node. Drops unreachables
        icmpList = filter.readNCAP(nodePath)

        # Passes valid icmp list into parser
        # Parser then creates a node#_filtered.csv file
        # for compute
        parser.process_node_file(icmpList, nodeCount)

        # Reads a node#_filtered.csv and outputs contents
        # in a single aggregate file
        compute.calculate_metrics()

        # Seperator between each summary
        nodeCount += 1
        print()

main()

