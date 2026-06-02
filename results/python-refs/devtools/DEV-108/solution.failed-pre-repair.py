import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    slo_target_pct = input_data["slo_target_pct"]
    measurement_period_days = input_data["measurement_period_days"]
    incidents = input_data["incidents"]
    
    # Calculate total minutes in measurement period
    total_minutes = measurement_period_days * 24 * 60
    
    # Calculate error budget (allowed downtime)
    error_budget_pct = 100 - slo_target_pct
    total_error_budget_minutes = total_minutes * (error_budget_pct / 100)
    
    # Calculate consumed error budget
    consumed_minutes = sum(incident["duration_minutes"] for incident in incidents)
    
    # Calculate remaining error budget
    remaining_minutes = total_error_budget_minutes - consumed_minutes
    
    # Calculate percentages
    consumed_pct = (consumed_minutes / total_error_budget_minutes) * 100
    remaining_pct = (remaining_minutes / total_error_budget_minutes) * 100
    
    # Calculate burn rate
    # Burn rate is how fast we're consuming error budget compared to ideal rate
    # Ideal rate would be consuming error budget evenly over the period
    ideal_burn_rate = 1.0
    actual_burn_rate = consumed_pct / 100 * measurement_period_days / measurement_period_days
    if total_error_budget_minutes > 0:
        burn_rate = consumed_minutes / total_error_budget_minutes * measurement_period_days
    else:
        burn_rate = 0
    
    # Output formatting
    print(f"SLO: {slo_target_pct}%")
    print(f"Measurement period: {measurement_period_days} days")
    print(f"Total error budget: {total_error_budget_minutes} minutes")
    print(f"Consumed: {consumed_minutes} minutes ({consumed_pct:.1f}%)")
    print(f"Remaining: {remaining_minutes} minutes ({remaining_pct:.1f}%)")
    print(f"Burn rate: {burn_rate:.2f}x")

if __name__ == "__main__":
    main()