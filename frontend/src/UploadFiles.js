import React, { Component } from 'react';

export default class FilesUploadComponent extends Component {

    constructor(props) {
        super(props);

        this.onFileChange = this.onFileChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);

        this.state = {
            filesCollection: ''
        }
    }

    onFileChange(e) {
        this.setState({ filesCollection: e.target.files })
    }

    onSubmit(e) {
        e.preventDefault()

        for (const key of Object.keys(this.state.filesCollection)) {
            var formData = new FormData();
            formData.append('file', this.state.filesCollection[key])
            var request = new XMLHttpRequest();
            request.open("POST", "http://localhost/api/common/upload",true);
            request.send(formData);

        }

    }


    render() {
        return (
            <div className="container">
                <div className="row">
                    <form onSubmit={this.onSubmit}>
                        <div className="form-group">
                            <input type="file" name="file" onChange={this.onFileChange} multiple />
                        </div>
                        <div className="form-group">
                            <button className="btn btn-primary" type="submit">Upload</button>
                        </div>
                    </form>
                </div>
            </div>
        )
    }
}
