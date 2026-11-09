import sys

PROBES = ("file:///etc/passwd", "file:///etc/hosts")
WORD = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")


def passwd_evidence(body):
    """The /etc/passwd root entry leaked into the response, or None."""
    at = body.find("root:")
    while at >= 0:
        if at == 0 or body[at - 1] not in WORD:
            end = at
            while end < len(body) and body[end] not in " \t<":
                end += 1
            return body[at:end]
        at = body.find("root:", at + 1)
    return None


def hosts_evidence(body):
    """'127.0.0.1 localhost' when the /etc/hosts loopback entry leaked, or None."""
    at = body.find("127.0.0.1")
    while at >= 0:
        j = at + len("127.0.0.1")
        k = j
        while k < len(body) and body[k] in " \t":
            k += 1
        if k > j and body.startswith("localhost", k):
            return "127.0.0.1 localhost"
        at = body.find("127.0.0.1", at + 1)
    return None


def main():
    lines = sys.stdin.read().split("\n")
    get = lambda i: lines[i].strip() if i < len(lines) else ""
    url = get(0)
    if not ((url.startswith("http://") and len(url) > 7) or
            (url.startswith("https://") and len(url) > 8)):
        print("ERROR: not an http(s) URL: %s" % url)
        return
    print("target: %s" % url)
    vuln = False
    for probe, body, find in ((PROBES[0], get(1), passwd_evidence),
                              (PROBES[1], get(2), hosts_evidence)):
        ev = find(body)
        if ev is None:
            print("probe %s: SAFE" % probe)
        else:
            vuln = True
            print("probe %s: VULNERABLE (%s)" % (probe, ev))
    print("result: %s" % ("VULNERABLE" if vuln else "SAFE"))


if __name__ == "__main__":
    main()
