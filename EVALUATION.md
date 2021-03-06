Error analysis
==============

### Different number of trees in the random forest

When using the default value of the RandomForestClassifierer from scikit-learn only 10 trees will be used.
This obviously results in quite different accuracies when running the program several times.
The following graph illustrates that the difference for small amounts of trees can be quite big whereas for bigger amounts the accuracy converges to a certain value.
The bigger the amount of trees, the more reproducible the accuracy gets.

Different number of trees for the _BEFORE_ class
![](plots/different_number_of_trees_0.jpg?raw=true "Different number of trees")
![](plots/number_of_trees_before_precision-recall.jpg?raw=true "Different number of trees")
Different number of trees for the _INCLUDES_ class
![](plots/different_number_of_trees_1.jpg?raw=true "Different number of trees")
![](plots/number_of_trees_includes_precision-recall.jpg?raw=true "Different number of trees")
Different number of trees for the _IS_INCLUDED_ class (not enough data and therefore no meaningful difference)
![](plots/different_number_of_trees_2.jpg?raw=true "Different number of trees")
![](plots/number_of_trees_is_included_precision-recall.jpg?raw=true "Different number of trees")
Different number of trees for the _NONE_ class (not enough data and therefore no meaningful difference)
![](plots/different_number_of_trees_3.jpg?raw=true "Different number of trees")
![](plots/number_of_trees_none_precision-recall.jpg?raw=true "Different number of trees")


### All relations vs. all relations in common

The provided XML file consists of annotated events and relations of events.
Those events and relations got annotated by more than one person and different people annotated different events and relations.

Therefore it was reasonable to check for which case the performance of the classification on the test set was higher.
It turned out that there is no noticeable difference in performance.


### Best combination of features

Since it was not feasible for me to test all 255 different combinations, I just tried out different promising combinations.
This however did not provide better results than just using all features together.


Evaluation
==========

### Learning rate
The following graphs show the learning rate of the random forest classifier for the individual temporal relations.  
Since it was not feasible for me to calculate the learning rate several times for each temporal relation the following plots are not averaged.
Therefore there are some data points which have a better f1-score than data points with less data.

The bad performance for _IS_INCLUDED_ and _NONE_ is explainable by looking at the distribution of the temporal relations.
There are only 129 _IS_INCLUDED_ and 66 _NONE_ temporal relations (when looking at all annotations and not at the intersection of relations by different annotators).  
_BEFORE_ and _INCLUDES_ did better since there was enough data for them.

Learning rate for the _BEFORE_ class:
![](plots/learning_rate_0.jpg?raw=true "Learning rate for BEFORE")
![](plots/learning_rate_before_precision-recall.jpg?raw=true "Learning rate for BEFORE")
Learning rate for the _INCLUDES_ class:
![](plots/learning_rate_1.jpg?raw=true "Learning rate for INCLUDES")
![](plots/learning_rate_includes_precision-recall.jpg?raw=true "Learning rate for INCLUDES")
Learning rate for the _IS_INCLUDED_ class:
![](plots/learning_rate_2.jpg?raw=true "Learning rate for IS_INCLUDED")
Learning rate for the _NONE_ class:
![](plots/learning_rate_3.jpg?raw=true "Learning rate for NONE")
Weighted learning rate over all classes:
![](plots/learning_rate_weighted.jpg?raw=true "Weighted learning rate over all classes")
![](plots/learning_rate_all_precision-recall.jpg?raw=true "Weighted learning rate over all classes")


### Importance of distance between events

Events in a temporal relation have different distances to each other.
This raises the question whether the distance is an important factor for the correctness of the classifierer.

The following graph shows the f1-score for changing distances.

There seems not to be a correlation between distance and performance.

Importance of distance for the _BEFORE_ class:
![](plots/distance_importance_0.jpg?raw=true "Distance importance")
Importance of distance for the _INCLUDES_ class:
![](plots/distance_importance_1.jpg?raw=true "Distance importance")
Importance of distance for the _IS_INCLUDED_ class:
![](plots/distance_importance_2.jpg?raw=true "Distance importance")
Importance of distance for the _NONE_ class:
![](plots/distance_importance_3.jpg?raw=true "Distance importance")

### Comparing different features in isolation

This is just one possible plot and not the averaged f1-score over many tries.
Therefore it is not too meaningful.  
One can see though that the Stem feature seems to be quite important for the classification.

Features in isolation for _BEFORE_ class:
![](plots/best_feature_0.jpg?raw=true "Features in isolation")
![](plots/best_feature_before_precision-recall.jpg?raw=true "Features in isolation")
Features in isolation for _INCLUDES_ class:
![](plots/best_feature_1.jpg?raw=true "Features in isolation")
![](plots/best_feature_includes_precision-recall.jpg?raw=true "Features in isolation")
Features in isolation for _IS_INCLUDED_ class:
![](plots/best_feature_2.jpg?raw=true "Features in isolation")
![](plots/best_feature_is_included_precision-recall.jpg?raw=true "Features in isolation")
Features in isolation for _NONE_ class:
![](plots/best_feature_3.jpg?raw=true "Features in isolation")
![](plots/best_feature_none_precision-recall.jpg?raw=true "Features in isolation")
