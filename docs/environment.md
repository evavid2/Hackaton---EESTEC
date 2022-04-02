# Getting started
To get started, fork the repository from [github](https://github.com/MediusInc/eestech-challenge-2022).

## Environment structure

The repository contains the following folders and files:
- `docs` contains the files for generating documentation in [Sphinx](https://www.sphinx-doc.org/en/1.4.9/index.html)
- `example` contains example files for Phase 2 submission
- `src` contains the starter code
- `src/utils` contains utility functions
- `src/leak_detection.py` python class you should implement and submit

## Challenge

Implement your solution in [leak_detection.py](../src/leak_detection.py) under the method predict.
The method takes in a list of features and should return a boolean. It should return true if leak
is detected and false if there is no leak. You can create new files and import them into `predict.py`.
Example of how predict method will be called is in `evaluate.py`. You can use it to test your solution.


## Set up environment
To set up environment you just have to install all the dependencies. You can do so with `pip`:
```bash
pip install -r requirements.txt
```

## Phase 1
The first task goal is to analyze and try to detect water discharges based
on unlabeled data from micro-turbine signals.

You have to use advanced anomaly detection algorithms through machine learning
or advanced statistical analysis to predict leakages.

### Submission
You have to upload json file with periods labels, where the leakage
occurred.

```json
{
    "prediction_results": [
        {
            "file_name" : "my-file4.csv",
            "end_periods": [360, 720, 10800, 14400],
            "leakages": [1,0,1,0]
        },
        {
            "file_name" : "my-file2.csv",
            "end_periods": [1800,5400,8700, 14400],
            "leakages": [1,0,1,0]

        }
    ]
}
```

## Phase 2
*Before participating in phase 2, you should finish phase 1.*

The second phase has more advance dataset, than the first one.
The labeled data (train dataset) also have seasonality component,
but the principle of leakage remains the same as it was analysed in phase 1.
Additionally, the trend could be easily analysed on dataset samples, describing
time series data signals, obtained from micro-turbine IoT device.

Beside the resulting json file, participants will also have to submit the
working algorithm, which is able to predict real time stream data. Such prediction
algorithm will be tested and evaluated in EvalAI platform.

After submitting final submission, the algorithm will be evaluated
in live stream data, which will also present the final result, and will be
presented as final challenge score.

### Submission
The `result.json` file should look something like this:

```json
{
    "prediction_results": [
        {
            "file_name" : "my-file4.csv",
            "end_periods": [360, 720, 10800, 14400],
            "leakages": [1,0,1,0]
        },
        {
            "file_name" : "my-file2.csv",
            "end_periods": [1800,5400,8700, 14400],
            "leakages": [1,0,1,0]

        }
    ]
}
```

When submitting the algorithm, you should also include the `requirements.txt` and all the necessary
files for the algorithm to work. You can submit everything in a `zip` format. An example of the
submission files can be seen in [example](../example) folder (file `tree.joblib` is optional).

## Submitting
To submit your solution you need to upload it to our [EvalAI server](https://evalai.srv.medius.si/).

## Solution documentation
After completing the tasks, please add documentation of your solutions to [solution.md](solution.md).


