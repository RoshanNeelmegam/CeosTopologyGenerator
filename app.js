document.addEventListener('DOMContentLoaded', () => {
    const addNodesButton = document.getElementById('addNodesButton');
    const addHostsButton = document.getElementById('addHostsButton');
    const topologyArea = document.getElementById('topologyArea');

    const nodeImageSrc = 'node.jpg'; // Replace with the path to your node image
    const hostImageSrc = 'host.jpg'; // Replace with the path to your host image

    addNodesButton.addEventListener('click', () => {
        const numberOfNodes = prompt('How many nodes do you want to add?');
        addElements(numberOfNodes, 'node', nodeImageSrc);
    });

    addHostsButton.addEventListener('click', () => {
        const numberOfHosts = prompt('How many hosts do you want to add?');
        addElements(numberOfHosts, 'host', hostImageSrc);
    });

    function addElements(count, type, imageSrc) {
        for (let i = 0; i < count; i++) {
            const element = document.createElement('img');
            element.src = imageSrc;
            element.classList.add(type);
            element.style.left = `${Math.random() * (topologyArea.clientWidth - 50)}px`;
            element.style.top = `${Math.random() * (topologyArea.clientHeight - 50)}px`;
            element.draggable = true;
            topologyArea.appendChild(element);

            element.addEventListener('dragstart', dragStart);
            element.addEventListener('dragend', dragEnd);
        }
    }

    function dragStart(event) {
        event.dataTransfer.setData('text/plain', event.target.id);
        setTimeout(() => {
            event.target.style.visibility = 'hidden';
        }, 0);
    }

    function dragEnd(event) {
        event.target.style.visibility = 'visible';
        const rect = topologyArea.getBoundingClientRect();
        event.target.style.left = `${event.clientX - rect.left - event.target.width / 2}px`;
        event.target.style.top = `${event.clientY - rect.top - event.target.height / 2}px`;
    }

    topologyArea.addEventListener('dragover', (event) => {
        event.preventDefault();
    });
    
});