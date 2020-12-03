import {createClassFromLiteSpec} from 'react-vega-lite';


export default createClassFromLiteSpec('ErrorGraph', {
    "description": "A simple line chart with embedded data.",
    "mark": {
        "type": "line"
    },
    "encoding": {
      "x": {"field": "time", "type": "temporal"},
      "y": {"field": "success", "type": "quantitative"},
      "color": {"field": "resource_id", "type":"nominal"}
    }
  });