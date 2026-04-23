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
    
    # PUT INSIDE CALCULATE
    packetDB = {
        "request": 
        {
            # 1 & 2
            "totalSent": 0,
            "totalRecieved": 0,

            # 5 - 8
            # based on frame/length
            "sentBytes": 0,
            "recievedBytes": 0,
            # based on payload
            "payloadSentBytes": 0,
            "payloadRecievedBytes": 0,

            # 9
            "totalTTL": 0,

            # 10 & 11
            "avgThrough": 0,
            "avgGood": 0,

            # 12 & 13
            "totalDelay": 0,
            "totalHops": 0
        },

        "reply":
        {
            # just these two for replies
            "totalSent": 0,
            "totalRecieved": 0,
        },
    }
    

    nodeCount = 1
    for nodePath in filepaths:
        validPackets = filter.readNCAP(nodePath)

        # creates Node#_filtered.txt
        parser.PLACEHOLD(validPackets)

        # change depending on final path and file extention
        with open("filtered/Node{nodeCount}_filtered.txt") as node:
            someEntry = node.readline()
            computedValues = compute.PLACEHOLD(someEntry)

            # identifier will be implemented 
            # return structure finalized
            for value in computedValues:
                print(value)

        # Seperator between each summary
        nodeCount += 1
        print()

main()

