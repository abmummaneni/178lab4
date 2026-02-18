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
    df = orders.copy()
    
    # if Country is 'United States'
    # the State list should only show US states
    if app.filters["Country/Region"] != "All":
        df = df[df["Country/Region"] == app.filters["Country/Region"]]
    if app.filters["Region"] != "All":
        df = df[df["Region"] == app.filters["Region"]]
        
    group_filters = {
        "Country/Region": sorted(list(orders["Country/Region"].unique())),
        "Region": sorted(list(df["Region"].unique())),
        "State/Province": sorted(list(df["State/Province"].unique())),
    }
    return group_filters


# TODO: define a function that returns the aggregated data
def get_aggregated_data():
    df = orders.copy()

    for col, val in app.filters.items():
        if val != "All":
            df = df[df[col] == val]
            
    if df.empty:
        return {}

    # Map "variance" to "var" for Pandas compatibility 
    actual_agg = "var" if app.agg == "variance" else app.agg

    aggregated_data = df.groupby(app.grouper)[app.value].agg(actual_agg)

    # Get all unique values for the current grouper from the original dataset
    all_grouper_values = orders[app.grouper].unique()

    # Reindex the aggregated data to include all possible grouper values and fill NaN with 0
    aggregated_data = aggregated_data.reindex(all_grouper_values, fill_value=0)
    
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
    
    # 3b: Reset all filters to "All" 
    app.filters = {"Country/Region": "All", "Region": "All", "State/Province": "All"}
    
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
    
    # 3a: If State is selected, automatically update Country and Region 
    if filter_type == "State/Province" and filter_val != "All":
        # Find the row to get parent info
        match = orders[orders["State/Province"] == filter_val].iloc[0]
        app.filters["Country/Region"] = match["Country/Region"]
        app.filters["Region"] = match["Region"]

    return {
        "group_filters": get_group_filters(), 
        "data": get_aggregated_data(), 
        "x_column": app.grouper, 
        "y_column": app.value,
        "active_filters": app.filters # Useful for syncing the UI
    }

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
