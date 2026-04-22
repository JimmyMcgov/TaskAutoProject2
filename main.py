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
    
    for nodePath in filepaths:
        validPackets = filter.readNCAP(nodePath)

        # packetDB = final mashmap of packet parser
        packetDB = parser.PLACEHOLD(validPackets)

        computedList = compute.PLACEHOLD(packetDB)
        
        print(f"PLACEHOLD METRIC: {computedList[0]}")
        print(f"PLACEHOLD METRIC: {computedList[1]}")
        print(f"PLACEHOLD METRIC: {computedList[2]}")
        print(f"PLACEHOLD METRIC: {computedList[3]}")
        print(f"PLACEHOLD METRIC: {computedList[4]}")
        print(f"PLACEHOLD METRIC: {computedList[5]}")
        # ...

        # Seperator between each summary
        print()




main()

