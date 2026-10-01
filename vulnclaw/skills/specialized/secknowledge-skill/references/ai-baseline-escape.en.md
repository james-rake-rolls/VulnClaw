# AI Foundation Security - Practical Container and Sandbox Escape Methodology

> Source: AISS NSFOCUS Large-Model Security Zhilian Community | split from ai-baseline-security.md
> Topic: container escape / persistence / lateral movement practical methodology

## 20. Practical Container and Sandbox Escape Testing Methodology

> Systematic escape and isolation testing for AI-application deployment environments (Docker/Sysbox/Daytona/Kubernetes)
> **General container-deployment security**: web-application container-deployment security checks → [web-deployment-security.md §2](web-deployment-security.md)

### 1. Testing-Process Overview

```
Information gathering → environment identification → isolation assessment → escape attempt → persistence verification → lateral movement → reporting
```

### 2. Information-Gathering Phase

#### 2.1 Container-Runtime Identification

| Check item | command | criterion |
|--------|------|----------|
| In a container? | `cat /proc/1/cgroup` | contains `docker`/`kubepods`/`containerd` |
| Docker marker file | `ls /.dockerenv` | if the file exists, it's a Docker container |
| Container-runtime type | `cat /proc/1/cgroup \| head` | `sysbox-fs` → Sysbox, `docker` → Docker |
| Kernel version | `uname -r` | match against CVE affected ranges |
| User Namespace | `cat /proc/self/uid_map` | `0 0 4294967295` → no isolation (dangerous) |
| Capabilities | `cat /proc/self/status \| grep Cap` | decode and check for dangerous caps |
| Seccomp | `cat /proc/self/status \| grep Seccomp` | 0=disabled, 2=filter |
| AppArmor | `cat /proc/self/attr/current` | `unconfined` → no protection |
| Mount points | `mount \| grep -v overlay` | detect host sensitive-path mounts |

#### 2.2 Sysbox-Specific Detection

| Check item | method | security impact |
|--------|------|----------|
| CE vs EE version | `sysbox-runc --version` or check the UID-mapping range | CE's shared mapping carries cross-tenant risk |
| UID-mapping exclusivity | `cat /proc/self/uid_map`, CE is usually `0 165536 65536` (shared) | shared mapping → cross-container privilege escalation possible |
| Virtualized /proc | `ls /proc/sys/net/` | degree of Sysbox virtualization |
| Docker-in-Docker | `docker ps 2>/dev/null` | the inner Docker may have no security restrictions |
| /dev/kvm | `ls /dev/kvm` | KVM available → nested-virtualization escape |

### 3. Isolation-Assessment Phase

#### 3.1 Process Isolation

```bash
# PID Namespace check
ps aux   # whether other containers'/host processes are visible
ls /proc/*/cmdline   # enumerate visible processes

# If PID 1 is not a container init but systemd/dockerd → isolation failed
cat /proc/1/cmdline | tr '\0' ' '
```

#### 3.2 Network Isolation

```bash
# Network interfaces
ip addr   # check network interfaces and IP ranges
ip route  # routing table; whether other subnets are reachable

# Same-subnet scan (discover neighbor containers)
for i in $(seq 1 254); do
  (ping -c 1 -W 1 $SUBNET.$i &>/dev/null && echo "$SUBNET.$i alive") &
done; wait

# Internal DNS probing
cat /etc/resolv.conf
nslookup kubernetes.default.svc.cluster.local 2>/dev/null
```

#### 3.3 Filesystem Isolation

```bash
# Check host-filesystem mounts
mount | grep -E "ext4|xfs|btrfs" | grep -v overlay
findmnt

# Path-traversal test
ls -la /var/lib/sysbox/ 2>/dev/null
ls -la /var/lib/docker/ 2>/dev/null
ls -la /run/containerd/ 2>/dev/null

# Symlink escape
ln -s /proc/1/root/etc/shadow /tmp/test_escape
cat /tmp/test_escape 2>&1  # if it succeeds → isolation failed
```

### 4. Escape-Testing Matrix

