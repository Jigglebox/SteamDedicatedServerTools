import shutil
from datetime import datetime
from pathlib import Path
import os

# Define the working directory (the original source of files)
working_dir = Path("P:/Users/Chalamander/Desktop/EnshroudedServer")

# Define the destination directory where backups are stored
destination_root = Path("D:/enshroudedbackups")

# Define where to restore the selected backup
restore_root = destination_root / "Restore"

def list_backups():
    backups = [d for d in destination_root.iterdir() if d.is_dir() and d.name != "Restore"]
    backups.sort(key=lambda x: x.stat().st_ctime)
    return backups

def print_backup_list(backups):
    print("Available backups:")
    for i, backup in enumerate(backups, start=1):
        # Assuming the folder name is in 'yyyyMMdd_HHmmss' format
        try:
            backup_time = datetime.strptime(backup.name, "%Y%m%d_%H%M%S")
            formatted_time = backup_time.strftime("%m/%d/%Y %H:%M")
        except ValueError:
            formatted_time = "Unknown Date"  # Fallback if the name doesn't match the expected format
        print(f"{i}. {formatted_time} - {backup.name}")

def restore_backup(backup_dir, restore_location, working_dir):
    if restore_location.exists():
        print(f"Restore location {restore_location} already exists. Please choose a different location or remove the existing one.")
        return False
    
    restore_location.mkdir(parents=True, exist_ok=True)
    
    # Copy files from the backup first
    for root, dirs, files in os.walk(backup_dir):
        rel_path = Path(root).relative_to(backup_dir)
        target_dir = restore_location / rel_path
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            src_file = Path(root) / file
            dest_file = target_dir / file
            shutil.copy2(src_file, dest_file)
    
    print(f"Backup from {backup_dir.name} has been partially restored to {restore_location}.")

    # Supplement with files from the working directory
    for root, dirs, files in os.walk(working_dir):
        rel_path = Path(root).relative_to(working_dir)
        target_dir = restore_location / rel_path
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            src_file = Path(root) / file
            dest_file = target_dir / file
            if not dest_file.exists():
                shutil.copy2(src_file, dest_file)
    
    print(f"Backup fully integrated and restored to {restore_location}.")
    os.startfile(restore_location)  # Open the restore folder in a new window
    return True
    
def main():
    backups = list_backups()
    print_backup_list(backups)
    
    choice = input("Enter the number of the backup you wish to restore: ")
    try:
        choice = int(choice) - 1
        if choice < 0 or choice >= len(backups):
            raise ValueError("Selection out of range.")
        selected_backup = backups[choice]
        
        # Prompt for restore location or use a default
        restore_location_input = input(f"Enter restore location or press Enter to use default ({restore_root}): ").strip()
        if restore_location_input:
            restore_location = Path(restore_location_input)
        else:
            # Create a unique restore directory based on the current timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            restore_location = restore_root / f"restore_{timestamp}"
        
        # Include the working_dir argument when calling restore_backup
        restore_backup(selected_backup, restore_location, working_dir)  # Updated call
    except ValueError as e:
        print(f"Invalid selection: {e}")
if __name__ == "__main__":
    main()
