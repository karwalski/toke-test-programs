import json
import sys

def calculate_cost():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    resources = json.loads(input_data)
    
    # Cost table for AWS resources (monthly pricing in USD)
    cost_table = {
        'ec2_t3_medium': {
            'us-east-1': 33.80,
            'us-west-2': 33.80,
            'eu-west-1': 37.18
        },
        'rds_t3_small': {
            'us-east-1': 29.20,
            'us-west-2': 29.20,
            'eu-west-1': 32.12
        },
        'ec2_t3_small': {
            'us-east-1': 16.90,
            'us-west-2': 16.90,
            'eu-west-1': 18.59
        },
        'ec2_t3_large': {
            'us-east-1': 67.60,
            'us-west-2': 67.60,
            'eu-west-1': 74.36
        }
    }
    
    total_cost = 0.0
    output_lines = []
    
    for resource in resources:
        resource_type = resource['resource_type']
        count = resource['size_or_count']
        region = resource['region']
        
        # Get unit cost for this resource type and region
        unit_cost = cost_table[resource_type][region]
        
        # Calculate total cost for this resource
        resource_cost = unit_cost * count
        total_cost += resource_cost
        
        # Format the output line
        output_lines.append(f"{resource_type} x{count}: ${resource_cost:.2f}/mo")
    
    # Print individual resource costs
    for line in output_lines:
        print(line)
    
    # Print total
    print(f"Total: ${total_cost:.2f}/mo")

if __name__ == "__main__":
    calculate_cost()