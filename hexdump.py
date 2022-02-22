# Testing hexdump function from pycat.

HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    # Decode bytes if byte string is passed in.
    if isinstance(src, bytes):
        src = src.decode()

    results = list()
    for i in range(0, len(src), length):
        # Grabbing piece of string to dump and put into 'word' variable.
        word = str(src[i:i+length])

        # Built-in 'translate' function subs string representation of char for
        # corresponding char in raw string.
        printable = word.translate(HEX_FILTER)
        # Sub hex representation of int value of char in raw string.
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexwidth = length*3
        # Create new array to hold strings holding hex value of index of first byte in word,
        # hex value of word, and printable representation.
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results
        
# String to dump as hex goes here.
hexdump('How much dump can a hexdump dump if a hex dump could dump hex')