import csv
import sys
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    dataset = pd.read_csv(filename)
    x = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values

    # Encode months
    enc1 = OrdinalEncoder()
    months = [
            ['Jan', 0], 
            ['Feb', 1], 
            ['Mar', 2], 
            ['Apr', 3],
            ['May', 4], 
            ['June', 5], 
            ['Jul', 6], 
            ['Aug', 7], 
            ['Sep', 8], 
            ['Oct', 9], 
            ['Nov', 10], 
            ['Dec', 11]]
    enc1.fit(months)

    # Encode visitors 
    enc2 = OrdinalEncoder()
    enc2.fit([['New_Visitor', 0], ['Returning_Visitor', 1]])

    # Encode weekends
    enc3 = OrdinalEncoder()
    enc3.fit([['FALSE', 0], ['TRUE', 1]])

    ct = ColumnTransformer(transformers=[
        ('months', enc1, [10]),
        ('visitors', enc2, [15]),
        ('weekends', enc3, [16])
        ], remainder='passthrough')

    x = np.array(ct.fit_transform(x))

    # Encode revenue
    le = LabelEncoder()
    y = le.fit_transform(y)

    return (x, y)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    TP = 0
    TN = 0
    positives = 0
    negatives = 0

    for i in range(len(predictions)):
        # Increment total positives and negatives
        if predictions[i] == 1:
            positives += 1
        else:
            negatives += 1

        # Determine if true positive or true negative and increment 
        if labels[i] == predictions[i] == 1:
            TP += 1
        elif labels[i] == predictions[i] == 0:
            TN += 1

    sensitivity = TP / positives
    specificity = TN / negatives

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
