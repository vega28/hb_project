"use strict";

// When user clicks on a cover, open up the manage_item part of the page
$('.user-media-id').on('click', (evt) => {
    // alert(`WHY HELLO THERE... my id is ${evt.target.id}`);
    $('#collection-details').html('');
    $.post('/manage_item', {'user_media_id': evt.target.id}, (res) => {
        console.log('item details have successfully been inserted into the html of this page');
        $('#item-details').html(res);
    });
})



// When user clicks delete button, remove association between item and user (UserMedia object)
$('#delete-from-library').on('click', () => {
    let id_to_del = $('#delete-from-library').val();
    console.log(`here's your value: "${id_to_del}"`);
    // NTH: pop up confirmation before actually deleting
    $.post('/delete_item', {'user_media_id': id_to_del}, (res) => {
        $('#item-details').html('');
        alert(res);
        console.log($(`#${id_to_del}`).val()); // ! currently undefined - Want to remove image associated with user_media_id for selected item... 
    }); // TODO: Delete is successful, but it doesn't rerender the template. remove that item from the JS side!
})

// When user clicks edit button, open rating/review/source/collections for editing
$('#edit-details').on('click', () => {
    alert(`JUST REBOOT THE UNIVERSE, WHY DON'T YOU. MOFFAT *shakes fist* `);
    // open up form entry for anything with class '.editable-detail' ... $('.editable-detail') ... then use new route called update?
    // OR... redirect to review_item page and AUTOFILL using $('.editable-detail') stuff and add a conditional to the add_item route to update instead
})


// When user clicks close button, close the expanded details (both colleciton and item)
$('.close-details').on('click', (evt) => {
    // alert(`WHY HELLO THERE... my id is ${evt.target.id}`);
    $('#collection-details').html('');
    $('#item-details').html('');
})


// When user clicks on a collections div, open up the manage_collections part of the page
$('.collection').on('click', (evt) => {
    // alert(`WHY HELLO THERE... my id is ${evt.target.id}`);
    $('#item-details').html('');
    $.post('/manage_collection', {'collection_id': evt.target.id}, (res) => {
        console.log('collection details have successfully been inserted into the html of this page');
        $('#collection-details').html(res);
    });
})
