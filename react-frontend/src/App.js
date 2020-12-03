import React from 'react';
import DisplayNodeNames from './components/DisplayNodeNames.js'
//import { ForceGraph } from "./components/ForceGraph.js";
import CheckboxPractice from "./components/CheckboxPractice.js"
import EventGraph from "./components/rechart-components/EventGraph.js"
import CPUGraph from './components/rechart-components/CPUGraph.js';
import LatencyGraph from './components/rechart-components/LatencyGraph.js'
import ErrorGraph from './components/rechart-components/ErrorGraph.js'
import MemGraph from './components/rechart-components/MemGraph.js'
import OpsGraph from './components/rechart-components/OpsGraph.js'
import D3Bar from './components/D3-components/D3Bar.js'
import Example from './components/rechart-components/ReChartLine.js'


function App() {
  var data = window.graphData
  var newData = data.replace(/&#34;/g, '"')
  data = JSON.parse(newData);

  var nodes = data.nodes
  var edges = data.edges; 

  /*
  var cpu = data.cpu;
  console.log("CPU: ", cpu);
  var events = data.event;
  console.log("events: ", events);

  var error = data.error;
  var latency = data.latency;
  var memory = data.memory; 
  var ops = data.ops;*/


  return (
    <div className="App">
      <header className="App-header">
        <DisplayNodeNames nodeData={nodes}/>
        <CheckboxPractice nodeData={nodes} linksData={edges}/>
      </header>
    </div>
  );
}

//         <Example />


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
