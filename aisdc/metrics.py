"""
Calculate metrics.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
from scipy import interpolate
from scipy.stats import norm
from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve

# pylint: disable = invalid-name

VAR_THRESH = 1e-2

def min_max_disc(
    y_true: np.ndarray, pred_probs: np.ndarray, x_prop: float = 0.1, log_p: bool = True
) -> tuple[float, float, float, float]:  # pylint: disable = line-too-long
    """
    Non-average-case methods for MIA attacks. Considers actual frequency of membership
    amongst samples with highest- and lowest- assessed probability of membership. If an
    MIA method confidently asserts that 5% of samples are members and 5% of samples are
    not, but cannot tell for the remaining 90% of samples, then these metrics will flag
    this behaviour, but AUC/advantage may not. Since the difference may be noisy, a
    p-value against a null of independence of true membership and assessed membership
    probability (that is, membership probabilities are essentially random) is also used
    as a metric (using a usual Gaussian approximation to binomial). If the p-value is
    low and the frequency difference is high (>0.5) then the MIA attack is successful
    for some samples.

    Parameters
    ----------
        y: np.ndarray
            true labels
        yp: np.ndarray
            probabilities of labels, or monotonic transformation of probabilties
        xprop: float
            proportion of samples with highest- and lowest- probability of membership to be
            considered
        logp: bool
            convert p-values to log(p).

    Returns
    -------
        maxd: float
            frequency of y=1 amongst proportion xprop of individuals with highest assessed
            membership probability
        mind: float
            frequency of y=1 amongst proportion xprop of individuals with lowest assessed
            membership probability
        mmd: float
            difference between maxd and mind
        pval: float
            p-value or log-p value corresponding to mmd against null hypothesis that random
            variables corresponding to y and yp are independent.

    Notes
    -----

    Examples
    --------
    >>> y = np.random.choice(2, 100)
    >>> yp = np.random.rand(100)
    >>> maxd, mind, mmd, pval = min_max_desc(y, yp, xprop=0.2, logp=True)

    """

    n_examples = int(np.ceil(len(y_true) * x_prop))
    pos_frequency = np.mean(y_true)  # average frequency
    y_order = np.argsort(pred_probs)  # ordering permutation

    # Frequencies
    # y values corresponding to lowest k values of yp
    y_lowest_n = y_true[y_order[:n_examples]]
    # y values corresponding to highest k values of yp
    y_highest_n = y_true[y_order[-(n_examples):]]
    maxd = np.mean(y_highest_n)
    mind = np.mean(y_lowest_n)
    mmd = maxd - mind

    # P-value
    # mmd is asymptotically distributed as N(0,sdm^2) under null.
    sdm = np.sqrt(2 * pos_frequency * (1 - pos_frequency) / n_examples)
    pval = 1 - norm.cdf(mmd, loc=0, scale=sdm)  # normal CDF
    if log_p:
        if pval < 1e-50:
            pval = -115.13
        else:
            pval = np.log(pval)

    # Return
    return maxd, mind, mmd, pval

def _tpr_at_fpr(
    y_true: Iterable[float],
    y_score: Iterable[float],
    fpr: float = 0.001,
    fpr_perc: bool = False,
) -> float:
    """Compute the TPR at a fixed FPR.
    In particular, returns the TPR value corresponding to a particular FPR. Uses interpolation
    to fill in gaps.

    Parameters
    ----------
    y_true: Iterable[float]
        actual class labels
    y_score: Iterable[float]
        predicted score
    fpr: float
        false positive rate at which to compute true positive rate
    fpr_perc: bool
        if the fpr is defined as a percentage

    Returns
    -------
    tpr: float
        true positive rate at fpr
    """

    if fpr_perc:
        fpr /= 100.0

    fpr_vals, tpr_vals, thresh_vals = roc_curve(y_true, y_score)
    thresh_from_fpr = interpolate.interp1d(fpr_vals, thresh_vals)
    tpr_from_thresh = interpolate.interp1d(thresh_vals, tpr_vals)

    thresh = thresh_from_fpr(fpr)
    tpr = tpr_from_thresh(thresh)

    return tpr

def _div(x: float, y: float, default: float) -> float:
    """Solve the problem of division by 0 and round up.
    If y is non-zero, perform x/y and round to 8dp. If it is zero, return the default

    Parameters
    ----------
    x: float
        numerator
    y: float
        denominator
    default: float
        return value if y == 0

    Returns
    -------
        division: float
            x / y, or default if y == 0
    """
    if y != 0:
        division = round(float(x / y), 8)
    else:
        division = float(default)
    return division


def _tpr_at_fpr(
    y_true: Iterable[float],
    y_score: Iterable[float],
    fpr: float = 0.001,
    fpr_perc: bool = False,
) -> float:
    """Compute the TPR at a fixed FPR.
    In particular, returns the TPR value corresponding to a particular FPR. Uses interpolation
    to fill in gaps.

    Parameters
    ----------
    y_true: Iterable[float]
        actual class labels
    y_score: Iterable[float]
        predicted score
    fpr: float
        false positive rate at which to compute true positive rate
    fpr_perc: bool
        if the fpr is defined as a percentage

    Returns
    -------
    tpr: float
        true positive rate at fpr
    """

    if fpr_perc:
        fpr /= 100.0

    fpr_vals, tpr_vals, thresh_vals = roc_curve(y_true, y_score)
    thresh_from_fpr = interpolate.interp1d(fpr_vals, thresh_vals)
    tpr_from_thresh = interpolate.interp1d(thresh_vals, tpr_vals)

    thresh = thresh_from_fpr(fpr)
    tpr = tpr_from_thresh(thresh)

    return tpr


def _expected_auc_var(auc: float, num_pos: int, num_neg: int) -> float:
    """ "Compute variance of AUC under assumption of uniform probabilities
    uses the expression given as eqn (2) in  https://cs.nyu.edu/~mohri/pub/area.pdf

    Parameters
    ----------

    auc: float
        auc value at which to compute the variance
    num_pos: int
        number of positive examples
    num_neg: int
        number of negative examples

    Returns
    -------
    var: float
        null variance of AUC
    """
    p_xxy = p_xyy = 1 / 3
    var = (
        auc * (1 - auc)
        + (num_pos - 1) * (p_xxy - auc**2)
        + (num_neg - 1) * (p_xyy - auc**2)
    ) / (num_pos * num_neg)
    return var


def auc_p_val(auc: float, n_pos: int, n_neg: int) -> tuple[float, float]:
    """Compute the p-value for a given AUC

    Parameters
    ----------
    auc: float
        Observed AUC value
    n_pos: int
        Number of positive examples
    n_neg: int
        Number of negative examples

    Returns
    -------
    auc_p: float
        p-value of observing an AUC > auc by chance
    auc_std: float
        standard deviation of the NULL AUC diustribution (mean = 0.5)

    """
    auc_std = np.sqrt(_expected_auc_var(0.5, n_pos, n_neg))
    auc_p = 1 - norm.cdf(auc, loc=0.5, scale=auc_std)
    return auc_p, auc_std

def get_probabilities(  # pylint: disable=too-many-locals
    clf,
    X_test: np.ndarray,
    y_test: np.ndarray = [],
    permute_rows: bool = None
):
    if permute_rows == True and len(y_test) == 0:
        raise ValueError ("If permute_rows is set to True, y_test must be supplied")

    if permute_rows:
        N, _ = X_test.shape
        order = np.random.RandomState(  # pylint: disable = no-member
            seed=10
        ).permutation(N)
        X_test = X_test[order, :]
        y_test = y_test[order]
    
    y_pred_proba = clf.predict_proba(X_test)
    
    if permute_rows == True:
        return y_pred_proba, y_test
    return y_pred_proba

def get_metrics(  # pylint: disable=too-many-locals
    y_test: np.ndarray,
    y_pred_proba: np.ndarray,
):

    invalid_format_error_message = "y_pred must be an array of shape [x,2] with elements of type float"

    shape = y_pred_proba.shape
    if len(shape) != 2:
        raise ValueError(invalid_format_error_message)
    else:
        if shape[1] != 2:
            raise ValueError("Multiclass classification is not supported")
            
    try:
        user_num = float(y_pred_proba[-1,-1])
    except ValueError:
        print(invalid_format_error_message)

    print("New Metrics")
    print(y_test.shape)
    """
    Calculate metrics, including attacker advantage for MIA binary.
    Implemented as Definition 4 on https://arxiv.org/pdf/1709.01604.pdf
    which is also implemented in tensorFlow-privacy https://github.com/tensorflow/privacy

    Parameters
    ----------
    clf: sklearn.Model
        trained model
    X_test: np.ndarray
        test data matrix
    y_test: np.ndarray
        test data labels

    Returns
    -------
    metrics: dict
        dictionary of metric values

    Notes
    -----
    Includes the following metrics:

    * True positive rate or recall (TPR).
    * False positive rate (FPR), proportion of negative examples incorrectly \
    classified as positives.
    * False alarm rate (FAR), proportion of objects classified as positives \
    that are incorrect, also known as false discovery rate.
    * True neagative rate (TNR).
    * Positive predictive value or precision (PPV).
    * Negative predictive value (NPV).
    * False neagative rate (FNR).
    * Accuracy (ACC).
    * F1 Score - harmonic mean of precision and recall.
    * Advantage.
    """
    metrics = {}

    print(y_pred_proba.shape)
    y_pred = np.argmax(y_pred_proba,axis=1)
    y_pred_proba = y_pred_proba[:, 1]

    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    # print('tn', tn, 'fp',fp,'fn', fn,'tp', tp)

    # true positive rate or recall
    metrics["TPR"] = round(float(tp / (tp + fn)), 8)
    # false positive rate, proportion of negative examples incorrectly classified as positives
    metrics["FPR"] = round(float(fp / (fp + tn)), 8)
    # False alarm rate, proportion of things classified as positives that are incorrect,
    # also known as false discovery rate
    metrics["FAR"] = _div(fp, (fp + tp), 0)
    # true negative rate or specificity
    metrics["TNR"] = round(float(tn / (tn + fp)), 8)
    # precision or positive predictive value
    metrics["PPV"] = _div(tp, (tp + fp), 0)
    # negative predictive value
    metrics["NPV"] = _div(tn, (tn + fn), 0)
    # false negative rate
    metrics["FNR"] = round(float(fn / (tp + fn)), 8)
    # overall accuracy
    metrics["ACC"] = round(float((tp + tn) / (tp + fp + fn + tn)), 8)
    # harmonic mean of precision and sensitivity
    metrics["F1score"] = _div(
        2 * metrics["PPV"] * metrics["TPR"], metrics["PPV"] + metrics["TPR"], 0
    )
    # Advantage: TPR - FPR
    metrics["Advantage"] = float(abs(metrics["TPR"] - metrics["FPR"]))

    # calculate AUC of model
    metrics["AUC"] = round(roc_auc_score(y_test, y_pred_proba), 8)

    # Calculate AUC p-val
    metrics["P_HIGHER_AUC"], _ = auc_p_val(
        metrics["AUC"], y_test.sum(), len(y_test) - y_test.sum()
    )

    fmax, fmin, fdif, pdif = min_max_disc(y_test, y_pred_proba)
    metrics["FMAX01"] = fmax
    metrics["FMIN01"] = fmin
    metrics["FDIF01"] = fdif
    metrics["PDIF01"] = -pdif  # use -log(p) so answer is positive

    print("In New Metrics")
    print(y_test.shape)
    print(y_pred_proba.shape)

    fmax, fmin, fdif, pdif = min_max_disc(y_test, y_pred_proba, x_prop=0.2)
    metrics["FMAX02"] = fmax
    metrics["FMIN02"] = fmin
    metrics["FDIF02"] = fdif
    metrics["PDIF02"] = -pdif  # use -log(p) so answer is positive

    fmax, fmin, fdif, pdif = min_max_disc(y_test, y_pred_proba, x_prop=0.01)
    metrics["FMAX001"] = fmax
    metrics["FMIN001"] = fmin
    metrics["FDIF001"] = fdif
    metrics["PDIF001"] = -pdif  # use -log(p) so answer is positive

    # Add some things useful for debugging / filtering
    metrics["pred_prob_var"] = y_pred_proba.var()

    # TPR at various FPR
    fpr_vals = [0.5, 0.2, 0.1, 0.01, 0.001, 0.00001]
    for fpr in fpr_vals:
        tpr = _tpr_at_fpr(y_test, y_pred_proba, fpr=fpr)
        name = f"TPR@{fpr}"
        metrics[name] = tpr

    fpr, tpr, roc_thresh = roc_curve(y_test, y_pred_proba)
    metrics["fpr"] = fpr
    metrics["tpr"] = tpr
    metrics["roc_thresh"] = roc_thresh

    metrics["n_pos_test_examples"] = y_test.sum()
    metrics["n_neg_test_examples"] = (1 - y_test).sum()

    return metrics

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

def format_column(df, name):
    df[name] = pd.Categorical(df[name])
    df[name+'_code'] = df[name].cat.codes
    return df

def binary_classification():
    df = pd.read_csv("Customer_Churn.csv")

    df = format_column(df, 'gender')
    df = format_column(df, 'SeniorCitizen')
    df = format_column(df, 'PhoneService')
    df = format_column(df, 'MultipleLines')
    df = format_column(df, 'PaymentMethod')
    df = format_column(df, 'Partner')
    df = format_column(df, 'Dependents')
    df = format_column(df, 'PaperlessBilling')
    df = format_column(df, 'OnlineSecurity')
    df = format_column(df, 'TechSupport')
    df = format_column(df, 'InternetService')
    df = format_column(df, 'Contract')
    df = format_column(df, 'StreamingTV')
    df = format_column(df, 'DeviceProtection')
    df = format_column(df, 'StreamingMovies')
    df = format_column(df, 'OnlineBackup')
    df = format_column(df, 'Churn')

    features = ['gender_code', 'SeniorCitizen_code', 'PhoneService_code', 'MultipleLines_code', 
        'InternetService_code', 'Partner_code', 'Dependents_code', 'PaymentMethod_code', 'PaperlessBilling_code','Contract_code', 'StreamingMovies_code',
        'StreamingTV_code', 'TechSupport_code', 'DeviceProtection_code', 'OnlineBackup_code',
        'OnlineSecurity_code', 'Dependents_code', 'Partner_code','tenure', 'MonthlyCharges']

    X = np.array(df[features])
    y = np.array(df['Churn_code'])

    return X, y

def multiclass_classification():
    attributes = ["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]
    dataset = pd.read_csv('iris.data', names = attributes)
    dataset.columns = attributes

    print(dataset.head())
    print(dataset['species'].value_counts())

    y = dataset['species']
    X = dataset.drop(columns=['species'])

    return X, y

if __name__ == "__main__":
    print("Hello world!")
    
    X, y = binary_classification()

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier()
    rf.fit(x_train, y_train)
    y_pred = rf.predict(x_test)

    # print(metrics.classification_report(y_test, y_pred))

    # tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
    # tpr = round(float(tp / (tp + fn)), 8)
    # fpr = round(float(fp / (fp + tn)), 8)
    # tnr = round(float(tn / (tn + fp)), 8)
    # fnr = round(float(fn / (tp + fn)), 8)

    # print("True positive: "+str(tpr))
    # print("False positive: "+str(fpr))
    # print("True negative: "+str(tnr))
    # print("False negative: "+str(fnr))

    # y_pred = rf.predict_proba(x_test)

    print("SHAPES")
    print(y_pred.shape)
    print(y_test.shape)

    y_pred_proba = get_probabilities(rf, x_test, permute_rows=False)

    print(y_pred_proba.shape)

    print(new_get_metrics(y_test, y_pred_proba))

    y_pred = rf.predict_proba(x_train)
    y_label = [1]*len(y_pred)
    print(len(y_label))

    y_pred_test = rf.predict_proba(x_test)
    y_label_y = [0]*len(y_pred_test)
    
    for y in y_label_y:
        y_label.append(y)
    print(len(y_label))
    print("End of ylabel")

    y_pred = np.append(y_pred, y_pred_test, axis=0)

    print(len(y_pred))
    print(len(y_label))

    print(y_pred.shape)

    attack_rf = RandomForestClassifier()
    x_train_attack, x_test_attack, y_train_attack, y_test_attack = train_test_split(np.array(y_pred), np.array(y_label), test_size=0.2, random_state=42)

    attack_rf.fit(x_train_attack,y_train_attack)

    permute_rows = False
    if permute_rows:
        N, _ = x_test.shape
        order = np.random.RandomState(  # pylint: disable = no-member
            seed=10
        ).permutation(N)
        x_train_attack = x_train_attack[order, :]
        y_test_attack = y_test_attack[order]
    y_pred = attack_rf.predict_proba(x_test_attack)

    before = get_metrics(attack_rf, x_test_attack, y_test_attack, permute_rows=False)

    y_pred_proba = get_probabilities(attack_rf, x_test_attack, permute_rows=False)
    after = new_get_metrics(y_test_attack, y_pred_proba)

    for key in before.keys():
        b = before[key]
        a = after[key]

        print(key)
        print(a == b)
        print()