import app.user_input


def test_soundex():
    assert isinstance( app.user_input.soundex( 'foo' ), str ), 'Not generating string'
    assert app.user_input.soundex( 1337 ) == '', 'Fails for numerical input'
    assert app.user_input.soundex( '1337^!£$%^&*()' ) == '', 'Fails for non-alphanumerical input'
    assert app.user_input.soundex( '' ) == '', 'Fails for empty string'

    spellings = [('accommodate', 'accomodate'),
                 ('achieve', 'acheive'),
                 ('caribbean', 'carribian'),
                 ('necesary', 'neccessary'),
                 ('tochi', 'tochu', 'toku', 'tochey'),
                 ('humza', 'hamza', 'hamsa'),
                 ('yousuf', 'yoesef', 'yuusuf'),
                 ('harte', 'hart', 'heart'),
                 ('proportional', 'porporsional'),
                 ('thought', 'thaut'),
                 ('einstein', 'einstain') ]

    for group in spellings:
        correct = app.user_input.soundex( group[0 ] )
        for misspelling in group[1:]:
            assert app.user_input.soundex( misspelling ) == correct, 'Fails to detect ' + misspelling + ' as ' + group[0 ]

    fasle_positives = [('tochi', 'torch'),
                       ('yousef', 'humza'),
                       ('distance', 'displacement'),
                       ('ghoust', 'toast')]

    for group in fasle_positives:
        correct = app.user_input.soundex( group[0 ] )
        for false in group[1:]:
            assert not app.user_input.soundex( false ) == correct, 'Incorrectly identifies ' + false + ' as ' + group[0 ]

    print('app.user_input.soundex() passed all tests!')

def test_mistype():
    assert isinstance(app.user_input.mistype('foo', 'bar', 2), bool), 'Not returning boolean value'

    typos = [('acceleration', 'avceleration'),
             ('force', 'dorrce', 'foyrce'),
             ('distance', 'dristance', 'distnace')]

    fasle_positives = [('yousef', 'humza'),
                       ('distance', 'displacement'),
                       ('gravity', 'gravide')]

    for typo in typos:
        correct = typo[0]
        for mistype in typo[1:]:
            assert app.user_input.mistype(mistype, correct, 2), 'Fails to identify '+mistype+' as '+correct

    for group in fasle_positives:
        correct = group[0]
        for false in group[1:]:
            assert not app.user_input.mistype(false, correct, 2), 'Incorrectly identifies ' + false + ' as ' + group[0 ]

    print('app.user_input.mistype() has passed all tests!')



test_soundex()
test_mistype()

