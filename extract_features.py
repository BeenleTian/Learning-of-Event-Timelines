from parser import parseXML

TEXTDIR = "McIntyreLapata09Resources/fables"

class Feature:
    def __init__(self, relation):
        self.relation = relation

    # Returns the number of characters between two events in a text
    def get_distance(self):
        # We want to compare different objects
        if self.relation.source == self.relation.target:
            return False
        # The two events have to be in the same file
        if self.relation.source.parent.parent != self.relation.target.parent.parent:
            return False

        # Distance is measured in characters between the end of the first word and the beginning of the second word
        if self.relation.source.begin > self.relation.target.begin:
            return (self.relation.source.begin - self.relation.target.end)
        elif self.relation.source.begin < self.relation.target.begin:
            return (self.relation.target.begin - self.relation.source.end)

    # Returns number which represents the time relation type
    def get_category(self):
        # same_as: 0, overlap: 1, after: 2, is_contained_in: 3, before: 4, contains: 5, includes: 6, is_included: 7
        if self.relation.time_type == "same_as":
            return 0
        elif self.relation.time_type == "overlap":
            return 1
        elif self.relation.time_type == "after":
            return 2
        elif self.relation.time_type == "is_contained_in":
            return 3
        elif self.relation.time_type == "before":
            return 4
        elif self.relation.time_type == "contains":
            return 5
        elif self.relation.time_type == "includes":
            return 6
        elif self.relation.time_type == "is_included":
            return 7

    # Returns 1 if the feature is in the category we want and 0 otherwise
    def get_result(self, category):
        if self.relation.time_type == category:
            return 1
        else:
            return 0

if __name__ == "__main__":
    data = parseXML("training.xml")

    for txt in data.textfiles:
        txt.compute_union_relations()
        for rel in txt.relations_union:
            f = Feature(rel)
            print f.get_distance(), f.get_category()