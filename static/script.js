// TODO: write the function to update all filter options
function update_filter_options(group_filters, active_filters){
    Object.keys(group_filters).forEach(group => {
        const select = d3.select(`#${group.replace('/', '\\/')}-filter`);
        
        // Clear existing options except 'All'
        select.selectAll("option:not([value='All'])").remove();
        
        // Add new filtered options
        group_filters[group].forEach(val => {
            select.append("option").attr("value", val).text(val);
        });
        
        // Re-set the value if it still exists in the list
        select.property("value", active_filters[group] || "All");
    });
}

// TODO: write the function to draw the bar chart
function draw_bar(data, x_column, y_column){
    const plotData = Object.entries(data).map(([key, val]) => ({ x: key, y: +val }));
    svg.selectAll("*").remove();

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

    let yMin = Math.min(0, d3.min(plotData, d => d.y));
    let yMax = Math.max(0, d3.max(plotData, d => d.y));
    if (yMin < 0) {
        yMin *= 1.1; // Add 10% padding if negative values exist
    } else {
        yMin = 0; // Start from 0 if all values are positive
    }
    yMax *= 1.1; // Add 10% padding to max value

    const y = d3.scaleLinear()
        .domain([yMin, yMax])
        .nice()
        .range([height, 0]);

    svg.append("g").call(d3.axisLeft(y));

    svg.selectAll("rect")
        .data(plotData)
        .enter()
        .append("rect")
        .attr("x", d => x(d.x))
        .attr("y", d => Math.min(y(0), y(d.y)))
        .attr("width", x.bandwidth())
        .attr("height", d => Math.abs(y(d.y) - y(0)))
        .attr("fill", "#4e79a7");

    // X-axis label
    svg.append("text")
        .attr("text-anchor", "middle")
        .attr("x", width / 2)
        .attr("y", height + margin.bottom - 10)
        .text(x_column);

    // Y-axis label
    svg.append("text")
        .attr("text-anchor", "middle")
        .attr("transform", "rotate(-90)")
        .attr("x", -height / 2)
        .attr("y", -margin.left + 20)
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
        update_filter_options(results["group_filters"], results["active_filters"]);
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
        update_filter_options(results["group_filters"], results["active_filters"]);

        draw_bar(results["data"], results["x_column"], results["y_column"]);
    })
}

margin = {top: 30, right: 30, bottom: 100, left: 80},
    width = 1080 - margin.left - margin.right,
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