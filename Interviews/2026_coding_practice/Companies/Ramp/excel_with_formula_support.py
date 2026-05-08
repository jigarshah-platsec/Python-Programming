"""
1. Implement a spreadsheet. 
The spreadsheet can be represented by a data type of your choosing, but it should be easy to get/update individual cells as well as display the entire spreadsheet. Each cell in the spreadsheet can have one of the following: Ex: "=C1C2" in D2 or "=C1+C2" in D3 cells that reference other cells with formulas are said to have dependencies. If the value in C1 or C2 changes, D2 will also need to be updated since it depends on those inputs. Define a class to represent spreadsheets Define a method setCell, which adds either a value or formula to a given cell in your spreadsheet Define a method getCell, which gets the value inside of a spreadsheet cell Assume the spreadsheet is initialized with 26 columns, 100 rows, with no values in any cell Assume valid input (no error checking needed on input, particularly formulas) Assume that if a string begins with a '=', it’s a valid formula Assume we just want to handle basic arithmetic operations for now (+-/) between two cells like '=B1-B2' or '=A1+A2'
"""
import re
from collections import defaultdict

class Spreadsheet:
    def __init__(self):
        """Initialize a 26-column × 100-row spreadsheet with all cells empty."""
        self.grid = defaultdict(int)
        
        # formula: dict mapping a cell to its exact formula string. 
        # Example: formula["C1"] = "=A1+B1"
        self.formula = defaultdict(str)
        
        # graph: adjacency list of dependents. Maps a cell to a set of cells that depend on it.
        # Example: if C1 = A1 + B1, then graph["A1"] contains "C1", and graph["B1"] contains "C1"
        self.graph = defaultdict(set) # Use a set to easily add/remove dependents

    def setCell(self, cell: str, value) -> None:
        """
        Set a cell to a raw value (int/float) or a formula string (e.g. "=A1+B2").
        Assuming formula equations do not change once set.
        
        Time Complexity: O(N) where N is the number of cells that depend on this cell (transitively). 
        Because we use eager evaluation, updating a cell triggers a recursive recalculation of all its dependents.
        """
        if value.startswith("="): # It's a "formula" like "=A1+B1"
            self.formula[cell] = value      # remember formula for this cell for future updates
            dep1, dep2, _ = self._parse_formula(value)
            
            # Record dependancies. When any of dep cell is updated, this cell needs to be updated
            self.graph[dep1].add(cell)
            if dep2 is not None:
                self.graph[dep2].add(cell)
            
            # Evaluate the new formula and trigger dependent updates
            self._recalculate(cell)
        else: # It's only value (e.g. "10")
            self.grid[cell] = int(value)
                
            # Because this cell's direct value changed, we must inform its dependents
            self._propagate(cell)

    def getCell(self, cell: str):
        """
        Time Complexity: O(1). Since we used "strict evaluation" to proactive update all cells during setCell!
        getting a cell is just a direct O(1) dictionary lookup.
        """
        return self.grid[cell]

    def _recalculate(self, cell: str):
        """
        Recalculates a cell based on its formula, and stores it in the grid.
        Then, it propagates the update to any cell that depends on it.
        """
        # Basic execution of the saved formula
        if cell in self.formula:
            dep1, dep2, op = self._parse_formula(self.formula[cell])
            
            if dep2 is not None:
                v1, v2 = self.grid[dep1], self.grid[dep2]
                
                match op:
                    case "+":
                        self.grid[cell] = v1 + v2
                    case "-":
                        self.grid[cell] = v1 - v2
                    case _:
                        raise ValueError(f"Unsupported operator: {op}. Only + and - are allowed.")
            else:
                # E.g., formula is "=A1"
                self.grid[cell] = self.grid[dep1]
                
        # Because this cell updated its value, cascade the update forward
        self._propagate(cell)

    def _propagate(self, cell: str):
        """
        Recursively triggers updates for all cells that depend on this one.
        """
        for conn in self.graph[cell]:
            self._recalculate(conn)

    def _parse_formula(self, formula: str):
        """
        Parses formula and returns (cell1, cell2, op) for "=A1+B1" or (cell1, None, None) for "=A1"
        """
        expr = formula[1:].replace(" ", "")  # Strip the '=' and any spaces
        
        # Regex to locate the first math operator
        op_match = re.search(r'[\+\-\*/]', expr)
        
        # Edge Case:If no operator is found, it's just a direct reference (e.g. "=A1")
        if not op_match:
            return (expr, None, None)
        
        op = op_match.group(0)
        cell1, cell2 = expr.split(op)
        return (cell1, cell2, op)