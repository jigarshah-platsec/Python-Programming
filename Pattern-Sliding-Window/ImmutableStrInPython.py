"""
Immutable Strings in Python: Analysis & Refactoring
--------------------------------------------------
In Python, strings are IMMUTABLE. Every "modification" (like +=) actually 
creates a brand new string object in memory. 

To manipulate strings efficiently (like reversing words), we typically 
convert them to a LIST, perform operations, and then JOIN them back.
"""

def reverse_str(text: str) -> str:
    """Uses Python's slicing magic to reverse a string beautifully."""
    return text[::-1]

def reverse_words_manual(text: str) -> str:
    """
    Reverses the order of words using a clean, manual sliding-window approach.
    This demonstrates how you'd handle the 'mutable' logic by building a new string.
    """
    words = []
    current_word = []
    
    # Loop through the text to extract words
    for char in text:
        if char == " ":
            if current_word:
                words.append("".join(current_word))
                current_word = []
        else:
            current_word.append(char)
            
    # Don't forget the final word!
    if current_word:
        words.append("".join(current_word))
        
    # Reverse the list of words and join with space
    return " ".join(words[::-1])

def reverse_words_pythonic(text: str) -> str:
    """
    The True 'Pythonic' way: Clear, concise, and state-of-the-art.
    .split() handles all whitespace variations automatically.
    """
    return " ".join(text.split()[::-1])

def main():
    test_cases = [
        "Apple is Banana",
        "   Leading spaces",
        "Trailing spaces   ",
        "Multiple   Spaces   In   Between"
    ]
    
    print(f"{'Original':<30} | {'Reversed (Beautifully)':<30}")
    print("-" * 65)
    
    for text in test_cases:
        result = reverse_words_pythonic(text)
        print(f"{text:<30} | {result:<30}")

if __name__ == "__main__":
    main()
