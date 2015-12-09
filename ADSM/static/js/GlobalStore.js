/**
 * We only need a single global store for tracking state.  Declaring it here allows you to import dispatch instead of passing
 * it down through the entire hierarchy
 */
import { createStore, applyMiddleware, compose } from 'redux'
import thunkMiddleware from 'redux-thunk'
import reducer  from './reducers/reducers'
import { devTools, persistState } from 'redux-devtools'


const finalCreateStore = compose(
    applyMiddleware(thunkMiddleware),
    devTools(),
    persistState(window.location.href.match(/[?&]debug_session=([^&]+)\b/))
)(createStore);

export const store = finalCreateStore(reducer)

export var dispatch = store.dispatch