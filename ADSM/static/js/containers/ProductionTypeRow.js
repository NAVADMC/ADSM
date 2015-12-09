

import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'


export default class ProductionTypeRow extends Component {
    render() {
        var { name, unit_count, progression, spread, control, zone } = this.props;
        return(
            <li>
                <a href="#">{ name }</a>
                <span>({ unit_count } units)</span>
                <span className={progression ? 'green-dot on' : 'green-dot'} />
                <span className={spread ? 'green-dot on' : 'green-dot'} />
                <span className={control ? 'green-dot on' : 'green-dot'} />
                <span className={zone ? 'green-dot on' : 'green-dot'} />
            </li>
        )
    }
}
