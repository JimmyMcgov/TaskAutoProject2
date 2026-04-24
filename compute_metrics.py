import csv
import os
import sys

def calculate_metrics(parsed_file, node_id=1):
    #Dictionaries used to track requests for RTT/Matching
    #key is (id, seq)
    requests = {}
    
    #accumulators
    stats = {
            'req_sent': 0, 'req_recieved': 0,
            'rep_sent': 0, 'rep_recieved': 0,
            'bytes_req_sent': 0, 'bytes_req_recv': 0,
            'payload_req_sent': 0, 'payload_req_recv': 0,
            'total_rtt': 0, 'total_hops': 0, 'matched_pairs': 0
    }

    host_ip = None

    HEADER_SIZE = 42 #ethernet(14) + IP(20) + ICMP(8)
    try:
        with open(parsed_file, mode="r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if host_ip is None:
                    host_ip = row['src']
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
                    elif dest == host_ip:
                        stats['req_recieved'] += 1
                    #store timestamp for RTT calculation
                    requests[(p_id, p_seq)] = t

                elif p_type == 'reply':
                    if src == host_ip:
                        stats['rep_sent'] += 1
                    elif dest == host_ip:
                        stats['rep_recieved'] += 1
                        stats['bytes_req_recv'] += b
                        stats['payload_req_recv'] += payload

                    #match reply with original request
                    if(p_id, p_seq) in requests:
                        req_t = requests[(p_id, p_seq)]
                        rtt = t - req_t

                        stats['total_rtt'] += rtt
                        stats['matched_pairs'] += 1

                        #hop count calculation using standard ttl baselines
                        #linux, mac, IoT
                        if ttl <= 64: 
                            stats['total_hops'] += (64 - ttl)
                        #Windows
                        elif ttl <= 128: 
                            stats['total_hops'] += (128 - ttl)
                        #network devices
                        else: 
                            stats['total_hops'] += (255 - ttl)

        #Derived averages
        avg_rtt_ms = (stats['total_rtt'] * 1000) / stats['matched_pairs'] if stats['matched_pairs'] > 0 else 0
        avg_delay_us = (stats['total_rtt'] * 1000000) / stats['matched_pairs'] if stats['matched_pairs'] > 0 else 0
        avg_hops = stats['total_hops'] / stats['matched_pairs'] if stats['matched_pairs'] > 0 else 0

        #Throughput/Goodput (sum of request bytes / sum of RTT)
        sum_rtt = stats['total_rtt']
        thru = ((stats['bytes_req_sent'] / 1024) / sum_rtt) if sum_rtt > 0 else 0
        good = ((stats['payload_req_sent'] / 1024) / sum_rtt) if sum_rtt > 0 else 0

        #mapping to output format
        output_rows = [
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

        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, 'project_2_results.csv')

        fileExists = os.path.exists('project_2_results.csv')
        with open(file_path, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not fileExists:
                writer.writerow(['Node', 'Category', 'Metric', 'Value'])
            writer.writerows(output_rows)

    except Exception as e:
        print(f'Error processing file: {e}')

if __name__ == "__main__":
    calculate_metrics(sys.argv[1])
