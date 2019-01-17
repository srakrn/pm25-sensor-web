function updateValues() {
  $.getJSON("/api/latest", function(data) {
    console.log(data);
    $("#pm25").html(data["PM2.5"]);
    $("#pm10").html(data["PM10"]);
    $("#pm1").html(data["PM1"]);
    $("#pm1").html(data["PM1"]);
    $("#timestamp").html(data["timestamp"]);
  });
}

$(".carousel").carousel({
  interval: 3000
});
setInterval(updateValues, 15 * 60 * 1000);
