let connHolder = {};
let connections = [];

document.addEventListener('DOMContentLoaded', () => {
    const addNodesButton = document.getElementById('addNodesButton');
    const addHostsButton = document.getElementById('addHostsButton');
    const topologyArea = document.getElementById('topologyArea');
    const linkModeButton = document.getElementById('linkModeButton');
        const submitButton = document.getElementById('submitTopologyButton');
    const nodeImageSrc = 'node.jpg'; // Replace with the path to your node image
    const hostImageSrc = 'host.jpg'; // Replace with the path to your host image

    // Declaring a few global trackers
    let isLinkMode = false;
    let selectedElement = null;
    let currentLine = null;
 // To store the connections

    addNodesButton.addEventListener('click', () => {
        const numberOfNodes = prompt('How many nodes do you want to add?');
        addElements(numberOfNodes, 'node', nodeImageSrc);
    });

    addHostsButton.addEventListener('click', () => {
        const numberOfHosts = prompt('How many hosts do you want to add?');
        addElements(numberOfHosts, 'host', hostImageSrc);
    });

    linkModeButton.addEventListener('click', () => {
        isLinkMode = !isLinkMode;
        toggleLinkMode(isLinkMode);
    });

    function addElements(count, type, imageSrc) {
        for (let i = 0; i < count; i++) {
            // creating the elements 
            const mainFig = document.createElement('figure');
            const element = document.createElement('img');
            const caption = document.createElement('figcaption');
            // adding the classes to the elements
            mainFig.classList.add('element-container');
            caption.classList.add('element-caption');
            element.classList.add(type);
            element.src = imageSrc;
            // appending the elements to the mainFig figure
            mainFig.append(element);
            mainFig.append(caption);
            mainFig.style.left = `${Math.random() * (topologyArea.clientWidth - 50)}px`;
            mainFig.style.top = `${Math.random() * (topologyArea.clientHeight - 50)}px`;
            mainFig.draggable = true;
            topologyArea.appendChild(mainFig);
            element.id = `${type}${i+ 1}`;
            caption.innerHTML = element.id;
            // adding the event listeners that help to move the figure
            mainFig.addEventListener('dragstart', dragStart);
            mainFig.addEventListener('dragend', dragEnd);
            mainFig.addEventListener('dblclick', changeName);
        }
    }

    function dragStart(event) {
        // need to set data for specific browsers
        event.dataTransfer.setData('text/plain', event.target.id);
        setTimeout(() => {
            event.target.style.visibility = 'hidden';
        }, 0);
    }

    function dragEnd(event) {
        event.target.style.visibility = 'visible';
        const rect = topologyArea.getBoundingClientRect();
        const mainFig = event.target;
        mainFig.style.left = `${event.clientX - rect.left - mainFig.clientWidth / 2}px`;
        mainFig.style.top = `${event.clientY - rect.top - mainFig.clientHeight / 2}px`;
    }
    
    function changeName(event) {
        const name = prompt("Node/Host name?");
        const elementContainer = event.currentTarget; // Get the container element
        const caption = elementContainer.querySelector('.element-caption'); // Find the caption inside the container
        if (caption) {
            caption.innerHTML = name.toLowerCase().replace(/\s+/g, '-');
        }
        // Update the element ID (assuming the ID is set on the container element)
        const element = elementContainer.querySelector('img'); 
        const newId = name.toLowerCase().replace(/\s+/g, '-'); // Generate new ID based on the name
        element.id = newId;
        }

    function toggleLinkMode(enable) {
        const elements = document.getElementsByClassName('node');
        const hostElements = document.getElementsByClassName('host');
        for (let element of elements) {
            element.draggable = !enable;
        }
        for (let element of hostElements) {
            element.draggable = !enable;
        }
        if (enable) {
            Array.from(elements).forEach(element => {
                element.removeEventListener('dragstart', dragStart);
                element.removeEventListener('dragend', dragEnd);
                element.addEventListener('click', startLinking);
            });
            Array.from(hostElements).forEach(element => {
                element.removeEventListener('dragstart', dragStart);
                element.removeEventListener('dragend', dragEnd);
                element.addEventListener('click', startLinking);
            });
        } else {
            Array.from(elements).forEach(element => {
                element.addEventListener('dragstart', dragStart);
                element.addEventListener('dragend', dragEnd);
                element.removeEventListener('click', startLinking);
            });
            Array.from(hostElements).forEach(element => {
                element.addEventListener('dragstart', dragStart);
                element.addEventListener('dragend', dragEnd);
                element.removeEventListener('click', startLinking);
            });
        }
    }
    
    function startLinking(event) {
        if (isLinkMode && !currentLine) {
            const rect = topologyArea.getBoundingClientRect();
            const x1 = event.clientX - rect.left;
            const y1 = event.clientY - rect.top;
    
            currentLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            currentLine.setAttribute('x1', x1);
            currentLine.setAttribute('y1', y1);
            currentLine.setAttribute('x2', x1);
            currentLine.setAttribute('y2', y1);
            svgArea.appendChild(currentLine);
    
            document.addEventListener('mousemove', drawLine);
            document.addEventListener('mouseup', endLinking);
            selectedElement = event.target;
        }
    }
    
    function drawLine(event) {
        if (!currentLine) return;
    
        const rect = topologyArea.getBoundingClientRect();
        const x2 = event.clientX - rect.left;
        const y2 = event.clientY - rect.top;
    
        currentLine.setAttribute('x2', x2);
        currentLine.setAttribute('y2', y2);
    }
    
    function endLinking(event) {
        document.removeEventListener('mousemove', drawLine);
        document.removeEventListener('mouseup', endLinking);
        if (event.target !== selectedElement && (event.target.classList.contains('node') || event.target.classList.contains('host'))) {
            const from = selectedElement;
            const to = event.target;
            // checks if node is in dictionary or not and accordingly records the state
            if (!(from.id in connHolder)){
                connHolder[from.id] = [1];
                fromPort = connHolder[from.id].slice(-1)[0];
            }
            else{
                fromPort = connHolder[from.id].slice(-1)[0] + 1 ;
                connHolder[from.id].push(fromPort);
            }

            if (!(to.id in connHolder)){
                connHolder[to.id] = [1];
                toPort = connHolder[to.id].slice(-1)[0];
            }
            else{
                toPort = connHolder[to.id].slice(-1)[0] + 1;
                connHolder[to.id].push(toPort);
            }
    
            const fromId = from.getAttribute('id') || `node${Date.now()}`;
            const toId = to.getAttribute('id') || `node${Date.now() + 1}`;
            from.setAttribute('id', fromId);
            to.setAttribute('id', toId);
    
            const connection = [`\"${fromId}:eth${fromPort}\"`, `\"${toId}:eth${toPort}\"`];
            connections.push(connection);
    
            // Display the connection in the console
            console.log(connections);
            console.log(connHolder);
            selectedElement = null;
        } else {
            // If the line is not connected to another element, remove it
            svgArea.removeChild(currentLine);
            selectedElement = null;
        }
    
        currentLine = null;
    }

    topologyArea.addEventListener('dragover', (event) => {
        event.preventDefault();
    });


    
});

