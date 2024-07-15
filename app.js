// Declaring data structures that hold the state
let connHolder = {}; // holds the state in the following format. { 'node1': [ 1, 2, 3], 'host1': [1, 2, 3] }
let connections = []; // holds the connection in the following format. [ ["leaf1:eth1","leaf2:eth1"], ["leaf1:eth3","leaf2:eth1"] ]

document.addEventListener('DOMContentLoaded', () => {
    const addNodesButton = document.getElementById('addNodesButton');
    const addHostsButton = document.getElementById('addHostsButton');
    const topologyArea = document.getElementById('topologyArea');
    const linkModeButton = document.getElementById('linkModeButton');
    const nodeImageSrc = 'node.jpg'; // Replace with the path to your node image
    const hostImageSrc = 'host.jpg'; // Replace with the path to your host image
    // Declaring a few global trackers
    let isLinkMode = false;
    let selectedElement = null;
    let currentLine = null;

    addNodesButton.addEventListener('click', () => {
        const numberOfNodes = prompt('How many nodes do you want to add?');
        addElements(numberOfNodes, 'node', nodeImageSrc);
    });

    addHostsButton.addEventListener('click', () => {
        const numberOfHosts = prompt('How many hosts do you want to add?');
        addElements(numberOfHosts, 'host', hostImageSrc);
    });

    linkModeButton.addEventListener('click', () => {
        isLinkMode = !isLinkMode; // this state is now passed to toggleLinkMode function that acts according to the state
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
        const elements = document.getElementsByClassName('element-container'); // returns an array of node/hosts
        for (let element of elements) { // using for/of to iterate through each element in the list. for/in will just interate through the list index
            element.draggable = !enable;
        }
        if (enable) {
            linkModeButton.style.backgroundColor = 'hotpink';
            // Using Array.from() to create a copy of elements array and run a function on each element of the array
            Array.from(elements).forEach(element => {
                element.removeEventListener('dragstart', dragStart);
                element.removeEventListener('dragend', dragEnd);
                element.addEventListener('click', startLinking);
            });
        } else {
            linkModeButton.style.backgroundColor = "#4CAF50";
            Array.from(elements).forEach(element => {
                element.addEventListener('dragstart', dragStart);
                element.addEventListener('dragend', dragEnd);
                element.removeEventListener('click', startLinking);
            });
        }
    }
    
    function startLinking(event) {
        if (isLinkMode && !currentLine) {
            const rect = topologyArea.getBoundingClientRect();
            // getting the x, y value of the mouse pointer 
            const x1 = event.clientX - rect.left; 
            const y1 = event.clientY - rect.top;
    
            currentLine = document.createElementNS('http://www.w3.org/2000/svg', 'line'); // creates an SVG element line
            currentLine.setAttribute('x1', x1); // setting the x1 value 
            currentLine.setAttribute('y1', y1); // setting the y1 value

            // hardcoding x2, y2 values to prevent abnormal behaviour
            currentLine.setAttribute('x2', x1); 
            currentLine.setAttribute('y2', y1);
            svgArea.appendChild(currentLine); // adding the element to the svg area

            document.addEventListener('mousemove', drawLine);
            document.addEventListener('mouseup', endLinking);
            selectedElement = event.target; // initial element
            const elements = document.getElementsByClassName('element-container');
            Array.from(elements).forEach(element => {
                element.removeEventListener('click', startLinking);
            });
        }
    }
    
    function drawLine(event) {
        // tracking the mouse event to drag the line as per the mouse pointer 
        if (!currentLine) return;

        const rect = topologyArea.getBoundingClientRect();    
        currentLine.setAttribute('x2', event.clientX - rect.left);
        currentLine.setAttribute('y2', event.clientY - rect.top);
    }
    
    function endLinking(event) {
        // removing the event listeners 
        document.removeEventListener('mousemove', drawLine);
        document.removeEventListener('mouseup', endLinking);
        
    
        // if the line is not on the initial element and if it's on another node or host and given that it's not on any other element
        if (event.target !== selectedElement && (event.target.classList.contains('node') || event.target.classList.contains('host'))) {
            const from = selectedElement; // initial element
            const to = event.target; // final element 
            // checks if node is in dictionary or not and accordingly records the state
            if (!(from.id in connHolder)){ 
                // if the node is not in the connHolder dictionary
                connHolder[from.id] = [1];
                fromPort = 1; 
            }
            else{
                // if the node is alredy there in the connHolder dictionary then just add the port to the list of ports of the node
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
        setTimeout(() => {
            const elements = document.getElementsByClassName('element-container');
            Array.from(elements).forEach(element => {
                element.addEventListener('click', startLinking);
            });
        }, 100); // Adjust the delay as needed
    }
  
    topologyArea.addEventListener('dragover', (event) => {
        event.preventDefault();
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const submitButton = document.getElementById('submitTopologyButton');
    const yamlOutput = document.getElementById('yamlOutput');

    // Declaring the nodeOS form
    const nodeOSSelect = document.getElementById('nodeOS');

    // Function to get the selected value when needed
    function getSelectedNodeOS() {
        const selectedValue = nodeOSSelect.value;
        return selectedValue;
    }

    // Declaring the hostOS form
    const hostOSSelect = document.getElementById('hostOS');

    // Function to get the selected value when needed
    function getSelectedHostOS() {
        const selectedValue = hostOSSelect.value;
        return selectedValue;

    }
    

    submitButton.addEventListener('click', () => {
        const nodes = document.getElementsByClassName('element-container');
        const links = document.getElementsByClassName('link-line');
        const selectedNodeOS = getSelectedNodeOS();
        const selectedHostOS = getSelectedHostOS();
        let ip = 10; // starting host ip address
        let yamlContent = "name: Lab" + Math.round(Math.random()*1000) + "\n";
        yamlContent += "topology:\n";
        yamlContent += "  kinds:\n";
        yamlContent += "    ceos:\n";
        yamlContent += "      image: " + selectedNodeOS + "\n";
        yamlContent += "    host:\n";
        yamlContent += "      image: " + selectedHostOS + "\n";
        yamlContent += "  nodes:\n";

        // Collecting nodes information
        Object.entries(connHolder).forEach(([key, value]) => {
            const nodeId = key;
            const element = document.getElementById(nodeId); // Fetch the DOM element by its ID
            const nodeType = element.classList.contains('node') ? 'ceos' : 'host';
        
            yamlContent += `    ${nodeId}:\n`;
            yamlContent += `      kind: ${nodeType}\n`;
            yamlContent += `      mgmt-ipv4: 172.200.10.${ip}\n`;
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
        yamlContent += "  network: LabNet" + Math.round(Math.random()*1000) + "\n";
        yamlContent += "  ipv4-subnet: 172.200.10.0/24\n";

        // Displaying YAML content in textarea
        yamlOutput.value = yamlContent;
    });

    // Other JavaScript functions and event listeners
});