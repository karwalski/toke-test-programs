import subprocess
import json
import sys

def get_docker_containers(filter_type):
    try:
        # Get container list based on filter
        if filter_type == "all":
            cmd = ["docker", "ps", "-a", "--format", "json"]
        elif filter_type == "running":
            cmd = ["docker", "ps", "--format", "json"]
        elif filter_type == "stopped":
            cmd = ["docker", "ps", "-a", "--filter", "status=exited", "--format", "json"]
        else:
            return []
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            return []
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    container = json.loads(line)
                    containers.append(container)
                except json.JSONDecodeError:
                    continue
        
        return containers
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

def get_container_stats(container_id):
    try:
        cmd = ["docker", "stats", "--no-stream", "--format", "json", container_id]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        if result.returncode != 0:
            return "0.00", "0"
        
        stats = json.loads(result.stdout.strip())
        cpu_percent = stats.get("CPUPerc", "0.00%").replace("%", "")
        mem_usage = stats.get("MemUsage", "0B / 0B").split(" / ")[0]
        
        # Convert memory to MB
        if "GiB" in mem_usage or "GB" in mem_usage:
            mem_mb = str(int(float(mem_usage.replace("GiB", "").replace("GB", "")) * 1024))
        elif "MiB" in mem_usage or "MB" in mem_usage:
            mem_mb = str(int(float(mem_usage.replace("MiB", "").replace("MB", ""))))
        elif "KiB" in mem_usage or "KB" in mem_usage:
            mem_mb = str(int(float(mem_usage.replace("KiB", "").replace("KB", "")) / 1024))
        else:
            mem_mb = "0"
        
        return cpu_percent, mem_mb
    except (subprocess.TimeoutExpired, json.JSONDecodeError, ValueError):
        return "0.00", "0"

def main():
    filter_type = input().strip()
    
    containers = get_docker_containers(filter_type)
    
    if not containers:
        print("No containers found")
        return
    
    for container in containers:
        name = container.get("Names", "unknown")
        image = container.get("Image", "unknown")
        status = container.get("Status", "unknown")
        ports = container.get("Ports", "")
        
        # Get resource usage only for running containers
        if "Up" in status:
            cpu_percent, mem_mb = get_container_stats(container.get("ID", ""))
        else:
            cpu_percent, mem_mb = "0.00", "0"
        
        print(f"{name} {image} {status} {ports} {cpu_percent}% {mem_mb}")

if __name__ == "__main__":
    main()