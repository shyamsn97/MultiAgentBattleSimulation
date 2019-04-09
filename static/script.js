    var ws = new WebSocket("ws://localhost:8000/websocket");
    var count = 0;
    var curr = 0;
    var scale = 1;
    var frames = [[]];
    var playing = false;
    var num_teams = 1;
    var colors = ["red","blue","green","orange"];
    var agentarr = [[]]
    var agent_counts = 0
    function drawBoard(scale) {
      map = frames[curr]
      var p = 5;
      var bw = map[0].length;
      var bh = map.length;
      var padding = 10;

      var canvas = document.getElementById("canvas");
      var context = canvas.getContext("2d");
      context.canvas.width = (padding + bw*p)*scale;
      context.canvas.height = (padding + bh*p)*scale;
      context.setTransform(scale, 0, 0, scale, 0, 0);
      context.clearRect(0, 0, context.canvas.width, context.canvas.height);
      context.beginPath();
      //border
      context.moveTo(padding,padding);
      context.lineTo(padding+(bw*p),padding);
      context.lineTo(padding+(bw*p),padding + bh*p);
      context.lineTo(padding,padding + bh*p);
      context.lineTo(padding,padding);
      for (var y = 0; y < bh; y += 1) {
        for (var x = 0; x < bw; x += 1) {
          // for grid
          // context.moveTo(padding + x*p,padding + y*p);
          // context.lineTo(padding + x*p + p,padding + y*p);
          // context.lineTo(padding + x*p + p,padding + y*p + p)
          // context.lineTo(padding + x*p, padding + y*p + p)
          // context.lineTo(padding + x*p,padding + y*p);
          if (map[y][x] > 0) {
            context.fillStyle = colors[map[y][x]-1];
            context.fillRect(padding + x*p,padding + y*p,p,p);
            // context.moveTo(padding + x*p + p,padding + y*p + p/2);
            // context.lineTo(padding + x*p + p/2,padding + y*p + p/2)
          }
          if (map[y][x] == 0) {
            context.fillStyle = "#d6f8d2";
            context.fillRect(padding + x*p,padding + y*p,p,p);          
          }
        }
      }
      context.strokeStyle = "black";
      context.stroke();
    };

    function showFrame(value) {
      curr = value;
      drawBoard(scale);
    }

    function setSlider() {
      document.getElementById("frame_replay").value = curr;
    }

    function pressPlay() {
      if (playing == false || curr == frames.length - 1) {
        playing = true;
        play();
      }
    }
    function play() {
      if (curr >= frames.length - 1) {
        curr = -1;
      }
      change_frame('right');
      if (curr < frames.length - 1) {
        timer = setTimeout(play,10);
      }
    }

    function stop() {
      playing = false;
      if (timer) {
        clearInterval( timer );
        timer=null;
      }
    }

    function change_frame(direction) {
        if (direction === 'left' && curr > 0) {
          curr--;
          setSlider();
          drawBoard(scale);
        }
        if (direction === 'right' && curr < frames.length - 1) {
          curr++;
          setSlider();
          drawBoard(scale);
        }
        changeCounts();
    }

    function reset(direction) {
      stop()
      if (direction === 'left') {
        curr = 1;
        change_frame(direction);
      }
      if (direction === 'right') {
        curr = frames.length - 2;
        change_frame(direction);
      }
    }

    function zoomin() {
      if (scale < 4) {
        scale = scale + 0.5;
        drawBoard(scale);
      }
    };

    function zoomout() {
      if (scale > 1) {
        scale = scale - 0.5;
        drawBoard(scale);
      }
    };

    function sendMessage(job,message) {
        var payload = {
          "job": job,
          "message": message,
        }
        // Make the request to the WebSocket.
        ws.send(JSON.stringify(payload));
    };

    function changeCounts() {
      document.getElementById("stats_text").innerHTML = "Counts: " + parseInt(agent_counts[curr]);
    }

    function createTable() {
      var table = document.getElementById("table");
      var agentarr = agents[curr]
    }
    ws.onmessage = function(evt) {
      var messageDict = JSON.parse(evt.data);
      if (messageDict.job == "setup") {
        console.log("Setting up UI...");
        console.log(messageDict.agents[0]);
        agents = messageDict.agents;
        frames = messageDict.frames;
        num_teams = messageDict.num_teams;
        agent_counts = messageDict.counts
        document.getElementById("frame_replay").max = parseInt(frames.length - 1)
        var canvas = document.getElementById("canvas");
        drawBoard(1);
        changeCounts();
        sendMessage("tick","UI loaded successfully!");
        count++;
      }
      if (messageDict.job == "tick") {
        sendMessage("tick","tick " + parseInt(count))
        count++;
      }
    };