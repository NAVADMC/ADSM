/**
 * Created by josiah on 1/4/2016.
 */
import React, { Component, PropTypes } from 'react';
import {dispatch} from '../GlobalStore'
import {select_value_changed} from '../actions/actions'

export default class SpreadAssigner extends Component {

    onChangeSource(event) {
        var {spread_type, pk, input_state} = this.props
        var new_value = event.target.value;
        new_value = Object.assign({}, input_state, {source: new_value})  //wrap in the old values
        dispatch(select_value_changed(spread_type, pk, 'source', new_value, input_state))
    }
    onChangeDestinations(event) {
        var {spread_type, pk, input_state} = this.props
        var new_value = event.target.value;
        new_value = Object.assign({}, input_state, {destinations: new_value})  //wrap in the old values
        dispatch(select_value_changed(spread_type, pk, 'destinations', new_value, input_state))
    }

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
                <select name="source" required value={input_state.source} onChange={this.onChangeSource.bind(this)}>
                    <option value="">------</option>
                    {options}
                </select>

                <label htmlFor="destinations" className="control-label requiredField">
				    Destinations<span className="asteriskField">*</span>
                </label>
                <select name="destinations" multiple="multiple" required
                        value={input_state.destinations}
                        onChange={this.onChangeDestinations.bind(this)}
                        className="productiontypelist">
                    {destination_options}
                </select>
            </div>
        )
    }
}