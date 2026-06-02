import tarfile
import zipfile
import os
import sys

archive_path = input().strip()
dest_dir = input().strip()

if not os.path.exists(archive_path):
    print(f"ERROR: archive not found: {archive_path}")
    sys.exit(0)

os.makedirs(dest_dir, exist_ok=True)

extracted_files = []

try:
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            for member in zip_ref.namelist():
                zip_ref.extract(member, dest_dir)
                extracted_path = os.path.join(dest_dir, member)
                if not member.endswith('/'):
                    extracted_files.append(extracted_path)
                    print(f"extracted: {extracted_path}")
    elif archive_path.endswith('.tar.gz') or archive_path.endswith('.tgz'):
        mode = 'r:gz'
        with tarfile.open(archive_path, mode) as tar_ref:
            for member in tar_ref.getmembers():
                tar_ref.extract(member, dest_dir)
                extracted_path = os.path.join(dest_dir, member.name)
                if member.isfile():
                    extracted_files.append(extracted_path)
                    print(f"extracted: {extracted_path}")
    elif archive_path.endswith('.tar.bz2'):
        with tarfile.open(archive_path, 'r:bz2') as tar_ref:
            for member in tar_ref.getmembers():
                tar_ref.extract(member, dest_dir)
                extracted_path = os.path.join(dest_dir, member.name)
                if member.isfile():
                    extracted_files.append(extracted_path)
                    print(f"extracted: {extracted_path}")
    elif archive_path.endswith('.tar'):
        with tarfile.open(archive_path, 'r:') as tar_ref:
            for member in tar_ref.getmembers():
                tar_ref.extract(member, dest_dir)
                extracted_path = os.path.join(dest_dir, member.name)
                if member.isfile():
                    extracted_files.append(extracted_path)
                    print(f"extracted: {extracted_path}")
except Exception:
    pass

print(f"Done: {len(extracted_files)} files extracted to {dest_dir}.")