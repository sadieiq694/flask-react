import * as d3 from "d3";
import React from 'react'
//import "@fortawesome/fontawesome-free/css/all.min.css";
//import styles from "./forceGraph.module.css";


const imgScale = d3.scaleOrdinal() //=d3.scaleOrdinal(d3.schemeSet2)
    .domain(["node", "container", "pod", "service", "deployment"])
    .range(['https://cdn2.iconfinder.com/data/icons/mixd/512/21_kubernetes-512.png', 'https://cdn4.iconfinder.com/data/icons/vectory-symbols/40/hexagon-512.png', 'https://image.flaticon.com/icons/svg/73/73326.svg','https://static.thenounproject.com/png/32460-200.png', 'https://cdn1.iconfinder.com/data/icons/materia-arrows-symbols-vol-9/24/018_343_insignia_badge_shape_triangle-512.png'])

const edgeColorScale = d3.scaleOrdinal() //=d3.scaleOrdinal(d3.schemeSet2)
    .domain(["scheduled on", "runs", "references", "targets", "calls", "owns", "backs", "points to"])
    .range(['red', 'black', 'blue','pink','green','brown','yellow','orange'])

class ForceGraphClass extends React.Component{
    componentDidMount(){
        this.createGraph();
    }
    componentDidUpdate(){
        var svg = d3.select('svg');
        svg.selectAll("*").remove();
        this.createGraph(); 
    }

    createGraph = ()=>{
        const width = 1000;
        const height = 400; 
        var links = this.props.links.map((d) => Object.assign({}, d));
        var nodes = this.props.nodes.map((d) => Object.assign({}, d));


        const drag = (simulation) => {
            function dragsubject(event) {
              return simulation.find(event.x, event.y);
            }
          
            const dragstarted = (d) => {
              if (!d.active) simulation.alphaTarget(0.3).restart();
              d.subject.fx = d.subject.x;
              d.subject.fy = d.subject.y;
            }
            
            const dragged = (d) => {
              d.subject.fx = d.x;
              d.subject.fy = d.y;
            }
            
            const dragended = (d) => {
              if (!d.active) simulation.alphaTarget(0);
              d.subject.fx = null;
              d.subject.fy = null;
            }
            
            return d3.drag()
                .subject(dragsubject)
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
          }

        const simulation = d3
            .forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(-200))
            .force("x", d3.forceX())
            .force("y", d3.forceY());


        var svg = d3
            .select('svg')
            //.append("svg")
            .attr("viewBox", [-width/2, -height/2, width, height]);

        const def = svg.append('defs').append('marker')
            .attr("id",'arrowhead')
            .attr('viewBox','-0 -5 10 10') //the bound of the SVG viewport for the current SVG fragment. defines a coordinate system 10 wide and 10 high starting on (0,-5)
            .attr('refX',23) // x coordinate for the reference point of the marker. If circle is bigger, this need to be bigger.
            .attr('refY',0)
            .attr('orient','auto')
            .attr('markerWidth', 4)
            .attr('markerHeight', 4)
            .attr('xoverflow','visible')
            .append('svg:path')
            .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
            .attr('fill', 'black')
            .style('stroke','none');

        const link = svg
            .append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .selectAll("line")
            .data(links)
            .join("line")
            .style("stroke", d => edgeColorScale(d.type))
            .attr("stroke-width",3)
            .attr('marker-end','url(#arrowhead)');
        
        const text = svg.append("g") // deleting this gets rid of images 
            .attr("class", "text")
            .selectAll("text")
            .data(nodes)
            .enter().append("text")
            .attr("font-family", "sans-serif")
            .attr("font-size", 15)
            .text(d => d.name)
            .call(drag(simulation));;

        const img = svg.append("g")
            .attr("class", "image")
            .selectAll("image")
            .data(nodes)
            .enter().append("image")
            .attr("xlink:href",d => imgScale(d.group) )
            .attr("width", 30)
            .attr("height", 30)
            //.on("click", clickNode)
            .call(drag(simulation));

          const legend_g = svg.selectAll(".legend")
              .data(imgScale.domain())
              .enter().append("g") 
              .attr("transform", (d, i) => `translate(${width-650},${ -50 + i * 25})`); 
        
          legend_g.append("image")
              .attr("xlink:href",imgScale )
              .attr("width", 20)
              .attr("height", 20);
        
          legend_g.append("text")
              .attr("x", 25)
              .attr("y", 20)
              .text(d => d);
          
