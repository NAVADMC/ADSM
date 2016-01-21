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
        var {cell, spread_options, type} = this.props;
        var title = cell[type]
        if(typeof spread_options !== 'undefined' && cell[type]){
            console.log("spread_options[type]", spread_options[type])
            console.log("cell[type]", cell[type])
            console.log("''+cell[type]", ""+cell[type])
            console.log("spread_options[type][''+cell[type]]", spread_options[type][""+cell[type]])
            title = spread_options[type][''+cell[type]].name
        }
        var pk = cell[type] ? cell[type] : 'new'  //#704 Each cell links to the Spread Model that it represents.
        return <a href={'/setup/DiseaseSpread/?next=/setup/' + type + '/' + pk + '/'}>
            <span className={type + (cell[type]? " assigned": "")}
                     title={title}> </span>
        </a>
    }
}

class SpreadDisplaySelector extends Component {
    constructor(props) {
        super(props)
        this.state = {selectedType: 'All'};
    }
    selectType(type){
        this.setState({selectedType: type});
    }

    render(){
         return <div className="spread-display-selector">
                    <div style={ {color: 'darkgrey', padding: '5px'} }>Show |</div>
                    <RadioGroup
                        name="display-type"
                        selectedValue={this.state.selectedType}
                        onChange={this.selectType.bind(this)}>
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
/**
 <div style={ {color: 'rgb(161, 134, 87)'} }><div className="green-dot"></div>DIRECT</div>
 <div style={ {color: 'rgb(146, 203, 170)'} }><div className="green-dot"></div>INDIRECT</div>
 <div style={ {color: 'rgb(52, 192, 209)'} }><div className="green-dot"></div>AIRBORNE</div>
 <div style={ {color: 'black'}             }><div className="green-dot"></div>ALL</div>
 */

export class SpreadGrid extends Component {

    componentDidMount(){
        this.props.dispatch(refresh_disease_spread())
        this.props.dispatch(refresh_spread_options())
    }

    render() {
        var {disease_spread, spread_options} = this.props
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
                                            <SpreadLight type="DirectSpread" cell={cell} spread_options={spread_options}/>
                                            <SpreadLight type="IndirectSpread" cell={cell} spread_options={spread_options}/>
                                            <SpreadLight type="AirborneSpread" cell={cell} spread_options={spread_options}/>
                                        </div>
                                    </td>
                                })}
                            </tr>
                        })}
                    </tbody>
                </table>
                <SpreadDisplaySelector />
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
