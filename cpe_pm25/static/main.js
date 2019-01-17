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

function updateChart() {
  var ctx = $("#pm25-chart");
  $.getJSON("/api/history", function(data) {
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
            backgroundColor: ["rgba(255, 99, 132, 0.2)"],
            borderColor: ["rgba(255,99,132,1)"],
            borderWidth: 1
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
