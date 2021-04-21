"use strict";

//--------------------------------------------------------------------//
// *** Item Management Functions                                      //
//--------------------------------------------------------------------//

//* When user clicks on a cover, open up the view_item part of the page
//      allow user to add item to a collection

$('.user-media-id').on('click', (evt) => {
    $('#collection-details').html('');
    $.post('/view_item', {'user_media_id': evt.target.id}, (res) => {
        $('#item-details').html(res);
        console.log('item details have successfully been displayed on this page');
 
        $('#add-to-collection').on('click', (evt) => {
            evt.preventDefault();
            $.get('/list_collections', (userCollections) => {
            
                $('#which-collection-to-add-to').append('<form id="add-to-collection-form">');
                for (let i in userCollections) {
                    $('#which-collection-to-add-to').append(`<p><input type="radio" name="which-collection" value="${i}">${userCollections[i]['name']}</p>`);
                }
                $('#which-collection-to-add-to').append('<input type="submit" id="coll-submit-button"></form>');
                
                // ? WHY didn't this next line work?!
                // $('#add-to-collection-form').on('submit', (evt) => { 
                $('#coll-submit-button').on('click', () => {
                    let user_media_id = $('#add-to-collection').val();
                    let collection_id = $('input[type="radio"]:checked').val();
                    let postData = {'user_item_id': user_media_id, 
                                    'collection_id': collection_id}
                    $.post('/add_item_to_collection', postData, (res2) => {
                        alert(res2['alert']);
                        $(`#collection-display-${collection_id}`).append(`<img src="${res2['cover']}" class="${user_media_id}">`);
                    });
                    $('#which-collection-to-add-to').html('');
                });
            });
    
        });
    });
});



//* When user clicks delete button, remove association between item and user (UserMedia object)

$('#delete-from-library').on('click', () => {
    let id_to_del = $('#delete-from-library').val();
    console.log(`here's your value: "${id_to_del}"`);
    console.log($(`.${id_to_del}`)[0].id); 
    // NTH: pop up confirmation before actually deleting
    $.post('/delete_item', {'user_media_id': id_to_del}, (res) => {
        $('#item-details').html('');
        alert(res);
        $(`.${id_to_del}`).remove(); 
    }); 
})


// TODO: When user clicks edit button, open rating/review/source/collections for editing

$('#edit-details').on('click', () => {
    alert(`JUST REBOOT THE UNIVERSE, WHY DON'T YOU. MOFFAT *shakes fist* `);
    // open up form entry for anything with class '.editable-detail' ... $('.editable-detail') ... then use new route called update?
    // OR... redirect to review_item page and AUTOFILL using $('.editable-detail') stuff and add a conditional to the add_item route to update instead
})


//* When user clicks close button, close the expanded details (both collection and item)

$('.close-details').on('click', () => {
    $('#collection-details').html('');
    $('#item-details').html('');
})


//--------------------------------------------------------------------//
// *** Collection Management Functions                                //
//--------------------------------------------------------------------//

// When user clicks on a collections div, open up the view_collection part of the page
// ! working... but weird multiplication of post requests happening! related to number of clicks? 2^num_clicks.

$('.collection').on('click', (evt) => {
    // evt.preventDefault();
    // alert(`WHY HELLO THERE... my id is ${evt.target.id}`);
    $('#item-details').html('');
    $.post('/view_collection', {'collection_id': evt.target.id}, (res) => {
        $('#collection-details').html(res);
    })
    console.log('collection details have successfully been displayed on the page');
})


// TODO: add button to toggle public status of each collection.


// TODO: When user clicks "Rename Collection" button, ask for new name and then update that collection's record


//* When user clicks on "Add New Collection" button, ask for a name and then make collection

$('#create-collection').on('click', () => {
    $('#new-collection').html('<form id="new-collection-form"><p>New collection name: <input type="text" id="new-collection-name"></p><p><input type="radio" name="new-collection-public-status" value="True" id="new-collection-public-true" required> Public</p><p><input type="radio" name="new-collection-public-status" value="False" id="new-collection-public-false" required> Private</p><input type="submit" id="submit-new-collection"></form>');

    $('#new-collection-form').on('submit', (evt) => {
        evt.preventDefault();
        let collection_name = $('#new-collection-name').val();
        console.log(`The collection ${collection_name} is being created...`);
        $.post('/create_collection', {'collection_name': collection_name}, (res) => {
            console.log('collection has successfully been added.');
            alert(res);
        })
        $('#new-collection').html('');
        // TODO: show the new collection on the page like with new media item
    })
})


//* When user clicks delete button, delete collection

$('#delete-collection').on('click', () => {
    let id_to_del = $('#delete-collection').val();
    console.log(`here's your value: "${id_to_del}"`);
    // NTH: pop up confirmation before actually deleting
    $.post('/delete_collection', {'collection_id': id_to_del}, (res) => {
        $('#collection-details').html('');
        $(`#collection-display-${id_to_del}`).remove();
        alert(res);
    }); 
})


