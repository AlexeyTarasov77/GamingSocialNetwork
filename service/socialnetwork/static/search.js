// document.addEventListener("DOMContentLoaded", function () {
//     const searchForm = document.querySelector('#search-form');
//     const searchInput = document.querySelector('#search-input');
//     let searchInputLastValue = searchInput.value;
//     const searchResults = document.querySelector('#search-results');
//     searchInput.addEventListener('input', searchInputHandler);
//     searchForm.addEventListener('submit', searchHandler);
//     function searchHandler(e) {
//         e.preventDefault();
//         const query = searchInput.value
//         fetch(searchForm.action + '?' + new URLSearchParams({q: query}))
//         .then(response => response.json())
//         .then(data => {
//             searchResultsHandler(data)
//         })
//     }
//     let timeoutId;
//     function searchInputHandler(e) {
//       let obj = e.target
//       if (obj.value.length > 0 && obj.value != searchInputLastValue) {
//         searchInputLastValue = obj.value;
//         clearTimeout(timeoutId);
//         timeoutId = setTimeout(function () {
//           searchHandler(e)
//         }, 1800);
//       }
//     }

//     function clearSearch() {
//         searchInput.value = '';
//         searchInputLastValue = '';
//         searchResults.innerHTML = '';
//     }

//     function searchResultsHandler(data) {
//       clearSearch()
//       console.log(data);
//     }
// })

// document.addEventListener("DOMContentLoaded", function () {
//     const clearBtn = document.querySelector('.ais-SearchBox-reset');
//     const searchInput = document.querySelector('.ais-SearchBox-input');
//     const searchResults = document.querySelector('#hits');
//     if (clearBtn) {
//       clearBtn.addEventListener('click', function () {
//         searchInput.value = '';
//         searchResults.innerHTML = '';
//       })
      
//     }
// })

const algoliaClient = algoliasearch('RBET4E0JU0', '6deb5d118df506fca82b57edf2487db2');

const searchClient = {
    search(requests) {
      if (requests.every(({ params }) => !params.query)) {
        return Promise.resolve({
          results: requests.map(() => ({
            hits: [],
            nbHits: 0,
            nbPages: 0,
            page: 0,
            processingTimeMS: 0,
            hitsPerPage: 0,
            exhaustiveNbHits: false,
            query: '',
            params: '',
          })),
        });
      }
  
      return algoliaClient.search(requests);
    },
  }

const search = instantsearch({
  indexName: 'posts',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
    placeholder: 'Поиск',
  }),

  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
      item: `
        <div>
          <h6><a href="{{ url }}">{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</a></h6>
          <p>{{#helpers.highlight}}{ "attribute": "content" }{{/helpers.highlight}}</p>
        </div>
      `,
    },
  }),
  instantsearch.widgets.refinementList({
    container: '#content-types',
    attribute: 'get_type_display',
  }),
  instantsearch.widgets.refinementList({
    container: '#status',
    attribute: 'get_status_display',
  }),
]);

search.start();
