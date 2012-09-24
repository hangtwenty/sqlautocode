import sys
import config, util, constants
from util import emit
from declarative import ModelFactory

def emit_table(indent, db, options, table):
    """Emit table representation."""
    emit('%s%s%s%s = %r' % (indent, options.table_prefix, table.name, options.table_suffix, table))
    emit_index(indent, db, options, table)

def emit_z3c_objects(indent, db, options, table):
    emit_table(indent, db, options, table)
    emit(indent + ('class %(tn)sObject(MappedClassBase): pass\n'
                    '%(tab)smapper(%(tn)sObject, %(tn)s)') % {'tn':table.name, 'tab':indent})

def emit_index(indent, db, options, table):
    """docstring for emit_index"""
    if not options.noindex:
        indexes = []
        if not table.indexes:
            # for certain dialects we need to include index support
            if hasattr(db.dialect, 'indexloader'):
                indexes = db.dialect.indexloader(db).indexes(table)
            else:
                print >>config.err, 'It seems that this dialect does not support indexes!'
        else:
            indexes = list(table.indexes)
        emit(*[indent + repr(index) for index in indexes])

def main():
    config.configure()

    options = config.options
    if options.declarative:
        config.interactive = None
        if options.interactive:
            config.interactive = True
        config.schema = None
        if options.schema:
            config.schema = options.schema
        config.example=False
        if options.example:
            config.example=True
        factory = ModelFactory(config)
        emit(repr(factory))
        config.out.close()
        config.out = sys.stdout
        print >>config.err, "Output written to %s" % options.output
        return

    import formatter
    formatter.monkey_patch_sa()
    
    import sqlalchemy
    from sqlalchemy.engine.reflection import Inspector
    db, options = config.engine, config.options
    metadata = sqlalchemy.MetaData(db)

    print >>config.err, 'Starting...'
    conn = db.connect()
    inspector = Inspector.from_engine(conn)

    if options.schema != None:
        reflection_schema=options.schema
    else:
        try:
            reflection_schema = inspector.default_schema_name
        except NotImplementedError:
            reflection_schema = None

    tablenames = inspector.get_table_names(reflection_schema)

    # fixme: don't set up output until we're sure there's work to do!
    if options.tables:
        subset, missing, unglobbed = util.glob_intersection(tablenames,
                                                            options.tables)
        for identifier in missing:
            print >>config.err, 'Table "%s" not found.' % identifier
        for glob in unglobbed:
            print >>config.err, '"%s" matched no tables.' % glob
        if not subset:
            print >>config.err, "No tables matched!"
            sys.exit(1)

        tablenames = subset

    # some header with imports
    if options.generictypes:
        dialect = ''
    else:
        d1 = 'from sqlalchemy.databases.%s import *\n' % db.name
        d2 = 'from sqlalchemy.dialects.%s import *\n' % db.name
        #Determine with one is correct...
        dialect = util.select_imports([d1, d2])
    
    header = options.z3c and constants.HEADER_Z3C or constants.HEADER
    emit(header % {'dialect': dialect, 'encoding': options.encoding})

    for tname in tablenames:
        print >>config.err, "Generating python model for table %s" % (
            util.as_sys_str(tname))

        table = sqlalchemy.Table(tname, metadata, schema=reflection_schema, autoload=True)
        if options.schema is None:
            # we're going to remove the schema from the table so that it
            #  isn't rendered in the output.  If we don't put back the
            #  correct value, it may cause errors when other tables reference
            #  this one.
            original_schema = table.schema
            table.schema = None
        else:
            original_schema = options.schema

        indent = ''

        INC = '\n\n'
        emit(INC)
        if options.z3c:
            emit_z3c_objects(constants.TAB, db, options, table)
        else:
            emit_table('', db, options, table)

        table.schema = original_schema

    if options.z3c:
        emit(constants.FOOTER_Z3C)

    # print some example
    if options.example:
        emit('\n' + constants.FOOTER_EXAMPLE % {
            'url': unicode(db.url), 'tablename': tablenames[0]})

    if options.output:
        emit('\n')
        config.out.close()
        config.out = sys.stdout
        print >>config.err, "Output written to %s" % options.output

# vim:ts=4:sw=4:expandtab
