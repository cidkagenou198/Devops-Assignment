# System Information Shell Script

This script displays basic system information and saves the running processes to a file.

## Commands Used

- `date` - shows the current date
- `hostname` - shows the computer hostname
- `whoami` - shows the current username
- `df -h` - shows disk usage
- `ps` - shows running processes
- `read -p` - takes input from the user
- `mkdir` - creates a directory
- `touch` - creates a file
- `echo` - prints text
- `>` - saves command output to a file

system_info.sh

#code

#!/bin/bash

# Store basic information in variables
date=$(date)
hostname=$(hostname)
username=$(whoami)

echo "Enter the directory name:"
read -p "Directory: " dir

# Create directory
mkdir -p "$dir"

# Create file
touch "$dir/processes.txt"

# Save running processes to the file
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

# Store basic information in variables
date=$(date)
hostname=$(hostname)
username=$(whoami)

echo "Enter the directory name:"
read -p "Directory: " dir

# Create directory
mkdir -p "$dir"

# Create file
touch "$dir/processes.txt"

# Save running processes to the file
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



## Output

```text
sunny@SaiCharan:~$ ./system_info.sh

Directory: system_info

System Information
------------------
Date: Fri Sep 4 2026
Hostname: SaiCharan
Username: sunny

Disk Usage:
Filesystem      Size  Used Avail Use% Mounted on
...

Running Processes:
    PID TTY          TIME CMD
   1234 pts/0    00:00:00 bash
   1250 pts/0    00:00:00 ps
   ...

Process information saved in: system_info/processes.txt
```






