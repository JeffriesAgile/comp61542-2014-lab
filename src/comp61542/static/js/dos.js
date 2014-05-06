/**
 * Created by cipherhat on 07/04/2014.
 */

var w = 900,
    h = 500,
    fill = d3.scale.category20();

var vis = d3.select("#chart")
    .append("svg:svg")
    .attr("width", w)
    .attr("height", h);

d3.json("js/dos.json", function(json) {
    var force = d3.layout.force()
        .charge(-300)
        .linkDistance(50)
        .nodes(json.nodes)
        .links(json.links)
        .size([w, h])
        .start();

    var link = vis.selectAll("line.link")
        .data(json.links)
        .enter().append("svg:line")
        .attr("class", "link")
        .style("stroke-width", function(d) { return Math.sqrt(d.value); })
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    var node = vis.selectAll("circle.node")
        .data(json.nodes)
        .enter().append("svg:circle")
        .attr("class", "node")
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; })
        .attr("r", 10)
        .style("fill", function(d) { return fill(d.group); })
        .on('mouseover', fade(true))
        .on('mouseout', fade(false))
        .call(force.drag);

    node.append("svg:title")
        .text(function(d) { return d.name; });

    vis.style("opacity", 1e-6)
        .transition()
        .duration(1000)
        .style("opacity", 1);

    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    });

    function fade(bo) {
        return function(d) {
            var opacity = bo ? 0.2 : 1;
            var rad = radius(d);

            node.style('stroke-opacity', function(o) {
                thisOpac = isConnected(d, o) ? 1 : opacity;
                this.setAttribute('fill-opacity', thisOpac);
                return thisOpac;
            });

            link.style('stroke-opacity', function(o) {
                return o.source === d || o.target === d ? 1 : opacity;
            });

            node.select('name').remove();

            if (bo) {
                node.filter(function(o) {
                        return o === d;
                    })
                    .append('name')
                    .text(function(o) { return o.name; });
            }
        };
    }
});