import unittest
import app.userInput


class test_userInput(unittest.TestCase):
    def test_soundex(self):
        assert isinstance(app.userInput.soundex('foo'), str), 'Not generating string'
        assert app.userInput.soundex(1337) == '', 'Fails for numerical input'
        assert app.userInput.soundex('1337^!£$%^&*()') == '', 'Fails for non-alphanumerical input'
        assert app.userInput.soundex('') == '', 'Fails for empty string'

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
                     ('einstein', 'einstain')]

        for group in spellings:
            correct = app.userInput.soundex(group[0])
            for misspelling in group[1:]:
                assert app.userInput.soundex(misspelling) == correct, \
                    'Fails to detect ' + misspelling + ' as ' + group[0]

        faslePositives = [('tochi', 'torch'),
                          ('yousef', 'humza'),
                          ('distance', 'displacement'),
                          ('ghoust', 'toast')]

        for group in faslePositives:
            correct = app.userInput.soundex(group[0])
            for false in group[1:]:
                assert not app.userInput.soundex(false) == correct, \
                    'Incorrectly identifies ' + false + ' as ' + group[0]

    def test_isTypo(self):
        assert isinstance(app.userInput.isTypo('foo', 'bar'), bool), 'Not returning boolean value'

        typos = [('acceleration', 'avceleration'),
                 ('force', 'dorrce', 'foyrce'),
                 ('distance', 'dristance', 'distnace')]

        faslePositives = [('yousef', 'humza'),
                          ('distance', 'displacement'),
                          ('gravity', 'gravide')]

        for typo in typos:
            correct = typo[0]
            for mistype in typo[1:]:
                assert app.userInput.isTypo(mistype, correct), \
                    'Fails to identify ' + mistype + ' as ' + correct

        for group in faslePositives:
            correct = group[0]
            for false in group[1:]:
                assert not app.userInput.isTypo(false, correct), \
                    'Incorrectly identifies ' + false + ' as ' + group[0]


if __name__ == '__main__':
    unittest.main()
