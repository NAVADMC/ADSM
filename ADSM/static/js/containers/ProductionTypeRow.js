

import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'


export default class ProductionTypeRow extends Component {
    render() {
        var { name, unit_count, progression, spread, control, zone } = this.props;
        var units = "("+unit_count +" units)"
        var css = "green-dot"
        return(
            <li>
                <a href="#">{ name }</a>
                <span>{units}</span>
                <div className="productiontypes-header"><div className={progression ? css + ' filled' : css} /></div>
                <div className="productiontypes-header"><div className={spread ?      css + ' filled' : css} /></div>
                <div className="productiontypes-header"><div className={control ?     css + ' filled' : css} /></div>
                <div className="productiontypes-header"><div className={zone ?        css + ' filled' : css} /></div>
            </li>
        )
    }
}
