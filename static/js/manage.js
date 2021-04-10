"use strict";

$('.user-media-id').on('click', (evt) => {
    evt.preventDefault();
    alert(`WHY HELLO THERE... my id is ${evt.target.id}`);
    // go to /manage_item route carrying user-media-id!
    $.post('/manage_item', {"user_media_id": evt.target.id}, (res) => {
        document.write(res); 
    });
    // $(location).attr('href', '/manage_item');
})