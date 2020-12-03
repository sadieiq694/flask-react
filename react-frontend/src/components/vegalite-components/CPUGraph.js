//import React, { PropTypes } from 'react';
import {createClassFromLiteSpec} from 'react-vega-lite';


export default createClassFromLiteSpec('CPUGraph', {
    "description": "A simple line chart with embedded data.",
    "mark": {
        "type": "line"
    },
    "encoding": {
      "x": {"field": "time", "type": "temporal"},
      "y": {"field": "cpu", "type": "quantitative"},
      "color": {"field": "resource_id", "type":"nominal"}
    }
  });

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