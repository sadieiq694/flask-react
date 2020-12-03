import {createClassFromLiteSpec} from 'react-vega-lite';


export default createClassFromLiteSpec('EventGraph', {
    "description": "A simple line chart with embedded data.",
    "mark": {
        "type": "circle"
    },
    "encoding": {
      "x": {"field": "time", "type": "temporal"},
      "y": {"field": "reason", "type": "ordinal"},
      "size": {"field":"importance"},
      "color": {"field": "object-type", "type":"nominal"}
    }
  });