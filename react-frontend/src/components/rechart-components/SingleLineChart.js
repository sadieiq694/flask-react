import React, { PureComponent } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Brush,
  AreaChart, Area, Label,
} from 'recharts';

class SingleLineChart extends PureComponent {
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

    render() {
        let brush; 
        if(this.props.brush) {
            brush = <Brush />;
        } else {
            brush = <div></div>;
        }
        return (
        <LineChart
          width={this.props.width}
          height={this.props.height}
          data={this.props.data}
          syncId={this.props.syncID}
          margin={{
            top: 10, right: 30, left: 20, bottom: 20,
          }}
        >
		  {brush}
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={this.props.xDataKey}>
			  <Label value={this.props.xLabel} position="bottom"/>
		  </XAxis>
          <YAxis dataKey={this.props.yDataKey}>
              <Label value={this.props.yLabel} angle={-90} position='left'/>
          </YAxis> 
          <Tooltip />
          <Line type="monotone" dataKey={this.props.yDataKey} stroke="#8884d8" fill="#8884d8" />
        </LineChart>)
    }
}

export default SingleLineChart
