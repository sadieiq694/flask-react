//import React, { PropTypes } from 'react';
import {createClassFromLiteSpec} from 'react-vega-lite';


export default createClassFromLiteSpec('MemGraph', {
    "description": "A simple line chart with embedded data.",
    "mark": {
        "type": "line"
    },
    "encoding": {
      "x": {"field": "time", "type": "temporal"},
      "y": {"field": "memory", "type": "quantitative"},
      "color": {"field": "resource_id", "type":"nominal"}
    }
  });