| Escape path | prerequisites | danger level | test method |
|----------|----------|----------|----------|
| cgroup release_agent | CAP_SYS_ADMIN + cgroup v1 | Critical | write release_agent to execute host commands |
| Docker Socket | /var/run/docker.sock exposed | Critical | create a privileged container via the API |
| /proc/1/root | PID namespace not isolated | Critical | directly read/write host files |
| Privileged container | --privileged mode | Critical | mount the host disk |
| runc fd leak | CVE-2024-21626 | High | use /proc/self/fd to reach the host |
| Dirty Pipe | CVE-2022-0847, 5.8≤kernel≤5.16.11 | High | overwrite read-only files for privilege escalation |
| OverlayFS | CVE-2023-0386, 5.11≤kernel≤6.2 | High | SUID-file privilege escalation |
| Sensitive mount | a host path is mounted into the container | High | write host files |
| CAP_DAC_READ_SEARCH | capability not restricted | Medium | read files via open_by_handle_at |
| CAP_SYS_PTRACE | capability not restricted | Medium | inject into host processes |
| Docker-in-Docker | the inner Docker is unrestricted | Medium | create a privileged container in the inner Docker |

### 5. Persistence Testing

> Verify the feasibility of cross-session persistence attacks on the sandbox (especially for persistent sandboxes like Daytona)

| Test item | session 1 action | session 2 verification | expected secure result |
|--------|-----------|-----------|-------------|
| .bashrc backdoor | `echo 'malicious_cmd' >> ~/.bashrc` | open a new shell to check whether it runs | a new session doesn't inherit / is reset |
| Crontab | `echo "* * * * * cmd" \| crontab -` | `crontab -l` | crontab is cleared or unavailable |
| SSH key | write to ~/.ssh/authorized_keys | test the SSH connection | the SSH service is unavailable or the key is cleared |
| Background process | `nohup cmd &` | `ps aux \| grep cmd` | the process is terminated when the session closes |
| File poisoning | write a malicious file into the workspace | does the AI read and execute it | the AI does not automatically execute instructions in a file |
| History residue | type sensitive commands in the shell | `cat ~/.bash_history` | history is cleared across sessions |
| Environment variable | `export SECRET=leaked` | `echo $SECRET` | environment variables don't persist across sessions |

### 6. Lateral-Movement Testing

```
Inside the container → internal-service discovery → direct database/cache/API connection → other tenants' sandboxes
         ↓
         Cloud metadata service (169.254.169.254) → IAM-credential theft → cloud-resource access
         ↓
         K8s API (kubernetes.default.svc) → obtain the Pod list / secrets
```

| Target | detection command | exploitation method |
|------|----------|----------|
| Cloud metadata | `curl 169.254.169.254` | obtain temporary IAM credentials |
| K8s API | `curl -k https://kubernetes.default.svc` | enumerate Pods / obtain secrets |
| K8s ServiceAccount | `cat /var/run/secrets/kubernetes.io/serviceaccount/token` | authenticate to the K8s API |
| Internal database | `echo \| nc DB_HOST 5432` | connect directly to the database |
| Redis | `redis-cli -h REDIS_HOST ping` | unauthorized access |
| Docker Registry | `curl http://REGISTRY:5000/v2/_catalog` | pull sensitive images |

### 7. Defense-Validation Checklist

```
[ ] The container runs as a non-root user (or User-namespace isolation is effective)
[ ] No excess capabilities (least principle: only essentials such as NET_BIND_SERVICE)
[ ] A Seccomp profile is enabled (not disabled)
[ ] AppArmor/SELinux is not unconfined
[ ] /var/run/docker.sock is not exposed
[ ] Not running in --privileged mode
[ ] No host sensitive-path mounts (/, /etc, /var/run)
[ ] The kernel version is not affected by known escape CVEs
[ ] cgroup v2, or release_agent is not writable
[ ] PID-namespace isolation is effective (only own processes are visible)
[ ] Network policies / firewall restrict inter-container communication
[ ] The 169.254.169.254 metadata service is blocked
[ ] Sensitive data between sessions (history/credentials) is cleared
[ ] All user data is completely cleared when the sandbox is destroyed
[ ] Sysbox uses the EE edition or an exclusive UID mapping
```

---
