import json
import sys

def validate_kubernetes_manifest(manifest):
    errors = []
    
    # Check required top-level fields
    required_fields = ['apiVersion', 'kind', 'metadata']
    for field in required_fields:
        if field not in manifest:
            errors.append(f"ERROR: {field} - required field missing")
    
    # Validate metadata
    if 'metadata' in manifest:
        if not isinstance(manifest['metadata'], dict):
            errors.append("ERROR: metadata - must be an object")
        elif 'name' not in manifest['metadata']:
            errors.append("ERROR: metadata.name - required field missing")
        elif not isinstance(manifest['metadata']['name'], str) or not manifest['metadata']['name']:
            errors.append("ERROR: metadata.name - must be a non-empty string")
    
    # Validate kind-specific requirements
    kind = manifest.get('kind', '')
    
    if kind in ['Deployment', 'StatefulSet', 'DaemonSet', 'ReplicaSet']:
        if 'spec' not in manifest:
            errors.append("ERROR: spec - required field missing")
        else:
            spec = manifest['spec']
            if not isinstance(spec, dict):
                errors.append("ERROR: spec - must be an object")
            else:
                # For Deployment, StatefulSet, ReplicaSet - replicas should be present
                if kind in ['Deployment', 'StatefulSet', 'ReplicaSet']:
                    if 'replicas' in spec:
                        if not isinstance(spec['replicas'], int) or spec['replicas'] < 0:
                            errors.append("ERROR: spec.replicas - must be a non-negative integer")
                
                # Check for selector (required for most workload resources)
                if kind in ['Deployment', 'StatefulSet', 'ReplicaSet']:
                    if 'selector' not in spec:
                        errors.append("ERROR: spec.selector - required field missing")
                
                # Check for template (required for most workload resources)
                if 'template' not in spec:
                    errors.append("ERROR: spec.template - required field missing")
                else:
                    template = spec['template']
                    if not isinstance(template, dict):
                        errors.append("ERROR: spec.template - must be an object")
                    else:
                        if 'spec' not in template:
                            errors.append("ERROR: spec.template.spec - required field missing")
                        else:
                            pod_spec = template['spec']
                            if not isinstance(pod_spec, dict):
                                errors.append("ERROR: spec.template.spec - must be an object")
                            else:
                                if 'containers' not in pod_spec:
                                    errors.append("ERROR: spec.template.spec.containers - required field missing")
                                else:
                                    containers = pod_spec['containers']
                                    if not isinstance(containers, list) or len(containers) == 0:
                                        errors.append("ERROR: spec.template.spec.containers - must be a non-empty array")
                                    else:
                                        for i, container in enumerate(containers):
                                            if not isinstance(container, dict):
                                                errors.append(f"ERROR: spec.template.spec.containers[{i}] - must be an object")
                                            else:
                                                if 'name' not in container:
                                                    errors.append(f"ERROR: spec.template.spec.containers[{i}].name - required field missing")
                                                if 'image' not in container:
                                                    errors.append(f"ERROR: spec.template.spec.containers[{i}].image - required field missing")
    
    elif kind == 'Service':
        if 'spec' not in manifest:
            errors.append("ERROR: spec - required field missing")
        else:
            spec = manifest['spec']
            if not isinstance(spec, dict):
                errors.append("ERROR: spec - must be an object")
            else:
                if 'ports' not in spec:
                    errors.append("ERROR: spec.ports - required field missing")
    
    elif kind == 'Pod':
        if 'spec' not in manifest:
            errors.append("ERROR: spec - required field missing")
        else:
            spec = manifest['spec']
            if not isinstance(spec, dict):
                errors.append("ERROR: spec - must be an object")
            else:
                if 'containers' not in spec:
                    errors.append("ERROR: spec.containers - required field missing")
                else:
                    containers = spec['containers']
                    if not isinstance(containers, list) or len(containers) == 0:
                        errors.append("ERROR: spec.containers - must be a non-empty array")
    
    # Validate apiVersion format
    if 'apiVersion' in manifest:
        api_version = manifest['apiVersion']
        if not isinstance(api_version, str) or not api_version:
            errors.append("ERROR: apiVersion - must be a non-empty string")
    
    # Validate kind
    if 'kind' in manifest:
        if not isinstance(manifest['kind'], str) or not manifest['kind']:
            errors.append("ERROR: kind - must be a non-empty string")
    
    return errors

def main():
    try:
        input_data = sys.stdin.read().strip()
        manifest = json.loads(input_data)
        
        errors = validate_kubernetes_manifest(manifest)
        
        if errors:
            for error in errors:
                print(error)
        else:
            print("VALID")
            
    except json.JSONDecodeError:
        print("ERROR: - invalid JSON format")
    except Exception:
        print("ERROR: - failed to process manifest")

if __name__ == "__main__":
    main()