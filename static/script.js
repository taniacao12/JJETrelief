var svg = d3.select("#landing_map");
var mapLegend = d3.select("#mapLegend");
var placeholder = d3.select("#loading")

var path = d3.geoPath();

//Year display on HTML
var slider = document.getElementById("year")
var display = document.getElementById("current_year")

var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .attr("id", "map-tooltip")
    .style("opacity", 0);

//Loading average temperature data

//Drawing US map
//JSON file being used here is an online version of the map.json file in the data directory. We aren't using the local version to bypass Chrome errors with opening a local file.
d3.json("https://cdn.jsdelivr.net/npm/us-atlas@2/us/10m.json", function(error, us) {
  if (error) throw error;

  svg.append("g")
      .attr("class", "counties")
    .selectAll("path")
    .data(topojson.feature(us, us.objects.counties).features)
    .enter().append("path")
      .attr("class", "county-path")
      .attr("id", function(d) {
        return d.properties.name;
      })
      .attr("d", path)
      .on("click", function(d) {
          console.log(this)
      });

  svg.append("path")
      .attr("class", "county-borders")
      .attr("d", path(topojson.mesh(us, us.objects.counties, function(a, b) { return a !== b; })));

  svg.append("g")
      .attr("class", "states")
    .selectAll("path")
    .data(topojson.feature(us, us.objects.states).features)
    .enter().append("path")
      .attr("d", path);

  svg.append("path")
      .attr("class", "state-borders")
      .attr("d", path(topojson.mesh(us, us.objects.states, function(a, b) { return a !== b; })));

});

//Loading average temperature data
d3.json("https://raw.githubusercontent.com/puneetjohal/ShrimpCrackers/master/climatecrackers/data/newLandingData.json", function(error, data) {
  if (error) throw error;

  //Color interpolation
  var fill = d3.scaleLinear()
      .domain([15, 100])
      .range(["steelblue", "red"]);
    //.interpolator(d3.interpolateCool);

  //Helper that get the tavg from temps object
  function getTemp(name, year) {
    var temp;
    name = name + " County";
    temp = data[year][name];

    if (temp == undefined || temp.toString() === "" || temp.toString() === "0") {
      return 0;
    }
    else {
        // console.log(temp);
        return parseFloat(temp);
    }
  }

  function changeColor(name, value) {
      temp = getTemp(name, value);
      if (temp == 0) {
        return "#D3D3D3";
      }
      else {
      return fill(temp);
  }
};

  function update(value) {
    svg.selectAll(".county-path")
      .style("fill", d => changeColor(d.properties.name, value));
  }

  //Year display on HTML
  display.innerHTML = slider.value;
  slider.oninput = function() {
    display.innerHTML = this.value;
    update(+this.value);
  }

  //Color change when slider is adjusted
  // d3.select("#year").on("input", function() {
  //   update(+this.value);
  // });

  function tooltipText(name, value) {
      text = name + " County<br/>"
      temp = getTemp(name, value);
      if (temp == 0) {
          return text + "N/A";
      }
      else {
          return text + temp + " F";
      }
  }

  svg.selectAll(".county-path")
    .on("mouseover", function(d) {
      div.style("opacity", .9);
      div.html(tooltipText(d.properties.name, slider.value))
      .style("left", (d3.event.pageX) + "px")
      .style("top", (d3.event.pageY - 45) + "px");
      // console.log(d3.select(this));
      d3.select(this).style("fill", "#ffffad")
  })
    .on("mouseout", function(d) {
      // div.transition()
      // .duration(500)
      d3.select(this).style("fill", d => changeColor(d.properties.name, slider.value))
      div.style("opacity", 0);
  })


  update(2010);
  placeholder.remove();
}); //Close temps JSON

//Add legend
var w = 140, h = 300;

var key = mapLegend
	.append("g")
	.attr("width", w)
	.attr("height", h)
	.attr("class", "legend");

var legend = key.append("defs")
	.append("svg:linearGradient")
	.attr("id", "gradient")
	.attr("x1", "100%")
	.attr("y1", "0%")
	.attr("x2", "100%")
	.attr("y2", "100%")
	.attr("spreadMethod", "pad");

legend.append("stop")
	.attr("offset", "0%")
	.attr("stop-color", "red")
	.attr("stop-opacity", 1);

legend.append("stop")
	.attr("offset", "100%")
	.attr("stop-color", "steelblue")
	.attr("stop-opacity", 1);

key.append("rect")
	.attr("width", w - 100)
	.attr("height", h)
	.style("fill", "url(#gradient)")
	.attr("transform", "translate(0,10)");

var y = d3.scaleLinear()
	.range([h, 0])
	.domain([15, 100]);

var yAxis = d3.axisRight(y);

key.append("g")
	.attr("class", "y axis")
	.attr("transform", "translate(41,10)")
	.call(yAxis);
