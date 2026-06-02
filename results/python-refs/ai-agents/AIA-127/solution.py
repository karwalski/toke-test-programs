import json, sys

def main():
    data = json.loads(sys.stdin.read())
    tasks = data['tasks']
    resources = data['resources']
    # Deterministic order: by duration descending, then id ascending
    order = sorted(tasks, key=lambda t: (-t['duration_ms'], t['id']))
    # Greedy: for each task in order, find earliest start time where all resources available throughout duration
    # Track timeline as list of (time, delta_dict) events
    scheduled = []  # (task_id, start, end, needs)
    def usage_at(t):
        u = {r: 0 for r in resources}
        for tid, s, e, n in scheduled:
            if s <= t < e:
                for r, v in n.items():
                    u[r] = u.get(r, 0) + v
        return u
    def can_fit(start, duration, needs):
        end = start + duration
        # Check at all event points within [start, end)
        critical = {start}
        for tid, s, e, n in scheduled:
            if s < end and e > start:
                if s >= start: critical.add(s)
                if e < end and e > start: critical.add(e)
        for t in critical:
            u = usage_at(t)
            for r, v in needs.items():
                if u.get(r, 0) + v > resources.get(r, 0):
                    return False
        return True
    for task in order:
        needs = task['resource_needs']
        # Check feasibility per-task
        for r, v in needs.items():
            if v > resources.get(r, 0):
                print(json.dumps({'error': 'infeasible'}))
                return
        # Candidate start times: 0 and all end times of scheduled tasks
        candidates = sorted(set([0] + [e for _, _, e, _ in scheduled]))
        chosen = None
        for c in candidates:
            if can_fit(c, task['duration_ms'], needs):
                chosen = c
                break
        if chosen is None:
            chosen = max(e for _, _, e, _ in scheduled) if scheduled else 0
        scheduled.append((task['id'], chosen, chosen + task['duration_ms'], needs))
    # Build output sorted by start then task_id
    scheduled_sorted = sorted(scheduled, key=lambda x: (x[1], x[0]))
    schedule_out = [{'task_id': t[0], 'start_ms': t[1], 'end_ms': t[2]} for t in scheduled_sorted]
    makespan = max((t[2] for t in scheduled), default=0)
    # Utilisation: sum(duration*need) / (capacity*makespan) averaged over resources
    if makespan == 0:
        util = 0.0
    else:
        ratios = []
        for r, cap in resources.items():
            total = sum((t[2]-t[1]) * t[3].get(r, 0) for t in scheduled)
            if cap > 0:
                ratios.append(total / (cap * makespan))
        util = round(sum(ratios)/len(ratios), 2) if ratios else 0.0
    out = {'schedule': schedule_out, 'total_duration_ms': makespan, 'resource_utilisation': util}
    print(json.dumps(out))

main()
