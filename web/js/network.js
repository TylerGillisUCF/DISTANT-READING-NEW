// Network Visualization using D3.js
function createNetwork(networkData) {
    const container = document.getElementById('network');
    const width = container.clientWidth;
    const height = 600;

    // Clear any existing SVG
    container.innerHTML = '';

    // Create SVG
    const svg = d3.select('#network')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // Define colors for authors
    const colorScale = d3.scaleOrdinal()
        .domain(['Plato', 'Aristotle'])
        .range(['#3498db', '#e74c3c']);

    // Create force simulation
    const simulation = d3.forceSimulation(networkData.nodes)
        .force('link', d3.forceLink(networkData.links)
            .id(d => d.id)
            .distance(d => 150 - (d.weight * 100))) // Closer for higher similarity
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(50));

    // Create links
    const link = svg.append('g')
        .selectAll('line')
        .data(networkData.links)
        .join('line')
        .attr('stroke', '#95a5a6')
        .attr('stroke-opacity', d => d.weight * 2) // Opacity based on similarity
        .attr('stroke-width', d => Math.max(1, d.weight * 10));

    // Create nodes
    const node = svg.append('g')
        .selectAll('circle')
        .data(networkData.nodes)
        .join('circle')
        .attr('r', 25)
        .attr('fill', d => colorScale(d.author))
        .attr('stroke', '#fff')
        .attr('stroke-width', 3)
        .call(drag(simulation));

    // Add labels
    const labels = svg.append('g')
        .selectAll('text')
        .data(networkData.nodes)
        .join('text')
        .text(d => d.label.replace('Plato ', 'P:').replace('Aristotle ', 'A:'))
        .attr('font-size', 12)
        .attr('font-weight', 'bold')
        .attr('text-anchor', 'middle')
        .attr('dy', 40)
        .attr('fill', '#2c3e50');

    // Add tooltips on hover
    node.append('title')
        .text(d => d.label);

    // Update positions on each tick
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);

        labels
            .attr('x', d => d.x)
            .attr('y', d => d.y);
    });

    // Drag functionality
    function drag(simulation) {
        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        return d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended);
    }

    // Add legend
    const legend = svg.append('g')
        .attr('transform', `translate(${width - 150}, 20)`);

    legend.append('circle')
        .attr('cx', 0)
        .attr('cy', 0)
        .attr('r', 10)
        .attr('fill', colorScale('Plato'));

    legend.append('text')
        .attr('x', 20)
        .attr('y', 5)
        .text('Plato')
        .attr('font-size', 14);

    legend.append('circle')
        .attr('cx', 0)
        .attr('cy', 30)
        .attr('r', 10)
        .attr('fill', colorScale('Aristotle'));

    legend.append('text')
        .attr('x', 20)
        .attr('y', 35)
        .text('Aristotle')
        .attr('font-size', 14);
}
