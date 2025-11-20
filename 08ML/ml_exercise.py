"""
Naive Bayes vs Decision Trees

Goal:
    - Use scikit-learn to compare Gaussian Naive Bayes and Decision Trees
    - Work with train / test splits and simple cross-validation
    - Detect and reduce overfitting by tuning max_depth

Complete all TODO sections.

Students should:
    1. Load the Digit dataset.
    2. Split into train/test.
    3. Train and evaluate a Gaussian Naive Bayes classifier.
    4. Train and evaluate a fully grown Decision Tree (likely overfits).
    5. Use cross-validation on the training set.
    6. Retrain a tuned tree and compare results.

Cross-validation reminder:
    - Only split off ONE test set.
    - Hyperparameter tuning is done on the TRAINING set using K-fold
      cross-validation (here K=5), to avoid using the test set for decisions.
"""

import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt


# -------------------------------------------------------------------
# 1. Data loading (provided)
# -------------------------------------------------------------------
def load_digits_data():
    """Load the Digits dataset from sklearn.

    Returns:
        X            : (n_samples, n_features) feature matrix
        y            : (n_samples,) labels
        feature_names: list of feature names
        class_names  : list of class names
    """
    data = load_digits()
    X = data.data
    y = data.target
    feature_names = data.feature_names
    class_names = data.target_names.tolist()
    return X, y, feature_names, class_names


# -------------------------------------------------------------------
# 2. TODO: Train/test split
# -------------------------------------------------------------------
def make_splits(X, y, random_state=42):
    """Split into train and test.

    Requirements:
        - 80% train, 20% test
        - given random_state
    """
    # TODO: use train_test_split to create X_train, X_test, y_train, y_test


    X_train, X_test, y_train, y_test = None, None, None, None  # TODO
    return X_train, X_test, y_train, y_test


# -------------------------------------------------------------------
# 3. TODO: Naive Bayes
# -------------------------------------------------------------------
def run_naive_bayes(X_train, y_train, X_test, y_test):
    """Train Gaussian Naive Bayes and return model, train_acc, test_acc."""
    # TODO: create and fit GaussianNB

    nb = None  # TODO

    # TODO: compute training and test accuracy
    train_acc = None
    test_acc = None

    print("\n=== Naive Bayes (GaussianNB) ===")
    print("Train accuracy:", train_acc)
    print("Test  accuracy:", test_acc)

    return nb, train_acc, test_acc


# -------------------------------------------------------------------
# 4. TODO: Full decision tree (overfitting demo)
# -------------------------------------------------------------------
def run_full_decision_tree(X_train, y_train, X_test, y_test):
    """Train a full Decision Tree (no max_depth limit).

    Return model, train_acc, test_acc.
    """
    # TODO: create DecisionTreeClassifier with max_depth=None
    dt = None  # TODO

    # TODO: fit on training data

    # TODO: compute training and test accuracy

    train_acc = None
    test_acc = None

    print("\n=== Decision Tree (unconstrained) ===")
    print("Train accuracy:", train_acc)
    print("Test  accuracy:", test_acc)

    return dt, train_acc, test_acc


# -------------------------------------------------------------------
# 5. TODO: Tuning decision tree with cross-validation
# -------------------------------------------------------------------
def tune_decision_tree(X_train, y_train, X_test, y_test):
    """
    Tune max_depth using 5-fold cross-validation on the training set,
    and plot mean CV accuracy vs depth so you can see the 'knee'.
    """
    depths = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    cv_results = []

    print("\n=== Decision Tree – depth tuning with cross-validation ===")
    for depth in depths:
        # TODO: create model
        model = None  # TODO

        # TODO: compute cross_val_score on X_train, y_train with cv=5
        scores = None  # TODO

        # TODO: mean CV accuracy
        mean_score = None
        cv_results.append((depth, mean_score))
        print(f"max_depth={depth}, mean CV accuracy={mean_score}")

    # Plot depth vs CV accuracy
    depths_list, cv_scores = zip(*cv_results)

    plt.figure()
    plt.plot(depths_list, cv_scores, marker="o")
    plt.xlabel("max_depth")
    plt.ylabel("Mean 5-fold CV accuracy")
    plt.title("Decision tree depth tuning (cross-validation)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# -------------------------------------------------------------------
# 6. Main
# -------------------------------------------------------------------
def main():
    X, y, feature_names, class_names = load_digits_data()
    print("Data shape:", X.shape)
    print("Features:", feature_names)
    print("Classes:", class_names)

    X_train, X_test, y_train, y_test = make_splits(X, y, random_state=42)
    print("Train size:", None if X_train is None else X_train.shape[0])
    print("Test size:", None if X_test is None else X_test.shape[0])

    # Naive Bayes
    nb_model, nb_train_acc, nb_test_acc = run_naive_bayes(
        X_train, y_train, X_test, y_test
    )

    # Full decision tree (overfit)
    dt_full, dt_full_train_acc, dt_full_test_acc = run_full_decision_tree(
        X_train, y_train, X_test, y_test
    )

    # Tuned decision tree
    tune_decision_tree(
        X_train, y_train, X_test, y_test
    )

    print("\n=== Summary (fill in your interpretation) ===")
    print("Naive Bayes      – test acc:", nb_test_acc)
    print("Full tree        – test acc:", dt_full_test_acc)



if __name__ == "__main__":
    main()
