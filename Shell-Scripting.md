# System Information Shell Script

This is a simple shell script that displays basic system information, takes a directory name from the user, and saves running process information into a file.

## Commands Used

* `date` - shows the current date
* `hostname` - shows the system hostname
* `whoami` - shows the current username
* `df -h` - shows disk usage
* `ps` - shows running processes
* `read -p` - takes input from the user
* `mkdir` - creates a directory
* `touch` - creates a file
* `echo` - prints text
* `>` - saves command output into a file
* Variables - store information for later use

## Shell Script

```bash
#!/bin/bash

date=$(date)
hostname=$(hostname)
username=$(whoami)

read -p "Directory: " dir

mkdir -p "$dir"
touch "$dir/processes.txt"

ps > "$dir/processes.txt"

echo ""
echo "System Information"
echo "------------------"
echo "Date: $date"
echo "Hostname: $hostname"
echo "Username: $username"

echo ""
echo "Disk Usage:"
df -h

echo ""
echo "Running Processes:"
ps

echo ""
echo "Process information saved in: $dir/processes.txt"
```

## Running the Script

First, give the script execute permission:

```bash
chmod +x system_info.sh
```

Then run the script:

```bash
./system_info.sh
```

## Input and Output

```text
sunny@SaiCharan:~/shell-homework$ ./system_info.sh

Directory: system_info

System Information
------------------
Date: Fri Sep 4 2026
Hostname: SaiCharan
Username: sunny

Disk Usage:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdd        251G   18G  221G   8% /
none            3.8G     0  3.8G   0% /usr/lib/modules/...
none            3.8G     0  3.8G   0% /usr/lib/wsl/...

Running Processes:
    PID TTY          TIME CMD
      1 pts/0    00:00:00 bash
    123 pts/0    00:00:00 bash
    456 pts/0    00:00:00 ps

Process information saved in: system_info/processes.txt
```

> **Note:** The `df -h` and `ps` output can be different on every system. The values above are only an example.

## Files Created

After running the script, the directory will look like this:

```text
shell-homework/
├── system_info.sh
└── system_info/
    └── processes.txt
```

The `processes.txt` file contains the output of the `ps` command.

## Checking the Created File

```bash
ls
```

Output:

```text
system_info
system_info.sh
```

Check the file:

```bash
cat system_info/processes.txt
```

Output:

```text
    PID TTY          TIME CMD
      1 pts/0    00:00:00 bash
    123 pts/0    00:00:00 bash
    456 pts/0    00:00:00 ps
```

## Result

The script successfully:

1. Displays the current date.
2. Displays the hostname.
3. Displays the username.
4. Displays disk usage.
5. Displays running processes.
6. Uses variables to store information.
7. Takes directory input using `read -p`.
8. Creates a directory using `mkdir`.
9. Creates a file using `touch`.
10. Saves process information using `>` redirection.
