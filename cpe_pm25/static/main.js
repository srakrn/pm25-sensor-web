function updateValues() {
  $.getJSON("/api/latest", function(data) {
    console.log(data);
    $("#pm25").html(data["PM2.5"]);
    $("#pm10").html(data["PM10"]);
    $("#pm1").html(data["PM1"]);
    $("#pm1").html(data["PM1"]);
    var timestamp = moment(data["timestamp"]);
    $("#timestamp").html(timestamp.format("DD/MM/YYYY HH:mm"));
  });
}

var ctx = document.getElementById("pm25-chart").getContext("2d");
var gradientStroke = ctx.createLinearGradient(0, 0, 0, 200);
gradientStroke.addColorStop(0, "rgba(255, 160, 0, 0.8)");
gradientStroke.addColorStop(1, "rgba(255, 160, 0, 0)");

function updateChart() {
  $.getJSON("/api/history?amount=100", function(data) {
    var dataPoints = [];
    var labels = [];
    for (var i = 0; i < data.length; i++) {
      dataPoints.unshift(data[i]["PM2.5"]);
      timestamp = moment(data[i]["timestamp"]);
      labels.unshift(timestamp.format("DD/MM/YYYY HH:mm"));
    }
    console.log(dataPoints);
    console.log(labels);
    var myChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "PM2.5",
            data: dataPoints,
            backgroundColor: gradientStroke,
            borderColor: "#FF6F00",
            borderWidth: 3
          }
        ]
      },
      options: {
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              }
            }
          ]
        }
      }
    });
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
