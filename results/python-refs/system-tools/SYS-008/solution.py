import sys


def main():
    lines = sys.stdin.read().split("\n")
    table, services, i = [], [], 0
    # the table ends at a "--" line; a blank line or end of input before it
    # ends the whole input, so no services are listed
    while i < len(lines) and lines[i].strip() not in ("--", ""):
        table.append(lines[i].strip())
        i += 1
    if i >= len(lines) or lines[i].strip() != "--":
        print("(empty output)")
        return
    i += 1
    while i < len(lines) and lines[i].strip():
        services.append(lines[i].strip())
        i += 1
    names = set()
    for cmd in table:
        names.add(cmd)
        if "/" in cmd:
            names.add(cmd[cmd.rfind("/") + 1:])
    if not services:
        print("(empty output)")
        return
    for svc in services:
        print("%s: %s" % (svc, "RUNNING" if svc in names else "STOPPED"))


if __name__ == "__main__":
    main()
