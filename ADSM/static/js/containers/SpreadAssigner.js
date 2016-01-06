/**
 * Created by josiah on 1/4/2016.
 */
import React, { Component, PropTypes } from 'react';

export default class SpreadAssigner extends Component {

    render(){
        var { population, input_state } = this.props
        var options = population.map(function(option, index){
            return <option value={option.pk} key={'s'+index}>{option.name}</option>;
        })
        var destination_options = population.map(function(option, index){
            return <option value={option.pk} key={'d'+index}>{option.name}</option>;
        })
        return (
            <div>
                <label htmlFor="source" className="control-label requiredField">
				    Source Production Type<span className="asteriskField">*</span>
                </label>
                <select name="source" required defaultValue={input_state.source}>
                    <option value="">------</option>
                    {options}
                </select>

                <label htmlFor="destinations" className="control-label requiredField">
				    Destinations<span className="asteriskField">*</span>
                </label>
                <select name="destinations" multiple="multiple" required defaultValue={input_state.destinations} className="productiontypelist">
                    {destination_options}
                </select>
            </div>
        )
    }
}