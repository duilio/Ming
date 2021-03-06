#{initial-imports
from ming import Session
from ming.datastore import DataStore
from ming.odm import ThreadLocalODMSession

bind = DataStore('mongodb://localhost:27017/', database='odm_tutorial')
doc_session = Session(bind)
session = ThreadLocalODMSession(doc_session=doc_session)
#}

#{odm-imports
from ming import schema
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm import Mapper
from ming.odm.declarative import MappedClass
#}

class WikiPage(MappedClass):
    
    class __mongometa__:
        session = session
        name = 'wiki_page'

    _id = FieldProperty(schema.ObjectId)
    title = FieldProperty(str)
    text = FieldProperty(str)

    comments=RelationProperty('WikiComment')

class WikiComment(MappedClass):

    class __mongometa__:
        session = session
        name = 'wiki_comment'

    _id = FieldProperty(schema.ObjectId)
    page_id = ForeignIdProperty('WikiPage')
    text=FieldProperty(str, if_missing='')

    page=RelationProperty('WikiPage')

def _(): pass
    
#{compileall
Mapper.compile_all()
#}        assert False

WikiPage.query.remove({})
WikiComment.query.remove({})


def snippet1():
    wp = WikiPage(title='FirstPage',
                  text='This is my first page')
    wp
    session
    session.flush()
    session
    session.clear()
    session

def snippet2():
    wp = WikiPage.query.get(title='FirstPage')
    session

    # Verify the IdentityMap keeps only one copy of the object
    wp2 = WikiPage.query.get(title='FirstPage')
    wp is wp2

    # Modify the object in memory
    wp.title = 'MyFirstPage'

    # Notice that the object has been marked dirty
    session
    wp
    session.flush()

    # We can also delete objects
    wp = WikiPage.query.get(title='MyFirstPage')
    wp.delete()
    session
    # Rather than flushing, we'll keep the object
    #   around and just clear the session instead
    session.clear()

def snippet3():
    wp = WikiPage.query.get(title='MyFirstPage')
    # Create some comments
    WikiComment(page_id=wp._id,
                text='A comment')
    WikiComment(page_id=wp._id,
                text='Another comment')
    session.flush()
    session.clear()
    # Load the original page
    wp = WikiPage.query.get(title='MyFirstPage')
    session
    # View its comments
    wp.comments
    session
    wp.comments[0].page
    wp.comments[0].page is wp

def snippet4():
    wp = WikiPage.query.get(title='MyFirstPage')
    results = WikiComment.query.find(dict(page_id=wp._id))
    list(results)
    
def snippet5():
    from ming.odm import mapper
    m = mapper(WikiPage)
    # m.collection is the 'base' Ming document class
    m.collection
    # Retrieve the 'base' Ming session
    session.impl
    
