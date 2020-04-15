import React from 'react'
import ReactDOM from 'react-dom'
import Moment from 'moment'

import "./FileManager.css";

import FileBrowser, {Icons} from 'react-keyed-file-browser'
import { PdfViewer, Child } from './PdfViewer';
import NewWindow from 'react-new-window'



class NestedEditableDemo extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      files: []
    };
  }
  componentDidMount() {
    fetch("http://localhost/api/common/files")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            files: result
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }



  handleCreateFolder = (key) => {
    this.setState(state => {
      state.files = state.files.concat([{
        key: key,
      }])
      return state
    })
  }

  handleCreateFiles = (files, prefix) => {
    this.setState(state => {
      const newFiles = files.map((file) => {
        let newKey = prefix
        if (prefix !== '' && prefix.substring(prefix.length - 1, prefix.length) !== '/') {
          newKey += '/'
        }
        newKey += file.name
        return {
          key: newKey,
          size: file.size,
          modified: +Moment(),
        }
      })

      const uniqueNewFiles = []
      newFiles.map((newFile) => {
        let exists = false
        state.files.map((existingFile) => {
          if (existingFile.key === newFile.key) {
            exists = true
          }
        })
        if (!exists) {
          uniqueNewFiles.push(newFile)
        }
      })
      state.files = state.files.concat(uniqueNewFiles)
      return state
    })
  }
  handleRenameFolder = (oldKey, newKey) => {
    this.setState(state => {
      const newFiles = []
      state.files.map((file) => {
        if (file.key.substr(0, oldKey.length) === oldKey) {
          newFiles.push({
            ...file,
            key: file.key.replace(oldKey, newKey),
            modified: +Moment(),
          })
        } else {
          newFiles.push(file)
        }
      })
      state.files = newFiles
      return state
    })
  }
  handleRenameFile = (oldKey, newKey) => {
    this.setState(state => {
      const newFiles = []
      state.files.map((file) => {
        if (file.key === oldKey) {
          newFiles.push({
            ...file,
            key: newKey,
            modified: +Moment(),
          })
        } else {
          newFiles.push(file)
        }
      })
      state.files = newFiles
      return state
    })
  }
  handleDeleteFolder = (folderKey) => {
    this.setState(state => {
      const newFiles = []
      state.files.map((file) => {
        if (file.key.substr(0, folderKey.length) !== folderKey) {
          newFiles.push(file)
        }
      })
      state.files = newFiles
      return state
    })
  }
  handleDeleteFile = (fileKey) => {
    this.setState(state => {
      const newFiles = []
      state.files.map((file) => {
        if (file.key !== fileKey) {
          newFiles.push(file)
        }
      })
      state.files = newFiles
      return state
    })
  }
  handleSelectFile = (filekey) => {
    console.log(filekey)

    return
  }

  render() {
    return (
      <FileBrowser
        files={this.state.files}
        icons={Icons.FontAwesome(4)}

        onCreateFolder={this.handleCreateFolder}
        onCreateFiles={this.handleCreateFiles}
        onMoveFolder={this.handleRenameFolder}
        onMoveFile={this.handleRenameFile}
        onRenameFolder={this.handleRenameFolder}
        onRenameFile={this.handleRenameFile}
        onDeleteFolder={this.handleDeleteFolder}
        onDeleteFile={this.handleDeleteFile}

        onSelectFile={this.handleSelectFile}
      />
    )
  }
}


export default NestedEditableDemo;
