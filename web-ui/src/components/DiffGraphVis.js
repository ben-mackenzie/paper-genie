import React, { Component, Fragment } from 'react';
import * as d3 from "d3v4";
import * as webcola from "webcola";
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
            drawGraph(this.props.genes, this.props.classified, this.props.interacting);
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

function getClassificationUnique(interacting) {
    const links =[];
    interacting.forEach((entry) => {
        entry.interaction_details.forEach((interaction) => {
            if(interaction.interacts) {
                
                const link = {
                    source: interaction.combo[0],
                    target: interaction.combo[1],
                    classUnique: true,
                };
                links.push(link);
            }
        })
    });
    return links;
}

function drawGraph(genes, classified, interacting) {
    const found = processClassified(classified);
    const inPub = getInPub(genes);
    const allgenes = getAll(genes);
    const score = getScore(allgenes, inPub);
    const classUniqueLinks = getClassificationUnique(interacting);
    const paperLinks = toLinks(genes, found);
    const links = paperLinks.concat(classUniqueLinks);
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

    var cola = webcola.d3adaptor(d3)
      .avoidOverlaps(true)
      .size([width, height]);

    cola.nodes(d3.values(nodes))
        .links(links)
        //.symmetricDiffLinkLengths(10)
        .jaccardLinkLengths(75,0.7)
        .start(30);

    var link = svg.selectAll("link")
        .data(links)
      .enter().append("line")
        .attr("class", "link")
        .style("stroke", (d) => {
          if (d.classUnique) {
              return "#FF0099";
          }
          if (d.overlap) {
            return "#3F52B5";
          } else return '#4a154b'; })
        .style("stroke-opacity", .75)
        .style("stroke-width", (d) => {
            if (d.overlap || d.classUnique) { return "6px";
          } else return "2px" });

    var node = svg.selectAll("node")
                  .data(d3.values(nodes))
                  .enter().append("g");

    var circle = node.append("circle")
        .attr("class", "node")
        .attr("r", (d) => {
          if (inPub.has(d.name)) {
              return 28;
          } else return 20;
        })
        .style("fill", (d) => {
          if (inPub.has(d.name)) {
              return '#3F52B5';
          } else return '#4a154b';
        })
        .style("stroke", "#fff")
        .style("stroke-width", (d) => {
          if (inPub.has(d.name)) {
              return "3px";
          } else return "2px";
        })
        .call(cola.drag);

    var label = node.append("svg:text")
        .text(function (d) { return d.name; })
        .style("paint-order", "stroke")
        .style("text-anchor", "middle")
        .style("fill", "white")
        .style("font-family", "helvetica neue")
        .style("font-weight", "bold")
        .style("stroke", (d) => {
          if (inPub.has(d.name)) {
              return '#3F52B5';
          } else return '#4a154b';
        })
        .style("stroke-width", (d) => {
          if (inPub.has(d.name)) {
              return "8px";
          } else return "6px";
        })
        .style("font-size", (d) => {
          if (inPub.has(d.name)) {
              return 19;
          } else return 13;
        })
        .style("stroke-linejoin", "round")
        .style("stroke-linecap", "round");

    cola.on("tick", function () {
        link.attr("x1", function (d) { return d.source.x; })
            .attr("y1", function (d) { return d.source.y; })
            .attr("x2", function (d) { return d.target.x; })
            .attr("y2", function (d) { return d.target.y; });

        node.attr("cx", function (d) { return d.x; })
            .attr("cy", function (d) { return d.y; });

            circle.attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            });

        label.attr("x", function (d) {
                return d.x;
        })
            .attr("y", function (d) {
                return d.y + 5; });
    });

}
