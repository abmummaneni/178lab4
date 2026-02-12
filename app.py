from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# TODO: load the superstore data into a pandas DataFrame
orders = []
app.filtered_orders = orders
app.filters = {}
app.grouper = "Country/Region"
app.value = "Profit"
app.agg = "sum"

# TODO: define the groups, values, and aggregate functions that the user can select
groups = []
values = []
aggs = []


# TODO: define a function for getting possible filter options for each grouper
def get_group_filters():
    pass


#    group_filters = ...
#    return group_filters


# TODO: define a function that returns the aggregated data
def get_aggregated_data():
    pass


#    aggregated_data = ...
#    return aggregated_data


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
    pass
    # ...
    # return {'data': ..., 'x_column': ..., }


# TODO: Complete the update_filter function
@app.route("/update_filter", methods=["POST"])
def update_filter():
    pass
    # ...
    # return {'group_filters': ..., 'data': ..., }


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
