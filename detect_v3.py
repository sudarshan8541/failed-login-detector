from datetime import datetime , timedelta

LOG_FILE = "/var/log/auth.log"
THRESHOLD = 5
WINDOW = timedelta(seconds=60)
events = {}

with open(LOG_FILE) as f:
     for line in f:
        if "password check failed" in line:
            timestamp = datetime.fromisoformat(line.split()[0])
            user = line.split("(")[-1].strip().rstrip(")")
            events.setdefault(user , []).append(timestamp)


for user , times in events.items():
    alerted = False
    last_alert = None
    for t in times:
        recent = [x for x in times if t - WINDOW <= x <= t]
        if len(recent) >= THRESHOLD and(last_alert is None or t - last_alert > WINDOW):
            print(f"[ALERT] {user} : {len(recent)} failures within 60s (at {t}")
            alerted = True
            last_alert = t
    if not alerted:
            print(f"[ok] {user}: {len(times)} total failures, no burst")

