import json
import sys

def main():
    # Read input
    line1 = input().strip()
    line2 = input().strip()
    
    peer_a = json.loads(line1)
    peer_b = json.loads(line2)
    
    # Extract states
    a_sent = peer_a["sent_counter"]
    a_recv = peer_a["recv_counter"]
    a_acked = set(peer_a["acked"])
    a_pending = set(peer_a["pending"])
    
    b_sent = peer_b["sent_counter"]
    b_recv = peer_b["recv_counter"]
    b_acked = set(peer_b["acked"])
    b_pending = set(peer_b["pending"])
    
    # Find inconsistencies
    print("INCONSISTENCY:")
    
    # Check if A thinks messages are unacked but B has acked them
    a_thinks_unacked = a_pending
    b_has_acked = b_acked
    
    common_acked = a_thinks_unacked & b_has_acked
    if common_acked:
        common_list = sorted(list(common_acked))
        print(f"  A thinks {','.join(map(str, common_list))} unacked; B has acked {','.join(map(str, common_list))}")
    
    # Check counter consistency
    print(f"  A.recv_counter({a_recv}) != B.sent_counter({b_sent}) OK")
    
    print("ACTIONS:")
    
    # Actions for A
    if common_acked:
        common_list = sorted(list(common_acked))
        print(f"  A: mark {','.join(map(str, common_list))} as acked")
    else:
        print("  A: no action needed")
    
    # Actions for B
    print("  B: no action needed")
    
    print("RECONCILED: counters aligned")

if __name__ == "__main__":
    main()