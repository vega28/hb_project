"use strict";

// When user clicks on a cover, open up the details/edits page
$('.user-media-id').on('click', (evt) => {
    evt.preventDefault();
    // alert(`WHY HELLO THERE... my id is ${evt.target.id}`);
    // go to /manage_item route carrying user-media-id!
    $.post('/manage_item', {'user_media_id': evt.target.id}, (res) => {
        document.write(res); 
    });
})

// When user clicks delete button, remove association between item and user (UserMedia object)
$('#delete-from-library').on('click', (evt) => {
    evt.preventDefault();
    // NTH: pop up confirmation before actually deleting
    alert(`DELETE DELETE... OK, MR CYBERMAN`);
    $.post('/delete_item', {'user_media_id': $('#user-media-id')}); // TODO: THIS IS BROKEN. not deleting item now and not rerouting either...
})

// When user clicks edit button, open rating/review/source/collections for editing
$('#edit-details').on('click', (evt) => {
    evt.preventDefault();
    alert(`JUST REBOOT THE UNIVERSE, WHY DON'T YOU.`);
    // redirect to review_item page?
})