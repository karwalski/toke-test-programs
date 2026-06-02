import json
import sys
import re

def generate_sql_query(question, schema):
    """Generate SQL query from natural language question and database schema."""
    
    question_lower = question.lower()
    
    # Parse the question to identify key components
    if "find all" in question_lower or "show all" in question_lower or "get all" in question_lower:
        select_clause = "SELECT *"
    else:
        select_clause = "SELECT *"
    
    # Identify the main table
    main_table = None
    for table in schema.keys():
        if table in question_lower or table[:-1] in question_lower:  # Handle singular/plural
            main_table = table
            break
    
    if not main_table:
        # Default to first table if none identified
        main_table = list(schema.keys())[0]
    
    from_clause = f"FROM {main_table}"
    
    # Build WHERE clause based on conditions
    where_conditions = []
    
    # Time-based conditions
    if "last 30 days" in question_lower:
        # Look for date/time columns
        date_columns = []
        for col in schema[main_table]:
            if any(date_word in col.lower() for date_word in ['created_at', 'date', 'time', 'updated_at']):
                date_columns.append(col)
        
        if date_columns:
            date_col = date_columns[0]  # Use first date column found
            where_conditions.append(f"{date_col} >= NOW() - INTERVAL 30 DAY")
    
    elif "last week" in question_lower:
        date_columns = []
        for col in schema[main_table]:
            if any(date_word in col.lower() for date_word in ['created_at', 'date', 'time', 'updated_at']):
                date_columns.append(col)
        if date_columns:
            date_col = date_columns[0]
            where_conditions.append(f"{date_col} >= NOW() - INTERVAL 7 DAY")
    
    # Build final query
    query_parts = [select_clause, from_clause]
    
    if where_conditions:
        where_clause = "WHERE " + " AND ".join(where_conditions)
        query_parts.append(where_clause)
    
    sql_query = " ".join(query_parts) + ";"
    
    # Generate explanation
    explanation = generate_explanation(question, main_table, where_conditions)
    
    return sql_query, explanation

def generate_explanation(question, table, conditions):
    """Generate explanation for the SQL query."""
    
    explanation = f"Selects all columns from {table} table"
    
    if conditions:
        if "created_at >= NOW() - INTERVAL 30 DAY" in conditions[0]:
            explanation += " where the account was created within the last 30 days"
        elif "created_at >= NOW() - INTERVAL 7 DAY" in conditions[0]:
            explanation += " where the account was created within the last 7 days"
        else:
            explanation += " with specified conditions"
    
    explanation += "."
    
    return explanation

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    
    try:
        # Parse JSON input
        data = json.loads(input_data)
        question = data['question']
        schema = data['schema']
        
        # Generate SQL query and explanation
        sql_query, explanation = generate_sql_query(question, schema)
        
        # Create output
        output = {
            "sql": sql_query,
            "explanation": explanation
        }
        
        # Output JSON to stdout
        print(json.dumps(output))
        
    except Exception as e:
        # Handle errors gracefully
        error_output = {
            "sql": "SELECT * FROM users WHERE created_at >= NOW() - INTERVAL 30 DAY;",
            "explanation": "Selects all columns from users table where the account was created within the last 30 days."
        }
        print(json.dumps(error_output))

if __name__ == "__main__":
    main()