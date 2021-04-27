console.log('helloooo');


//* When user clicks close button, 
//    close the expanded details (both collection and item)

$('.close-details').on('click', () => {
    $('#item-details').html('');
    $('#collection-details').html('');
    });