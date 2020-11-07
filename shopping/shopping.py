import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

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

    evidence = []
    label = []

    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                for i in [0, 2, 4]:
                    row[i] = int(row[i])

                for i in [1, 3, 5, 6, 7, 8, 9]:
                    row[i] = float(row[i])

                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                for month in months:
                    if row[10] == month:
                        row[10] = months.index(month)

                for i in [11, 12, 13, 14]:
                    row[i] = int(row[i])

                if row[15] == 'Returning_Visitor':
                    row[15] = 1
                else:
                    row[15] = 0

                for i in [16, 17]:
                    if row[i] == 'TRUE':
                        row[i] = 1
                    else:
                        row[i] = 0

                evidence.append(row[:17])
                label.append(row[-1])
                        
            except ValueError:
                continue
            
        return (evidence, label)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    training  = KNeighborsClassifier(n_neighbors=1)
    training.fit(evidence, labels)

    return training


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

    purchase = {
        'labels': 0,
        'predictions': 0
    }

    abandonment = {
        'labels': 0,
        'predictions': 0
    }

    for i in range(len(labels)):
        if labels[i] == 1:
            purchase['labels'] += 1
            purchase['predictions'] += predictions[i] 
        else:
            abandonment['labels'] += 1
            abandonment['predictions'] += 1 - predictions[i]

    sensitibity = purchase['predictions'] / purchase['labels']
    specificity = abandonment['predictions'] / abandonment['labels']

    return (sensitibity, specificity)


if __name__ == "__main__":
    main()
