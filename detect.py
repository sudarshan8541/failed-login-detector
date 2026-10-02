LOG_FILE = "/var/log/auth.log"

count = 0 

with open(LOG_FILE) as f :
    for line in f:
        if "password check failed" in line:
                 print(line.strip())
                 count += 1



print(f"\nTotal failed password checks: {count}")



