import React, {useState, useEffect} from 'react';
//import { ForceGraph } from "./components/ForceGraph.js";
import CheckboxPractice from "./components/CheckboxPractice.js"



class App extends React.Component {
  state = {
    graphData: {"nodes":[], "edges":[]}
  };

  async componentDidMount() {
    const response = await fetch('/data/graph');
    const data = await response.json(); 
    this.setState({graphData: data});
    console.log("graph data: ", this.state.graphData)
  }
  
  /*useEffect( () => {
    fetch("/data/graph").then(response =>
      response.json().then(data => {
        console.log(data)
        console.log("setting graph data!")
        setGraphData(data)
    }))
  })*/


  //var data = window.graphData
  //var newData = data.replace(/&#34;/g, '"')
  //data = JSON.parse(newData);


  /*
  var cpu = data.cpu;
  console.log("CPU: ", cpu);
  var events = data.event;
  console.log("events: ", events);

  var error = data.error;
  var latency = data.latency;
  var memory = data.memory; 
  var ops = data.ops;*/

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
