# OpenSSH Log Analysis: Threat Hunting & Incident Reconstruction

## Objective
To systematically analyze a raw OpenSSH server log file to identify, track, and document brute-force attack attempts, reconstruct the incident timeline, and understand the attacker's footprint using command-line interface (CLI) tools.

## Skills Demonstrated
* **Log Parsing & Filtering:** Using native Linux CLI tools to extract meaningful data from raw logs.
* **Threat Hunting & Pattern Recognition:** Identifying automated attack signatures and dictionary attack behaviors.
* **Incident Timeline Reconstruction:** Tracing an attacker's actions from initial reconnaissance to attack execution.

## Log Source & Tools Used
* **Log Source:** [Loghub - OpenSSH_2k.log](https://github.com/logpai/loghub/blob/master/OpenSSH/OpenSSH_2k.log)
* **Environment / Tools:** Linux CLI (`grep`, `cut`, `sort`, `uniq`, `comm`)

---

## Analysis & Investigation Process

### Step 1: Identify Key Fields
Before diving into the anomalies, I established the baseline parameters of the log file:
* **Timeline:** Dec 10 06:55:46 to Dec 10 11:04:45
* **Target Asset Hostname:** `LabSZ` 
* **Targeted Service/Process:** `sshd` (OpenSSH Daemon)

### Step 2: Categorize the Security Events
As I scanned the file at a surface level, I started seeing two distinct patterns indicating an automated attack tool:
1. Failed logins for existing system accounts.
2. Failed logins for non-existing system accounts.

First, I saved all the failed authentication attempts into a master file (`failed_login.log`). Then, I used `grep` to filter and save these two patterns into separate files: `invalid_user.log` and `incorrect_pass.log`.

![Invalid User Logs](/images/inv_user.png)

> **Note:** I added the `-v` argument with `grep` to filter out all the failed attempts that didn't contain the word 'user' to easily isolate existing account failures.

![Separated Files](/images/sepfile.png)

### Step 3: Identify Source IP Addresses
After that, I used CLI tools like `cut`, `uniq`, and `sort` to extract the IP addresses and the number of attempts they made on the host.

I wanted to narrow down the specific IP addresses and their frequency of attacks.
> **Note:** The `-c` argument in `uniq` made counting the repetitive IPs easy.

* **Invalid User IP extraction:**
![Source IPs - Invalid Users](/images/ipsrc_user.png)

* **Incorrect Password IP extraction:**
![Source IPs - Incorrect Passwords](/images/ipsrc_pass.png)

### Step 4: Brute-Force Identification (Anomaly Detection)
Now that I had the list of IPs, I decided to look into the count (how many times those IPs were on the list).

First, I decided to look into the `ipsrc_incorrectpass.log` file to see if there were any brute-force attempts on a particular system account.

![IP List - Passwords](/images/iplist_pass.png)

For this analysis, I decided to ignore other IPs and only focus on `183.62.140.253`, which seems to have made 253 failed attempts. By looking at the sheer volume of attempts (253), we can tell that it was a brute-force attack. Furthermore, I decided to look into which account it was trying to brute-force:

![Brute Force Attempt - Root](/images/bruteattempt_root.png)

From the screenshot above, we can confirm the following:
1. `183.62.140.253` attempted a brute-force attack, as we can see a lot of authentication attempts in less than 1 second.
2. `183.62.140.253` specifically targeted the username `root`.

I tried to run `cat OpenSSH_2k.log | grep "183.62.140.253" | grep -i -v "fail"` to see if the brute-force was successful, but found out that the brute-force attempt failed.

Now, it's time to look through the `ipsrc_invaliduser.log`.

![IP List - Users](/images/iplist_user.png)

I decided to only focus on `5.188.10.180` for this analysis. It seems this IP made 18 unsuccessful attempts on incorrect usernames.

![Brute Force Attempt - Invalid Users](/images/bruteattempt.png)

We can see this person tried to attempt logging in with usernames like `admin`, `0`, and `1234`. These usernames don't exist on the main system.

### Step 5: Common IP Identification
As we already have the IP list for both invalid user attempts and invalid password attempts, I decided to check if there are any common IPs that appear on both lists.

![Common IPs](/images/comm.png)

We got to see the familiar IP `183.62.140.253`. So let's check which other accounts that IP attempted to brute-force.

![Extended Common IPs](/images/extcomm.png)

We can see that it also attempted a bunch of other usernames too, showing a wider dictionary attack before focusing on the `root` account.

---

## Mitigation & Recommendations
Based on the threat behaviors identified in this log analysis, the following SSH hardening measures are recommended:

1. **Implement automated IP blocking:** Use a tool like **Fail2Ban** or **CrowdSec** to monitor logs in real-time and automatically block IPs at the firewall level after a set number of failed login attempts (e.g., 5 attempts).
2. **Disable Root SSH Login:** Modify `/etc/ssh/sshd_config` to set `PermitRootLogin no`. This eliminates the attacker's highest-value target. Administrators should log in as standard users and elevate privileges using `sudo`.
3. **Enforce Key-Based Authentication:** Disable password authentication entirely (`PasswordAuthentication no`) and require cryptographic SSH keys for access.
