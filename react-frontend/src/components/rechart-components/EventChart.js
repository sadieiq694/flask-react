import React, { PureComponent } from 'react';
import {
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Cell
} from 'recharts';
import { scaleOrdinal } from 'd3-scale';
import { schemeCategory10 } from 'd3-scale-chromatic';

const colors = scaleOrdinal(schemeCategory10).range();

const data = [
  { x: 100, y: 200, z: 200 },
  { x: 120, y: 100, z: 260 },
  { x: 170, y: 300, z: 400 },
  { x: 140, y: 250, z: 280 },
  { x: 150, y: 400, z: 500 },
  { x: 110, y: 280, z: 200 },
];

const CustomTooltip = ({ active, payload, label }) => {
    if (active) {
        if(payload !=null) {
            console.log(payload, label)
            return (
              <div className="custom-tooltip">
                <p className="mess">{`Message : ${payload[0].payload.message}`}</p>
                <p className="reason">{`reason : ${payload[0].payload.reason}`}</p>
                <p className="obj">{`object : ${payload[0].payload.object}`}</p>
              </div>
            );
        }
    }
  
    return null;
  };

export default class Example extends PureComponent {
  constructor(props) {
    super(props);
    /* Props:
        data
        width
        height
        syncID
        xDataKey
        yDataKey
        xLabel
        yLabel
        brush (true/false)
    */
  };

  //static jsfiddleUrl = 'https://jsfiddle.net/alidingling/9Lfxjjty/';

  render() {
    console.log("NUMBER OF EVENTS CHART SCRIPT: ", this.props.data)
    return (
      <ScatterChart
        width={this.props.width}
        height={this.props.height}
        margin={{
          top: 20, right: 20, bottom: 20, left: 20,
        }}
      >
        <CartesianGrid />
        <XAxis type="number" dataKey={this.props.xDataKey} name={this.props.xLabel} unit="s" domain={[this.props.xMin, this.props.xMax]} />
        <YAxis type="category" dataKey={this.props.yDataKey} name={this.props.yLabel} />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} content={<CustomTooltip />} />
        <Scatter name="Events" data={this.props.data} fill={colors}></Scatter>
      </ScatterChart>
    );
  }
}

//         syncId={this.props.syncID}

