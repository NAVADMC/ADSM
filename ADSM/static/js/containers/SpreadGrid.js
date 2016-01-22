/**
 * Created by josiah on 1/20/2016.
 */

import $ from 'jquery';
import React, { Component, PropTypes } from 'react';
import { connect } from 'react-redux';
import {refresh_disease_spread, refresh_spread_options} from '../actions/actions'
import {store} from '../GlobalStore'
import {RadioGroup} from './RadioButtons'


class SpreadLight extends Component {
    render(){
        var {cell, spread_options, type, being_displayed} = this.props;
        var title = cell[type]
        if(typeof spread_options !== 'undefined' && cell[type]){
            title = spread_options[type][''+cell[type]].name
        }
        var pk = cell[type] ? cell[type] : 'new'  //#704 Each cell links to the Spread Model that it represents.
        var style = {}
        if(being_displayed != 'All'){
            style = {display: "none"}
        }
        if(being_displayed == type){  // overrides none with a full height box
            style = {height: '60px', margin: '0'}
        }
        return <a href={'/setup/DiseaseSpread/?next=/setup/' + type + '/' + pk + '/'}>
            <span className={type + (cell[type]? " assigned": "")} style={style}
                     title={title}> </span>
        </a>
    }
}

class SpreadDisplaySelector extends Component {
    render(){
         return <div className="spread-display-selector">
                    <div style={ {color: 'darkgrey', padding: '5px'} }>Show |</div>
                    <RadioGroup
                        name="display-type"
                        selectedValue={this.props.being_displayed}
                        onChange={this.props.change_type}>
                        {Radio => (
                            <div>
                                <div style={ {color: 'rgb(161, 134, 87)'} }>
                                    <Radio value="DirectSpread" />DIRECT
                                </div>
                                <div style={ {color: 'rgb(146, 203, 170)'} }>
                                    <Radio value="IndirectSpread" />INDIRECT
                                </div>
                                <div style={ {color: 'rgb(52, 192, 209)'} }>
                                    <Radio value="AirborneSpread" />AIRBORNE
                                </div>
                                <div style={ {color: 'black'}             }>
                                    <Radio value="All" />ALL
                                </div>
                            </div>
                        )}
                    </RadioGroup>
                </div>
    }
}


export class SpreadGrid extends Component {
    constructor(props) {
        super(props)
        this.state = {being_displayed: 'All'};
    }
    change_type(type){
        this.setState({being_displayed: type});
    }

    componentDidMount(){
        this.props.dispatch(refresh_disease_spread())
        this.props.dispatch(refresh_spread_options())
    }


    render() {
        var {disease_spread, spread_options} = this.props
        var being_displayed = this.state.being_displayed
        var order = Object.keys(disease_spread).sort()
        return (
            <div className="spread-grid-contents">
                <table className="spread-grid-table">
                    <thead><tr><th></th>
                        {$.map(order, function(source, index){
                            return <th className="spread-destinations">{source}</th>
                        })}
                    </tr></thead>
                    <tbody>
                        {$.map(order, function(source, index){
                            var row = disease_spread[source]
                            return <tr>
                                <th className="spread-source">{source}</th>
                                {$.map(order, function(destination){
                                    var cell = row.destinations[destination]
                                    return <td>
                                        <div className="spread-cell">
                                            <SpreadLight type="DirectSpread" cell={cell} spread_options={spread_options} being_displayed={being_displayed}/>
                                            <SpreadLight type="IndirectSpread" cell={cell} spread_options={spread_options} being_displayed={being_displayed}/>
                                            <SpreadLight type="AirborneSpread" cell={cell} spread_options={spread_options} being_displayed={being_displayed}/>
                                        </div>
                                    </td>
                                })}
                            </tr>
                        })}
                    </tbody>
                </table>
                <SpreadDisplaySelector change_type={this.change_type.bind(this)} being_displayed={being_displayed}/>
            </div>

        );
    }
}


/*disease_spread is the main data structure that drives everything.
* It is a 2D array of cells that each contain {IndirectSpread:pk, DirectSpread: pk, AirborneSpread:pk}
* in them.  The Array is indexed by the Production Type name, rather than a numerical index, so we use Objects
* (python dictionaries) instead of Array[].  Rows are source production types and Columns are destination Production
* Types.  */
SpreadGrid.propTypes = {
    disease_spread: PropTypes.objectOf(
        //sheep: {pk: 3, desinations: {...}
        PropTypes.shape({
            pk: PropTypes.number.isRequired,
            destinations: PropTypes.objectOf(
                //cow: {"IndirectSpread": 2, "DirectSpread": 5, AirborneSpread: null }
                PropTypes.shape({
                    IndirectSpread: PropTypes.number,  //not required, may be null
                    DirectSpread: PropTypes.number,
                    AirborneSpread: PropTypes.number
                })
            ).isRequired
        })
    ).isRequired,
};


function select(state) {
    return {
        disease_spread: state.disease_spread,
        spread_options: state.spread_options
    }
}

// Wrap the component to inject dispatch and state into it
export default connect(select)(SpreadGrid)
