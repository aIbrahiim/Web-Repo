import React from "react";
import tabib from "../../tabib.png";

export class Register extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="base-container" ref={this.props.containerRef}>
        <div className="header">Register</div>
        <div className="content">
          <div className="image">
            <img src={tabib} />
          </div>
          <div className="form">
            <div className="form-group">
              <label htmlFor="email"></label>
              <input type="text" name="email" placeholder="Email" />
            </div>
            <div className="form-group">
              <label htmlFor="password"></label>
              <input type="password" name="password" placeholder="Password" />
            </div>
            <div className="form-group">
              <label htmlFor="password2"></label>
              <input type="password" name="password2" placeholder="Confirm password" />
            </div>
          </div>
        </div>
        <div className="footer">
          <button type="submit" className="btn">
            Register
          </button>
        </div>
      </div>
    );
  }
}