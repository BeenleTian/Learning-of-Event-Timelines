from lxml import etree
from copy import deepcopy
from feature.preprocessing.text import get_sentence, get_surrounding
from feature.preprocessing.polarity import get_polarity
from feature.preprocessing.modality import get_modality
from parsexml.event import Event
from parsexml.text import Text
from parsexml.relation import Relation
from parsexml.annotator import Annotator

class Holder():
    """Holds all text objects."""
    textfiles = []


def parse_XML(filename, dirname):
    """Takes xml filename and name of directory as arguments an returns all Text objects bundled in a Holder instance."""
    tree = etree.parse(filename)
    root = tree.getroot()

    data = Holder()

    for i, txt in enumerate(root.iterdescendants("file")):
        # Create Text object
        text = Text(i, txt.get("name"))

        for j, ann in enumerate(txt.iterdescendants("annotator")):
            # Create an Annotator object
            annotator = Annotator(j, text, ann.get("id"))

            # Create link from Text object
            text.append_annotator(annotator)

            for k, ev in enumerate(ann.iterdescendants("event")):
                event_text = ev.get("text")

                # Get the surrounding text and sentence for this event
                sentence, num_words_as_event_before_event = get_sentence(event_text, text.name, dirname, int(ev.get("begin")))
                surrounding = get_surrounding(event_text, text.name, dirname, int(ev.get("begin")), Event.surrounding_words_left, Event.surrounding_words_right)

                pos_surrounding = get_surrounding(event_text, text.name, dirname, int(ev.get("begin")), Event.pos_surrounding_words_left, Event.pos_surrounding_words_right)
                # Get the polarity of the event
                polarity = get_polarity(surrounding)

                # Get the modality of the event
                modality = get_modality(surrounding)

                # Create an Event object
                event = Event(annotator, k, event_text, sentence, num_words_as_event_before_event, surrounding, pos_surrounding, polarity, modality, ev.get("begin"), ev.get("end"))
                # Create link from Annotator object
                annotator.events.append(event)

            for k, tlink in enumerate(ann.iterdescendants("tlink")):
                # Connect corresponding event objects to this relation object
                # Doing this by going through all possible events
                source = tlink[1]
                begin = source.get("begin")
                end = source.get("end")

                # Search through the events of this annotator
                source_event = None
                for event in annotator.events:
                    if event.begin == int(begin) and event.end == int(end):
                        source_event = event
                        break

                target = tlink[2]
                begin = target.get("begin")
                end = target.get("end")

                target_event = None
                for event in annotator.events:
                    if event.begin == int(begin) and event.end == int(end):
                        target_event = event
                        break

                # Create a Relation object
                temporal_relation = tlink[0].get("type")

                relation = Relation(annotator, source_event, target_event, temporal_relation)

                # Create link from Annotator object
                annotator.relations.append(relation)

        # Include text to data structure
        data.textfiles.append(text)

    # Create Text_structure objects, remove not needed relations and then all other possible relations
    for text in data.textfiles:
        for ann in text.annotator:
            ann.create_text_structure()
            ann.remove_none_relations()
            ann.create_other_relations()

    return data
