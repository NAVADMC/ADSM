

import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'


export default class ProductionTypeRow extends Component {
    render() {
        var { name, unit_count, progression, spread, control, zone } = this.props;
        var units = "("+unit_count +" units)"
        return(
            <li>
                <a href="#">{ name }</a>
                <span>{units}</span>
                <div className={progression ? 'green-dot filled' : 'green-dot'} />
                <div className={spread ?      'green-dot filled' : 'green-dot'} />
                <div className={control ?     'green-dot filled' : 'green-dot'} />
                <div className={zone ?        'green-dot filled' : 'green-dot'} />
            </li>
        )
    }
}
