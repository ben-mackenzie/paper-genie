import React, { Component, Fragment } from 'react';
import * as d3 from "d3";


const width = 1200, height = 600;

export default class DiffGraphVis extends Component {
    render() {
        return (<div>
            <svg id="main-canvas" width={width} height={height} />
        </div>);
    }

    componentDidUpdate() {
        if (this.props.genes) {
            drawGraph(this.props.genes);
        }
    }

}

function toLinks(genes) {
    const links = [];
    genes.forEach((gene) => {
        gene.known_interactions.forEach((interaction) => {
            const link = {
                source: gene.name,
                target: interaction.preferredName_A,
            };
            links.push(link);
        });
    });
    return links;
}

/** get a list of genes found in the pub, for now just all source nodes */
function getInPub(genes) {
    return new Set(genes.map((g) => g.name));
}

function drawGraph(genes) {
    const inPub = getInPub(genes);
    const links = toLinks(genes);
    const nodes = {};
    links.forEach((link) => {
        link.source = nodes[link.source] ||
            (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] ||
            (nodes[link.target] = {name: link.target});
    });
    const svg = d3.select("#main-canvas");
    var force = d3.forceSimulation()
        .nodes(d3.values(nodes))
        .force("link", d3.forceLink(links).distance(40))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-100))
        .alphaTarget(1)
        .on("tick", tick);
    const node = svg.selectAll(".node")
        .data(force.nodes())
      .enter().append("g");
    const path = svg.append("g")
      .selectAll("path")
      .data(links)
      .enter()
      .append("path")
      .attr("class", "link");
    node.append("circle")
      .attr("r", 15)
      .attr("fill", (d) => {
        if (inPub.has(d.name)) {
            return 'green';
        } else return 'red';
      });
     node.append("text").text((d) => d.name);
    function tick() {
        path.attr("d", (d) => {  
            const dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" +
                d.source.x + "," +
                d.source.y + "A" +
                dr + "," + dr + " 0 0,1 " +
                d.target.x + "," +
                d.target.y;
        });
        node.attr("transform", (d) => {
            return "translate(" + d.x + "," + d.y + ")"; })
    };
}

