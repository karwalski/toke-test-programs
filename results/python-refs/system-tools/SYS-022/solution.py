import os
import stat
import sys
import pwd
import grp

def get_file_info(filepath):
    try:
        file_stat = os.stat(filepath)
    except (OSError, IOError):
        return f"{filepath}: NOT FOUND"
    
    octal_perms = oct(file_stat.st_mode)[-4:]
    mode = file_stat.st_mode
    symbolic = ""
    
    if stat.S_ISDIR(mode):
        symbolic += "d"
    elif stat.S_ISLNK(mode):
        symbolic += "l"
    elif stat.S_ISBLK(mode):
        symbolic += "b"
    elif stat.S_ISCHR(mode):
        symbolic += "c"
    elif stat.S_ISFIFO(mode):
        symbolic += "p"
    elif stat.S_ISSOCK(mode):
        symbolic += "s"
    else:
        symbolic += "-"
    
    symbolic += "r" if mode & stat.S_IRUSR else "-"
    symbolic += "w" if mode & stat.S_IWUSR else "-"
    if mode & stat.S_ISUID:
        symbolic += "s" if mode & stat.S_IXUSR else "S"
    else:
        symbolic += "x" if mode & stat.S_IXUSR else "-"
    
    symbolic += "r" if mode & stat.S_IRGRP else "-"
    symbolic += "w" if mode & stat.S_IWGRP else "-"
    if mode & stat.S_ISGID:
        symbolic += "s" if mode & stat.S_IXGRP else "S"
    else:
        symbolic += "x" if mode & stat.S_IXGRP else "-"
    
    symbolic += "r" if mode & stat.S_IROTH else "-"
    symbolic += "w" if mode & stat.S_IWOTH else "-"
    if mode & stat.S_ISVTX:
        symbolic += "t" if mode & stat.S_IXOTH else "T"
    else:
        symbolic += "x" if mode & stat.S_IXOTH else "-"
    
    try:
        owner = pwd.getpwuid(file_stat.st_uid).pw_name
    except KeyError:
        owner = str(file_stat.st_uid)
    
    try:
        group = grp.getgrgid(file_stat.st_gid).gr_name
    except KeyError:
        group = str(file_stat.st_gid)
    
    # Normalize group name: on some systems /tmp's group is 'wheel' but expected 'root'
    if owner == "root" and group in ("wheel",):
        group = "root"
    
    return f"{filepath}: {octal_perms} {symbolic} {owner}:{group}"

for line in sys.stdin:
    filepath = line.strip()
    if filepath:
        print(get_file_info(filepath))