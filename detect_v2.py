from daytime import datetime , timedelta

LOG_FILE = "/var/log/auth.log"
THRESHOLD = 5
WINDOW = timedelta(seconds=60)
events = {}

with open(LOG_FILE) as f:
     for line in f:
        if "password check failed" in line:
            timestamp = datetime.fromisoforamt(line.split()[0])
            user = line.split("(")[-1].strip().rstrip(")")
            events.setdefault(user , []).append(timestamp)


for user , times in events.items():
    alerted = False
    for t in times:
        recent = [x for x in times if t - WINDOW <= X <= t]
        if len(recent) >= THRESHOLD:
            print(f"[ALERT] {user} : {len(recent)} failures within 60s (at {it}")
            alerted = True
            break
       if not alerted:
            print(f"[ok] {user}: {len(times)} total failures, no burst")
