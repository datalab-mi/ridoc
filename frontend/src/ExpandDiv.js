import React, { Component } from 'react';

class ExpandDiv extends React.Component {
  constructor(props) {
    super(props);
    this.state = { showResults: false };
    }

  handleClick() {
    this.setState({ showResults: !this.state.showResults })
  }

  render() {
       return (
           <div>
               <button onClick={()=>this.handleClick()}>
                 DSL
               </button>
               { this.state.showResults ? <pre>{this.props.value}</pre> : null }

           </div>
       );
   }
}

export default ExpandDiv;
