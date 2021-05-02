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
    let j = 1;
    for (let i in results) {
      console.log(i, j)
      // let cardHTML = `<div class="card" style="height: 18em; width: 15em;"> 
      //                   <div class="card-body">
      //                     <div class="row">
      //                       <img style="width: auto;" src=${results[i]['cover']}>
      //                     </div>
      //                     <input type="radio" name="chosen-item" value="${i}" required> 
      //                     <span class="card-text">${results[i]['title']}</span>
      //                     <p><a href="#" class="btn btn-primary">this one!</a></p>
      //                   </div>
      //                 </div>`;
      let cardHTML = `<div class="card" style="height: 24em; width: 15em;"> 
                        <div class="card-header">${results[i]['media_type']}</div>
                        <div class="card-body">
                          <div class="row">
                            <img style="width: auto;" src="${results[i]['cover']}">
                          </div>
                          <div class="row">
                            <p class="card-text"><h5>${results[i]['title']}</h5></p>
                            <p><button class="btn btn-primary" type="submit" name="chosen-item" value="${i}">this one!</button></p>
                          </div>
                        </div>
                      </div>`;
      if (j % 3 == 1) {
        console.log(`hello from the ${(j + 2) / 3} row ${typeof((j + 2) / 3)}`)
        $('#db-search-results').append(`<div class="row row-${(j + 2) / 3}"></div>`);
        $(`.row-${(j + 2) / 3}`).append(cardHTML);
      }
      if (j % 3 == 2) {
        $(`.row-${(j + 1) / 3}`).append(cardHTML);
      }
      if (j % 3 == 0) {
        $(`.row-${j / 3}`).append(cardHTML);
      }
    j += 1;
    }
  }


//* Display updated DB Search results based on user input (in real time!)

$('.choice').on('input', (evt) => {
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