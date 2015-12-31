/**
 * Created by josiah on 12/31/2015.
 */


'use strict';

import React from 'react';
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux';
import {store} from './GlobalStore'
import ConnectedSpreadWidget from './containers/SpreadWidget'


ReactDOM.render(
    <Provider store={store}>
        <ConnectedSpreadWidget />
    </Provider>,
    document.getElementById('spread-widget')
);