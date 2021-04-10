"use strict";

// When user clicks on a cover, open up the details/edits page
$('.user-media-id').on('click', (evt) => {
    evt.preventDefault();
    // alert(`WHY HELLO THERE... my id is ${evt.target.id}`);
    // go to /manage_item route carrying user-media-id!
    $.post('/manage_item', {'user_media_id': evt.target.id}, (res) => {
        console.log('item details have successfully been inserted into the html of this page');
        $('#item-details').html(res);
    });
})

// debugging: alert when either item-actions button is clicked.
$('#item-cover').on('click', () => {
    alert('hullooooooooo')
})


// When user clicks delete button, remove association between item and user (UserMedia object)
$('#delete-from-library').on('click', () => {
    console.log('HALLOOOOOOOOOOO');
    let id_to_del = $('#delete-from-library').val();
    console.log(`here's your value: "${id_to_del}"`);
    // NTH: pop up confirmation before actually deleting
    $.post('/delete_item', {'user_media_id': id_to_del}, () => {
        $('#item-details').html('');
        console.log($(`#${id_to_del}`).val()); // ! currently undefined - Want to remove image associated with user_media_id for selected item... 
    }); // TODO: Delete is successful, but it doesn't rerender the template. remove that item from the JS side!
})

// When user clicks edit button, open rating/review/source/collections for editing
$('#edit-details').on('click', () => {
    alert(`JUST REBOOT THE UNIVERSE, WHY DON'T YOU. MOFFAT *shakes fist* `);
    // open up form entry for anything with class '.editable-detail' ... $('.editable-detail') ... then use new route called update?
    // OR... redirect to review_item page and AUTOFILL using $('.editable-detail') stuff and add a conditional to the add_item route to update instead
})