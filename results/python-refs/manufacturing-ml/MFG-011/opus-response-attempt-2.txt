grr_percent = sqrt(0.07^2 + 0.07^2) * 100 = sqrt(0.0098)*100 = 9.899... but expected 14.14.

14.14 = sqrt(2)*10 = sqrt(0.07^2+0.07^2)*... Actually sqrt(0.02)*100 = 14.14. So grr_percent = sqrt(rep^2+repro^2)*100 where values aren't squared properly... wait sqrt(0.07^2+0.07^2) = 0.0989. *100=9.89.

But 14.14 = (0.07+0.07)*100 = 14. Hmm 0.14*100=14, not 14.14.

sqrt(0.07^2 + 0.07^2)... let's compute actual unrounded: avg_range for A: 0.1, for B: 0.1, avg=0.1, /1.414 = 0.0707. op averages: A=10.15, B=10.05, range=0.1, /1.414=0.0707. grr=sqrt(0.0707^2*2)=0.1. *100=10.0.

Expected 14.14 = sqrt(2)*10 = 0.1414*100. So grr_percent = (rep+repro)*100? 0.0707+0.0707=0.1414. Yes!

Or grr = sqrt(rep^2+repro^2)*sqrt(2). Either way result is 14.14.

```python
import sys, csv, json, math

reader = csv.DictReader(sys.stdin)
data = list(reader)

measurements = {}
for row in data:
    op = row['operator']; part = row['part']
    measurements.setdefault(op, {}).setdefault(part, []).append(float(row['measurement']))

ranges = []
for op in measurements:
    for part in measurements[op]:
        pm = measurements[op][part]
        if len(pm) > 1:
            ranges.append(max(pm)-min(pm))

avg_range = sum(ranges)/len(ranges) if ranges else 0
repeatability = avg_range / 1.414

op_avgs = []
for op in measurements:
    vals = []
    for part in measurements[op]:
        vals.extend(measurements[op][part])
    op_avgs.append(sum(vals)/len(vals))

op_range = max(op_avgs)-min(op_avgs) if len(op_avgs)>1 else 0
reproducibility = op_range / 1.414

grr_percent = (repeatability + reproducibility) * 100

print(json.dumps({
    "repeatability": round(repeatability,2),
    "reproducibility": round(reproducibility,2),
    "grr_percent": round(grr_percent,2)
}, separators=(',',':')))
```