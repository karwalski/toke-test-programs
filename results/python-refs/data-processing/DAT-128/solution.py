import sys
import zlib
from io import StringIO

class ColumnStore:
    def __init__(self):
        self.columns = {}
        self.column_names = []
        self.num_rows = 0
    
    def load_csv(self, csv_data):
        lines = csv_data.strip().split('\n')
        if not lines:
            return
        
        # Parse header
        self.column_names = lines[0].split(',')
        
        # Initialize columns
        for col_name in self.column_names:
            self.columns[col_name] = []
        
        # Parse data rows
        for line in lines[1:]:
            if line.strip():
                values = line.split(',')
                for i, value in enumerate(values):
                    col_name = self.column_names[i]
                    # Try to convert to int if possible
                    try:
                        converted_value = int(value)
                    except ValueError:
                        converted_value = value
                    self.columns[col_name].append(converted_value)
        
        self.num_rows = len(self.columns[self.column_names[0]]) if self.column_names else 0
        
        # Compress columns
        self._compress_columns()
    
    def _compress_columns(self):
        # Simple compression using zlib
        compressed_columns = {}
        for col_name, values in self.columns.items():
            # Convert to string representation for compression
            data_str = ','.join(str(v) for v in values)
            compressed_data = zlib.compress(data_str.encode())
            compressed_columns[col_name] = (compressed_data, type(values[0]) if values else str)
        self.compressed_columns = compressed_columns
    
    def _decompress_column(self, col_name):
        if col_name not in self.compressed_columns:
            return []
        
        compressed_data, data_type = self.compressed_columns[col_name]
        decompressed_str = zlib.decompress(compressed_data).decode()
        
        if not decompressed_str:
            return []
        
        values = decompressed_str.split(',')
        
        # Convert back to original type
        if data_type == int:
            return [int(v) for v in values]
        else:
            return values
    
    def execute_query(self, query):
        # Parse query: SELECT col WHERE col op val
        parts = query.strip().split()
        
        if len(parts) != 6 or parts[0] != 'SELECT' or parts[2] != 'WHERE':
            return []
        
        select_col = parts[1]
        where_col = parts[3]
        operator = parts[4]
        where_val = parts[5]
        
        # Convert where_val to appropriate type
        try:
            where_val = int(where_val)
        except ValueError:
            pass
        
        # Get the columns we need
        where_column_data = self._decompress_column(where_col)
        select_column_data = self._decompress_column(select_col)
        
        if not where_column_data or not select_column_data:
            return []
        
        # Apply WHERE condition
        matching_indices = []
        for i, value in enumerate(where_column_data):
            if self._evaluate_condition(value, operator, where_val):
                matching_indices.append(i)
        
        # Get results
        results = [select_column_data[i] for i in matching_indices]
        return results
    
    def _evaluate_condition(self, value, operator, target):
        if operator == '>':
            return value > target
        elif operator == '<':
            return value < target
        elif operator == '>=':
            return value >= target
        elif operator == '<=':
            return value <= target
        elif operator == '==':
            return value == target
        elif operator == '!=':
            return value != target
        return False

def main():
    # Read all input
    input_data = sys.stdin.read().strip()
    
    # Split on blank line
    parts = input_data.split('\n\n')
    csv_data = parts[0]
    queries = parts[1].strip().split('\n') if len(parts) > 1 else []
    
    # Create and load data store
    store = ColumnStore()
    store.load_csv(csv_data)
    
    # Execute queries
    for query in queries:
        if query.strip():
            results = store.execute_query(query.strip())
            
            # Output results
            if results:
                # Get column name from query
                select_col = query.strip().split()[1]
                print(select_col)
                for result in results:
                    print(result)

if __name__ == "__main__":
    main()