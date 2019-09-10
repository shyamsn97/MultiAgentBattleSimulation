    var ws = new WebSocket("ws://localhost:8888/websocket");
    var count = 0;
    var curr = 0;
    var scale = 1;
    var frames = [[]];
    var playing = false;
    var num_teams = 1;
    var colors = ["blue","red","green","orange"];
    var agents = [[]]
    var agent_counts = 0
    var teamHeaders = [];
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
      setSlider();
      drawBoard(scale);
      changeCounts();
      updateTeamRow();
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
        updateTeamRow();
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

    function createNewHeader(headerTitle) {
      const temp = document.createElement('th');
      temp.appendChild(document.createTextNode(headerTitle));
      return temp
    }

    function createHeader(tableheader,tableHeaders) {
      tableheader.innerHTML = "";
      tableHeaders.forEach(header=>{
        tableheader.appendChild(createNewHeader(header));   
      })  
    }

    function createRow(table,values) {
      var row = table.insertRow(-1);
      for (var i = 0; i < values.length; i++) {
        row.insertCell(i).innerHTML = values[i];
      }
    }

    function createTeamTable() {
      var table = document.getElementById("team-table");
      var tableheader = document.getElementById("team-table-header");
      createHeader(tableheader,teamHeaders);
      createRow(table,team_counts[curr])
    }

    function updateTeamRow() {
      var table = document.getElementById("team-table");
      var row = table.rows[table.rows.length - 1];
      var team_count = team_counts[curr];
      for (var i = 0; i < num_teams; i++) {
        row.cells[i].innerHTML = team_count[i];
      }
    }

    ws.onmessage = function(evt) {
      var messageDict = JSON.parse(evt.data);
      console.log(messageDict);
      if (messageDict.job == "setup") {
        console.log("Setting up UI...");
        agents = messageDict.agents;
        frames = messageDict.frames;
        num_teams = messageDict.num_teams;
        agent_counts = messageDict.agent_counts;
        team_counts = messageDict.team_counts;
        var teamHeaders = [];
        for (var i = 0; i < num_teams; i++) {
          teamHeaders.push("Team " + parseInt(i))
        }
        document.getElementById("frame_replay").max = parseInt(frames.length - 1)
        var canvas = document.getElementById("canvas");
        drawBoard(1);
        changeCounts();
        createTeamTable();
        sendMessage("tick","UI loaded successfully!");
        count++;
      }
      if (messageDict.job == "tick") {
        sendMessage("tick","tick " + parseInt(count))
        count++;
      }
    };

