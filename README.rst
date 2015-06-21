pgnlexer
========


This modules uses David M. Beazley ply.lex modules to implement a `PGN
<https://en.wikipedia.org/wiki/Portable_Game_Notation>`_ lexer.

It may be inaccurate in more than one places but works pretty well for PGNs
found in the wild.
    
Example usage::

    import lexer

    with open('filename.pgn') as pgn_file:
        pgn_text = pgn_file.read()
    
    tokens = lexer.tokenize(pgn_text)

..
