import re  # Python's built-in regular expression module

sound_map = [ 'AEIOUWYH',
              'BFPV',
              'CGJKQSXZ',
              'DT',
              'L',
              'MN',
              'R' ]  # Original soundex map

# Graph of keys on a QWERTY keyboard to resolve accidental miss-entering of keys
key_graph = dict( a='qwez', b='vghn', c='xdfv ', d='sferxc', e='wsdfr', f='dgrcv', g='fthvb', h='gjybn',
                  i='uojk', j='hkunm', k='jlim', l='kop', m='jkn', n='bhjm', o='ipkl', p='okl',
                  q='was', r='etfdg', s='adwzx', t='rygfh', u='yijhk', v='fgcb ', w='qes', x='zcsd',
                  y='tugh', z='xas' )


# Generates (improved) soundex code for a given word
def soundex( word ):
    if word == '' or not isinstance( word, str ):
        return ''

    word = word.upper( )  # Capitalises word
    word = re.sub( r'[^A-Z]+', '', word )  # Removes everything that's not a letter
    word = re.sub( r'PH', 'F', word )  # PH --> F
    word = re.sub( r'TH', 'D', word )  # TH --> D
    word = re.sub( r'.GH', 'T', word )  # GH --> T where GH are not the first letters (ie Ghost)
    word = re.sub( r'TION', 'SION', word )  # TION --> SION
    if re.match( r'(KN)|(GN)|(PN)|(AE)|(WR)', word ):  # Uses regex match to removes first letter if silent
        word = word[ 1: ]

    if len( word ) < 2:
        return word

    # Replaces letters using group code from sound map
    code = str( )
    previous_group = None
    for letter in word:
        group = 0
        while letter not in sound_map[ group ]:
            group += 1
        if 0 != group != previous_group:
            code += str( group )
            previous_group = group

    '''for letter in word:
        for group in sound_map:
            if letter in group:
                soundex += str( sound_map.index(group) )
                break

    soundex = soundex.replace('0', '') # Removes 0s
    for sound in soundex:
        soundex = soundex.replace(sound*2, sound) # Removes duplicates of all length'''

    return word[ 0 ] + code[ 1: ]  # Retains first letter of 'word'

# Identifies if a word has bee miss-entered
def mistype( word, goal, depth ):
    #print('   '*(len(word)*depth-depth), word, ' ', goal)
    if word == goal:
        return True
    elif depth < 1:
        return False

    aa = str( )
    bb = str( )
    word = re.sub( r'[^a-z]+', '', word )
    word = ''.join( sorted( set( word ) ) )
    goal = ''.join( sorted( set( goal ) ) )
    for a, b in zip( word, goal ):
        if a != b:
            aa += a
            bb += b

    if len( aa ) < 2:
        return True

    for a in aa:
        for i in range( len(key_graph[ a ] ) ):
            if mistype( aa.replace( a, key_graph[ a ][ i ], 1 ), bb, depth - 1 ):  # Recursive call
                return True

    return False

