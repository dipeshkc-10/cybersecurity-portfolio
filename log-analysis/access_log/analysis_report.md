# Log Analysis: Log Analysis of Apache Access Log (access.log)

## Objective

To analyze a sample Apache access log file and identify, track, and document suspicious activities while understanding the attacker's behavior and footprint.

## Skills Demonstrated

* Log Parsing & Filtering (`grep`, `cut`, `awk`, `sort`, `uniq`)
* Threat Hunting & Pattern Recognition
* Incident Timeline Reconstruction
* Web Server Log Analysis
* Basic Incident Investigation
* Knowledge of MITRE ATT&CK TTPs:

  * T1595 - Active Scanning
  * T1110 - Brute Force
  * T1190 - Exploit Public-Facing Application

## Log Source & Tools Used

* **Log Source:** Apache access log provided by TryHackMe.
* **Tools Used:** Linux CLI (`grep`, `cut`, `awk`, `sort`, `uniq`), Excel, CyberChef.

---

## Analysis & Investigation Process

### Identifying High-Frequency IP Addresses

Firstly, I extracted all source IP addresses from the log file and counted the number of occurrences for each IP.

**Command Used**

```bash
cut -d ' ' -f 1 access.log | uniq -c | sort -n -r
```

*(Image: /images/anamol_idi.png)*

The output showed that **43.133.134.155** appeared significantly more often than any other IP address in the log file. This immediately made it a strong candidate for further investigation.

---

### Isolating Suspicious Activity

To focus only on this IP's activity, I created a separate file containing all requests originating from 43.133.134.155.

**Command Used**

```bash
grep "43.133.134.155" access.log > target.log
```

---

### Examining Requested URLs

I extracted all requested URLs to understand what resources the attacker was attempting to access.

**Command Used**

```bash
cut -d '"' -f2 target.log
```

*(Image: /images/urls.png)*

Many of the requested URLs appeared random and unrelated to the website's normal content. The requests resembled attempts to discover hidden directories, administrative panels, backup files, or other sensitive resources.

This behavior is commonly observed during the reconnaissance phase of an attack where automated tools attempt to enumerate accessible endpoints.

---

### Reviewing HTTP Status Codes

Next, I checked the HTTP status codes returned by the server.

**Command Used**

```bash
awk '{ print $9 }' target.log
```

*(Image: /images/st_code.png)*

Every request returned a **401 (Unauthorized)** status code.

This indicates that the attacker was unable to access any of the targeted resources because authentication was required. Although the requests were unsuccessful, they still reveal malicious intent and provide evidence of reconnaissance activity.

---

### User-Agent Analysis

I then extracted the User-Agent field from each request.

**Command Used**

```bash
cut -d '"' -f6 target.log
```

*(Image: /images/usr_agnt.png)*

The requests contained multiple browser User-Agent strings including Chrome, Firefox, and Safari.

A legitimate user typically browses using a single browser during a short session. The rapid switching between different User-Agent strings suggests the use of automated scanning tools configured to rotate User-Agents in an attempt to evade simple detection mechanisms.

---

### Timeline Analysis

I reviewed the timestamps associated with the requests.

*(Image: /images/tmstmp.png)*

The IP address generated multiple requests within extremely short time intervals. In several cases, five requests were sent within approximately two seconds.

This behavior differs significantly from normal human browsing patterns, where users require time to read pages, navigate menus, and interact with website content.

The speed and volume of requests strongly suggest the use of an automated tool such as a web scanner, directory brute-forcer, or vulnerability enumeration utility.

---

## Findings

| Indicator           | Observation                                    |
| ------------------- | ---------------------------------------------- |
| Source IP           | 43.133.134.155                                 |
| Request Volume      | Highest in the log file                        |
| Requested Resources | Multiple suspicious and seemingly guessed URLs |
| Status Codes        | 401 Unauthorized                               |
| User Agents         | Multiple browser signatures used               |
| Request Rate        | Several requests within seconds                |
| Likely Activity     | Automated scanning / reconnaissance            |

---

## MITRE ATT&CK Mapping

### T1595 - Active Scanning

The attacker actively probed the web server by requesting numerous URLs in an attempt to identify accessible resources.

### T1110 - Brute Force

The repeated requests against protected resources may indicate attempts to identify authentication endpoints or discover weakly protected areas.

### T1190 - Exploit Public-Facing Application

The attacker targeted a public-facing web server while attempting to locate potentially vulnerable or exposed resources.

---

## Conclusion

The investigation identified **43.133.134.155** as the most suspicious source within the Apache access log.

Several indicators support the assessment that this activity was automated and malicious:

* High request volume compared to other IP addresses.
* Requests for numerous suspicious URLs.
* Rapid request frequency inconsistent with normal user behavior.
* Multiple User-Agent strings used within a short timeframe.
* Consistent 401 responses indicating attempts to access protected resources.

While no successful compromise was observed, the activity strongly resembles automated reconnaissance and directory enumeration performed during the early stages of an attack. Continuous monitoring and alerting on similar behavior would help detect future attempts against the web server.
