import sys
from collections import defaultdict
from datetime import datetime

def main():
    lines = sys.stdin.read().strip().split('\n')
    header = lines[0]
    data_lines = lines[1:]
    
    # Parse data
    user_activities = defaultdict(set)
    cohorts = defaultdict(set)
    
    for line in data_lines:
        user_id, signup_date, activity_date = line.split(',')
        user_id = int(user_id)
        
        # Track which cohort each user belongs to
        cohorts[signup_date].add(user_id)
        
        # Track user activities by month
        user_activities[user_id].add(activity_date)
    
    # Calculate retention rates
    retention_data = {}
    
    for cohort_month, users in cohorts.items():
        retention_data[cohort_month] = {}
        total_users = len(users)
        
        # Find all activity months for this cohort
        all_months = set()
        for user_id in users:
            all_months.update(user_activities[user_id])
        
        # Sort months to determine offsets
        sorted_months = sorted(all_months)
        
        # Calculate retention for each month offset
        for i, month in enumerate(sorted_months):
            if month >= cohort_month:  # Only consider months >= signup month
                active_users = 0
                for user_id in users:
                    if month in user_activities[user_id]:
                        active_users += 1
                
                retention_rate = (active_users / total_users) * 100
                month_offset = i if month == cohort_month else len([m for m in sorted_months if m < month and m >= cohort_month])
                retention_data[cohort_month][month_offset] = retention_rate
    
    # Output results
    # Find max month offset for header
    max_offset = 0
    for cohort_data in retention_data.values():
        if cohort_data:
            max_offset = max(max_offset, max(cohort_data.keys()))
    
    # Print header
    header_parts = ["Cohort"]
    for i in range(max_offset + 1):
        header_parts.append(f"M{i}")
    print("  ".join(f"{part:>6}" if i > 0 else part for i, part in enumerate(header_parts)))
    
    # Print data rows
    for cohort_month in sorted(retention_data.keys()):
        row_parts = [cohort_month]
        for i in range(max_offset + 1):
            if i in retention_data[cohort_month]:
                rate = retention_data[cohort_month][i]
                if rate == 100.0:
                    row_parts.append("100%")
                else:
                    row_parts.append(f"{rate:.0f}%")
            else:
                row_parts.append("")
        
        print("  ".join(f"{part:>6}" if i > 0 else part for i, part in enumerate(row_parts)))

if __name__ == "__main__":
    main()