# Nice print stuff
TAB = 4*' '

NLTAB = ',\n'+TAB

HEADER = """\
# -*- coding: %(encoding)s -*-
## File autogenerated by SQLAutoCode
## see http://code.google.com/p/sqlautocode/

from sqlalchemy import *
%(dialect)s
metadata = MetaData()
"""

HEADER_Z3C = """\
# -*- coding: %(encoding)s -*-
## File autogenerated by SQLAutoCode
## see http://code.google.com/p/sqlautocode/
## Export type: z3c.sqlalchemy

from sqlalchemy import *
%(dialect)s
from z3c.sqlalchemy import Model
from z3c.sqlalchemy.mapper import MappedClassBase

def getModel(metadata):
    model = Model()
"""

PG_IMPORT = """\
try:
    from sqlalchemy.dialects.postgresql import *
except ImportError:
    from sqlalchemy.databases.postgres import *
"""

FOOTER_Z3C = """
    return model
"""

FOOTER_EXAMPLE = """
# some example usage
if __name__ == '__main__':
    db = create_engine(%(url)r)
    metadata.bind = db

    # fetch first 10 items from %(tablename)s
    s = %(tablename)s.select().limit(10)
    rs = s.execute()
    for row in rs:
        print row
"""

#I suppose you wondering why here we use list for columns and constraints 
#python have a maximum number of arguments set to 255 ;(
TABLE = """Table('%(name)s', metadata,*[%(columns)s,%(constraints)s]%(schema)s)"""

COLUMN = """Column(%(name)r, %(type)s%(constraints)s%(args)s)"""

FOREIGN_KEY = """ForeignKeyConstraint(%(names)s, %(specs)s, name=%(name)s)"""

INDEX = """Index(%(name)s, %(columns)s, unique=%(unique)s)"""

HEADER_DECL = """#autogenerated by sqlautocode

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

engine = create_engine('%s')
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = engine

"""

EXAMPLE_DECL = """#example on how to query your Schema
from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)()
objs = session.query(%s).all()
print 'All %s objects: %%s'%%objs
"""

INTERACTIVE = """
print 'Trying to start IPython shell...',
try:
    from IPython.Shell import IPShellEmbed
    print 'Success! Press <ctrl-d> to exit.'
    print 'Available models:%%s'%%%s
    print '\\nTry something like: session.query(%s).all()'
    ipshell = IPShellEmbed()
    ipshell()
except:
    'Failed. please easy_install ipython'
"""

CHECK_CONSTRAINT = """CheckConstraint('%(sqltext)s')"""
