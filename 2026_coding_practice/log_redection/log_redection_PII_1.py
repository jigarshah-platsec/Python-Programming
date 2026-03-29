import re

def redact_stream(chunks):
    """
    A generator that processes a stream of text chunks, redacting SSNs.
    It uses O(1) memory and handles SSNs split across chunk boundaries.
    """
    buffer = ""
    # Regex for standard 9-digit SSN
    ssn_pattern = re.compile(r'\d{3}-\d{2}-\d{4}')

    for chunk in chunks:
        # STATE MANAGEMENT 
        # Add the new piece to our working buffer
        buffer += chunk
        
        # Redact any fully formed SSNs currently in the buffer
        buffer = ssn_pattern.sub('***-**-****', buffer)
        
        # SLIDING WINDOW of 10 chars in moving live-stream
        # THE MAGIC TRICK: 
        # An SSN is 11 chars max. We can safely 'yield' (send away) 
        # everything EXCEPT the last 10 characters.
        if len(buffer) > 10:
            safe_text = buffer[:-10]
            yield safe_text  # Spit out the safe text!          # PYTHON ITERATORS (SAVES MEMORY!)
            
            # Keep only the last 10 chars for the next loop
            buffer = buffer[-10:] 

    # Once the stream is totally finished, spit out whatever is left
    if buffer:
        yield buffer

# --- How to Test It ---
def main():
    # Notice how the SSN is split exactly across the two chunks!
    incoming_stream = [
        "Hello, my SSN is 123-45", 
        "-6789. Please don't steal it!"
    ]
    
    # We consume the generator
    safe_output = "".join(redact_stream(incoming_stream))
    print(safe_output)
    # Output: Hello, my SSN is ***-**-****. Please don't steal it!

if __name__ == "__main__":
    main()