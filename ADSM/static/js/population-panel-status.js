'use strict';

import React from 'react';
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux';
import {store} from './GlobalStore'
import ConnectedPopulation from './containers/PopulationPanelStatus'


ReactDOM.render(
    <Provider store={store}>
        <ConnectedPopulation />
    </Provider>,
    document.getElementById('population_panel_status')
);