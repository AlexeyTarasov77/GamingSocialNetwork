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

const baseEndpoint = `${window.location.origin}/api/search`;

async function createAlgoliaInstance() {
  return await fetch(`${baseEndpoint}/credentials/`)
    .then(response => response.json())
    .then(data => algoliasearch(data.app_id, data.api_key))
}

createAlgoliaInstance()
.then(algoliaClient => {
  function getIndexTitle(index_name) {
    index_name[0] = index_name[0].toUpperCase();
    return `<h4>${index_name} results</h4>`
  }
  const searchClient = {
    search(requests) {
      const hits = document.querySelectorAll('.search-container');
      if (requests.every(({ params }) => !params.query)) {
        hits.forEach(h => h.style.display = 'none');
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
      hits.forEach(h => h.style.display = 'block');
      return algoliaClient.search(requests);
    },
  }
  const postsIndex = "posts"
  const productsIndex = "products"

  const search = instantsearch({
    indexName: postsIndex,
    searchClient,
  });

  search.addWidgets([
    instantsearch.widgets.searchBox({
      container: '#searchbox',
      placeholder: 'Поиск',
    }),

    instantsearch.widgets.hits({
      container: `#${postsIndex}-hits`,
      templates: {
        item: `
          <div class="${postsIndex}-hit">
            <h6><a href="{{ url }}">{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</a></h6>
            <p>{{#helpers.highlight}}{ "attribute": "content" }{{/helpers.highlight}}</p>
          </div>
        `,
      },
    }),
    instantsearch.widgets.refinementList({
      container: `#${postsIndex}-faceting-1`,
      attribute: 'get_type_display',
    }),
    instantsearch.widgets.refinementList({
      container: `#${postsIndex}-faceting-2`,
      attribute: 'get_status_display',
    }),

    instantsearch.widgets.index({"indexName": productsIndex})
    .addWidgets([
      instantsearch.widgets.hits({
        container: `#${productsIndex}-hits`,
        templates: {
          item: `
          <div class="${productsIndex}-hit">
            <h6><a href="{{ url }}">{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</a></h6>
            <p class="fw-bold">{{final_price}}  $</p>
          </div>
          `,
        }
      }),
      instantsearch.widgets.refinementList({
        container: `#${productsIndex}-faceting-1`,
        attribute: '_category',
      }),
      instantsearch.widgets.refinementList({
        container: `#${productsIndex}-faceting-2`,
        attribute: '_available',
      })
    ])
  ]);
  search.start();
})


