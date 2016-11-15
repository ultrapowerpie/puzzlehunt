var clock;

$(document).ready(function() {

  // Grab the current date
  var currentDate = new Date();

  // Set some date in the future. In this case, it's always Jan 1
  var futureDate  = new Date(currentDate.getFullYear(), 11, 3, 21);

  // Calculate the difference in seconds between the future and current date
  var diff = futureDate.getTime() / 1000 - currentDate.getTime() / 1000;

  // Instantiate a coutdown FlipClock
  clock = $('.clock').FlipClock(diff, {
    clockFace: 'DailyCounter',
    countdown: true
  });
});

function rsvp(input) {
  $.ajax({
      url: '/rsvp',
      data: {'data':input},
      type: 'POST',
      success: function(response) {
          console.log(response);
      },
      error: function(error) {
          console.log(error);
      }
  });
}

$('#squaredThree').click(function() {
    if (this.checked) {
      $("#cancelled").hide();
      $("#clockContainer").css("visibility","visible");
      rsvp("1");
    }
    else {
      $("#clockContainer").css("visibility","hidden");
      $("#cancelled").show();
      rsvp("0");
    }

});
