# Naive Bayes vs Decision Trees 

In this exercise you will compare **Naive Bayes** and **Decision Trees** on the classic **Digits** dataset from `scikit-learn`.

You will practice:

- Loading a real dataset using `sklearn.datasets`
- Doing a **train/test** split
- Using **cross-validation** on the training set
- Training a **Gaussian Naive Bayes** classifier
- Training a **Decision Tree** classifier
- Detecting and reducing **overfitting** by tuning `max_depth`


---

## Dataset: Digits

We use the built-in Digits dataset. 
No cleaning or feature engineering is needed; you directly plug it into `scikit-learn`.

---

## What is cross-validation?

When we tune hyperparameters (like `max_depth` of a decision tree), we should not use the **test set**, because the test set should only be used once at the very end to estimate generalization performance.

Instead, we use **cross-validation** on the **training data**:

1. Split the training set into **K folds** (for example, K = 5).
2. For each hyperparameter setting (for example, `max_depth = 4`):
   - Use K−1 folds for training.
   - Use the remaining fold for validation.
   - Repeat this K times (each fold becomes the validation set once).
3. Average the K validation scores. This is the **cross-validation score** for that hyperparameter.
4. Choose the hyperparameter with the **best average score**.
5. Retrain a final model on the **full training set** with that chosen hyperparameter.
6. Finally, evaluate once on the **held-out test set**.

This reduces the risk of accidentally overfitting to a single validation split, and it allows you to make better use of limited data.

### Visual intuition

The following picture (from the scikit-learn docs) shows the idea of cross-validation folds:

![Cross-validation illustration](https://scikit-learn.org/stable/_images/grid_search_cross_validation.png)

Each color block represents a different fold being used as the validation set, while the others are used for training.

---

## Your tasks (in `ml_exercise.py`)

### 1. Data loading and split

1. Use the provided `load_digits_data()` function to get:

   ```python
   X, y, feature_names, class_names
   ```

2. Implement `make_splits(X, y, random_state=42)`:

   - Use `train_test_split` to split into:
     - **Training set**: 80 %
     - **Test set**: 20 %
   - Use  `random_state=42`.

Return: `X_train, X_test, y_train, y_test`.

---

### 2. Naive Bayes (GaussianNB)

Implement `run_naive_bayes(...)`:

1. Create and fit a `GaussianNB` model on the **training set**.
2. Compute and print:
   - **Training accuracy**
   - **Test accuracy**
3. Return the model and both accuracies.

---

### 3. Decision Tree and overfitting

Implement `run_full_decision_tree(...)`:

1. Create a `DecisionTreeClassifier` with **no depth limit**:

   ```python
   DecisionTreeClassifier(random_state=42)
   ```

2. Train on the **training set**.
3. Compute and print:
   - **Training accuracy**
   - **Test accuracy**
4. Return the model and both accuracies.


---

### 4. Fixing overfitting with cross-validation

Implement `tune_decision_tree(...)`:

1. For each `max_depth` in:

   ```python
   depths = [2, 4, 6, 8, 10, 12, 14, 16 ,18, 20]
   ```

   - Create a `DecisionTreeClassifier(max_depth=depth, random_state=42)`.
   - Use `cross_val_score` with `cv=5` on the **training set**.
   - Compute the **mean cross-validation accuracy**.
   - Print: `max_depth`, mean CV accuracy.

2. Look at the implemented plot, from which point does the model start overfitting.
3. Which depth would you choose?



---

## Setup & running

Install required packages:

```bash
pip install numpy scikit-learn matplotlib
```

Run the student script:

```bash
python ml_exercise.py
```

Then fill in all the `TODO` parts until it runs and prints sensible results.
