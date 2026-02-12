// TODO: write the function to update all filter options
function update_filter_options(group_filters){

}

// TODO: write the function to draw the bar chart
function draw_bar(data, x_column, y_column){

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
        var results = JSON.parse(JSON.stringify((await response.json())))
        // TODO: extract the necessary data from the results and re-draw the bars
        // ...
        // draw_bar(...)
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
        // TODO: extract the necessary data from the results, re-draw the bars, and update the filters
        // ...
        // update_filter_options(...)
        // draw_bar(...)
    })
}

margin = {top: 30, right: 30, bottom: 70, left: 80},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

svg = d3.select("#plot-container")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("id", "plot")
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

update_aggregate(null, null)