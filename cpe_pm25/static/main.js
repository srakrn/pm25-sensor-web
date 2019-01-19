function updateValues() {
  $.getJSON("api/latest", function(data) {
    console.log(data);
    $("#pm25-valie").html(data["PM2.5"]);
    $("#pm10-value").html(data["PM10"]);
    $("#pm1-value").html(data["PM1"]);
    var timestamp = moment(data["timestamp"]);
    $("#timestamp").html(timestamp.format("DD/MM/YYYY HH:mm"));
  });
}

var ctx = document.getElementById("pm25-chart").getContext("2d");
var gradientStroke = ctx.createLinearGradient(0, 0, 0, 200);
gradientStroke.addColorStop(0, "rgba(255, 160, 0, 0.8)");
gradientStroke.addColorStop(1, "rgba(255, 160, 0, 0)");

function updateChart() {
  $.getJSON("api/history?amount=100", function(data) {
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
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              }
            }
          ]
        },
        annotation: {
          annotations: [
            {
              drawTime: "afterDatasetsDraw",
              id: "startingHealthAffection",
              type: "line",
              mode: "horizontal",
              scaleID: "y-axis-0",
              value: 50,
              borderColor: "black",
              borderWidth: 2,
              borderDash: [2, 2],
              label: {
                enabled: true,
                backgroundColor: "#FF6F00",
                content: "เริ่มมีผลกระทบต่อสุขภาพ",
                position: "left",
                xAdjust: 10
              }
            },
            {
              drawTime: "afterDatasetsDraw",
              id: "healthAffection",
              type: "line",
              mode: "horizontal",
              scaleID: "y-axis-0",
              value: 90,
              borderColor: "black",
              borderWidth: 2,
              borderDash: [2, 2],
              label: {
                enabled: true,
                backgroundColor: "#D84315",
                content: "มีผลกระทบต่อสุขภาพ",
                position: "left",
                xAdjust: 10
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
