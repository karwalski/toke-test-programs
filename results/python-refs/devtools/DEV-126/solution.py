import json
import sys

def generate_deployment_manifest(config):
    # Convert env_vars dict to list of name/value objects
    env_list = []
    for key, value in config["env_vars"].items():
        env_list.append({"name": key, "value": value})
    
    # Build the deployment manifest
    manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": config["app_name"],
            "labels": {
                "app": config["app_name"],
                "version": config["version"]
            }
        },
        "spec": {
            "replicas": config["replicas"],
            "template": {
                "spec": {
                    "containers": [
                        {
                            "env": env_list,
                            "image": config["image"],
                            "name": config["app_name"],
                            "ports": [
                                {
                                    "containerPort": config["port"]
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
    
    return manifest

# Read input from stdin
input_data = sys.stdin.read().strip()
config = json.loads(input_data)

# Generate manifest
manifest = generate_deployment_manifest(config)

# Output JSON without spaces after separators
print(json.dumps(manifest, separators=(',', ':')))