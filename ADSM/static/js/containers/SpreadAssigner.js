/**
 * Created by josiah on 1/4/2016.
 */
import React, { Component, PropTypes } from 'react';

export default class SpreadAssigner extends Component {

    render(){
        var destinations = this.props.input_state.destinations
        var { source, population, input_state } = this.props
        var options = population.map(function(option, index){
            return <option value={option.pk} key={'s'+index}>{option.name}</option>;
        })
        var destination_options = population.map(function(option, index){
            return <option value={option.pk} key={'d'+index}>{option.name}</option>;
        })
        return (
            <div>
                <label for="source" class="control-label requiredField">
				    Source Production Type<span class="asteriskField">*</span>
                </label>
                <select name="source" required defaultValue={source}>
                    <option value="">------</option>
                    {options}
                </select>

                <label for="destinations" class="control-label requiredField">
				    Destinations<span class="asteriskField">*</span>
                </label>
                <select name="destinations" multiple="multiple" required defaultValue={destinations} className="productiontypelist">
                    {destination_options}
                </select>
            </div>
        )
    }
}