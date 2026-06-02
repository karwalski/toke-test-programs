import json
import sys
import math

def calculate_distance(lat1, lng1, lat2, lng2):
    # Haversine formula to calculate distance between two points
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def calculate_composite_score(relay, sender_lat, sender_lng, recipient_lat, recipient_lng):
    # Distance from sender to relay
    dist_sender_relay = calculate_distance(sender_lat, sender_lng, relay['lat'], relay['lng'])
    
    # Distance from relay to recipient
    dist_relay_recipient = calculate_distance(relay['lat'], relay['lng'], recipient_lat, recipient_lng)
    
    # Total distance through this relay
    total_distance = dist_sender_relay + dist_relay_recipient
    
    # Direct distance from sender to recipient
    direct_distance = calculate_distance(sender_lat, sender_lng, recipient_lat, recipient_lng)
    
    # Geographic proximity score (higher is better, normalized to 0-100)
    if total_distance > 0:
        proximity_score = max(0, 100 - ((total_distance - direct_distance) / direct_distance) * 100)
    else:
        proximity_score = 100
    
    # Latency score (lower latency is better, normalized to 0-100)
    max_latency = 200  # Assume max reasonable latency
    latency_score = max(0, 100 - (relay['latency_ms'] / max_latency) * 100)
    
    # Capacity score (higher capacity is better)
    capacity_score = relay['capacity_pct']
    
    # Weighted composite score
    composite_score = (proximity_score * 0.4 + latency_score * 0.3 + capacity_score * 0.3)
    
    return int(round(composite_score))

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    sender = json.loads(lines[0])
    recipient = json.loads(lines[1])
    relays = json.loads(lines[2])
    
    # Calculate scores for each relay
    scored_relays = []
    for relay in relays:
        score = calculate_composite_score(relay, sender['lat'], sender['lng'], 
                                        recipient['lat'], recipient['lng'])
        scored_relays.append((relay, score))
    
    # Sort by score (descending)
    scored_relays.sort(key=lambda x: x[1], reverse=True)
    
    # Output ranked relay nodes
    for i, (relay, score) in enumerate(scored_relays, 1):
        print(f"{i}. {relay['id']} (score: {score}) - {relay['region']}, {relay['latency_ms']}ms, {relay['capacity_pct']}% cap")
    
    # Recommended path uses the best relay
    best_relay = scored_relays[0][0]
    print(f"recommended path: sender -> {best_relay['id']} -> recipient")

if __name__ == "__main__":
    main()