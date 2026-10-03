# Failed Login Detector

A Python tool that scans Linux authentication logs for failed sudo
password attempts and flags bursts that look like automated brute force.

## Lab Setup
- Ubuntu 26.04 ARM64 VM (VMware Fusion, Apple Silicon)
- rsyslog → `/var/log/auth.log`
- Python 3 standard library only

## What It Detects
Repeated failed password checks per user. v3 alerts only when 5+ failures
happen within 60 seconds, which separates a typo from a script hammering
the password prompt.

## How It Evolved
- **detect.py**: counts every failed password check. Simple, but no context.
- **detect_v2.py**: groups failures per user and alerts above a threshold.
  Weakness: 9 failures over 3 hours looks the same as 9 in 10 seconds.
- **detect_v3.py**: parses timestamps, uses a 60-second sliding window,
  and adds a cooldown so one attack produces one alert, not four.

## How to Run
    python3 detect_v3.py

No sudo required: `auth.log` is readable by the `adm` group, and the
default Ubuntu user is a member.

## Sample Output
    [ALERT] sudarshan1 : 5 failures within 60s (at 2026-10-01 22:25:31-04:00)
    [ALERT] sudarshan1 : 5 failures within 60s (at 2026-10-02 22:38:43-04:00)

## Testing
Generated failures two ways on my own VM:
1. Manual: wrong password typed at `sudo` prompts
2. Automated: a bash loop piping a wrong password into `sudo -S`
   (8 attempts in ~14 seconds)

## Limitations
- Reports the count at the moment the threshold is crossed (5), not the
  full attack size (8)
- A frustrated human can trigger it: my own manual typos did
- Only matches `password check failed`; SSH and other sources not covered
- Batch only: rereads the full log each run, no live monitoring

## What I Learned
- Log access is a permissions question: group membership decides what
  tools (and attackers) can read
- Logs can mix timezones and contain null bytes; `grep` called my log
  "binary" while Python read it fine, so cross-check with multiple tools
- PAM's ~2s delay after each failure is a real defense: it caps brute
  force at ~25 attempts/minute
- More alerts ≠ better detection. Duplicates cause alert fatigue.
