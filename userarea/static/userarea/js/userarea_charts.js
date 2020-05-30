$(document).ready(function() {
    let bar_chart_data = JSON.parse($("#bar_chart_data").text());

    let options = {
        axisX:{
            showGrid: false,
        },
        axisY:{
            showGrid: false,
        },
        high: 100,
        low: 0,
      };

    let data = {
        labels:bar_chart_data.bar_labels,
        series:[
            bar_chart_data.bar_series
        ],
    };

    new Chartist.Bar("#bar-chart", data, options);
});