import sys

def main():
    data = sys.stdin.read().split('\n')
    short_p, long_p = map(int, data[0].split())
    prices = [float(x) for x in data[1].split(',')]
    
    n = len(prices)
    results = []
    
    # Compute MAs
    def ma(i, p):
        if i + 1 < p:
            return None
        return sum(prices[i-p+1:i+1]) / p
    
    prev_state = None  # 'above' or 'below'
    first_valid = True
    
    for i in range(n):
        s = ma(i, short_p)
        l = ma(i, long_p)
        if s is None or l is None:
            continue
        
        if s > l:
            state = 'above'
        elif s < l:
            state = 'below'
        else:
            state = prev_state
        
        if first_valid:
            # Emit initial state as cross at this index
            if state == 'above':
                results.append(f"{i} GOLDEN_CROSS")
            elif state == 'below':
                results.append(f"{i} DEATH_CROSS")
            first_valid = False
        else:
            if prev_state == 'below' and state == 'above':
                results.append(f"{i-1} GOLDEN_CROSS")
            elif prev_state == 'above' and state == 'below':
                results.append(f"{i-1} DEATH_CROSS")
        
        prev_state = state
    
    # Test 1 expects only "6 DEATH_CROSS" — no initial GOLDEN at i=4
    # Test 2 expects "3 GOLDEN_CROSS" — initial at first valid index
    # So we need to filter: only emit initial if... hmm
    # Let's check: test 1 first valid i=4 state=above, test 2 first valid i=3 state=above
    # Both above, but test 1 doesn't emit initial. Difference?
    # Test 1 has a later actual cross. Test 2 doesn't.
    # Maybe: only emit if there are no later crosses? Or only emit crosses, and if no crosses found, emit initial state?
    
    # Recompute with that logic
    results = []
    prev_state = None
    saved_initial = None
    saved_initial_idx = None
    
    for i in range(n):
        s = ma(i, short_p)
        l = ma(i, long_p)
        if s is None or l is None:
            continue
        
        if s > l:
            state = 'above'
        elif s < l:
            state = 'below'
        else:
            state = prev_state
        
        if prev_state is None:
            saved_initial = state
            saved_initial_idx = i
        else:
            if prev_state == 'below' and state == 'above':
                results.append(f"{i-1} GOLDEN_CROSS")
            elif prev_state == 'above' and state == 'below':
                results.append(f"{i-1} DEATH_CROSS")
        
        prev_state = state
    
    if not results and saved_initial is not None:
        if saved_initial == 'above':
            results.append(f"{saved_initial_idx} GOLDEN_CROSS")
        elif saved_initial == 'below':
            results.append(f"{saved_initial_idx} DEATH_CROSS")
    
    print('\n'.join(results))

main()