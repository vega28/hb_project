"use strict";

$('#media_type').on('click', (evt) => {
    evt.preventDefault();
    const selectedOption = $(evt.target);
    alert(`You clicked ${$('#media_type').val()} as your media type!`);
    $('.type-of-media').hide();
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