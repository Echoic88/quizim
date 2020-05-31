$(document).ready(function () {

    checkForChartData()

    function checkForChartData() {
        let bar_chart_data = JSON.parse($("#bar_chart_data").text());

        if (parseInt(bar_chart_data.bar_labels.length) > 0) {
            drawGraph(bar_chart_data)
        }
    }
    
    function drawGraph(chart_data) {
        let options = {
            axisX: {
                showGrid: false,
            },
            axisY: {
                showGrid: false,
            },
            high: 100,
            low: 0,
        };

        let data = {
            labels: chart_data.bar_labels,
            series: [
                chart_data.bar_series
            ],
        };

        new Chartist.Bar("#bar-chart", data, options);
    }
});


// function drawGraph(chart_data) {
//     let options = {
//         axisX: {
//             showGrid: false,
//         },
//         axisY: {
//             showGrid: false,
//         },
//         high: 100,
//         low: 0,
//     };

//     let data = {
//         labels: bar_chart_data.bar_labels,
//         series: [
//             bar_chart_data.bar_series
//         ],
//     };

