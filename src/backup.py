import os
import shutil
import datetime
import tarfile

def create_backup(source_dir, backup_dir):
    if not os.path.exists(source_dir):
        print(f"Error: Source directory {source_dir} does not exist.")
        return
    
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.tar.gz"
    backup_path = os.path.join(backup_dir, backup_name)
    
    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    
    print(f"Backup created at: {backup_path}")
    
    # Pruning: Keep only last 5 backups
    backups = sorted([f for f in os.listdir(backup_dir) if f.startswith("backup_")], reverse=True)
    if len(backups) > 5:
        for old_backup in backups[5:]:
            os.remove(os.path.join(backup_dir, old_backup))
            print(f"Pruned old backup: {old_backup}")

if __name__ == "__main__":
    # Example usage: backup config
    CONFIG_DIR = "/data/data/com.termux/files/home/.ai-haklab"
    BACKUP_ROOT = "/data/data/com.termux/files/home/.ai-haklab/backups"
    create_backup(CONFIG_DIR, BACKUP_ROOT)
