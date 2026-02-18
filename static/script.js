// TODO: write the function to update all filter options
function update_filter_options(group_filters){
    Object.keys(group_filters).forEach(group => {
        const select = d3.select(`#${group.replace('/', '\\/')}-filter`);
        const currentValue = select.property("value");
        
        // Clear existing options except 'All'
        select.selectAll("option:not([value='All'])").remove();
        
        // Add new filtered options
        group_filters[group].forEach(val => {
            select.append("option").attr("value", val).text(val);
        });
        
        // Re-set the value if it still exists in the list
        select.property("value", currentValue);
    });
}

// TODO: write the function to draw the bar chart
function draw_bar(data, x_column, y_column){
    // Convert dictionary format {key: val} -> array of objects [{x: key, y: val}]
    const plotData = Object.entries(data).map(([key, val]) => ({ x: key, y: val }));

    // Clear previous elements
    svg.selectAll("*").remove();

    // X axis
    const x = d3.scaleBand()
        .range([0, width])
        .domain(plotData.map(d => d.x))
        .padding(0.2);

    svg.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
            .attr("transform", "translate(-10,0)rotate(-45)")
            .style("text-anchor", "end");

    // Y Axis
    // buffered min
    let minY = d3.min(plotData, d => d.y);
    if (minY < 0) {
        minY *= 1.1; // 10% buffer
    } else {
        minY *= 0.9; // 10% buffer
    }
    const y = d3.scaleLinear()
        .domain([minY, d3.max(plotData, d => d.y) * 1.1]) // 10% buffer
        .range([height, 0]);

    svg.append("g")
        .call(d3.axisLeft(y));

    // Bars
    svg.selectAll("rect")
        .data(plotData)
        .enter()
        .append("rect")
            .attr("x", d => x(d.x))
            .attr("y", d => y(d.y))
            .attr("width", x.bandwidth())
            .attr("height", d => height - y(d.y))
            .attr("fill", "#4e79a7");

    // axis Labels
    svg.append("text")
        .attr("text-anchor", "end")
        .attr("x", width/2 + margin.left)
        .attr("y", height + margin.bottom - 5)
        .text(x_column);

    svg.append("text")
        .attr("text-anchor", "end")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 20)
        .attr("x", -height/2)
        .text(y_column);
}

function update_aggregate(value, key){    
    fetch('/update_aggregate', {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify({value: value, key: key}),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': 'application/json'
        })
    }).then(async function(response){
        var results = await response.json();
        draw_bar(results["data"], results["x_column"], results["y_column"]);
        // Reset dropdowns
        d3.selectAll("#filters-container select").property("value", "All");

        draw_bar(results["data"], results["x_column"], results["y_column"])
    })
}

function update_filter(value, key){
    fetch('/update_filter', {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify({value: value, key: key}),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': 'application/json'
        })
    }).then(async function(response){
        var results = JSON.parse(JSON.stringify((await response.json())))
        // Update the dropdown options
        update_filter_options(results["group_filters"]);
        
        // Sync UI: Set dropdown values to match the backend state 
        Object.keys(results["active_filters"]).forEach(k => {
            d3.select(`#${k.replace('/', '\\/')}-filter`).property("value", results["active_filters"][k]);
        });

        // Re-draw chart
        draw_bar(results["data"], results["x_column"], results["y_column"]);
    })
}

margin = {top: 30, right: 30, bottom: 70, left: 80},
    width = 805 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

svg = d3.select("#plot-container")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("id", "plot")
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

const default_agg = document.getElementById("agg").value;
const default_x = document.getElementById("grouper").value;
const default_y = document.getElementById("value").value;
update_aggregate(default_x, "grouper")
update_aggregate(default_y, "value")
update_aggregate(default_agg, "agg")