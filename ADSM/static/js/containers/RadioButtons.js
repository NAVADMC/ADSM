import React, {PropTypes, Component} from 'react';

function radio(name, selectedValue, onChange) {
    return React.createClass({
        render: function() {
            const optional = {};
            if(selectedValue !== undefined) {
                optional.checked = (this.props.value === selectedValue);
            }
            if(typeof onChange === 'function') {
                optional.onChange = onChange.bind(null, this.props.value);
            }

            return (
                <input
                    {...this.props}
                    type="radio"
                    name={name}
                    {...optional} />
            );
        }
    });
}

export class RadioGroup extends Component {
    render() {
        const {name, selectedValue, onChange, children} = this.props;
        const renderedChildren = children(radio(name, selectedValue, onChange));
        return renderedChildren && React.Children.only(renderedChildren);
    }
}

RadioGroup.propTypes = {
    name: PropTypes.string,
    selectedValue: PropTypes.oneOfType([
        PropTypes.string,
        PropTypes.number,
        PropTypes.bool,
    ]),
    onChange: PropTypes.func,
    children: PropTypes.func.isRequired,
}