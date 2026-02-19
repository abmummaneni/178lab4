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
    group_filters = {}
    for group in groups:
        # Build options using all active filters EXCEPT this dropdown itself
        df = orders
        for k, v in app.filters.items():
            if k != group and v != "All":
                df = df[df[k] == v]
        group_filters[group] = sorted(df[group].dropna().unique().tolist())
    return group_filters


# TODO: define a function that returns the aggregated data
def get_aggregated_data():
    actual_agg = "var" if app.agg == "variance" else app.agg
    agg = app.filtered_orders.groupby(app.grouper)[app.value].agg(actual_agg).fillna(0)

    # Keep all categories visible; missing groups become 0
    all_groups = sorted(orders[app.grouper].dropna().unique().tolist())
    agg = agg.reindex(all_groups, fill_value=0)
    return agg.to_dict()


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

    # 3b: Reset all filters to "All" 
    app.filters = {"Country/Region": "All", "Region": "All", "State/Province": "All"}
    app.filtered_orders = orders

    if key == "grouper":
        app.grouper = val
    elif key == "value":
        app.value = val
    elif key == "agg":
        app.agg = val

    return {
        "data": get_aggregated_data(), 
        "x_column": app.grouper, 
        "y_column": app.value,
        "group_filters": get_group_filters(),
        "active_filters": app.filters
    }

# TODO: Complete the update_filter function
@app.route("/update_filter", methods=["POST"])
def update_filter():
    data = request.get_json()

    # Change 'group' to 'key' to match frontend fetch call
    filter_type = data["key"] 
    filter_val = data["value"]

    app.filters[filter_type] = filter_val
    # Reset downsteram filters
    if filter_type == "Country/Region":
        app.filters["Region"] = "All"
        app.filters["State/Province"] = "All"
    elif filter_type == "Region":
        app.filters["State/Province"] = "All"

    # 3a: If State is selected, automatically update Country and Region 
    if filter_type == "State/Province" and filter_val != "All":
        # Find the row to get parent info
        match = orders[orders["State/Province"] == filter_val].iloc[0]
        app.filters["Country/Region"] = match["Country/Region"]
        app.filters["Region"] = match["Region"]
    app.filtered_orders = orders
    for k, v in app.filters.items():
        if v != "All":
            app.filtered_orders = app.filtered_orders[app.filtered_orders[k] == v]

    return {
        "group_filters": get_group_filters(), 
        "data": get_aggregated_data(), 
        "x_column": app.grouper, 
        "y_column": app.value,
        "active_filters": app.filters # Useful for syncing the UI
    }

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
