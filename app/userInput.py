import re  # Python's built-in regular expression module
import math
from decimal import Decimal

soundMap = ['AEIOUWYH',
            'BFPV',
            'CGJKQSXZ',
            'DT',
            'L',
            'MN',
            'R']  # Original soundex map

# Graph of keys on a QWERTY keyboard to resolve accidental miss-entering of keys
keyGraph = dict(a='qwez', b='vghn', c='xdfv ', d='sferxc', e='wsdfr', f='dgrcv', g='fthvb',
                h='gjybn', i='uojk', j='hkunm', k='jlim', l='kop', m='jkn', n='bhjm', o='ipkl', p='okl',
                q='was', r='etfdg', s='adwzx', t='rygfh', u='yijhk', v='fgcb ',
                w='qes', x='zcsd', y='tugh', z='xas')

synonyms = [
    ["net", "total", "resultant", "sum"],
    ["equals", "cancel out", "cancels out", "equal to"],
    [" per ", " / ", " \\  ", " divided by "],
    [" x ", " times ", " multiplied by "],
    [" energy ", " work done ", " work ", " wd "],
    [" rate of change ", " gradient ", " slope "],
    [" kinetic energy ", "  ke ", " ekin "],
    ["increases", "gets bigger"],
    ["decreases", "reduces", "gets smaller"],
    ["particle", "molecule"],
    ["squared", "^2"],
    [" is 0", " is zero"],
    ["mass", "weight"]
]

# Returns how many significant figures a float is given to
def getSF(number):
    if number == 0:
        return 1  # Special case

    digits = str(number).replace("." or "-", "")
    sf = 0
    for digit in digits:
        if digit in "123456789" or sf > 0:
            sf += 1
    return sf

# Rounds a given float to a given number of significant figures
def roundSF(number, sf=3):
    if number == 0:
        return 0 # Special case; log(0) is undefined
    shift = math.floor(math.log10(abs(number)))+2-sf  # Number of places to shift decimal place
    normalised = number/(10**shift)  # Gets X0XX0X.Y format where Y is the last significant digit
    rounded = round(normalised, 1)*(10**shift)  # Rounds shifted number using built-in function then undos shift
    return rounded

# Checks if text is a single word
def isWord(text):
    return len(text.split()) == 1 and text.split()[0].isalpha()

# Returns lower case and replaces synonyms
def normalise(text):
    text = text.lower()
    text = re.sub(r'[^a-z\+\-\\/]+', ' ', text)

    while "  " in text:
        text.replace("  ", " ")

    if len(text) > 0 and text[0] == " ":
        text = text[1:]

    if len(text) > 0 and text[-1] == " ":
        text = text[:-1]

    for group in synonyms:
        for synonym in group[1:]:
            text = text.replace(synonym, group[0])

    return text

# Generates (improved) soundex code for a given word
def soundex(word):
    if word == '' or not isinstance(word, str):
        return ''

    word = word.upper()  # Capitalises word
    word = re.sub(r'[^A-Z]+', '', word)  # Removes everything that's not a letter
    word = re.sub(r'PH', 'F', word)  # PH --> F
    word = re.sub(r'TH', 'D', word)  # TH --> D
    word = re.sub(r'.GH', 'T', word)  # GH --> T where GH are not the first letters (ie Ghost)
    word = re.sub(r'TION', 'SION', word)  # TION --> SION
    if re.match(r'(KN)|(GN)|(PN)|(AE)|(WR)', word):  # Uses regex match to removes first letter if silent
        word = word[1:]

    if len(word) < 2:
        return word

    # Replaces letters using group code from sound map
    code = str()
    previousGroup = None
    for letter in word:
        group = 0
        while letter not in soundMap[group]:
            group += 1
        if 0 != group != previousGroup:
            code += str(group)
            previousGroup = group

    '''for letter in word:
        for group in soundMap:
            if letter in group:
                soundex += str( soundMap.index(group) )
                break

    soundex = soundex.replace('0', '') # Removes 0s
    for sound in soundex:
        soundex = soundex.replace(sound*2, sound) # Removes duplicates of all length'''

    return word[0] + code[1:]  # Retains first letter of 'word'


# Identifies if a word has been miss-entered
def isTypo(word, goal, depth=2):

    if word == goal:
        return True
    elif depth < 1:
        return False

    aa = str()
    bb = str()
    word = re.sub(r'[^a-z]+', '', word)
    word = ''.join(sorted(set(word.lower())))
    goal = ''.join(sorted(set(goal.lower())))
    for a, b in zip(word, goal):
        if a != b:
            aa += a
            bb += b

    if abs(len(word) - len(goal)) > (len(word) + len(goal)) // 4:
        return False

    #f len(aa) < 2:
        #return True

    for a in aa:
        for i in range(len(keyGraph[a])):
            if isTypo(aa.replace(a, keyGraph[a][i], 1), bb, depth - 1):  # Recursive call
                return True

    return False
