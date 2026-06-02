import sys
import socket
import threading
from queue import Queue
import time

def dns_lookup(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return ip
    except socket.gaierror:
        return None

def worker(queue, domain, results, lock):
    while True:
        word = queue.get()
        if word is None:
            break
        
        subdomain = f"{word}.{domain}"
        ip = dns_lookup(subdomain)
        
        if ip:
            with lock:
                results.append((subdomain, ip))
                print(f"{subdomain} -> {ip}")
        
        queue.task_done()

def main():
    # Read input
    domain = input().strip()
    wordlist_path = input().strip()
    concurrency = int(input().strip())
    
    # Read wordlist
    try:
        with open(wordlist_path, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        words = []
    
    # Setup threading
    queue = Queue()
    results = []
    lock = threading.Lock()
    
    # Start worker threads
    threads = []
    for _ in range(concurrency):
        t = threading.Thread(target=worker, args=(queue, domain, results, lock))
        t.start()
        threads.append(t)
    
    # Add words to queue
    for word in words:
        queue.put(word)
    
    # Wait for all tasks to complete
    queue.join()
    
    # Stop worker threads
    for _ in range(concurrency):
        queue.put(None)
    
    for t in threads:
        t.join()
    
    # Print summary
    print("Summary:")

if __name__ == "__main__":
    main()