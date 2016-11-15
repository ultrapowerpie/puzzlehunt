var puzzle = document.getElementById("puzzle"),
puzzleCanvas = puzzle.getContext('2d'),
brushRadius = 25,
img = new Image();

img.onload = function(){
  puzzleCanvas.drawImage(img, 0, 0, puzzle.width, puzzle.height);
}

img.src = '/static/images/front_t.png';

function detectLeftButton(event) {
    if ('buttons' in event) {
        return event.buttons === 1;
    } else if ('which' in event) {
        return event.which === 1;
    } else {
        return event.button === 1;
    }
}

function getBrushPos(xRef, yRef) {
  var puzzleRect = puzzle.getBoundingClientRect();
    return {
    x: Math.floor((xRef-puzzleRect.left)/(puzzleRect.right-puzzleRect.left)*puzzle.width),
    y: Math.floor((yRef-puzzleRect.top)/(puzzleRect.bottom-puzzleRect.top)*puzzle.height)
    };
}

function drawDot(mouseX,mouseY){
  puzzleCanvas.beginPath();
    puzzleCanvas.arc(mouseX, mouseY, brushRadius, 0, 2*Math.PI, true);
    puzzleCanvas.fillStyle = '#000';
    puzzleCanvas.globalCompositeOperation = "destination-out";
    puzzleCanvas.fill();
}

puzzle.addEventListener("mousemove", function(e) {
  var brushPos = getBrushPos(e.clientX, e.clientY);
  var leftBut = detectLeftButton(e);
  if (leftBut == 1) {
    drawDot(brushPos.x, brushPos.y);
  }
}, false);

puzzle.addEventListener("touchmove", function(e) {
    e.preventDefault();
    var touch = e.targetTouches[0];
    if (touch) {
      var brushPos = getBrushPos(touch.pageX, touch.pageY);
      drawDot(brushPos.x, brushPos.y);
    }
}, false);

function isNumeric(n) {
  return !isNaN(parseInt(n)) && isFinite(n);
}

function submitAnswer() {
  var answer = $("#answer").val();

  if (!(isNumeric(answer))) {
   $("#hint1").hide();
   $("#hint2").hide();
   $("#hint3").hide();
   $("#hint0").fadeIn();
  }
  else if (answer == "1891") {
   $("#welcomeContainer").hide();
   $("#loginContainer").fadeIn(1000);
  }
  else if (answer == "1524") {
   $("#hint0").hide();
   $("#hint1").hide();
   $("#hint3").hide();
   $("#hint2").fadeIn();
  }
  else if (answer == "1341") {
   $("#hint0").hide();
   $("#hint1").hide();
   $("#hint2").hide();
   $("#hint3").fadeIn();
  }
  else {
   $("#hint0").hide();
   $("#hint2").hide();
   $("#hint3").hide();
   $("#hint1").fadeIn();
  }
}

$(document).ready(function() {

  $('#answer').on('keypress', function (e) {
    if(e.which === 13) { submitAnswer(); }
   });
});
