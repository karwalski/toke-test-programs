import sys
import json
import csv
from collections import defaultdict
from datetime import datetime

def parse_timestamp(ts_str):
    return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))

def detect_port_scan(connections):
    anomalies = []
    by_src = defaultdict(list)
    for conn in connections:
        by_src[conn['src_ip']].append(conn)
    
    for src_ip, conns in by_src.items():
        conns_sorted = sorted(conns, key=lambda c: parse_timestamp(c['timestamp']))
        n = len(conns_sorted)
        for i in range(n):
            ports = set()
            t_start = parse_timestamp(conns_sorted[i]['timestamp'])
            for j in range(i, n):
                t_j = parse_timestamp(conns_sorted[j]['timestamp'])
                if (t_j - t_start).total_seconds() <= 60:
                    ports.add(conns_sorted[j]['dst_port'])
                else:
                    break
            if len(ports) >= 2:
                anomalies.append({
                    'type': 'port_scan',
                    'severity': 'high',
                    'src_ip': src_ip,
                    'evidence': f'Scanned {len(ports)} ports within 60s',
                    'timestamp': conns_sorted[i]['timestamp']
                })
                break
    return anomalies

def detect_data_exfiltration(connections):
    anomalies = []
    for conn in connections:
        if conn['bytes'] > 100 * 1024 * 1024:
            anomalies.append({
                'type': 'data_exfiltration',
                'severity': 'high',
                'src_ip': conn['src_ip'],
                'evidence': f'Single transfer of {conn["bytes"]} bytes',
                'timestamp': conn['timestamp']
            })
    return anomalies

def detect_beaconing(connections):
    src_dst_connections = defaultdict(list)
    for conn in connections:
        key = (conn['src_ip'], conn['dst_ip'])
        src_dst_connections[key].append(conn)
    
    anomalies = []
    for (src_ip, dst_ip), conns in src_dst_connections.items():
        if len(conns) >= 3:
            timestamps = sorted([parse_timestamp(c['timestamp']) for c in conns])
            intervals = [(timestamps[i] - timestamps[i-1]).total_seconds() for i in range(1, len(timestamps))]
            if len(intervals) >= 2:
                avg = sum(intervals) / len(intervals)
                if avg > 0 and all(abs(iv - avg) < 5 for iv in intervals):
                    anomalies.append({
                        'type': 'beaconing',
                        'severity': 'medium',
                        'src_ip': src_ip,
                        'evidence': f'Regular connections to {dst_ip} every ~{avg:.0f}s',
                        'timestamp': conns[0]['timestamp']
                    })
    return anomalies

def main():
    connections = []
    reader = csv.reader(sys.stdin)
    for row in reader:
        if len(row) < 6:
            continue
        try:
            connections.append({
                'timestamp': row[0],
                'src_ip': row[1],
                'dst_ip': row[2],
                'dst_port': int(row[3]),
                'bytes': int(row[4]),
                'protocol': row[5]
            })
        except ValueError:
            continue
    
    anomalies = []
    anomalies.extend(detect_port_scan(connections))
    anomalies.extend(detect_data_exfiltration(connections))
    anomalies.extend(detect_beaconing(connections))
    
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