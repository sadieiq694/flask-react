import React, { PureComponent } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Brush,
  AreaChart, Area, Label,
  ScatterChart, Scatter, Cell
} from 'recharts';
import SingleLineChart from './SingleLineChart.js';

const unique = (value, index, self) => {
	return self.indexOf(value) == index
}

var cpu = require('../../data/cpu.json')
var ops = require('../../data/ops.json')
var latency = require('../../data/latency.json')
var error = require('../../data/err.json')
var memory = require('../../data/memory.json')

var mem_resources = memory.map(a => a.resource_id)
var u_mem_resource = mem_resources.filter(unique)
console.log(u_mem_resource)

var mem_data_1  = memory.filter( item => {
	return item["resource_id"] == "details-v1-6c9f8bcbcb-crqvr/details"
  });

for(var i in mem_data_1) {
	mem_data_1[i].memory = parseInt(mem_data_1[i].memory)
}

var mem_data_2  = memory.filter( item => {
	return item["resource_id"] == "productpage-v1-7df7cb7f86-5pdhd/productpage"
  });

for(var i in mem_data_2) {
	mem_data_2[i].memory = parseInt(mem_data_2[i].memory)
}

console.log(mem_data_1);

const data = [
	{name: 'Page A', uv: 4000,  amt: 2400},
	{name: 'Page B', uv: 3000, amt: 2210},
	{name: 'Page C', uv: 2000, amt: 2290},
	{name: 'Page D', uv: 2780,  amt: 2000},
	{name: 'Page E', uv: 1890,  amt: 2181},
];
const data2 = [
	{name: 'Page A',  pv: 2400, amt: 2400},
	{name: 'Page B', pv: 1398, amt: 2210},
	{name: 'Page C',  pv: 9800, amt: 2290},
	{name: 'Page D', pv: 3908, amt: 2000},
];

class Example extends PureComponent {
  static jsfiddleUrl = 'https://jsfiddle.net/alidingling/nskpgcrz/';

  render() {
    return (
      <div>
        <h4>Metric Plots</h4>
		<SingleLineChart  
			data={ops} 
			width={500} 
			height={200}
            syncID="anyID"
            xDataKey="time"
            yDataKey="ops"
            xLabel="time"
            yLabel="Ops/s"
            brush={true}/>
		<SingleLineChart  
			data={cpu} 
			width={500} 
			height={200}
            syncID="anyID"
            xDataKey="time"
            yDataKey="cpu"
            xLabel="time"
            yLabel="cpu"
            brush={false}/>
		<SingleLineChart  
			data={latency} 
			width={500} 
			height={200}
            syncID="anyID"
            xDataKey="time"
            yDataKey="lat"
            xLabel="time"
            yLabel="latency"
            brush={false}/>
		<SingleLineChart  
			data={error} 
			width={500} 
			height={200}
            syncID="anyID"
            xDataKey="time"
            yDataKey="success"
            xLabel="time"
            yLabel="Success rate"
            brush={false}/>
		
		<LineChart
          width={600}
          height={300}
          //data={memory}
          syncId="anyId"
          margin={{
            top: 10, right: 30, left: 20, bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time">
			  <Label value="time" position="bottom"/>
		  </XAxis>
          <YAxis/>
          <Tooltip />
		  <Legend />
		  <Line data={mem_data_1} type="monotone" dataKey="memory" stroke="#8884d8" activeDot={{r: 8}}/>
      	  <Line data = {mem_data_2} type="monotone" dataKey="memory" stroke="#82ca9d" />
        </LineChart>
      </div>
    );
  }
}

export default Example

/*
<LineChart
          width={500}
          height={200}
          data={ops}
          syncId="anyId"
          margin={{
            top: 10, right: 30, left: 20, bottom: 20,
          }}
        >
		  <Brush />
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time">
			  <Label value="time" position="bottom"/>
		  </XAxis>
          <YAxis dataKey="ops" label={{ value: 'Ops/s', angle: -90, position: 'insideLeft' }}/>
          <Tooltip />
          <Line type="monotone" dataKey="ops" stroke="#8884d8" fill="#8884d8" />
		</LineChart>
		<LineChart
          width={500}
          height={200}
          data={cpu}
          syncId="anyId"
          margin={{
            top: 10, right: 30, left: 20, bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time">
			  <Label value="time" position="bottom"/>
		  </XAxis>
          <YAxis dataKey="cpu" label={{ value: 'cpu', angle: -90, position: 'insideLeft' }}/>
          <Tooltip />
          <Line type="monotone" dataKey="cpu" stroke="#82ca9d" fill="#82ca9d" />
        </LineChart>
        <AreaChart
          width={500}
          height={200}
          data={latency}
          syncId="anyId"
          margin={{
            top: 10, right: 30, left: 20, bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time">
			  <Label value="time" position="bottom"/>
		  </XAxis>
          <YAxis dataKey="lat" label={{ value: 'Latency in various quantiles', angle: -90, position: 'insideLeft' }}/>
          <Tooltip />
          <Area type="monotone" dataKey="lat" stroke="#82ca9d" fill="#82ca9d" />
		</AreaChart>
		
		<LineChart
          width={500}
          height={200}
          data={error}
          syncId="anyId"
          margin={{
            top: 10, right: 30, left: 20, bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time">
			  <Label value="time" position="bottom"/>
		  </XAxis>
          <YAxis dataKey="success" label={{ value: 'Success rate', angle: -90, position: 'insideLeft' }}/>
          <Tooltip />
          <Line type="monotone" dataKey="success" stroke="#8884d8" fill="#8884d8" />
        </LineChart>
		<LineChart
          width={500}
          height={200}
          data={memory}
          syncId="anyId"
          margin={{
            top: 10, right: 30, left: 20, bottom: 20,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time">
			  <Label value="time" position="bottom"/>
		  </XAxis>
          <YAxis dataKey="memory" label={{ value: 'memory', angle: -90, position: 'insideLeft' }}/>
          <Tooltip />
          <Line type="monotone" dataKey="memory" stroke="#8884d8" fill="#8884d8" />
		</LineChart>
		

		<SingleLineChart  
			data={memory} 
			width={500} 
			height={200}
            syncID="anyID"
            xDataKey="time"
            yDataKey="memory"
            xLabel="time"
            yLabel="memory"
            brush={false}/>
		*/