import datetime
import json
import os

import pandas as pd
import numpy as np
import sys

from .graph import plot_timeseries, evaluation_graphs, draw_error
from .metrics import calculate_regression_metrics


def set_constant_period(amp, period):
    """
    Set constant period
    :param amp: amplitude eiter 0 or 1
    :param period: how long is the amp
    :return: :param the amp value over period
    """
    amplitude = pd.Series(np.ones(period, dtype=int)*amp, name="amplitude")

    return amplitude


def generate_steps(freq='10s', amplitude=[0], end_periods=[604800], start_date="2022-03-01", fixed_end=604800):
    """
    Generate the signal. It transforms amplitudes and end periods into timeseries label.
    :param freq: time between each label (this should be fixed to 10s)
    :param amplitude: a list of 0 and 1
    :param end_periods: when amplitude changed in seconds from the start_date
    :return: pandas dataframe with time and label
    """
    end_periods = [int(p/10) * 10 for p in end_periods]
    f = int(freq[:-1])
    idx = pd.date_range(start_date, periods=fixed_end/f, freq=freq)
    ts = pd.Series(idx, name="date")

    # fix init 0
    if len(end_periods) > 0 and end_periods[0] == 0:
        print("ERROR: the end of a period should not be 0.")
        sys.exit(1)

    end_periods = [0] + end_periods
    if len(end_periods)-1 != len(amplitude):
        print("ERROR: the length are not the same")
        sys.exit(2)

    if end_periods[-1] < fixed_end:
        end_periods.append(fixed_end)
        amplitude.append(int(amplitude[-1] == 0))

    ampl = pd.Series(name="amplitude", dtype=int)
    for i,a in enumerate(amplitude):
        delta = end_periods[i+1] - end_periods[i]
        amp = set_constant_period(a, int(delta/f))
        ampl = pd.concat([ampl, amp], ignore_index=True, sort=False)

    data = pd.concat([ts, ampl], axis=1)
    return data


def evaluate(org_data, prediction_data):
    """
    Evaluate ground truth and predictions
    :param org_data: ground truth data
    :param prediction_data: predicted data
    :return: a dictionary of metrics
    """
    org_data['origin'] = ["truth"]*org_data.shape[0]
    prediction_data['origin'] = ["predicted"]*prediction_data.shape[0]
    metrics = calculate_regression_metrics(org_data.amplitude, prediction_data.amplitude)
    if os.environ.get('DRAW', False) == 'True':
        draw_data = pd.concat([org_data, prediction_data], ignore_index=True, sort=False)
        charts = plot_timeseries(draw_data)

        charts += evaluation_graphs(org_data.amplitude, prediction_data.amplitude)

        org_data.rename(columns={'amplitude': 'amp_org',}, inplace=True)
        prediction_data.rename(columns={'amplitude': 'amp_pred',}, inplace=True)
        prediction_data.drop(prediction_data.columns[0], axis=1, inplace=True)
        data_df = pd.concat([org_data, prediction_data], axis=1)
        e_diff = pd.DataFrame({'d': (data_df.amp_org - data_df.amp_pred)})
        eval_diff = pd.concat([data_df, e_diff], axis=1)
        eval_diff.drop(columns=["amp_pred", "amp_org", "origin"], axis=1, inplace=True)
        charts += draw_error(eval_diff)
        return metrics, charts
    else:
        return metrics


def convert_json_data_to_dataframe(data_dict):
    """
    Convert json data into one big dataframe
    """
    sorted_data_list = sorted(data_dict['prediction_results'], key=lambda d: d['file_name'])
    df = pd.DataFrame(columns=['date', 'amplitude'])
    start_date = datetime.datetime.strptime('2022-03-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    seven_days = datetime.timedelta(days=7)
    for data in sorted_data_list:
        p = generate_steps('10s', data['leakages'], data['end_periods'], start_date=str(start_date))
        df = pd.concat([df, p])
        start_date += seven_days
    return df


def read_json(json_file):
    with open(json_file, 'r') as j:
        contents = json.loads(j.read())
    return contents


def convert_date_to_seconds(date_string, start_date_string='2022-03-01 00:00:00'):
    d = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    start = datetime.datetime.strptime(start_date_string, '%Y-%m-%d %H:%M:%S')
    return int((d - start).total_seconds())
