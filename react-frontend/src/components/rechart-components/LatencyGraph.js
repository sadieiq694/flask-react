import {createClassFromLiteSpec} from 'react-vega-lite';


export default createClassFromLiteSpec('LatencyGraph', {
    "description": "A simple line chart with embedded data.",
    "mark": {
        "type": "line"
    },
    "encoding": {
      "x": {"field": "time", "type": "temporal"},
      "y": {"field": "lat", "type": "quantitative"},
      "color": {"field": "quantile", "type":"nominal"}
    }
  });
