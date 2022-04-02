from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import r2_score


def calculate_regression_metrics(y_true, y_predicted):
    """
    Calculate prediction metrics
    :param y_true: true labels
    :param y_predicted: predicted labels
    :return: dictionary of score metrics
    """

    xvs = explained_variance_score(y_true, y_predicted)
    mse = mean_squared_error(y_true, y_predicted)
    msle = mean_squared_log_error(y_true, y_predicted)
    r2 =  r2_score(y_true, y_predicted)

    data_table = [
        ["Explained variance score", xvs],
        ["Mean squared error", mse],
        ["Mean squared log error", msle],
        ["R2 score", r2],
    ]
    return {d[0]: d[1] for d in data_table}
