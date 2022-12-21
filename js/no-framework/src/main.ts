import './index.css';
import * as vis from 'vis-network';
import edges from './data/edges_vis.json';

document.querySelector('#drawGraphVis')?.addEventListener('click', drawGraphVis);
const my_datavis = document.querySelector<HTMLElement>('#my_dataviz')!;

function setGroups() {
    edges.nodes = edges.nodes.map((node) => {
        let group = 'std';
        if (node.label[0] == '-') {
            group = 'ahfs';
        }
        return {id: node.id, label: node.label, group: group};
    });

    return edges;
}

function drawGraphVis() {
    console.log('graphvis');
    my_datavis?.classList.remove('hidden');
    const dataset = setGroups();
    // create a network
    const data = {
        nodes: dataset.nodes,
        edges: dataset.edges,
    };

    const options: vis.Options = {
        interaction: {
            dragNodes: false,
            hover: true,
            // zoomView: false,
        },
        groups: {
            ahfs: {color: 'red'},
        },
    };

    // create a network
    const network = new vis.Network(my_datavis, data, options);

    // setable dynamically
    // options.interaction.dragView = false;
    // network.setOptions(options);
}

// import * as d3 from 'd3';
// let hcg = false;
// document.querySelector('#drawGraph')?.addEventListener('click', drawGraph);
// function drawGraph() {
//     console.log('loading graph. hcg= ' + hcg);
//     // set the dimensions and margins of the graph
//     const margin = {top: 10, right: 30, bottom: 30, left: 40},
//         width = 400 - margin.left - margin.right,
//         height = 400 - margin.top - margin.bottom;

//     // append the svg object to the body of the page
//     my_datavis.innerHTML = '';
//     my_datavis.classList.remove('hidden');
//     const svg = d3
//         .select('#my_dataviz')
//         .append('svg')
//         .attr('width', width + margin.left + margin.right)
//         .attr('height', height + margin.top + margin.bottom)
//         .append('g')
//         .attr('transform', `translate(${margin.left}, ${margin.top})`);
//     let path = './src/data/data_network.json';
//     if (hcg) {
//         path = './src/data/edges.json';
//     }
//     hcg = !hcg;

//     d3.json(path).then(function (data) {
//         // Initialize the links
//         const link = svg.selectAll('line').data(data.links).join('line').style('stroke', '#aaa');

//         // Initialize the nodes
//         const node = svg.selectAll('circle').data(data.nodes).join('circle').attr('r', 20).style('fill', '#69b3a2');

//         // Let's list the force we wanna apply on the network
//         const simulation = d3
//             .forceSimulation(data.nodes) // Force algorithm is applied to data.nodes
//             .force(
//                 'link',
//                 d3
//                     .forceLink() // This force provides links between nodes
//                     .id(function (d) {
//                         return d.id;
//                     }) // This provide  the id of a node
//                     .links(data.links) // and this the list of links
//             )
//             .force('charge', d3.forceManyBody().strength(-400)) // This adds repulsion between nodes. Play with the -400 for the repulsion strength
//             .force('center', d3.forceCenter(width / 2, height / 2)) // This force attracts nodes to the center of the svg area
//             .on('end', ticked);

//         // This function is run at each iteration of the force algorithm, updating the nodes position.
//         function ticked() {
//             link.attr('x1', function (d) {
//                 return d.source.x;
//             })
//                 .attr('y1', function (d) {
//                     return d.source.y;
//                 })
//                 .attr('x2', function (d) {
//                     return d.target.x;
//                 })
//                 .attr('y2', function (d) {
//                     return d.target.y;
//                 });

//             node.attr('cx', function (d) {
//                 return d.x + 6;
//             }).attr('cy', function (d) {
//                 return d.y - 6;
//             });
//         }
//     });
// }
