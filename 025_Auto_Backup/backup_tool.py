import os
import zipfile
import shutil
import datetime
import argparse
from pathlib import Path

class BackupManager:
    def __init__(self, source_dir, backup_dir, max_versions=5):
        self.source_dir = Path(source_dir).resolve()
        self.backup_dir = Path(backup_dir).resolve()
        self.max_versions = max_versions

    def create_backup(self):
        """Creates a timestamped ZIP backup of the source directory."""
        if not self.source_dir.exists():
            print(f"Error: Source directory '{self.source_dir}' does not exist.")
            return False

        if not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_filename = f"backup_{timestamp}.zip"
        zip_path = self.backup_dir / zip_filename

        print(f"Creating backup: {zip_filename}...")
        
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(self.source_dir):
                    for file in files:
                        file_path = Path(root) / file
                        # Calculate relative path to store in zip
                        arcname = file_path.relative_to(self.source_dir)
                        zipf.write(file_path, arcname)
            
            print(f"Successfully created: {zip_path}")
            return True
        except Exception as e:
            print(f"Failed to create backup: {e}")
            return False

    def rotate_backups(self):
        """Maintains only the latest N backups, deleting the rest."""
        backups = sorted(self.backup_dir.glob("backup_*.zip"), key=os.path.getmtime, reverse=True)
        
        if len(backups) > self.max_versions:
            excess_backups = backups[self.max_versions:]
            print(f"\nCleaning up old backups (Limit: {self.max_versions})...")
            
            for backup in excess_backups:
                try:
                    os.remove(backup)
                    print(f"Deleted old backup: {backup.name}")
                except Exception as e:
                    print(f"Error deleting {backup.name}: {e}")
        else:
            print("\nSpace check: Backup limits not reached.")

def create_dummy_files(target_dir):
    """Creates dummy files for testing purpose."""
    target = Path(target_dir)
    target.mkdir(exist_ok=True)
    
    # Create a few text files
    for i in range(1, 6):
        with open(target / f"project_file_{i}.txt", "w") as f:
            f.write(f"This is the content of project file {i}\nTimestamp: {datetime.datetime.now()}")
    
    # Create a subfolder
    (target / "assets").mkdir(exist_ok=True)
    with open(target / "assets" / "config.txt", "w") as f:
        f.write("Configuration settings go here.")
        
    print(f"Dummy project created at: {target.resolve()}")

def main():
    parser = argparse.ArgumentParser(description="Auto Backup & Versioning Tool")
    parser.add_argument("--source", help="Source directory to backup")
    parser.add_argument("--dest", help="Destination directory for backups")
    parser.add_argument("--keep", type=int, default=5, help="Number of backups to keep (default: 5)")
    parser.add_argument("--dummy", action="store_true", help="Create dummy files for testing")
    
    args = parser.parse_args()

    # Interaction if no args provided
    if not args.source and not args.dummy:
        print("=== Auto Backup Tool ===")
        print("1. Run Backup")
        print("2. Create Dummy Files (Test)")
        choice = input("Select option (1/2): ").strip()
        
        if choice == '2':
            args.dummy = True
        else:
            args.source = input("Enter source folder path: ").strip()
            args.dest = input("Enter backup destination path (default: './backups'): ").strip()
            if not args.dest:
                args.dest = "./backups"
                
            keep_input = input("Max versions to keep (default: 5): ").strip()
            if keep_input.isdigit():
                args.keep = int(keep_input)

    # 1. Handle Dummy Creation
    if args.dummy:
        dummy_path = "dummy_project"
        create_dummy_files(dummy_path)
        if not args.source:
           print(f"\nTo backup this dummy folder, run:\npython backup_tool.py --source {dummy_path} --dest backups")
           return

    # 2. Run Backup
    if args.source:
        dest = args.dest if args.dest else "backups"
        manager = BackupManager(args.source, dest, args.keep)
        if manager.create_backup():
            manager.rotate_backups()

if __name__ == "__main__":
    main()
