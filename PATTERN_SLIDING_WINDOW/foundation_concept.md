# Pattern: Sliding Window

## Mental Model
A sublist (window) that slides over an array to find a specific property (e.g., max sum, longest substring).

## Key Patterns
- **Fixed Size:** The window size stays constant. Move both `left` and `right` pointers.
- **Dynamic Size:** The window grows and shrinks based on constraints. Typically, `right` expands and `left` shrinks.
