# FTP Honeypot Server

A lightweight FTP honeypot server written in Python. Simulates a real FTP server to lure and log unauthorized access attempts, built from scratch without any FTP libraries.

## Design (Please Note)

This honeypot uses a **virtual filesystem** instead of exposing the host's real filesystem. The virtual filesystem simulates directories and files that appear realistic to attackers while preventing them from interacting with or discovering actual system files. This improves isolation, reduces risk if the honeypot is compromised, and allows the environment to be fully controlled for logging and analysis.

## Features

- Active (PORT) and passive (PASV) mode support
- Virtual filesystem with fake log files to entice attackers
- Real file serving via `RETR`
- Full command logging to `logs/log.txt`
- Multi-client support via threading

## Project Structure

```
ftp_honeypot/
├── main.py            # Entry point
├── server.py          # TCP server + client thread handler
├── session.py         # Per-client session state
├── cmd_handler.py     # Command dispatcher
├── logger.py          # Logs all commands to logs/log.txt
└── commands/
    ├── user.py        # USER
    ├── pass_cmd.py    # PASS
    ├── quit.py        # QUIT
    ├── pwd.py         # PWD
    ├── cwd.py         # CWD
    ├── list_cmd.py    # LIST
    ├── retr_cmd.py    # RETR
    ├── port_cmd.py    # PORT (active mode)
    ├── pasv_cmd.py    # PASV (passive mode)
    ├── type_cmd.py    # TYPE
    └── size_cmd.py    # SIZE
```

## Setup

```bash
git clone https://github.com/yourusername/ftp-honeypot
cd ftp-honeypot
python3 main.py
```

No dependencies — standard library only.

## Configuration

In `commands/retr_cmd.py` and `commands/size_cmd.py`, set `FTP_ROOT` to the directory containing the files you want to serve:

```python
FTP_ROOT = "/path/to/your/ftp_files"
```

The server listens on `0.0.0.0:2121` by default. To change it, edit `main.py`:

```python
server = FTPServer(host="0.0.0.0", port=2121)
```

## Usage

Connect with any FTP client:

```bash
ftp 127.0.0.1 2121
```

All commands and responses are logged to `logs/log.txt`:

```
[2024-06-28 12:00:01] 127.0.0.1 >>> USER root | 331 Password required.
[2024-06-28 12:00:02] 127.0.0.1 >>> PASS 1234 | 230 "/"
[2024-06-28 12:00:03] 127.0.0.1 >>> LIST | 226 Transfer complete.
[2024-06-28 12:00:05] 127.0.0.1 >>> RETR auth.log | 226 Transfer complete.
```

## Supported Commands

| Command | Description |
|---------|-------------|
| `user`  | Set username |
| `pass`  | Set password |
| `pwd`   | Print working directory |
| `cd`   | Change directory |
| `ls`  | List directory contents |
| `get`  | Download a file |
| `quit`  | Disconnect |

## Disclaimer

This project is intended for educational and research purposes only. Only deploy on networks you own or have explicit permission to monitor.
