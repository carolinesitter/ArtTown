// Get the edit title button and assign it to a variable
const editTitleButton = document.querySelector('#edit-title-btn');

// Create a function that unhides the edit title features
function unhideTitleEdit(evt) {

    // Get the button Id
    const buttonId = evt.target.id;

    // Show the hidden editing features
    if (buttonId){
        document.querySelector('.Title').removeAttribute('hidden');
    };
}

// When the edit button is clicked, show the edit features
editTitleButton.addEventListener('click', unhideTitleEdit);


// Get the edit description button and assign it to a variable
const editDescriptionButton = document.querySelector('#edit-description-btn');

// Create a function that unhides the edit description features
function unhideDescriptionEdit(evt) {
    
    // Get the button Id
    const buttonId = evt.target.id;

    // Show the hidden editing features
    if (buttonId){
        document.querySelector('.Description').removeAttribute('hidden');
    }
}

// When the edit button is clicked, show the edit features 
editDescriptionButton.addEventListener('click', unhideDescriptionEdit);


// Get the edit image title button and assign it to a variable
const editImageTitleButton = document.querySelector('#edit-image-title-btn');

// Create a function that unhides the edit image title button
function unhideImageTitleEdit(evt) {

    // Get the button id
    const buttonId = evt.target.id;

    // Show the hidden editing features
    if (buttonId){
        document.querySelector('.Img-Title').removeAttribute('hidden');
    }
}

// When the edit button is clicked, show the edit features
editImageTitleButton.addEventListener('click', unhideImageTitleEdit);


// Get the cancel post title button and assign it to a variable
const cancelTitleButton = document.querySelector('.Cancel-Title');

// Allow users to cancel editing the post title 
function cancelTitleEdit(evt) {

    // Get the evt Id and assign it to a variable
    const cancelButtonId = evt.target.id

    // Re-hide the editing features
    evt.target.parentElement.setAttribute('hidden', "");
}

cancelTitleButton.addEventListener('click', cancelTitleEdit);