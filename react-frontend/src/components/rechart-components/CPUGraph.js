import React, {Component} from 'react'
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Legend} from 'recharts';
//import { renderModule } from 'vega';

class ReChartLine extends Component {

  constructor(props) {
    super(props);
    /*this.state = {
      options: []
    };
    
    this.onChange = this.onChange.bind(this)
    */
    //this.handleInputChange = this.handleInputChange.bind(this);
  };

  render() {  
      return(
      <LineChart width={600} height={300} data={this.props.data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" interval="preserveEnd" />
          <YAxis dataKey="cpu" />
          <Legend />
          <Line type="monotone" dataKey="cpu" stroke="#8884d8" activeDot={{ r: 8 }} />
      </LineChart>
      );
  }
}

//  <Line type="monotone" dataKey="uv" stroke="#82ca9d" />


export default ReChartLine;

  /*


/*
const selectlegend = vl.selectMulti().fields("resource_id").bind("legend")
  console.log(xmin,xmax)
  return vl.markLine({size:4},{interpolate:"linear"})
    .width(700)
    .data(filtered_cpu_data)
    .select(selectlegend)
    .encode(
      vl.y().fieldQ("cpu"),
      vl.x().fieldT("time").scale({domain:[xmin, xmax]}),
      vl.color().value("white").if(selectlegend,vl.color().fieldN("resource_id")),
      vl.opacity().value(".5").if(selectlegend,vl.opacity().value("1")),
     vl.tooltip(['resource_id','time','cpu']) 

      )*/