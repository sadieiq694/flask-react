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
  //console.log("CONSOLE LOG APP: ", data)
  var newData = data.replace(/&#34;/g, '"')
  //console.log("CONSOLE LOG APP: ", newData, typeof(newData))
  data = JSON.parse(newData);

  var nodes = data.graph.nodes
  var edges = data.graph.edges; 

  /*
  var cpu = data.cpu;
  console.log("CPU: ", cpu);
  var events = data.event;
  console.log("events: ", events);

  var error = data.error;
  var latency = data.latency;
  var memory = data.memory; 
  var ops = data.ops;*/

  var cpu = require('./smallData/cpu_small.json')
  var ops = require('./smallData/ops_small.json')
  var latency = require('./smallData/latency_small.json')
  var events = require('./smallData/events_small.json')
  var error = require('./smallData/err_small.json')
  var memory = require('./smallData/memory_small.json')
  // these are all lists of objects

  const barData = [
    [10, 30, 40, 20],
    [10, 40, 30, 20, 50, 10],
    [60, 30, 40, 20, 30]
  ]



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
