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
        # Parser creates the filtered directory then
        # dumps output of each filtered node into 
        # filtered/Node#_filtered.csv
        parsedFile = parser.process_node_file(icmpList, nodeCount)

        # Reads a node#_filtered.csv to perform calculations
        # Creates the computed directory then
        # dumps output of each calculation into 
        # computed/project_2_Node#_results.csv
        compute.calculate_metrics(parsedFile, nodeCount)
        nodeCount += 1
main()
