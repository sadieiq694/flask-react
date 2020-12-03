import React from 'react'
//import { ForceGraph } from "./ForceGraph.js";
import ForceGraphClass from "./ForceGraphClass.js"


class CheckboxPractice extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        options: []
      };
      
      this.onChange = this.onChange.bind(this)
  
      //this.handleInputChange = this.handleInputChange.bind(this);
    };

    onChange(e) {
        // current array of options
        const options = this.state.options
        let index
    
        // check if the check box is checked or unchecked
        if (e.target.checked) {
          // add the numerical value of the checkbox to options array
          console.log(e.target.value, typeof(e.target.value))
          options.push(e.target.value)
        } else {
          // or remove the value from the unchecked checkbox from the array
          index = options.indexOf(e.target.value)
          options.splice(index, 1)
        }
    
        // update the state with the new array of options
        this.setState({ options: options })
      }

    render() {
        var nodes = this.props.nodeData;
        var edges = this.props.linksData;
        //console.log("Edge example:", edges[0])
        var top_resources = ["pod", "node", "container"]
        var serv_resources = ["deployment", "pod", "service"]
        //console.log("One node:", nodes[1])
        var filtered_nodes = nodes.filter( item => { 
            return ( ((this.state.options.includes(item['group']) || 
            this.state.options.includes('all'))) || 
            (this.state.options.includes('topology') && top_resources.includes(item['group']) ) || 
            (this.state.options.includes('call graph') && serv_resources.includes(item['group']) ))
            });

        var verts = filtered_nodes.map(a => a.id);

        var filtered_edges = edges.filter( item => {
            return (verts.includes(item['source']) && verts.includes(item['target']))
        })
        //console.log("filtered nodes", filtered_nodes, "filtered edges", filtered_edges )
        var listItems = filtered_nodes.map((node) => <li>{node.name}</li>);

      //console.log(this.state.options)
      return (
        <div>
        <form>
          <label>
            Pods: <input name="pods" type="checkbox" value="pod" onChange={this.onChange} />
          </label>
          <br />
          <label>
            Nodes: <input name="nodes" type="checkbox" value="node" onChange={this.onChange} />
          </label>
          <br />
          <label>
            Containers: <input name="containers" type="checkbox" value="container" onChange={this.onChange} />
          </label>
          <br />
          <label>
            Services: <input name="services" type="checkbox" value="service" onChange={this.onChange} />
          </label>
          <br />
          <label>
            Deployments: <input name="deployments" type="checkbox" value="deployment" onChange={this.onChange} />
          </label>
        </form>
        <ForceGraphClass height={500} width={500} links={filtered_edges} nodes={filtered_nodes}/> 
        </div>
      );
    }
  }
  //        <ForceGraph linksData={filtered_edges} nodesData={filtered_nodes}/>


export default CheckboxPractice