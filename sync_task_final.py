import os
import shutil
import hashlib
import argparse
import time

def calculate_hash(file_path, block_size=65536):
    """Calculate the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            hash_md5.update(block)
    return hash_md5.hexdigest()

def synchronize_folders(source_folder, replica_folder, log_file):
    """Synchronize source folder to replica folder."""
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source_folder)
            replica_path = os.path.join(replica_folder, relative_path)
                

            # Check if file exists in replica folder
            if os.path.exists(replica_path):
                source_hash = calculate_hash(source_path)
                replica_hash = calculate_hash(replica_path)
                
                # Compare hashes to check if synchronization is needed
                if source_hash != replica_hash:
                    shutil.copy2(source_path, replica_path)
                    log_entry = f"[{time.ctime()}] Updated: {relative_path}\n"
                    print(log_entry, end="")
                    log_file.write(log_entry)
            else:
                shutil.copy2(source_path, replica_path)
                log_entry = f"[{time.ctime()}] Added: {relative_path}\n"
                print(log_entry, end="")
                log_file.write(log_entry)

        for dir in dirs:
            source_subfolder = os.path.join(root, dir)
            relative_path = os.path.relpath(source_subfolder, source_folder)
            replica_subfolder = os.path.join(replica_folder, relative_path)

            # Recreate subfolders in replica folder
            if not os.path.exists(replica_subfolder):
                os.makedirs(replica_subfolder)
                log_entry = f"[{time.ctime()}] Added subfolder: {relative_path}\n"
                print(log_entry, end="")
                log_file.write(log_entry)

    # Check for deleted files and subfolders in replica folder
    for root, dirs, files in os.walk(replica_folder, topdown=False):
        for file in files:
            replica_path = os.path.join(root, file)
            relative_path = os.path.relpath(replica_path, replica_folder)
            source_path = os.path.join(source_folder, relative_path)
            
            if not os.path.exists(source_path):
                os.remove(replica_path)
                log_entry = f"[{time.ctime()}] Removed: {relative_path}\n"
                print(log_entry, end="")
                log_file.write(log_entry)

        for dir in dirs:
            replica_subfolder = os.path.join(root, dir)
            relative_path = os.path.relpath(replica_subfolder, replica_folder)
            source_subfolder = os.path.join(source_folder, relative_path)
            
            if not os.path.exists(source_subfolder):
                shutil.rmtree(replica_subfolder)
                log_entry = f"[{time.ctime()}] Removed subfolder: {relative_path}\n"
                print(log_entry, end="")
                log_file.write(log_entry)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder synchronization program")
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("replica_folder", help="Path to the replica folder")
    parser.add_argument("sync_interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    args = parser.parse_args()

    if not os.path.exists(args.replica_folder):
        os.makedirs(args.replica_folder)

    if not os.path.exists(args.source_folder):
        raise ValueError("Source folder does not exist.")

    if args.sync_interval <= 0:
        raise ValueError("Sync interval must be a positive value.")

    with open(args.log_file, "a") as log_file:
        try:
            while True:
                synchronize_folders(args.source_folder, args.replica_folder, log_file)
                log_file.flush()
                time.sleep(args.sync_interval)
        finally:
            log_file.close()
