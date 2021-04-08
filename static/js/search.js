"use strict";

$('#media_type').on('change', (evt) => {
    evt.preventDefault();
    const selectedOption = $(evt.target);
    $('.type-of-media').hide();
    // TODO: empty the vals for any specific media type
    // $(`#its-a-${$('#media_type').val()}`).slideDown();
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

// Show search results from database:

function displayResults(results) {
    console.log(results)
    $('#db-search-results').html('')
    for (let i in results) {
      $('#db-search-results').append(`<div><input type="radio" name="chosen-item" value="${i}"> ${results[i]['title']} <img src=${results[i]['cover']}></div>`);
    }
}

$('.choice').on('change', (evt) => {
    evt.preventDefault();
    // get the vals
    let formData = {'media_type': $('#media_type').val(),
                    'title': $('#title').val(),
                    'year': $('#year').val(),
                    'genre': $('#genre').val()};
    $.get('/process_search', formData, displayResults);
    // alert('WHY HELLO THERE');
})