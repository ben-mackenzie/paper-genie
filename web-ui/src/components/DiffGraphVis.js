import React, { Component, Fragment } from 'react';
import * as d3 from "d3v4";
import * as webcola from "webcola";
import * as jaccard from "jaccard";

const width = 1400, height = 900;

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

function removeFalseUnique(links) {
    const overlapping = {};
    const filtered = [];
    links.forEach( (link) => {
        const id = `${link.source} ${link.target}`;
        const inv_id = `${link.target} ${link.source}`;
        if (link.overlap === true && !overlapping[id]) {
            overlapping[id] = true;
            overlapping[inv_id] = true;
            filtered.push(link);
        }
    } )
    links.forEach( (link) => {
        const id = `${link.source} ${link.target}`;
        if (overlapping[id]) {

        } else {
            filtered.push(link);
        }
    })
    return filtered;
}

function drawGraph(genes, classified, interacting) {
    const found = processClassified(classified);
    const inPub = getInPub(genes);
    const allgenes = getAll(genes);
    const score = getScore(allgenes, inPub);
    const classUniqueLinks = getClassificationUnique(interacting);
    const paperLinks = toLinks(genes, found);
    const linksRedundant = paperLinks.concat(classUniqueLinks);
    const nodes = {};
    const links = removeFalseUnique(linksRedundant);
    links.forEach((link) => {
        link.source = nodes[link.source] ||
        (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] ||
        (nodes[link.target] = {name: link.target});
    });
    const svg = d3.select("#main-canvas");
    svg.append("text")
        .text(`Jaccard score:  ${score}`)
        .attr("x", 5)
        .attr('y', 50)
        .attr('font', 'helvetica')
        .attr('font-weight', 'bold')
        .attr('font-size', 18);

    svg.append("text")
        .text(`1: perfect match; 0: no match`)
        .attr("x", 5)
        .attr('y', 70)
        .attr('font', 'helvetica')
        .attr('font-weight', 'bold')
        .attr('font-size', 14);

    var nodesLegendData = [
        {"color": "#3F52B5", "text": "Paper and StringDB"},
        {"color": "#4a154b", "text": "StringDB only"}
    ]

    var nodesLegend = svg.selectAll('.nodelegend').data(nodesLegendData);
    var nodesLegend_g = nodesLegend.enter()
    .append('g')
    .attr('class', 'nodelegend')

    nodesLegend_g.append("circle")
        .attr("fill", d => d['color'])
        .attr("r", 10)
        .attr("cx", 10)
        .attr("cy", (d, i) => 98 + 30*i)

        nodesLegend_g.append("text")
        .text(d => d["text"])
        .attr("width", 30)
        .attr("height", 20)
        .attr("x", 35)
        .attr("y", (d, i) => 105 + 25*i)


    var edgesLegendData = [
        {"color": "#3F52B5", "text": "Paper and StringDB", "height": 4},
        {"color": "#D46A6A", "text": "Paper only", "height": 4},
        {"color": "#4a154b", "text": "StringDB only", "height": 2}
    ]

    var edgesLegend = svg.selectAll('.edgelegend').data(edgesLegendData);
    var edgesLegend_g = edgesLegend.enter()
    .append('g')
    .attr('class', 'edgelegend')

    edgesLegend_g.append("rect")
        .attr("fill", d => d['color'])
        .attr("width", 30)
        .attr("height", d => d['height'])
        .attr("x", 0)
        .attr("y", (d, i) => 150 + 25*i)

    edgesLegend_g.append("text")
        .text(d => d["text"])
        .attr("width", 30)
        .attr("height", 20)
        .attr("x", 35)
        .attr("y", (d, i) => 155 + 25*i)

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
          if (d.overlap) {
            return "3F52B5";//"#129E90";
          } else if (d.classUnique) {
            return "D46A6A";//"#AA3939";
          } else return '#4a154b'; })
        .style("stroke-opacity", 0.8)
        .style("stroke-width", (d) => {
            if (d.overlap || d.classUnique) { return "4px";
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
        .style("user-select", "none")
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
