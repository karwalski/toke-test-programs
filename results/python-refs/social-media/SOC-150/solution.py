import json
import sys

def main():
    # Read input from stdin
    input_data = json.loads(sys.stdin.read().strip())
    
    # Extract action and api_version
    action = input_data.get("action")
    requested_version = input_data.get("api_version")
    
    # Handle version_info action
    if action == "version_info":
        # Define version support info
        current_version = "v2"
        supported_versions = {
            "v1": {
                "supported": True,
                "deprecated": True,
                "sunset_date": "2026-06-01",
                "migration_guide": "https://docs.social.app/migrate/v1-to-v2"
            },
            "v2": {
                "supported": True,
                "deprecated": False,
                "sunset_date": None,
                "migration_guide": None
            }
        }
        
        # Build response
        response = {
            "current_version": current_version,
            "requested_version": requested_version,
            "supported": supported_versions.get(requested_version, {}).get("supported", False),
            "deprecated": supported_versions.get(requested_version, {}).get("deprecated", False),
            "sunset_date": supported_versions.get(requested_version, {}).get("sunset_date"),
            "migration_guide": supported_versions.get(requested_version, {}).get("migration_guide")
        }
        
        # Remove null values for clean output
        response = {k: v for k, v in response.items() if v is not None}
        
        # Output JSON response
        print(json.dumps(response, separators=(',', ':')))

if __name__ == "__main__":
    main()