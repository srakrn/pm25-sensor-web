function updateValues() {
  $.getJSON("api/latest", function(data) {
    console.log(data);
    $("#aqi-badge")
      .removeClass()
      .addClass(
        "badge badger badge-" + data["description"]["shortcode"] + "-air"
      );
    $("#aqi-badge").html(data["description"]["brief_description"]);
    $("#aqi-description").html(data["description"]["description"]);
    $("#pm25-value").html(data["PM2.5"]);
    $("#pm10-value").html(data["PM10"]);
    $("#pm1-value").html(data["PM1"]);
    var timestamp = moment(data["timestamp"]);
    $("#timestamp").html(timestamp.format("DD/MM/YYYY HH:mm"));
  });
}

var pmchart = echarts.init(document.getElementById("pm25-chart-wrapper"));

function updateChart() {
  $.getJSON("api/history?amount=100", function(data) {
    var d = [];
    for (var i = 0; i < data.length; i++) {
      pm25 = data[i]["PM2.5"];
      timestamp = moment(data[i]["timestamp"]);
      d.unshift([timestamp.toDate(), pm25]);
    }
    console.log(d);
    var option = {
      title: {
        text: "ECharts entry example"
      },
      tooltip: {},
      legend: {
        data: ["Sales"]
      },
      xAxis: {
        type: "time",
        boundaryGap: false,
        axisLabel: {
          formatter: function(value) {
            return moment(value).format("DD/MM/YYYY HH:mm");
          }
        }
      },
      yAxis: [
        {
          type: "value"
        }
      ],
      series: [
        {
          name: "PM2.5",
          type: "line",
          data: d
        }
      ]
    };
    pmchart.setOption(option);
  });
}

$(".carousel").carousel({
  interval: 3000
});

function update() {
  updateValues();
  updateChart();
}

update();
setInterval(update, 5 * 60 * 1000);
