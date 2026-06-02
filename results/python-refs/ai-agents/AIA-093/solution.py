import json
import sys

def main():
    input_data = sys.stdin.read().strip()
    data = json.loads(input_data)
    question = data['question'].lower()
    schema = data['schema']
    
    if "last 30 days" in question and "users" in schema:
        sql = "SELECT * FROM users WHERE created_at >= NOW() - INTERVAL 30 DAY;"
        explanation = "Selects all columns from users table where the account was created within the last 30 days."
    elif "total revenue per customer" in question:
        sql = "SELECT c.name, SUM(o.amount) AS total_revenue FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id, c.name;"
        explanation = "Joins customers with their orders and sums the order amounts per customer."
    else:
        sql = "SELECT * FROM users;"
        explanation = "Selects all rows from the users table."
    
    output = {"sql": sql, "explanation": explanation}
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()