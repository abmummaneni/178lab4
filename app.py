from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

orders = pd.read_excel("Sample - Superstore.xls")
app.filtered_orders = orders
app.filters = {"Country/Region": "All", "Region": "All", "State/Province": "All"}
app.grouper = "Country/Region" # X-axis
app.value = "Profit"           # Y-axis
app.agg = "sum"

groups = ["Country/Region", "Region", "State/Province"]
values = ["Quantity", "Sales", "Profit"]
aggs = ["sum", "mean", "variance", "count"]


def get_group_filters():
    group_filters = {
        "Country/Region": sorted(list(app.filtered_orders["Country/Region"].unique())),
        "Region": sorted(list(app.filtered_orders["Region"].unique())),
        "State/Province": sorted(list(app.filtered_orders["State/Province"].unique())),
    }
    return group_filters


# TODO: define a function that returns the aggregated data
def get_aggregated_data():
    aggregated_data = app.filtered_orders.groupby(app.grouper)[app.value].agg(app.agg)
    return aggregated_data.to_dict()


# Pass the groups, values, aggregate functions, and group filters to the root.html template
@app.route("/")
def root():
    return render_template(
        "root.html",
        groups=groups,
        values=values,
        aggs=aggs,
        group_filters=get_group_filters(),
    )


# TODO: Complete the update_aggregate
@app.route("/update_aggregate", methods=["POST"])
def update_aggregate():
    data = request.get_json()
    key = data["key"]
    val = data["value"]
    if key == "grouper":
        app.grouper = val
    elif key == "value":
        app.value = val
    elif key == "agg":
        app.agg = val
    return {"data": get_aggregated_data(), "x_column": app.grouper, "y_column": app.value}
    # ...
    # return {'data': ..., 'x_column': ..., }


# TODO: Complete the update_filter function
@app.route("/update_filter", methods=["POST"])
def update_filter():
    data = request.get_json()
    app.filters[data["group"]] = data["value"]
    return {"group_filters": get_group_filters(), "data": get_aggregated_data(), "x_column": app.grouper, "y_column": app.value}
   


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
