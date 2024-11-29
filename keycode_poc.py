# Python Keypress Encoding POC,

def text_to_keypad(text):
    # Dictionary mapping letters to keypad numbers
    keypad = {
        'a': '2', 'b': '22', 'c': '222',
        'd': '3', 'e': '33', 'f': '333',
        'g': '4', 'h': '44', 'i': '444',
        'j': '5', 'k': '55', 'l': '555',
        'm': '6', 'n': '66', 'o': '666',
        'p': '7', 'q': '77', 'r': '777', 's': '7777',
        't': '8', 'u': '88', 'v': '888',
        'w': '9', 'x': '99', 'y': '999', 'z': '9999',
        ' ': '0'
    }
    # Convert text to lowercase and encode each character
    result = ''
    for char in text.lower():
        if char in keypad:
            if result and result[-1] == keypad[char][0]:
                result += ' '  # Add space between same-key sequences
            result += keypad[char]
        else:
            result += char
    return result
 
# Example usage
text = "hello world"
encoded = text_to_keypad(text)
print(f"Original: {text}")
print(f"Encoded: {encoded}")
