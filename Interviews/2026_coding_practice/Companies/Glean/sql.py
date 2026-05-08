import json
class GleanTable:
    def __init__(self, name: str, columns: list):
        self.name = name
        self.columns = list(columns)
        self.data = []  
        # Staff-level: Secondary index for O(1) searches on a specific column (e.g., 'id')
        self.indexes = {} 

    def add_row(self, row_data: dict):
        new_row = {col: row_data.get(col) for col in self.columns}
        self.data.append(new_row)
        
        # Update indexes if you've implemented them
        # (e.g., if 'id' is a unique column)
        if 'id' in row_data:
            self.indexes[row_data['id']] = new_row

    def add_column(self, col_name: str, default_value=None):
        """
        ADD COLUMN: Updates the schema and all existing rows.
        Complexity: O(N) where N is number of rows.
        """
        if col_name in self.columns:
            print(f"Error: Column '{col_name}' already exists.")
            return

        self.columns.append(col_name)
        for row in self.data:
            row[col_name] = default_value

    def remove_column(self, col_name: str):
        """
        REMOVE COLUMN: Drops a column from the schema and all rows.
        Complexity: O(N * C) - necessary in a row-major format.
        """
        if col_name not in self.columns:
            print(f"Error: Column '{col_name}' not found.")
            return

        self.columns.remove(col_name)       # Delete this col from cols list
        for row in self.data:               # Delete this col data from each row
            if col_name in row:
                del row[col_name]

    def print_table(self):
        """
        PRINT TABLE: Formats the table for display.
        """
        if not self.columns:
            print("Table is empty.")
            return

        # Header
        header = " | ".join(f"{col:10}" for col in self.columns)
        print(f"\nTable: {self.name}")
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        # Rows
        for row in self.data:
            row_str = " | ".join(f"{str(row.get(col, '')):10}" for col in self.columns)
            print(row_str)
    
    def search_table(self, column: str, value: any):
        """
        SEARCH: Returns all rows where the column matches the value.
        Complexity: O(N) for a scan, or O(1) if using an index.
        """
        if column not in self.columns:
            print(f"Error: Column '{column}' does not exist.")
            return []

        # If we have an index for this specific search, use it
        if column == 'id' and value in self.indexes:
            return [self.indexes[value]]

        # Fallback to linear scan
        results = [row for row in self.data if row.get(column) == value]
        return results

    def save_to_json(self, filename: str):
        """
        PERSISTENCE: Saves the schema and data to a JSON file.
        """
        table_state = {
            "name": self.name,
            "columns": self.columns,
            "data": self.data
        }
        try:
            with open(filename, 'w') as f:
                json.dump(table_state, f, indent=4)
            print(f"Successfully saved {self.name} to {filename}")
        except Exception as e:
            print(f"Failed to save table: {e}")

    @classmethod
    def load_from_json(cls, filename: str):
        """
        RECOVERY: Reconstructs the GleanTable from a JSON file.
        """
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            table = cls(state['name'], state['columns'])
            table.data = state['data']
            return table
        except Exception as e:
            print(f"Failed to load table: {e}")
            return None

    # ... existing methods (print_table, add_column, etc.) ...