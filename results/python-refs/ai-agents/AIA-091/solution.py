import json
import sys

def improve_error_message(error_message, context):
    error_lower = error_message.lower()
    context_lower = context.lower()
    
    # Database connection errors
    if "econnrefused" in error_lower and "5432" in error_message:
        return {
            "improved_message": "Cannot connect to the database server.",
            "suggestion": "Ensure PostgreSQL is running on port 5432. Try: sudo systemctl start postgresql",
            "error_code": "DB_CONNECTION_REFUSED"
        }
    
    # Generic database connection errors
    if "econnrefused" in error_lower and "database" in context_lower:
        return {
            "improved_message": "Cannot connect to the database server.",
            "suggestion": "Check if the database service is running and the connection details are correct.",
            "error_code": "DB_CONNECTION_REFUSED"
        }
    
    # File not found errors
    if "no such file or directory" in error_lower or "file not found" in error_lower:
        return {
            "improved_message": "The requested file or directory could not be found.",
            "suggestion": "Check the file path and ensure the file exists with correct permissions.",
            "error_code": "FILE_NOT_FOUND"
        }
    
    # Permission denied errors
    if "permission denied" in error_lower or "access denied" in error_lower:
        return {
            "improved_message": "Access to the resource was denied due to insufficient permissions.",
            "suggestion": "Check file permissions or try running with appropriate privileges.",
            "error_code": "ACCESS_DENIED"
        }
    
    # Network connection errors
    if "econnrefused" in error_lower:
        return {
            "improved_message": "Connection was refused by the target server.",
            "suggestion": "Check if the service is running and the port is correct.",
            "error_code": "CONNECTION_REFUSED"
        }
    
    # Generic fallback
    return {
        "improved_message": "An error occurred while processing your request.",
        "suggestion": "Please check the system logs for more details or contact support.",
        "error_code": "GENERIC_ERROR"
    }

def main():
    try:
        input_data = json.loads(sys.stdin.read().strip())
        error_message = input_data.get("error_message", "")
        context = input_data.get("context", "")
        
        result = improve_error_message(error_message, context)
        
        print(json.dumps(result, separators=(',', ':')))
        
    except (json.JSONDecodeError, KeyError) as e:
        error_result = {
            "improved_message": "Invalid input format provided.",
            "suggestion": "Please provide valid JSON with 'error_message' and 'context' fields.",
            "error_code": "INVALID_INPUT"
        }
        print(json.dumps(error_result, separators=(',', ':')))

if __name__ == "__main__":
    main()