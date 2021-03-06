from train import *
from temporalrelation import TemporalRelation
from sklearn.metrics import classification_report

def get_prediction(temporal_rel, new=True, annotations="union", features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"]):
    """This function is suited to test the different options and get a result for them

    Args:
        temporal_rel (TemporalRelation): temporal relation we are interested in.
        new (bool): Load features from file (False) or calculate them new (True)?
        annotations (str): Either "union" or "intersected". All data vs. data which annotators have in common
        features (list): Which features should be used

    """
    X, y = load_data(new, temporal_rel, annotations, features)

    print "Len data in main after: " + str(len(y))

    # Split dataset into training set (80%) and test set (20%)
    X_train, X_test, y_train, y_test = split(X, y)

    # Train the random forest classifier
    rf = RandomForestClassifier(n_jobs=2, n_estimators=100)
    rf.fit(X_train, y_train)

    y_predicted = rf.predict(X_test)

    # Transform to list
    y_predicted = y_predicted.tolist()
    y_test = y_test.tolist()
    print y_test
    print y_predicted

    print "F1-Score"
    print f1_score(y_test, y_predicted)
    print

    print "Ground truth"
    print y_test
    print
    print "Predicted"
    print y_predicted

    print
    print "Classification report:"
    print classification_report(y_test, y_predicted)

if __name__ == "__main__":
    # With 'python main.py --reload' a "fresh parsing" will be enforced
    if (len(sys.argv) >= 2 and sys.argv[1] == "--reload") or not os.path.isfile("save.p"):
        new = True
    else:
        new = False

    print "Information for class BEFORE"
    get_prediction(TemporalRelation.BEFORE, features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"])
    print
    """

    print "Information for class INCLUDES"
    get_prediction(TemporalRelation.INCLUDES, features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"])
    print

    print "Information for class IS_INCLUDED"
    get_prediction(None, features=["modality"])
    #get_prediction(None, features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"])
    print

    print "Information for class NONE"
    get_prediction(TemporalRelation.NONE, features=["pos", "stem", "aspect", "tense", "distance", "similarity", "polarity", "modality"])
    print
    """