          const legend_g2 = svg.selectAll(".legend")
              .data(edgeColorScale.domain())
              .enter().append("g") 
              .attr("transform", (d, i) => `translate(${width-640},${100+ i * 20})`); 
        
          legend_g2.append("circle")
              .attr("cx", 0)
              .attr("cy", 0)
              .attr("r", 5)
              .attr("fill", edgeColorScale);
            
          legend_g2.append("text")
              .attr("x", 10)
              .attr("y", 5)
              .text(d => d);

        simulation.on("tick", () => {
            //update link positions
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
        
            img
                .attr("x", d => d.x-15) //position of the lower left point of the text
                .attr("y", d => d.y-15); //position of the lower left point of the text
            text
                .attr("x", d => d.x + 15) //position of the lower left point of the text
                .attr("y", d => d.y + 5); //position of the lower left point of the text

            });
        

        return {
            destroy: () => {
                //d3.select(svg).remove()
                //link.exit().remove()
                //img.exit().remove();
                simulation.stop();
            },
            nodes: () => {
                return svg.node();
            }
        };
 
    }

    

    render(){
        console.log(this.props.data)
        return(
            <svg>

            </svg>
        );
    }

} 

export default ForceGraphClass

/*
runForceGraph(
  container,
  linksData,
  nodeData,
) {
  console.log("IN GRAPHGENERATOR", nodeData)
  const links = linksData.map((d) => Object.assign({}, d));
  const nodes = nodeData.map((d) => Object.assign({}, d));

  const containerRect = container.getBoundingClientRect();
  const height = containerRect.height;
  const width = containerRect.width;

  const color = () => { return "#9D79A0"; };




  const link = svg
    .append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .join("line")
    .style("stroke", d => edgeColorScale(d.type))
    .attr("stroke-width",3)
    .attr('marker-end','url(#arrowhead)');
    
  const node = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r",5)
    // .style("fill", d => colorScale(d.group))
    .style("fill", "#ffffff");

  const img = svg.append("g")
    .attr("class", "image")
    .selectAll("image")
    .data(nodes)
    .enter().append("image")
    .attr("xlink:href",d => imgScale(d.group) )
    .attr("width", 30)
    .attr("height", 30)
    //.on("click", clickNode)
    .call(drag(simulation));

  /*const label = svg.append("g")
    .attr("class", "labels")
    .selectAll("text")
    .data(nodes)
    .enter()
    .append("text")
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'central')
    .attr("class", d => `fa ${getClass(d)}`)
    .text(d => {return icon(d);})
    .call(drag(simulation));

  const text = svg.append("g") // deleting this gets rid of images 
    .attr("class", "text")
    .selectAll("text")
    .data(nodes)
    .enter().append("text")
    .attr("font-family", "sans-serif")
    .attr("font-size", 15)
    .text(d => d.name)
    .call(drag(simulation));;


  label.on("mouseover", (d) => {
    addTooltip(nodeHoverTooltip, d, d3.event.pageX, d3.event.pageY);
  })
    .on("mouseout", () => {
      removeTooltip();
    });

  simulation.on("tick", () => {
    //update link positions
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    // update node positions
    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
    img
      .attr("x", d => d.x-15) //position of the lower left point of the text
      .attr("y", d => d.y-15); //position of the lower left point of the text

    text
      .attr("x", d => d.x + 15) //position of the lower left point of the text
      .attr("y", d => d.y + 5); //position of the lower left point of the text
  });

  const legend_g = svg.selectAll(".legend")
    .data(imgScale.domain())
    .enter().append("g") 
    .attr("transform", (d, i) => `translate(${width-600},${ -50 + i * 25})`); 

  legend_g.append("image")
        .attr("xlink:href",imgScale )
        .attr("width", 20)
      .attr("height", 20);

  legend_g.append("text")
    .attr("x", 25)
    .attr("y", 20)
    .text(d => d);
  
  const legend_g2 = svg.selectAll(".legend")
    .data(edgeColorScale.domain())
    .enter().append("g") 
    .attr("transform", (d, i) => `translate(${width-590},${100+ i * 20})`); 

  legend_g2.append("circle")
    .attr("cx", 0)
    .attr("cy", 0)
    .attr("r", 5)
    .attr("fill", edgeColorScale);
    
  legend_g2.append("text")
    .attr("x", 10)
    .attr("y", 5)
    .text(d => d);

  return {
    destroy: () => {
      simulation.stop();
    },
    nodes: () => {
      return svg.node();
    }
  };
}
*/