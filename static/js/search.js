"use strict";

//--------------------------------------------------------------------//
// *** DB Search Functions                                            //
//--------------------------------------------------------------------//

//* Update DB Search form based on selected media type

$('#media_type').on('change', (evt) => {
    evt.preventDefault();
    let selectedOption = $(evt.target);
    $('.media-specific').val('');
    $('.type-of-media').hide();
    if ($('#media_type').val() === 'book') {
        $('#its-a-book').slideDown();
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
    console.log(results)
    $('#db-search-results').html('')
    for (let i in results) {
      $('#db-search-results')
      .append(
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