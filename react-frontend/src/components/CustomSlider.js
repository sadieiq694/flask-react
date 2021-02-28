//import Slider from '@react-native-community/slider';
import Slider from 'rc-slider'
// slider will get passed min and max values

import React from 'react'

const wrapperStyle = { width: 400, margin: 50 };
const { createSliderWithTooltip } = Slider;
const Range = createSliderWithTooltip(Slider.Range);
const { Handle } = Slider;

class CustomSlider extends React.Component{

    constructor(props) {
        super(props)
        this.state = {
            minDistance: this.props.minVal,
            maxDistance: this.props.maxVal,
        }
    };

    render() {
        return(
            <div style={wrapperStyle}>
                <Slider />
                <p>Slider with custom handle</p>
                <Slider min={0} max={100} defaultValue={3} marks={{ 20: 20, 40: 40, 100: 100 }} step={null} />
            </div>
                
        )
    }
}

export default CustomSlider

/*
<View style={styles.container}>
            <Slider
                minimumValue={this.state.minDistance}
                maximumValue={this.state.maxDistance}
                onValueChange={value => this.setState({value: value})}
            />
            <View style={styles.textCon}>
                    <Text style={styles.colorGrey}>{this.state.minDistance} s</Text>
                    <Text style={styles.colorGrey}>{this.state.maxDistance} s</Text>
                </View>
        </View>

<Slider
                    defaultValue={this.state.minDistance}
                    onChange={handleChange}
                    getAriaValueText={valuetext}
                    aria-labelledby="continuous-slider"
                    step={1}
                    min={this.state.minDistance}
                    max={this.state.maxDistance}
                    valueLabelDisplay="on"
/>
        */