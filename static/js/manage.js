"use strict";

// When user clicks on a cover, open up the view_item part of the page
//      allow user to add item to a collection
// TODO: when item is added to collection, it does not rerender template, so need to add manually!
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
                $('#coll-submit-button').on('click', (evt) => {
                    let postData = {'user_item_id': $('#add-to-collection').val(), 
                                    'collection_id': $('input[type="radio"]:checked').val()}
                    $.post('/add_item_to_collection', postData, (res2) => {
                        alert(res2);
                    })    
                });
            });
    
        });
    });
});



// When user clicks delete button, remove association between item and user (UserMedia object)
// TODO: Delete is successful, but it doesn't rerender the template. remove that item cover from the page on the JS side!
$('#delete-from-library').on('click', () => {
    let id_to_del = $('#delete-from-library').val();
    console.log(`here's your value: "${id_to_del}"`);
    console.log($(`#${id_to_del}`).val()); // ! doesn't work in browser console either... even hardcoding in the id num!
    // NTH: pop up confirmation before actually deleting
    $.post('/delete_item', {'user_media_id': id_to_del}, (res) => {
        $('#item-details').html('');
        alert(res);
        console.log($(`#${id_to_del}`).val()); // ! currently undefined - Want to remove image associated with user_media_id for selected item... 
    }); 
})


// TODO: When user clicks edit button, open rating/review/source/collections for editing
$('#edit-details').on('click', () => {
    alert(`JUST REBOOT THE UNIVERSE, WHY DON'T YOU. MOFFAT *shakes fist* `);
    // open up form entry for anything with class '.editable-detail' ... $('.editable-detail') ... then use new route called update?
    // OR... redirect to review_item page and AUTOFILL using $('.editable-detail') stuff and add a conditional to the add_item route to update instead
})


// When user clicks close button, close the expanded details (both collection and item)
$('.close-details').on('click', () => {
    $('#collection-details').html('');
    $('#item-details').html('');
})


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


// When user clicks on add collection button, ask for a name and then make collection
$('#create-collection').on('click', () => {
    $('#new-collection').html('<form id="new-collection-form">New collection name: <input type="text" id="new-collection-name"><input type="submit" id="submit-new-collection"></form>');

    $('#new-collection-form').on('submit', (evt) => {
        evt.preventDefault();
        let collection_name = $('#new-collection-name').val();
        console.log(`The collection ${collection_name} is being created...`);
        $.post('/create_collection', {'collection_name': collection_name}, (res) => {
            console.log('collection has successfully been added.');
            alert(res);
        })
        $('#new-collection').html('');
    })
})


// When user clicks delete button, delete collection
// TODO: Delete is successful, but it doesn't rerender the template. remove that collection from the page on the JS side!
$('#delete-collection').on('click', () => {
    let id_to_del = $('#delete-collection').val();
    console.log(`here's your value: "${id_to_del}"`);
    // NTH: pop up confirmation before actually deleting
    $.post('/delete_collection', {'collection_id': id_to_del}, (res) => {
        $('#collection-details').html('');
        alert(res);
    }); 
})


