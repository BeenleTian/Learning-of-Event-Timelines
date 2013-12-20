from lxml import etree
from copy import deepcopy

class Text():
    def __init__(self, id=None, name=None):
        self.id = None
        self.name = name
        self.relations_union_count = 0
        self.relations_intersection_count = 0
        self.annotator = []
        self.relations_union = []
        self.relations_intersection = []
        self.events_union = []

    def set_annotator(self, annotator):
        self.annotator.append(annotator)

    """Since different annotators annotate different events we might
    be interested in the union of all events for a textfile"""
    def compute_union_events(self):
        del self.events_union[:]

        all_in_one = []
        for ann in self.annotator:
            all_in_one = all_in_one + ann.events

        # x if the word contained in x is not already in our list of words so far
        self.events_union = [x for i, x in enumerate(all_in_one) if x.content not in [y.content for y in all_in_one[:i]]]

    """Since different annotators annotate different relations we might
    want to know which relations all annotators for a textfile have in common (intersection)"""
    def compute_intersection_relations(self):
        del self.relations_intersection[:]
        self.relations_intersection_count = 0

        relations = []
        relations_tmp = []

        for rel in self.annotator[0].relations:
            relations_tmp.append(rel)

        for ann in self.annotator[1:]:
            # Add rel to list if we have rel already in relations_tmp[]
            for rel in ann.relations:
                if rel.identifier in [x.identifier for x in relations_tmp]:
                    relations.append(rel)

            del relations_tmp[:]
            relations_tmp = deepcopy(relations)

        self.relations_intersection = relations
        self.relations_intersection_count = len(self.relations_intersection)

    """Union over all relations annotated in a certain textfile"""
    def compute_union_relations(self):
        del self.relations_union[:]
        self.relations_union= 0

        # Put all relations from all annotators in one list
        relations = []
        for ann in self.annotator:
            for rel in ann.relations:
                relations.append({rel.identifier : rel})

        # Go through all relations and add a relation to a list if
        # the identifier of the relation is not already in the list
        union = []
        for r in relations:
            if r.keys()[0] not in [x.keys()[0] for x in union]:
                union.append(r)

        self.relations_union = [x.values()[0] for x in union]
        self.relations_union_count = len(self.relations_union)

class Event():
    def __init__(self, parent=None, id=None, content=None, begin=None, end=None):
        self.parent = parent
        self.id = id
        self.content = content
        self.begin = begin
        self.end = end


class Relation():
    def __init__(self, parent=None, source=None, target=None, time_type=None):
        self.parent = parent
        self.source = source
        self.target = target
        self.identifier = None

        if time_type in ["same_as", "overlap", "after", "is_contained_in", "before", "contains"]:
            self.time_type = time_type
        else:
            self.time_type = None

    def set_time_type(self, time_type):
        if time_type in ["same_as", "overlap", "after", "is_contained_in", "before", "contains"]:
            self.time_type = time_type
        else:
            self.time_type = None

    def set_identifier(self, source_begin, source_end, target_begin, target_end):
        self.identifier = source_begin+source_end+target_begin+target_end


class Annotator():
    def __init__(self, id=None, xml_id=None):
        self.parent = None
        self.events = []
        self.relations = []
        self.id = id
        self.xml_id = xml_id


class Holder():
    textfiles = []


def parseXML(filename):
    tree = etree.parse(filename)
    root = tree.getroot()

    data = Holder()

    for i, txt in enumerate(root.iterdescendants("file")):
        # Create Text object
        text = Text(i, txt.get("name"))

        for j, ann in enumerate(txt.iterdescendants("annotator")):
            # Create an Annotator object
            annotator = Annotator(j, ann.get("id"))
            annotator.parent = text

            # Create link from Text object
            text.set_annotator(annotator)

            for k, ev in enumerate(ann.iterdescendants("event")):
                # Create an Event object
                event = Event(annotator, k, ev.get("text"), ev.get("begin"), ev.get("end"))
                # Create link from Annotator object
                annotator.events.append(event)

            for k, tlink in enumerate(ann.iterdescendants("tlink")):
                # Create a Relation object
                relation = Relation()
                relation.parent = annotator
                relation.id = k
                relation.set_time_type(tlink[0].get("type"))

                # Create link from Annotator object
                annotator.relations.append(relation)

                # Lets figure out which events we have
                source = tlink[1]
                begin = source.get("begin")
                end = source.get("end")

                # Search through the events of this annotator
                for event in annotator.events:
                    if event.begin == begin and event.end == end:
                        relation.source = event
                        break

                target = tlink[2]
                begin = target.get("begin")
                end = target.get("end")

                for event in annotator.events:
                    if event.begin == begin and event.end == end:
                        relation.target = event
                        break

                # Identifier, so we can identify two relations which are the same
                relation.set_identifier(relation.source.begin, relation.source.end, relation.target.begin, relation.target.end)

        # Include text to data structure
        data.textfiles.append(text)

    return data