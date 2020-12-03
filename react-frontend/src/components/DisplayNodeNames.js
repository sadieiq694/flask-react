import React from 'react'

class DisplayNodeNames extends React.Component{
    constructor(props) {
        super(props)
        this.state = {value: ''};
    

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this); 
    }

    handleChange(event) {
        this.setState({value: event.target.value});
    }

    handleSubmit(event) {
        alert("A name was submitted: " + this.state.value);
        event.preventDefault();
    }

    render() {
        var nodes = this.props.nodeData; 
        //var edges = this.props.linksData;
        //console.log("CONSOLE LOG DISPLAY: ", nodes)

        // filter nodes whose group matches the current state
        var filtered_nodes = nodes.filter( item => {
            return item.group == this.state.value
            });
        //console.log("NODES:", misDataFiltered2)
        const listItems = filtered_nodes.map((node) => <li>{node.name}</li>);


        return (
            <div>
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Name:
                        <input type="text" value={this.state.value} onChange={this.handleChange} />
                    </label>
                    <input type="submit" value="Submit" />
                </form>
                <h1>Current state: {this.state.value}</h1>
                <h1>NODE LIST</h1>
                <ul>{listItems}</ul>
            </div>
        );
    }
    
}
    
    export default DisplayNodeNames
