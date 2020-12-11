import React, {useState, useEffect} from 'react';
//import { ForceGraph } from "./components/ForceGraph.js";
import CheckboxPractice from "./components/CheckboxPractice.js"



class App extends React.Component {
  state = {
    graphData: {"nodes":[], "edges":[]}
  };

  // add button to re-update data from database
  async componentDidMount() {
    const response = await fetch('/data/graph');
    const data = await response.json(); 
    this.setState({graphData: data});
    console.log("graph data: ", this.state.graphData)
  }

  render() {
    console.log(this.state.graphData.nodes)
    return (
      <div className="App">
        <header className="App-header">
        <CheckboxPractice nodeData={this.state.graphData.nodes} linksData={this.state.graphData.edges}/>
        </header>
      </div>
    );

  }
  
}

//                 <CheckboxPractice nodeData={this.graphData.nodes} linksData={this.graphData.edges}/>
// <CheckboxPractice nodeData={nodes} linksData={edges}/>

// <Example />         <DisplayNodeNames nodeData={nodes}/>



/*
  <CPUGraph data={cpu} />
  <MemGraph data={memory} />
  <ErrorGraph data={error} />
  <LatencyGraph data={latency} />
  <OpsGraph data={ops} />
  <EventGraph data={events} />
*/

//         <p>My token: {window.token}</p>
//         <ForceGraph linksData={edges} nodesData={nodes}/>
//         <EventGraph data={eventData} />
//         <D3Bar width={500} height={500} data={barData}/>



export default App;