document.addEventListener('DOMContentLoaded', () => {
    const submitButton = document.getElementById('submitTopologyButton');
    const yamlOutput = document.getElementById('yamlOutput');

    submitButton.addEventListener('click', () => {
        const nodes = document.getElementsByClassName('element-container');
        const links = document.getElementsByClassName('link-line');
        let ip = 10;
        let yamlContent = "topology:\n";
        yamlContent += "  kinds:\n";
        yamlContent += "    ceos:\n";
        yamlContent += "      image: ceosimage:4.27.3F\n";
        yamlContent += "    linux:\n";
        yamlContent += "      image: alpine-host\n";
        yamlContent += "  nodes:\n";

        // Collecting nodes information
        Object.entries(connHolder).forEach(([key, value]) => {
            const nodeId = key;
            const element = document.getElementById(nodeId); // Fetch the DOM element by its ID
            const nodeType = element.classList.contains('node') ? 'ceos' : 'linux';
        

            yamlContent += `    ${nodeId}:\n`;
            yamlContent += `      kind: ${nodeType}\n`;
            yamlContent += `      mgmt-ipv4: 172.100.100.${ip}\n`;
            ip += 1;
        });


        yamlContent += "  links:\n";

        // Assuming connections is an array of objects with endpoints property
        connections.forEach(link => {
            const endpoints = link; // Assuming link has endpoints property

            yamlContent += `    - endpoints: [${endpoints}]\n`;
        });

        // Append mgmt section to YAML content
        yamlContent += "\nmgmt:\n";
        yamlContent += "  network: mplsevpnirb\n";
        yamlContent += "  ipv4-subnet: 172.100.100.0/24\n";
        yamlContent += "  ipv6-subnet: 2001:172:100:100::/80\n";

        // Displaying YAML content in textarea
        yamlOutput.value = yamlContent;
    });

    // Other JavaScript functions and event listeners
});