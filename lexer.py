"""
This modules uses David M. Beazley ply.lex modules to implement a `PGN
<https://en.wikipedia.org/wiki/Portable_Game_Notation>`_ lexer.

It may be inaccurate in more than one places but works pretty well for PGNs
found in the wild.
"""
import ply.lex as lex


tokens = ('STRING',
          'LEFT_BRACKET',
          'RIGHT_BRACKET',
          'LEFT_PARENTHESIS',
          'RIGHT_PARENTHESIS',
          'LEFT_BRACE',
          'RIGHT_BRACE',
          'REST_OF_LINE_COMMENT',
          'NAG',
          'TAG',
          'MOVENO',
          'SAG',
          'COMMENT',
          'RESULT')
states = (('comment', 'exclusive'), )


def t_comment(t):
    r'\{'
    t.lexer.push_state('comment')


def t_comment_RIGHT_BRACE(t):
    r'\}'
    t.lexer.pop_state()


def t_comment_COMMENT(t):
    r'[^}]+'
    t.value = t.value.replace('\n', ' ')
    return t


t_comment_ignore = '\r\t\n'


def t_comment_error(t):
    """Error handler in `comment` state"""
    raise Exception("Illegal character '%s'" % t.value[0])


check = r'[+#]'
board_rank = r'[1-8]'
board_file = r'[a-h]'
piece = r'[NBRQK]'

promotion = r'x?{board_file}[18]=(?!K){piece}'.format(
    board_file=board_file,
    piece=piece,
    check=check)
pawnmove = r'(?:{board_file}?x)?{board_file}(?![18]){board_rank}'.format(
    board_file=board_file, board_rank=board_rank)

standardmove = r'{piece}{board_file}?{board_rank}?x?{board_file}{board_rank}'
standardmove = standardmove.format(
    piece=piece,
    board_file=board_file,
    board_rank=board_rank)
castling = r'O-O(?:-O)?'


t_TAG = r'[A-Za-z]+'
t_STRING = r'".{,253}"'
t_LEFT_BRACKET = r'\['
t_RIGHT_BRACKET = r'\]'
# Parenthesis enclose a 'Movetext RAV (Recursive Annotation Variation)
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_REST_OF_LINE_COMMENT = r';.*'
# Angle brackets are defined in the PGN spec for 'future' expansion. A future
# that up to now has never come.
# t_LEFT_ANGLE_BRACKET = r'<'
# t_RIGHT_ANGLE_BRACKET = r'>'
t_MOVENO = r'\d+\.(\.\.)?'
# NAGs (Numeric Annotation Glyphs) should be a numeric code in the range 0-255
# prefixed by a '$' but a comination of '!' and '$' is often found.
t_NAG = r'\$1[0-9][0-9]|\$2[0-4][0-9]|\$25[0-5]|\$[1-9][0-9]|\$[1-9]|[!\?]{1,2}'
t_SAG = r'(?:{promotion}|{pawnmove}|{standardmove}|{castling}){check}?'.format(
    promotion=promotion,
    pawnmove=pawnmove,
    standardmove=standardmove,
    castling=castling,
    check=check)
t_RESULT = r'1-0|0-1|1/2-1/2|\*'
t_ignore = ' \r\t\n'


def t_error(t):
    """General token error handler"""
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


def tokenize(data):
    """Tokenizes a PGN text passed as string.

    Example::

        with open('filename.pgn') as pgn_file:
            pgn_text = pgn_file.read()

        tokens = tokenize(pgn_text)

    .."""
    lexer = lex.lex()
    lexer.input(data)
    parsed_tokens = []

    while True:
        tok = lexer.token()
        if tok:
            parsed_tokens.append(tok)
        else:
            break
    return parsed_tokens
