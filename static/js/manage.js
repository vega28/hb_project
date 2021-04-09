"use strict";

$('.user-media-id').on('click', (evt) => {
    evt.preventDefault();
    alert(`WHY HELLO THERE... my id is ${evt.target.id}`);
})