AutoCode is a flexible tool to autogenerate a model from an existing database.

This is a slightly different approach to SqlSoup, 
that lets you use tables without explicitly defining them.

Requirements:

    sqlalchemy 0.6+

Documentation:

    Call sqlautocode --help for a list of available options.

    Examples:
    
        sqlautocode -o model.py mysql://foo@bar/my_database
        sqlautocode -o model.py -u postgres://postgres:user@password/MyDatabase -s myschema -t Person*,Download

Current Maintainer:
    
    Chris Perkins (percious)
    E-mail: chris@percious.com

    Simon Pamies (spamsch)
    E-Mail: s.pamies at banality dot de
    
    Michael Floering - maintains mirror on GitHub
    github.com/hangtwenty

Authors:

    Paul Johnson (original author)
    
    Christophe de Vienne (cdevienne)
    E-Mail: cdevienne at gmail dot com

    Svilen Dobrev (sdobrev)
    E-Mail: svilen_dobrev at users point sourceforge dot net
    
License:
    
    MIT
    see license.txt

ToDo:

    + Generate ActiveMapper / Elixir model

Notes (random):

    ATT: sqlautocode currently does not handle function indexes well. It generates
    code not understood by sqlalchemy.

    (old) metadata stuff from:
    http://sqlzoo.cn/howto/source/z.dir/tip137084/i12meta.xml

