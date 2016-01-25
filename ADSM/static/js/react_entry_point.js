'use strict';

import "babel-polyfill"

import React from 'react';
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux';
import {store} from './GlobalStore'
import ConnectedPopulation from './containers/PopulationPanelStatus'
import ConnectedSpreadWidget from './containers/SpreadWidget'
import ConnectedSpreadGrid from './containers/SpreadGrid'

ReactDOM.render(
    <Provider store={store}>
        <ConnectedPopulation />
    </Provider>,
    document.getElementById('population_panel_status')
);

$('#spread-widget').livequery(function() { //will add react elements whenever a DOM node is added
    ReactDOM.render(
        <ConnectedSpreadWidget store={store}/>,
        document.getElementById('spread-widget')
    );
})

$('#spread-grid').livequery(function() { //will add react elements whenever a DOM node is added
    ReactDOM.render(
        <ConnectedSpreadGrid store={store}/>,
        document.getElementById('spread-grid')
    );
})