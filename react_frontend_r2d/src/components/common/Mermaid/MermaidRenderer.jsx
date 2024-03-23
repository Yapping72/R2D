import React from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
    startOnLoad: false, 
    theme: 'forest',
    securityLevel: 'loose',
    fontFamily: 'monospace',
    useMaxWidth:true,
    themeVariables: {
        fontSize: '20px', 
      }
  });

  export default class MermaidRenderer extends React.Component {
    componentDidMount() {
        this.updateDiagram();
    }
    
    componentDidUpdate() {
        this.updateDiagram();
    }
    
    updateDiagram() {
        const { chart } = this.props;
        
        // Clear the current content
        if (this.divRef.current) {
            this.divRef.current.innerHTML = '';
        }
        
        // Generate a unique ID for the diagram
        const diagramId = `diagram-${Math.random().toString(36).slice(2, 9)}`;
        
        // Create a new element with the diagram code
        const diagramElement = document.createElement('div');
        diagramElement.classList.add('mermaid');
        diagramElement.id = diagramId;
        // Directly assign the chart data to the div
        diagramElement.textContent = chart;
        
        // Append the diagram element to the container
        if (this.divRef.current) {
            this.divRef.current.appendChild(diagramElement);
        }
        
        // Initialize Mermaid for the new diagram
        mermaid.init(undefined, diagramElement);
    }
    
    divRef = React.createRef();
    
    render() {
        // Apply full width and height to the div that Mermaid will use
        return <div ref={this.divRef} style={{width: '100%', height: '100%', overflow:'hidden' }}></div>;
    }
}
