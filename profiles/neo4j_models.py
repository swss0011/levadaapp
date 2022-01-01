from neomodel import StructuredRel, StructuredNode, RelationshipTo, RelationshipFrom
from neomodel import (StringProperty, BooleanProperty, FloatProperty, IntegerProperty, ArrayProperty, JSONProperty, DateTimeProperty, UniqueIdProperty)
import neomodel

#Models
class Male(StructuredNode):
    node_id        = StringProperty(required=True)
    address        = StringProperty(required=True)
    born           = StringProperty(required=True)
    dead           = StringProperty(required=True)
    treeid         = StringProperty(required=True)
    copyid         = StringProperty(required=True)
    
    first_name     = StringProperty(required=True)
    last_name      = StringProperty(required=True)
    to_son         = RelationshipTo('Male', 'FATHER_TO_SON')
    to_daughter    = RelationshipTo('Female', 'FATHER_TO_DAUGHTER')
    from_father    = RelationshipFrom('Male', 'FATHER_TO_SON', cardinality=neomodel.cardinality.ZeroOrOne)
    from_mother    = RelationshipFrom('Female', 'MOTHER_TO_SON', cardinality=neomodel.cardinality.ZeroOrOne)

class Female(StructuredNode):
    node_id        = StringProperty(required=True)
    address        = StringProperty(required=True)
    born           = StringProperty(required=True)
    dead           = StringProperty(required=True)
    treeid         = StringProperty(required=True)
    copyid         = StringProperty(required=True)

    first_name     = StringProperty(required=True)
    last_name      = StringProperty(required=True)
    to_son         = RelationshipTo('Male', 'MOTHER_TO_SON')
    to_daughter    = RelationshipTo('Female', 'MOTHER_TO_DAUGHTER')
    from_father    = RelationshipFrom('Male', 'FATHER_TO_DAUGHTER', cardinality=neomodel.cardinality.ZeroOrOne)
    from_mother    = RelationshipFrom('Female', 'MOTHER_TO_DAUGHTER', cardinality=neomodel.cardinality.ZeroOrOne)