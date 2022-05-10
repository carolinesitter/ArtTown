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
const editImageTitleButtons = document.querySelectorAll('.Edit');

// Create a function that unhides the edit image title button
function unhideImageTitleEdit(evt) {

    // Get the button id
    const buttonInfo = evt.target.id;
    const buttonArray = buttonInfo.split('-');
    const imageId = buttonArray[4];


    // Show the hidden editing features
    if (imageId){
        document.querySelector(`#img-title-${imageId}`).removeAttribute('hidden');
    }
}

// When the edit button is clicked, show the edit features
for (button of editImageTitleButtons){
    button.addEventListener('click', unhideImageTitleEdit);
}


// Get the cancel post title button and assign it to a variable
const cancelTitleButton = document.querySelector('.Cancel-Title');

// Allow users to cancel editing the post title 
function cancelTitleEdit(evt) {

    // Get the evt Id and assign it to a variable
    const cancelButtonId = evt.target.id

    // Re-hide the editing features
    evt.target.parentElement.setAttribute('hidden', "");
}

// When the cancel button is clicked, hide the editing features
cancelTitleButton.addEventListener('click', cancelTitleEdit);


// Get the cancel description edit button and assign it to a variable
const cancelDescriptionButton = document.querySelector('.Cancel-Desc');

// Allow users to cancel editing their post description
function cancelDescriptionEdit(evt) {

    // Get the evt Id and assign it to a variable
    const cancelButtonId = evt.target.id

    // Re-hide the editing features
    evt.target.parentElement.setAttribute('hidden', "");
}

// When the cancel button is clicked, hide the editing features
cancelDescriptionButton.addEventListener('click', cancelDescriptionEdit);


// Get the cancel image title edit button and assign it to a variable
const cancelImageTitleButton = document.querySelectorAll('.Cancel-Img-Title');

// Allow users to cancel editing their image title
function cancelImageTitleEdit(evt) {

    // Get the evt Id and assign it to a variable
    const cancelButton = evt.target.id

    // Re-hide the editing features
    evt.target.parentElement.setAttribute("hidden", "");
}

// When the cancel button is clicked, hide the editing features
for (button of cancelImageTitleButton){
    button.addEventListener('click', cancelImageTitleEdit);
}



// Get the save title edit button and assign it to a variable
const saveTitleButton = document.querySelector('.Save-Title');

// Allow users to save their edited post title
function saveEditedTitle(evt){

    // Parse through the event target to get the artist collection ID
    const eventTargetInfo = evt.target.id;
    const eventTargetArray = eventTargetInfo.split('-');
    const artistCollectionId = eventTargetArray[2];

    fetch(`/user_profile/edit/${artistCollectionId}/post_title`, {
        method: 'POST',
        body: JSON.stringify({
            gallery_title_text : evt.target.parentElement.querySelector('input').value,
        }),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then (response => response.json())
    .then(responseData => {
        if (responseData["status"] === "OK"){
            evt.target.parentElement.querySelector('input').value = responseData["gallery_title"];
            document.querySelector('#art-collection-title').innerHTML = responseData["gallery_title"];
            evt.target.parentElement.setAttribute("hidden", "");
        }
    })
}

// When the save button is clicked, save the edited post title
saveTitleButton.addEventListener('click', saveEditedTitle);


// Get the save description edit button and assign it to a variable
const saveDescriptionButton = document.querySelector('.Save-Desc');

// Allow users to save their edited description
function saveEditedDescription(evt){

    // Parse through evt target to get the artistCollectionId
    const eventTargetInfo = evt.target.id;
    const eventTargetArray = eventTargetInfo.split('-');
    const artistCollectionId = eventTargetArray[2];

    fetch(`/user_profile/edit/${artistCollectionId}/desc`,{
        method: 'POST',
        body: JSON.stringify({
            gallery_description_text : evt.target.parentElement.querySelector('input').value,
        }),
        headers: { 
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(responseData => {
        if (responseData["status"] === "OK"){
            evt.target.parentElement.querySelector('input').value = responseData["gallery_description"];
            document.querySelector('#art-collection-description').innerHTML = responseData["gallery_description"];
            evt.target.parentElement.setAttribute("hidden", "");
        }
    })
}

// When the save button is clicked, save the updated gallery description
saveDescriptionButton.addEventListener('click', saveEditedDescription);


// Get the save edited image title button and assign it to a variable
const saveImageTitleButton = document.querySelectorAll('.Save-Img-Title');

// Allow users to save their edited image title
function saveEditedImageTitle(evt) {

    // Parse through the evt target to find the ArtistCollectionId
    const eventTargetInfo = evt.target.id;
    const eventTargetArray = eventTargetInfo.split('-');
    const artistCollectionId = eventTargetArray[2];
    const imageId = eventTargetArray[3]


    fetch(`/user_profile/edit/${artistCollectionId}/img_title`,{
        method: 'POST',
        body: JSON.stringify({
            image_id: document.querySelector('#image').dataset.id,
            image_title_text : evt.target.parentElement.querySelector('input').value,
        }),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(responseData => {
        if (responseData["status"] === "OK"){
            evt.target.parentElement.querySelector('input').value = responseData["image_title"];
            console.log(responseData);
            document.querySelector(`#para-img-title-${imageId}`).innerHTML = responseData["image_title"];
            //evt.target.parentElement.parentElement.querySelector('p').innerHTML = responseData["image_title"];
            evt.target.parentElement.setAttribute("hidden", "");
        }
    })
}

// When the save button is clicked, save the edited image title
for (button of saveImageTitleButton){
    button.addEventListener('click', saveEditedImageTitle);
}