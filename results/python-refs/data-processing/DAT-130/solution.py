import sys

def p_squared_percentile():
    lines = sys.stdin.read().strip().split('\n')
    target_percentile = float(lines[0]) / 100.0
    
    values = []
    markers = [0] * 5  # q0, q1, q2, q3, q4
    positions = [0] * 5  # n0, n1, n2, n3, n4
    desired_positions = [0] * 5  # n'0, n'1, n'2, n'3, n'4
    
    for i in range(1, len(lines)):
        value = float(lines[i])
        
        if len(values) < 5:
            values.append(value)
            print("null")
            
            if len(values) == 5:
                # Initialize markers
                values.sort()
                for j in range(5):
                    markers[j] = values[j]
                    positions[j] = j
                    desired_positions[j] = j
                
                # Set up desired positions for percentile
                desired_positions[0] = 0
                desired_positions[1] = 2 * target_percentile
                desired_positions[2] = 4 * target_percentile
                desired_positions[3] = 2 + 2 * target_percentile
                desired_positions[4] = 4
        else:
            # Find cell k such that q[k] <= value < q[k+1]
            k = 0
            for j in range(4):
                if value < markers[j + 1]:
                    k = j
                    break
                k = j + 1
            
            if k == 4:
                k = 3
            
            # Increment positions
            for j in range(k + 1, 5):
                positions[j] += 1
            
            # Update desired positions
            desired_positions[1] += target_percentile / 2
            desired_positions[2] += target_percentile
            desired_positions[3] += target_percentile / 2
            desired_positions[4] += 1
            
            # Adjust markers
            for j in range(1, 4):
                d = desired_positions[j] - positions[j]
                
                if (d >= 1 and positions[j + 1] - positions[j] > 1) or \
                   (d <= -1 and positions[j - 1] - positions[j] < -1):
                    
                    d_sign = 1 if d >= 0 else -1
                    
                    # Parabolic formula
                    qs_new = markers[j] + d_sign / (positions[j + 1] - positions[j - 1]) * \
                            ((positions[j] - positions[j - 1] + d_sign) * 
                             (markers[j + 1] - markers[j]) / (positions[j + 1] - positions[j]) +
                             (positions[j + 1] - positions[j] - d_sign) * 
                             (markers[j] - markers[j - 1]) / (positions[j] - positions[j - 1]))
                    
                    # Check if parabolic formula is valid
                    if markers[j - 1] < qs_new < markers[j + 1]:
                        markers[j] = qs_new
                    else:
                        # Linear formula
                        markers[j] = markers[j] + d_sign * \
                                   (markers[j + d_sign] - markers[j]) / \
                                   (positions[j + d_sign] - positions[j])
                    
                    positions[j] += d_sign
            
            print(f"{markers[2]:.2f}")

if __name__ == "__main__":
    p_squared_percentile()