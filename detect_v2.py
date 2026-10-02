LOG_FILE = "/var/log/auth.log"
THRESHOLD = 5

Failures = {}

with open(LOG_FILE) as f:
     for line in f:
        if "password check failed" in line:
            user = line.split("(")[-1].strip().rstrip(")")
            Failures[user] = Failures.get(user , 0) + 1


for user , count in Failures.items():
    if count >= THRESHOLD:
        	print(f"[ALERT] {user}:{count} failed attempts")
    else:
         print(f"[ok] {user}: {count} failed attempts")
