# Project Name: Analysing Openssh Log file

## Objective
To analyze Openssh log to identify, track, and document bruteforce attempts and understand the attacker's footprint.

## Skills Demonstrated
* Log Parsing & Filtering
* Threat Hunting & Pattern Recognition
* Incident Timeline Reconstruction

## Log Source & Tools Used
* **Log Source:** https://github.com/logpai/loghub/blob/master/OpenSSH/OpenSSH_2k.log
* **Tools:** [e.g., PowerGUI, Timeline Explorer, CyberChef, Linux CLI]

## Analysis & Investigation Process

### step 1: Identify key fields
 Timeline: Dec 10 06:55:46 to Dec 10 11:04:45
 Hostname: LabSZ (The target asset)
 Process/Service: sshd
 
### step 2: Categorize the Security Events
 As I scanned the file in surface level, I started seeing two distinct patterns indicating 
 an automated attack tool:
 1. Failed logins for existing system accounts.
 2. Failed logins for non existing system accounts.
 
 I used grep to save these two patterns into seperate file.
 *screenshots*
     
### step 3: Identify Source IP addresses
After that I used cli tools like: cut, uniq, sort to extract the IP addresses and Number of attempts they made on the host.

### Step 2: Anomaly Identification
[Describe how you first noticed the issue. Did you filter by a specific Event ID or look for a spike in a chart?]
* *Screenshot of the statistical anomaly or initial query.*

### Step 2: Deep Dive & De-obfuscation
[Explain how you dug into the specific logs. What did you find? If there was encoded text, how did you decode it?]
* *Screenshot of the malicious log entry highlighting the key fields (IPs, processes, commands).*

### Step 3: Timeline Reconstruction
Below is the chronologically ordered sequence of events discovered during the analysis:

| Timestamp (UTC) | Source IP / Process | Event ID / Action | Outcome / Impact |
| :--- | :--- | :--- | :--- |
| YYYY-MM-DD HH:MM:SS | 192.168.1.50 | Evt 4625 / Failed Login | Attacker begins brute force |
| YYYY-MM-DD HH:MM:SS | 192.168.1.50 | Evt 4624 / Successful Login | Account compromised |

## Indicators of Compromise (IoCs)
* **Malicious IPs:** `X.X.X.X`
* **Hashes/Commands:** `[Insert malicious command or file hash found]`
* **Affected Host/User:** `Host-01 / TargetUser`

## Mitigation & Recommendations
1. [Bullet 1: e.g., Implement account lockout policies after 5 failed attempts.]
2. [Bullet 2: e.g., Restrict PowerShell execution policy via GPO and enable script block logging.]

