// Global variables for the video element
var video = document.getElementById("video");
var drafting = false;
var init_done = false;
var video_done = false;

// Update comment count with proper amount of comments
document.getElementById("comment_count").innerHTML = document.getElementById("comments").childElementCount;

// Format seconds to readable time format
function fancyTimeFormat(time) {
    var hrs = ~~(time / 3600);
    var mins = ~~((time % 3600) / 60);
    var secs = ~~time % 60;
    var ret = "";
    if (hrs > 0) {
        ret += "" + hrs + ":" + (mins < 10 ? "0" : "");
    }
    ret += "" + mins + ":" + (secs < 10 ? "0" : "");
    ret += "" + secs;
    return ret;
}

// Get integer value in seconds of a formatted time
function regularTimeFormat(time) {
  var data = time.split(":");
  var seconds = parseInt(data[1]);
  seconds += parseInt(data[0]*60);
  return seconds;
}

// Check to see if there's a comment to display at the current time of the video
function showcase(seconds) {
  document.getElementById("comment_showcase").style.opacity = "1";
  if (document.getElementsByClassName("comment" > 0)) {
    var times_inseconds = [];
    var comment_times = document.getElementsByClassName("time_stamp");
    for (var j = 0; j < comment_times.length; j++) {
      times_inseconds.push(regularTimeFormat(comment_times[j].innerHTML));
    }

    var showcase_options = [];
    for (var i = 0; i < times_inseconds.length; i++) {
      if (Math.floor(seconds) === times_inseconds[i]) {
        showcase_options.push([i, parseInt(document.getElementsByClassName("comment_score")[i].innerHTML)]);
        console.log(showcase_options);
      }
    }

    // If there are multiple comments at this time, display the comment with the higher rating
    if (showcase_options.length > 0) {
      var max = [-10000, -10000];
      for (var j = 0; j < showcase_options.length; j++) {
        if (showcase_options[j][1] > max[1]) {
          max = [showcase_options[j][0], showcase_options[j][1]];
        }
      }
      var comment_element = document.getElementsByClassName("comment")[max[0]];
      var copy = comment_element.cloneNode(true);

      document.getElementById("comment_showcase").innerHTML = '';
      document.getElementById("comment_showcase").appendChild(copy);
    }
  }
}

// Wait for video and comments to load to (hopefully) successfully initialize custom video controls
video.oncanplaythrough = function() {
  setTimeout(function(){
    video = document.getElementById("video");
    initControls();
    console.log(document.getElementsByClassName('comment'));
  }, 100);
}

// showcase any last comments
video.onended = function() {
  showcase(Math.ceil(video.duration));
  document.getElementById("pp").innerHTML = "play_arrow";
  video_done = true;
}

// Update time displays and progress bar everytime video time updates
video.ontimeupdate = function() {
  var seconds = video.currentTime;
  var ticks = document.getElementsByClassName("tick");
  if (!drafting) {
    document.getElementById("current_time").innerHTML = fancyTimeFormat(seconds);
  }
  if (ticks[Math.floor(seconds)]) {
    ticks[Math.floor(seconds)].classList.add("passed");
    if (ticks[Math.floor(seconds)].firstElementChild) {
      ticks[Math.floor(seconds)].firstElementChild.classList.add("passed");
    }
  }
  document.getElementById("cur").innerHTML = fancyTimeFormat(seconds);

  showcase(seconds);
}

// When progress bar clicked, update progress bar and skip to that point in the video
function jumpTo(pos) {
  var ticks = document.getElementsByClassName("tick");
  var ind = parseInt(pos.substring(1));
  console.log(ind);
  video.currentTime = ind;
  for (var i = 0; i < ind; i ++) {
    if (!ticks[i].classList.contains("passed")) {
      ticks[i].classList.toggle("passed");
      if (ticks[i].firstElementChild) {
        ticks[i].firstElementChild.classList.toggle("passed");
      }
    }
  }
  for (i = ind; i < ticks.length; i++) {
    if (ticks[i].classList.contains("passed")) {
      ticks[i].classList.toggle("passed");
      if (ticks[i].firstElementChild) {
        ticks[i].firstElementChild.classList.toggle("passed");
      }
    }
  }
}

// Initialize video controls: get current time and total duration, create the progress bar which is a table with a cell for every second of the video
function initControls() {
  if (!init_done) {
    console.log('Initializing controls');
    document.getElementById("tot").innerHTML = fancyTimeFormat(video.duration);
    for (var i = 0; i < Math.floor(video.duration)+1; i++) {
      var td = document.createElement("td");
      td.setAttribute('class', 'tick');
      td.setAttribute('id', 't'+i);
      td.setAttribute('onclick', 'jumpTo(this.id)');
      td.setAttribute('width', document.getElementById("video").clientWidth/Math.floor(video.duration+1));

      document.getElementById("prog_row").appendChild(td);
      var times_inseconds = [];

      var comment_times = document.getElementsByClassName("time_stamp");
      for (var j = 0; j < comment_times.length; j++) {
        times_inseconds.push(regularTimeFormat(comment_times[j].innerHTML));
      }

      for (j = 0; j < times_inseconds.length; j++) {
        if (i === times_inseconds[j]) {
          document.getElementsByClassName('tick')[i].classList.add('sqr');
        }
      }
    }
    init_done = true;
  }
}

// Play or pause the video depending on current state
function playPause() {
  if (video.paused) {
    if (video_done) {
      var ticks = document.getElementsByClassName('tick');
      for (i = 0; i < ticks.length; i++) {
        if (ticks[i].classList.contains("passed")) {
          ticks[i].classList.toggle("passed");
        }
      }
      video_done = false;
    }
    video.play();
    document.getElementById("pp").innerHTML = "pause";
  }
  else {
    video.pause();
    document.getElementById("pp").innerHTML = "play_arrow";
  }
}

// Mute or ubmute the video depending on current state
function muteUnmute() {
  if (video.muted) {
    video.muted = false;
    document.getElementById("mu").innerHTML = "volume_up"
  }
  else {
    video.muted = true;
    document.getElementById("mu").innerHTML = "volume_off"
  }
}
