import altair as alt
import pandas as pd
import io
import base64
from altair_saver import save


alt.data_transformers.disable_max_rows()


def _save_plot_to_img_tag(chart):
    figure_bytes = io.BytesIO()
    save(chart, figure_bytes, fmt='png', webdriver='chrome')
    figure_bytes.seek(0)
    return ''' <img src="data:image/png;base64,%s" width="640" height="480" border="0" /> ''' % (base64.b64encode(figure_bytes.read()).decode('utf-8'))


def plot_timeseries(data):
    data['date'] = data['date'].astype('str')
    chart = alt.Chart(data).mark_trail().encode(
        x=alt.X("date:T"),
        y=alt.Y("amplitude:Q"),
        color='origin',
        strokeDash='origin',
    ).interactive()
    return _save_plot_to_img_tag(chart)


def evaluation_graphs(y_true, y_predicted):
    """Evaluation graphs of absoluste error
    """
    eval_diff = (y_true - y_predicted)
    source = pd.DataFrame(
        {'category': ['wrong predicted leakage state', 'wrong predicted normal state', 'correct prediction'],
         'absolute value': [sum(eval_diff < 0), sum(eval_diff > 0), sum(eval_diff == 0)],
         }
    )
    bar = alt.Chart(source).mark_bar(size=30).encode(
        x=alt.X('category', axis=alt.Axis(
            labelAngle=-65,
            labelOverlap=False,
            title="",
        )
                ),
        y=alt.Y('absolute value:Q', title="Absolute value"),
        color=alt.condition(
            alt.datum.x == "correct prediction",  # If the year is 1810 this test returns True,
            alt.value('green'),     # which sets the bar orange.
            alt.value('red')   # And if it's not true it sets the bar steelblue.
        )
    ).properties(width=200)

    source = pd.DataFrame(
        {'category': ['wrong predicted leakage state', 'wrong predicted normal state', 'correct prediction'],
         'percent': [sum(eval_diff < 0)/eval_diff.shape[0], sum(eval_diff > 0)/eval_diff.shape[0], sum(eval_diff == 0)/eval_diff.shape[0]],
         }
    )

    pie = alt.Chart(source).mark_arc().encode(
        theta=alt.Theta(field="percent", type="quantitative"),
        color=alt.Color('category',legend=alt.Legend(title="Evaluation error/match category"))
    )
    chart = alt.hconcat(bar, pie).properties(
        title="Evaluation of predicted leakage periods.",
    )

    return _save_plot_to_img_tag(chart)


def draw_error(data):
    """Draw error on timeline graph
    """
    data['date'] = data['date'].astype('str')
    chart = alt.Chart(data).transform_calculate(
        negative='datum.d < 0'
    ).mark_area().encode(
        x="date:T",
        y=alt.Y('d', impute={'value': 0}),
        color='negative:N'
    )

    return _save_plot_to_img_tag(chart)
