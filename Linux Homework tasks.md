# Session 2 – Linux Homework Answers

## Task 1: Soft Link vs Hard Link

### Difference

* **Soft link:** Points to the path of another file. If the original file is deleted, the link breaks.
* **Hard link:** Points to the same inode as the original file. It still works even if the original file is deleted.

### Create Links

```bash
mkdir -p task1-links
cd task1-links

echo "linux practice" > original.txt

ln -s original.txt soft_link.txt
ln original.txt hard_link.txt

ls -li
```

### Delete Original File

```bash
rm original.txt

ls -li

cat hard_link.txt
cat soft_link.txt
```

The hard link still shows the content, while the soft link is broken.

**In short:** `ln -s` creates a soft link and `ln` creates a hard link. Soft links use the file path, while hard links use the inode.

---

## Task 2: `adduser` vs `useradd`

* **`useradd`:** Basic command for creating a user. You usually need to give extra options.
* **`adduser`:** Easier and interactive. It helps create the home directory and set the password.

On Ubuntu, I would normally use `adduser` because it is simpler.

### Create User

```bash
sudo adduser devops_test_user
id devops_test_user
```

### Delete User

```bash
sudo deluser --remove-home devops_test_user
```

---

## Task 3: `journalctl`

`journalctl` is used to check system logs in Linux. It can show logs from the system, boot process, kernel, and services.

### Useful Commands

```bash
journalctl
```

Shows all logs.

```bash
journalctl -b
```

Shows logs from the current boot.

```bash
journalctl -f
```

Shows new logs as they come in.

```bash
journalctl -u ssh.service
```

Shows SSH service logs.

```bash
journalctl -u ssh.service -n 100 --no-pager
```

Shows the last 100 SSH logs.

---

## Task 4: Linux Command Cheat Sheet

| Command    | Use                      | Example                     |
| ---------- | ------------------------ | --------------------------- |
| `pwd`      | Shows current directory  | `pwd`                       |
| `ls -lah`  | Lists files with details | `ls -lah`                   |
| `cd`       | Changes directory        | `cd /var/log`               |
| `mkdir`    | Creates a folder         | `mkdir practice`            |
| `touch`    | Creates an empty file    | `touch notes.txt`           |
| `cp`       | Copies a file            | `cp a.txt b.txt`            |
| `mv`       | Moves or renames a file  | `mv b.txt c.txt`            |
| `rm`       | Deletes a file           | `rm c.txt`                  |
| `cat`      | Shows file content       | `cat notes.txt`             |
| `grep`     | Searches for text        | `grep ubuntu file.txt`      |
| `find`     | Finds files              | `find . -name "*.sh"`       |
| `chmod`    | Changes permissions      | `chmod +x script.sh`        |
| `chown`    | Changes file owner       | `sudo chown user:user file` |
| `df -h`    | Shows disk space         | `df -h`                     |
| `du -sh`   | Shows folder size        | `du -sh .`                  |
| `ps aux`   | Shows running processes  | `ps aux`                    |
| `top`      | Shows processes live     | `top`                       |
| `free -h`  | Shows memory usage       | `free -h`                   |
| `uname -a` | Shows system information | `uname -a`                  |
