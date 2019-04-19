import React, { Component, Fragment } from 'react';
import * as d3 from "d3";

import * as jaccard from "jaccard";

const width = 1200, height = 600;

export default class DiffGraphVis extends Component {
    render() {
        return (<div>
            <svg id="main-canvas" width={width} height={height} />
        </div>);
    }

    componentDidUpdate() {
        if (this.props.genes) {
            clearGraph();
            drawGraph(this.props.genes, this.props.classified);
        }
    }

}

function processClassified(classified) {
    const found = {};
    classified.forEach( (classifiedInteraction) => {
        if(!found[classifiedInteraction.gene1]) {
            found[classifiedInteraction.gene1] = new Set();
        }
        if(!found[classifiedInteraction.gene2]) {
            found[classifiedInteraction.gene2] = new Set();
        }
        found[classifiedInteraction.gene1].add(classifiedInteraction.gene2);
        found[classifiedInteraction.gene2].add(classifiedInteraction.gene1);
    });
    return found;
}

function toLinks(genes, found) {
    const links = [];
    genes.forEach((gene) => {
        gene.known_interactions.forEach((interaction) => {
            const commonName = interaction.preferredName_A;
            const detectedInteractions = found[interaction.preferredName_A];
            const overlap = detectedInteractions && detectedInteractions.has(commonName);
            const link = {
                source: gene.name,
                target: commonName,
                overlap
            };
            links.push(link);
        });
    });
    return links;
}

function getScore(allgenes, inPub) {
    let score = jaccard.index( Array.from(allgenes), Array.from(inPub));
    score = Math.round(score * 100) / 100
    return score;
}

/** get a list of genes found in the pub, for now just all source nodes */
function getInPub(genes) {
    return new Set(genes.map((g) => g.name));
}

function getAll(genes) {
    const allInter = new Set();
    genes.forEach(  (gene) => {
        gene.known_interactions.forEach((interaction) => {
            const commonName = interaction.preferredName_A;
            allInter.add(commonName);
        });
    });
    return allInter;
}

function clearGraph() {
    var svg = d3.select("#main-canvas");
    svg.selectAll("*").remove();
}

function drawGraph(genes, classified) {
    const found = processClassified(classified);
    const inPub = getInPub(genes);
    const allgenes = getAll(genes);
    const score = getScore(allgenes, inPub);
    const links = toLinks(genes, found);
    const nodes = {};
    links.forEach((link) => {
        link.source = nodes[link.source] ||
            (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] ||
            (nodes[link.target] = {name: link.target});
    });
    const svg = d3.select("#main-canvas");
    svg.append("text")
        .text(`Jaccard score:  ${score}`)
        .attr("x", width/2)
        .attr('y', 20)
        .attr('font-size', 24);
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
      .attr("class", "link")
      .style("stroke",(d) => {
          if (d.overlap) return "green";
        })
        .style("stroke-width",(d) => {
            if (d.overlap) return "6.5px";
          })
        ;
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

