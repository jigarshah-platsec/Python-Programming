"""
Question-1 Given 1D string consisting of elements ('X', 'Y', 'O'). Find the minimum distance between X and Y.

Example : Input = "XOXOXXOOYOXO", output = 2

Question-2 Given 2D string consisting of elements ('X', 'Y', 'O'). Find the minimum distance between X and Y. Distance is calculated using manhattan distance.

Example : Input = [["XOO", "OOY", "OOY"]], output = 3
"""
def min_distance(input: str) -> int:
    # If both X and Y doesn't exists
    xPos, yPos = -1, -1
    localMin, globalMin = float('inf'), float('inf')

    for i, c in enumerate(input):
        if c == 'X':
            xPos = i        # Update latest pos of X
        elif c == 'Y':
            yPos = i        # Update latest pos of Y
        else:
            continue

        # Hisab if "X" or "Y"
        if xPos != -1 and yPos != -1:
            localMin = abs(xPos - yPos)
            globalMin = min(localMin, globalMin)


    return globalMin 


def min_distance_2D(input: str) -> int:
    # If both X and Y doesn't exists
    xPos, yPos = (-1, -1), (-1, -1)
    localMin, globalMin = float('inf'), float('inf')

    for row, rowChar in enumerate(input):
        for col, colChar in enumerate(input[row]):
            if colChar == 'X':
                xPos = (row, col)        # Update latest pos of X
            elif colChar == 'Y':
                yPos = (row, col)        # Update latest pos of Y
            else:
                continue

            # Hisab if "X" or "Y"
            if xPos != (-1, -1) and yPos != (-1, -1):
                localMin = abs(xPos[0] - yPos[0]) + abs(xPos[1] - yPos[1])
                globalMin = min(localMin, globalMin)


    return globalMin 

def main():
    assert min_distance("XOXOXXOOYOXO") == 2
    assert min_distance("XOXYXXOOYOXO") == 1

    assert min_distance_2D(["XOO", "OOY", "OOY"]) == 3


if __name__ == "__main__":
    main()