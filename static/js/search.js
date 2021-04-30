"use strict";

//--------------------------------------------------------------------//
// *** DB Search Functions                                            //
//--------------------------------------------------------------------//

//* Update DB Search form based on selected media type

$('#media_type').on('change', (evt) => {
    evt.preventDefault();
    let selectedOption = $(evt.target);
    $('.media-specific').val('');
    $('#go-search-api').html('');
    $('.type-of-media').hide();
    if ($('#media_type').val() === 'book') {
        $('#its-a-book').slideDown();
        $('#go-search-api').html(
            `<p>
              Not finding the book you're looking for? 
              <a href="/api_search">Search Google Books instead!</a>
            </p>`);
    }
    if ($('#media_type').val() === 'movie') {
        $('#its-a-movie').slideDown();    
    }
    if ($('#media_type').val() === 'tv_ep') {
        $('#its-a-tv-ep').slideDown();    
    }
    if ($('#media_type').val() === 'item') {
    }
})


//* Success function: show search results from database:

function displayResults(results) {
    console.log('NEW RESULTS')
    console.log(results)
    console.log(typeof(results))
    $('#db-search-results').html('')
    // TODO: deal with case of no results in db
    // !     why doesn't the below work?
    // if (results === {}) {
    //     $('#db-search-results').append('Sorry, that search is not turning up any results.');
    // }
    for (let i in results) {
      $('#db-search-results').append(
        `<div>
          <input type="radio" name="chosen-item" value="${i}" required> 
          ${results[i]['title']}
          <img src=${results[i]['cover']}>
        </div>`
        );
    }
}


//* Display updated DB Search results based on user input (in real time!)

$('.choice').on('change', (evt) => {
    evt.preventDefault();
    // get the vals
    let formData = {'media_type': $('#media_type').val(),
                    'title': $('#title').val(),
                    'year': $('#year').val(),
                    'author': $('#author').val(),
                    'length': $('#length').val(),
                    'season': $('#season').val(),
                    'genre': $('#genre option:selected').val()}; 
    $.get('/process_search', formData, displayResults);
})