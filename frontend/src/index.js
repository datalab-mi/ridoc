import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { PdfViewer, Child } from './PdfViewer';
import NestedEditableDemo from './FileManager';
import FilesUploadComponent from './UploadFiles';

import { BrowserRouter, Route, Router, Switch} from 'react-router-dom'
import * as serviceWorker from './serviceWorker';





ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
        <Switch>

          <Route exact path="/">
            <App />
          </Route>

          <Route exact path="/browse">
            <NestedEditableDemo />
          </Route>

          <Route exact path="/upload">
          <FilesUploadComponent />
        </Route>

          <Route path="/view/:id" children={<Child />}/>

        </Switch>
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
