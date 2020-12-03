import {createClassFromLiteSpec} from 'react-vega-lite';


export default createClassFromLiteSpec('OpsGraph', {
    "description": "A simple line chart with embedded data.",
    "mark": {
        "type": "line"
    },
    "encoding": {
      "x": {"field": "time", "type": "temporal"},
      "y": {"field": "ops", "type": "quantitative"},
      "color": {"field": "resource_id", "type":"nominal"}
    }
  });
