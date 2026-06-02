import json
import sys

def main():
    input_data = json.loads(sys.stdin.read().strip())
    
    slo_target_pct = input_data["slo_target_pct"]
    measurement_period_days = input_data["measurement_period_days"]
    incidents = input_data["incidents"]
    
    total_minutes = measurement_period_days * 24 * 60
    error_budget_pct = 100 - slo_target_pct
    total_error_budget_minutes = round(total_minutes * (error_budget_pct / 100), 1)
    
    consumed_minutes = 0.0
    for incident in incidents:
        if "duration_minutes" in incident:
            consumed_minutes += incident["duration_minutes"]
        elif "start_minutes_duration" in incident:
            consumed_minutes += incident["start_minutes_duration"]
        elif "end_minutes_duration" in incident:
            consumed_minutes += incident["end_minutes_duration"]
    consumed_minutes = round(float(consumed_minutes), 1)
    
    remaining_minutes = round(total_error_budget_minutes - consumed_minutes, 1)
    
    if total_error_budget_minutes > 0:
        consumed_pct = (consumed_minutes / total_error_budget_minutes) * 100
        remaining_pct = (remaining_minutes / total_error_budget_minutes) * 100
    else:
        consumed_pct = 0.0
        remaining_pct = 0.0
    
    if measurement_period_days > 0:
        burn_rate = consumed_pct / 100 / (measurement_period_days / 30)
    else:
        burn_rate = 0
    
    print(f"SLO: {slo_target_pct}%")
    print(f"Measurement period: {measurement_period_days} days")
    print(f"Total error budget: {total_error_budget_minutes} minutes")
    print(f"Consumed: {consumed_minutes} minutes ({consumed_pct:.1f}%)")
    print(f"Remaining: {remaining_minutes} minutes ({remaining_pct:.1f}%)")
    print(f"Burn rate: {burn_rate:.2f}x")

if __name__ == "__main__":
    main()