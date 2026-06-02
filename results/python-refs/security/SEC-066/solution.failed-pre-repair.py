import sys
import json
import csv
from collections import defaultdict
from datetime import datetime

def parse_timestamp(ts_str):
    return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))

def detect_port_scan(connections):
    # Group by src_ip and dst_ip combination
    src_dst_ports = defaultdict(set)
    src_dst_times = defaultdict(list)
    
    for conn in connections:
        key = (conn['src_ip'], conn['dst_ip'])
        src_dst_ports[key].add(conn['dst_port'])
        src_dst_times[key].append(conn['timestamp'])
    
    anomalies = []
    for (src_ip, dst_ip), ports in src_dst_ports.items():
        # Port scan: same source trying multiple ports on same destination
        if len(ports) >= 5:  # Threshold for port scan
            timestamps = src_dst_times[(src_ip, dst_ip)]
            anomalies.append({
                'type': 'port_scan',
                'severity': 'high',
                'src_ip': src_ip,
                'evidence': f'Scanned {len(ports)} ports on {dst_ip}',
                'timestamp': min(timestamps)
            })
    
    return anomalies

def detect_data_exfiltration(connections):
    # Group by src_ip
    src_bytes = defaultdict(int)
    src_times = defaultdict(list)
    
    for conn in connections:
        src_bytes[conn['src_ip']] += conn['bytes']
        src_times[conn['src_ip']].append(conn['timestamp'])
    
    anomalies = []
    for src_ip, total_bytes in src_bytes.items():
        # Data exfiltration: large amount of data from single source
        if total_bytes > 1000000:  # 1MB threshold
            anomalies.append({
                'type': 'data_exfiltration',
                'severity': 'high',
                'src_ip': src_ip,
                'evidence': f'Transferred {total_bytes} bytes',
                'timestamp': min(src_times[src_ip])
            })
    
    return anomalies

def detect_beaconing(connections):
    # Group by src_ip and dst_ip combination
    src_dst_connections = defaultdict(list)
    
    for conn in connections:
        key = (conn['src_ip'], conn['dst_ip'])
        src_dst_connections[key].append(conn)
    
    anomalies = []
    for (src_ip, dst_ip), conns in src_dst_connections.items():
        # Beaconing: regular connections with similar intervals
        if len(conns) >= 5:  # Need multiple connections to detect pattern
            timestamps = [parse_timestamp(c['timestamp']) for c in conns]
            timestamps.sort()
            
            intervals = []
            for i in range(1, len(timestamps)):
                interval = (timestamps[i] - timestamps[i-1]).total_seconds()
                intervals.append(interval)
            
            # Check for regular intervals (simple heuristic)
            if len(intervals) >= 4:
                avg_interval = sum(intervals) / len(intervals)
                if avg_interval > 0 and all(abs(interval - avg_interval) / avg_interval < 0.3 for interval in intervals):
                    anomalies.append({
                        'type': 'beaconing',
                        'severity': 'medium',
                        'src_ip': src_ip,
                        'evidence': f'Regular connections to {dst_ip} every ~{avg_interval:.0f}s',
                        'timestamp': conns[0]['timestamp']
                    })
    
    return anomalies

def main():
    connections = []
    reader = csv.DictReader(sys.stdin, fieldnames=['timestamp', 'src_ip', 'dst_ip', 'dst_port', 'bytes', 'protocol'])
    
    for row in reader:
        connections.append({
            'timestamp': row['timestamp'],
            'src_ip': row['src_ip'],
            'dst_ip': row['dst_ip'],
            'dst_port': int(row['dst_port']),
            'bytes': int(row['bytes']),
            'protocol': row['protocol']
        })
    
    anomalies = []
    anomalies.extend(detect_port_scan(connections))
    anomalies.extend(detect_data_exfiltration(connections))
    anomalies.extend(detect_beaconing(connections))
    
    # Sort anomalies by timestamp
    anomalies.sort(key=lambda x: x['timestamp'])
    
    summary = {
        'total_connections': len(connections),
        'total_anomalies': len(anomalies),
        'anomaly_types': {
            'port_scan': len([a for a in anomalies if a['type'] == 'port_scan']),
            'data_exfiltration': len([a for a in anomalies if a['type'] == 'data_exfiltration']),
            'beaconing': len([a for a in anomalies if a['type'] == 'beaconing'])
        }
    }
    
    result = {
        'anomalies': anomalies,
        'summary': summary
    }
    
    print(json.dumps(result))

if __name__ == '__main__':
    main()