from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from extract_features import Feature
from parser import parseXML
from helper import get_stem_class

# Create numpy array with samples and targets
data = parseXML("fables-100-temporal-dependency.xml", "McIntyreLapata09Resources/fables/")

# Get all word stems
stems = np.array([])
for txt in data.textfiles:
    # Use union relations
    txt.compute_union_relations()
    for rel in txt.relations_union:
        f = Feature(rel)
        if f.get_category() == -1:
            continue
        stems = np.append(stems, [f.get_stem_target()])
        stems = np.append(stems, [f.get_stem_source()])

stems = np.unique(stems)

X = np.array([], dtype=float).reshape(0,5)
y = np.array([], dtype=int)

null = 0
none = 0
for txt in data.textfiles:
    # Use union relations
    txt.compute_union_relations()
    for rel in txt.relations_union:
        f = Feature(rel)
        # If the time relation is not in (before, contains, is_contained_in), skip
        if f.get_category() == -1:
            continue
        if f.get_category() == 0:
            null += 1
            """
        if not f.get_aspect_combined():
            none += 1
            """
        if null > 450:
            continue
        # Building a row of all feature values
        X = np.append(X, [[f.get_distance(), f.get_similarity_of_words(), f.get_aspect_combined(), f.get_polarity(), f.get_modality()]], axis=0)
        y = np.append(y, [f.get_category()])


# Split dataset in training set(80%) and test set (20%)
len_train = len(X)*80/100
X_train, X_test = X[:len_train], X[len_train:]
y_train, y_test = y[:len_train], y[len_train:]

# Train the random forest classifier
rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
rf.fit(X_train, y_train)

# Print accuracy
print rf.score(X_test, y_test)
print "Predicted:"
print rf.predict(X_test)
print "True values:"
print y_test
