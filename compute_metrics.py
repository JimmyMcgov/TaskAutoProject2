import csv
# import os
from pathlib import Path
import sys

def calculate_metrics(parsed_file, node_id=1):
    #Dictionaries used to track requests for RTT/Matching
    #key is (id, seq)
    requests = {}
    recieved_requests = {}
    
    #accumulators
    stats = {
            'req_sent': 0, 'req_recieved': 0,
            'rep_sent': 0, 'rep_recieved': 0,
            'bytes_req_sent': 0, 'bytes_req_recv': 0,
            'payload_req_sent': 0, 'payload_req_recv': 0,
            'total_rtt': 0, 'total_hops': 0, 'matched_pairs': 0,
            'total_reply_delay': 0, 'delay_pairs': 0
            
    }

    host_ip = None

    HEADER_SIZE = 42 #ethernet(14) + IP(20) + ICMP(8)
    try:
        with open(parsed_file, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:

                # we are assuming first request is 
                # from the host
                if host_ip is None:
                    host_ip = row['src']

                # packet info
                src = row['src']
                dest = row['dst']
                t = float(row['time'])
                b = int(row['bytes'])
                p_type = row['type'].strip()
                p_id = row['id']
                p_seq = row['seq']
                ttl = int(row['ttl'])
                payload = b - HEADER_SIZE

                if p_type == 'request':
                    if src == host_ip:
                        stats['req_sent'] += 1
                        stats['bytes_req_sent'] += b
                        stats['payload_req_sent'] += payload

                        # store timestamp for RTT calculation
                        requests[(p_id, p_seq)] = t

                    elif dest == host_ip:
                        stats['req_recieved'] += 1
                        stats['bytes_req_recv'] += b
                        stats['payload_req_recv'] += payload

                        recieved_requests[(p_id, p_seq)] = t


                elif p_type == 'reply':
                    
                    if src == host_ip:
                        stats['rep_sent'] += 1

                        if (p_id, p_seq) in recieved_requests:
                            req_t = recieved_requests.pop((p_id, p_seq))
                            delay = t - req_t
                            stats['total_reply_delay'] += delay
                            stats['delay_pairs'] += 1

                    elif dest == host_ip:
                        stats['rep_recieved'] += 1
                        
                        # match reply with original request
                        if(p_id, p_seq) in requests:
                            req_t = requests[(p_id, p_seq)]
                            rtt = t - req_t

                            stats['total_rtt'] += rtt
                            stats['matched_pairs'] += 1

                        # hop count calculation using standard ttl baselines
                        # linux, mac, IoT
                        if ttl <= 64: 
                            stats['total_hops'] += (64 - ttl) + 1
                        # Windows
                        elif ttl <= 128: 
                            stats['total_hops'] += (128 - ttl) + 1
                        # network devices
                        else: 
                            stats['total_hops'] += (255 - ttl) + 1

        # Derived averages
        avg_rtt_ms = (stats['total_rtt'] * 1000) / stats['matched_pairs'] if stats['matched_pairs'] > 0 else 0

        avg_delay_us = (stats['total_reply_delay'] * 1000000) / stats['delay_pairs'] if stats['delay_pairs'] > 0 else 0
        avg_hops = stats['total_hops'] / stats['matched_pairs'] if stats['matched_pairs'] > 0 else 0

        # print(f"{node_id}")
        # print(f"Total RTT: {stats['total_rtt']}")
        # print(f"Matched Pairs: {stats['matched_pairs']}")
        # print(f"Total hops: {stats['total_rtt']}")
        # print()

        # Throughput/Goodput (sum of request bytes / sum of RTT)
        sum_rtt = stats['total_rtt']
        thru = ((stats['bytes_req_sent'] / 1000) / sum_rtt) if sum_rtt > 0 else 0
        good = ((stats['payload_req_sent'] / 1000) / sum_rtt) if sum_rtt > 0 else 0

        # mapping to output format
        output_rows = [
            ['Node', 'Category', 'Metric', 'Value'],
            [node_id, 'Size', 'Requests Sent', stats['req_sent']],
            [node_id, 'Size', 'Requests Recieved', stats['req_recieved']],
            [node_id, 'Size', 'Replies Sent', stats['rep_sent']],
            [node_id, 'Size', 'Replies Recived', stats['rep_recieved']],
            [node_id, 'Size', 'Request Bytes Sent', stats['bytes_req_sent']],
            [node_id, 'Size', 'Request Bytes Recieved', stats['bytes_req_recv']],
            [node_id, 'Size', 'Request Data Sent', stats['payload_req_sent']],
            [node_id, 'Size', 'Request Data Recieved', stats['payload_req_recv']],
            [node_id, 'Time', 'Average RTT (ms)', round(avg_rtt_ms, 2)],
            [node_id, 'Time', 'Request Throughput (kB/sec)', round(thru, 1)],
            [node_id, 'Time', 'Request Goodput (kB/sec)', round(good, 1)],
            [node_id, 'Time', 'Average Reply Delay (us)', round(avg_delay_us, 2)],
            [node_id, 'Distance', 'Average Request Hop Count', round(avg_hops, 2)]
        ]

        file_path = f"computed/project_2_Node{node_id}_results.csv"
        Path("computed/").mkdir(exist_ok = True)
        Path(file_path).touch()

        # script_dir = os.path.dirname(__file__)
        # file_path = os.path.join(script_dir, 'project_2_results.csv')
        # fileExists = os.path.exists(f'computed/project_2_Node{node_id}_results.csv')


        # script_dir = os.path.dirname(__file__)
        # file_path = os.path.join(script_dir, 'project_2_results.csv')
        # fileExists = os.path.exists('project_2_results.csv')

        with open(file_path, mode = 'a', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            # if not fileExists:
            # if not Path(file_path).is_file():
            #     writer.writerow(['Node', 'Category', 'Metric', 'Value'])
            
            writer.writerows(output_rows)

    except Exception as e:
        print(f'Error processing file: {e}')

if __name__ == "__main__":
    calculate_metrics(sys.argv[1])
