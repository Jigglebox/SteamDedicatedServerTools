
Server Backup and Restoration Scripts
This README provides detailed instructions on how to use two Python scripts designed for backing up and restoring dedicated server files. These scripts simplify the process of managing server backups, ensuring your data is safe and can be easily restored in case of any issues.

Requirements
Python: You must have Python installed on your system to run these scripts. These scripts are compatible with Python 3.x versions.
Script 1: Backup Script
Overview
The Backup Script automates the process of backing up your server's files. It intelligently copies only the files that have changed since the last backup, saving time and storage space. It also maintains a log file for tracking backups and a manifest file to keep track of file changes.

Features
Full and incremental backups.
Automated change detection.
Log file creation for backup tracking.
Manifest file for efficient change tracking.
How to Use
Configure Paths: Open the script in a text editor and set the source_dir variable to your server's directory path and destination_root to your desired backup location.

python
Copy code
source_dir = Path("E:/YourServerFolder")
destination_root = Path("D:/YourBackupLocation")
Run the Script: Execute the script using Python. On the first run, it performs a full backup. Subsequent runs will perform incremental backups based on changes.

Logging: Check the BackupLog.txt file in your backup directory for a record of each backup operation.

Script 2: Restoration Script
Overview
The Restoration Script facilitates the process of restoring your server from a backup. It allows you to select a backup from the list of available backups and restores it to a specified location, simplifying the restoration process.

Features
Lists all available backups.
User selection of backup to restore.
Restoration to a user-specified directory.
How to Use
Check Backup Availability: Ensure you have backups created by the Backup Script in the specified destination_root.

Run the Script: Execute the script. It will list all available backups and prompt you to choose one for restoration.

Select Backup and Restoration Directory: Follow the prompts to select which backup to restore and where to restore it. You can specify a custom location or use the default restoration directory.

Completion: Once the script completes, your selected backup will be fully restored to the specified location.

Notes
Regularly test your backups and restoration process to ensure they are functioning correctly.
Modify the script paths according to your server setup.
