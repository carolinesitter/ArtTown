
// ADD A COMMENT FUNCTIONALITY

// Assign variables to symbolize the image id and comment button
let imageId = document.querySelector('#image-id');

if (imageId) {
    imageId = imageId.value;
}

const addCommentButton = document.querySelector(`#add-comment-button-${imageId}`);

// Check if a user has added a comment 
addCommentButton.addEventListener('click', evt => {
    evt.preventDefault();

    const commentInput = evt.target.value;
    const commentsAdded = document.querySelector('#comment').value;

    const formInputs = {
        new_comment : commentsAdded,
    };

    // Get the values from our server and add updated values to the DOM
    fetch(`/user_profile/${imageId}/comments`, {
        method : 'POST',
        body: JSON.stringify(formInputs),
        headers : {
            'Content-Type': 'application/json',
        },
    }) 
    .then(response => response.json())
    .then(responseData => {
            document.querySelector('#added-comments').insertAdjacentHTML('beforeend',
                                `<li>${responseData.username} : ${responseData.comment}</li>`)
    });
});


// LIKE AN IMAGE FUNCTIONALITY 

// Assign variables to symbolize the like button and like count
const likeButton = document.querySelector(`#like-button-${imageId}`);
const likeCount = document.querySelector('#like-count');

// If a user likes, or unlikes an image, update the like count 
likeButton.addEventListener('click', evt =>{
    evt.preventDefault();

    console.log('triggered event')

    // If a user likes an image, add 1 to "like_count" 
    if (likeButton.innerHTML === 'Like'){
        console.log('entered if')
        const url = `/api/user_profile/${imageId}/likes`;
        likeButton.innerHTML = 'Unlike';

        fetch(url) 
        .then(response => response.json())
        .then(responseData => { 
                likeCount.innerHTML = responseData["like_count"];
        });

    // If a user unlikes an image, remove 1 from "like_count"
    }else {
        console.log('entered else')
        const url = `/api/user_profile/${imageId}/remove_likes`;
        likeButton.innerHTML = 'Like';

        fetch(url) 
        .then(response => response.json())
        .then(responseData => { 
            likeCount.innerHTML = responseData["like_count"];
        });
    };

});

