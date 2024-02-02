import os
import shutil
from datetime import datetime
from pathlib import Path
import json

# Define the source and destination directories
source_dir = Path("E:\PalWorldServer")
destination_root = Path("D:/PalWorld Backups")

# Log file setup
log_file = destination_root / "BackupLog.txt"

# Manifest file
manifest_file = destination_root / "backup_manifest.json"

def log_message(message):
    """Append a message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"{timestamp} - {message}\n")
    print(message)

def load_manifest():
    """Load the backup manifest."""
    if manifest_file.exists():
        with open(manifest_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_manifest(manifest):
    """Save the updated manifest."""
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

def update_and_copy_file(source_file, destination_file, manifest):
    """Update file in destination and manifest if it's new or modified. Create parent directory only if needed."""
    modified = source_file.stat().st_mtime
    if str(source_file) not in manifest or modified > manifest[str(source_file)]:
        # Only create the directory and copy the file if it's new or has been modified
        destination_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, destination_file)
        manifest[str(source_file)] = modified
        log_message(f"Copied: {source_file} to {destination_file}")
        return True  # Indicates that a file was copied
    return False  # Indicates no action was needed

def backup_files(source, destination, manifest):
    """Backup new or modified files based on the manifest."""
    files_processed = 0
    for root, _, files in os.walk(source):
        for file in files:
            source_file = Path(root) / file
            destination_file = destination / source_file.relative_to(source)
            if update_and_copy_file(source_file, destination_file, manifest):
                files_processed += 1
    return files_processed, manifest

def check_files_to_backup(source, manifest):
    """Check how many files need to be backed up based on the manifest."""
    files_to_backup = 0
    for root, _, files in os.walk(source):
        for file in files:
            source_file = Path(root) / file
            modified = source_file.stat().st_mtime
            if str(source_file) not in manifest or modified > manifest[str(source_file)]:
                files_to_backup += 1
    return files_to_backup

# Usage of the check_files_to_backup function
log_message("Backup script started.")
manifest = load_manifest()

# Check if any files need to be backed up by comparing to the manifest without copying them
files_to_backup = check_files_to_backup(source_dir, manifest)

if files_to_backup > 0:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder_name = f"{timestamp}"
    full_backup_path = destination_root / backup_folder_name
    full_backup_path.mkdir(parents=True, exist_ok=True)  # Now create the backup folder only if needed

    # Now call backup_files to perform the actual backup
    files_copied, updated_manifest = backup_files(source_dir, full_backup_path, manifest)
    save_manifest(updated_manifest)  # Save the updated manifest after successful backup

    log_message(f"Backup completed successfully to {full_backup_path}. {files_copied} files were copied/updated.")
else:
    log_message("No files were copied/updated. No changes detected since the last backup.")

log_message("Backup script ended.")

