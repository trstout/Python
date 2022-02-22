# Python 3 MD5 Brute Force String Extractor

import hashlib
import sys
import datetime

start = datetime.datetime.now()

def error(msg)     : print('\n[!] ' + msg)
def errorExit(msg) : raise SystemExit('[!] ' + msg)

def md5(string): 
    return hashlib.md5(string.encode()).hexdigest()

def xpermutation(characters, size):
    if size == 0:
        yield []
    else:
        for x in range(len(characters)):
            for y in xpermutation(characters[:x] + characters[x:], size - 1):
                yield [characters[x]] + y


def brute(hash):
    attempt = 0
    characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    maxLen = range(0,25)
    stringmaker = ''
    for length in maxLen:
        for x in xpermutation(characters, length):
            permutation = stringmaker + ''.join(x)
            attempt += 1
            if md5(permutation) == hash:
                end_time = str(datetime.datetime.now() - start).split('.')[0]
                print('[' + str(attempt) + '] == ' + permutation)
                print('\n\nMD5 Hash Cracked!\n\nString \'' + permutation + '\' extracted from md5sum \'' + hash + '\' in ' + end_time + '.')
                input('\nPress <ENTER> to Quit.')
                sys.exit()
            else:
                print('[' + str(attempt) + '] != ' + permutation)
    errorExit('Failed. Exiting.')


if len(sys.argv) == 2:
    if len(sys.argv[1]) == 32 and sys.argv[1].isalnum():
        brute(sys.argv[1])
    else:
        error('Invalid MD5 hash - must be 32 alphanumeric characters.')
        errorExit('Syntax: python3 md5crack3r.py <md5sum>')
else:
    error('Missing command line arguments.')
    errorExit('Syntax: python3 md5crack3r.py <md5sum>')