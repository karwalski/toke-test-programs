import tarfile
import zipfile
import os
import sys

# Read input
archive_path = input().strip()
dest_dir = input().strip()

# Create destination directory if it doesn't exist
os.makedirs(dest_dir, exist_ok=True)

extracted_files = []

try:
    # Determine archive type and extract
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                zip_ref.extract(member, dest_dir)
                extracted_path = os.path.join(dest_dir, member)
                if not member.endswith('/'):  # Don't list directories
                    extracted_files.append(extracted_path)
                    print(f"extracted: {extracted_path}")
    elif archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            for member in tar_ref.getmembers():
                tar_ref.extract(member, dest_dir)
                extracted_path = os.path.join(dest_dir, member.name)
                if member.isfile():  # Only list files, not directories
                    extracted_files.append(extracted_path)
                    print(f"extracted: {extracted_path}")
    elif archive_path.endswith('.tar.bz2'):
        with tarfile.open(archive_path, 'r:bz2') as tar_ref:
            for member in tar_ref.getmembers():
                tar_ref.extract(member, dest_dir)
                extracted_path = os.path.join(dest_dir, member.name)
                if member.isfile():  # Only list files, not directories
                    extracted_files.append(extracted_path)
                    print(f"extracted: {extracted_path}")
    elif archive_path.endswith('.tar'):
        with tarfile.open(archive_path, 'r:') as tar_ref:
            for member in tar_ref.getmembers():
                tar_ref.extract(member, dest_dir)
                extracted_path = os.path.join(dest_dir, member.name)
                if member.isfile():  # Only list files, not directories
                    extracted_files.append(extracted_path)
                    print(f"extracted: {extracted_path}")
except (tarfile.TarError, zipfile.BadZipFile, FileNotFoundError, OSError):
    pass

print(f"Done: {len(extracted_files)} files extracted to {dest_dir}.")