# Basic Python base64 Decoder.
# Can be accomplished in bash with 'echo "string" | base64 -d'

import base64

print(f'\nPython Base64 Decoder\n')
base64_string = input('Enter Base64 String:> ')
base64_bytes = base64_string.encode('ascii')
string_bytes = base64.b64decode(base64_bytes)
plaintext_string = string_bytes.decode('ascii')

print('\nPlaintext String:> ', plaintext_string)