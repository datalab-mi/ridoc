import React, { Component } from 'react';
import NewWindow from 'react-new-window'
import { ReactiveBase,
        DataSearch,
        DateRange,
        StateProvider,
        ReactiveList,
        ResultList,
        SelectedFilters,
        MultiList
} from '@appbaseio/reactivesearch';
import "./App.css";
import ExpandDiv from './ExpandDiv'

const { ResultListWrapper } = ReactiveList;


function ServerQuery(value, props){
  console.log(value)
  console.log(props)

  fetch("http://localhost:5000/common/build_query",{
    method: "POST",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin':'*',
      'Access-Control-Allow-Headers': 'Content-Type'
    },
    body: JSON.stringify({
      index_name: 'iga',
      value: 'test'
    })
  }).then(function(response) {
      if(response.ok) {
        console.log(response);
      } else {
        console.log('Mauvaise réponse du réseau');
        console.log(response);

      }
    })
    .catch(function(error) {
    console.log('Il y a eu un problème avec l\'opération fetch: ' + error.message);
  });

  return {
    query: {
        match: {
            content: value
        }
    }
  }
}

class App extends React.Component {
  constructor(props) {
  super(props);
  this.state = { dsl: '' };
  }

  render() {
    return (

      <div className="main-container">


        <ReactiveBase
          app="iga"
          url="http://localhost:9200"
        >

        <DataSearch
        componentId="SearchFilter"
        dataField={["content","title"]}
        className="search-bar"
        queryFormat="or"
        placeholder="Search for documents..."
        innerClass={{
            title: 'search-title',
            input: 'search-input'
        }}
        highlight={true}
        autosuggest={false}//no dropdown suggestion
        customHighlight={props => ({
      		highlight: {
            pre_tags: ['<mark>'],
            post_tags: ['</mark>'],
      			fields: {
      				content:{},
      				title: {},
      			},
            "fragment_size" : 300,
            "number_of_fragments" : 3,
            "order" : "score",
            "boundary_scanner" : "sentence",
            "boundary_scanner_locale" : "fr-FR"
      		},
      	})}
        //customQuery={function(value,props){
        //  return {query: {match:{content:'this is a test'}}}}}
        />

        <DataSearch
        componentId="SearchFilterServer"
        placeholder="Custom search for documents on server..."
        customQuery={ServerQuery}
        />


        <StateProvider
        includeKeys={['query']}
        render={({ searchState }) => {
            console.log(JSON.stringify(searchState.SearchResult))
            this.setState({dsl : JSON.stringify(searchState.SearchResult, undefined, 2)})
            return null
        }}
        />

        <DateRange
          componentId="DateFilter"
          dataField="date"
        />


        <SelectedFilters
            showClearAll={true}
            clearAllLabel="Clear filters"
        />



        <ExpandDiv value={this.state.dsl}/>



        <ReactiveList
            react={{ //https://docs.appbase.io/docs/reactivesearch/v3/advanced/reactprop/
              "and" : {
                "or": ["SearchFilterServer", "SearchFilter"],
                "and":["DateFilter"]
              }
            }}
            componentId="SearchResult"
        >
          {({ data }) => (
              <ResultListWrapper>
                  {
                      data.map(item => (
                          <ResultList key={item._id}>
                              <ResultList.Content>
                                  <ResultList.Title
                                      dangerouslySetInnerHTML={{
                                          __html: item.title
                                      }}
                                  />
                                  <ResultList.Description
                                        dangerouslySetInnerHTML={{
                                          __html: item.content
                                      }}
                                  />
                                  <div>
                                  <div>Par {item.author}</div>
                                  <span>
                                      Pub {item.date}
                                  </span>
                                  </div>
                              </ResultList.Content>
                          </ResultList>
                      ))
                  }
              </ResultListWrapper>
          )}
        </ReactiveList>

        </ReactiveBase>
      </div>
    );
  }
}

export default App;
