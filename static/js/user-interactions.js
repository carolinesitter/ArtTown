
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
            document.querySelector('#user-comments').insertAdjacentHTML('beforeend',
                                `<div>${responseData.username} : ${responseData.comment}</div>
                                <button type="button" id="delete-comment-button-${imageId}">Delete</button>`)
    });
});

// DELETE A COMMENT FUNCTIONALITY

// Assign a variable to symbolize the delete comment button
const deleteCommentButton = document.querySelector(`#delete-comment-button-${imageId}`);

deleteCommentButton.addEventListener('click', evt => {
    evt.preventDefault();

    const url = `/api/user_profile/${imageId}/delete_comment`;

    //const commentInput = evt.target.value;
    const commentsAdded = document.querySelector('#comment').value;

    const formInputs = {
        new_comment : commentsAdded,
        };

    // Get the updated comment values from the server and add changes to the DOM
    fetch(url, {
        method : 'POST',
        body: JSON.stringify(formInputs),
        headers : {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseData => {
            document.querySelector('#user-comments').insertAdjacentHTML('beforeend',
                                `<div>${responseData.username} : ${responseData.comment}</div>
                                <button type="button" id="delete-comment-button-${imageId}">Delete</button>`)
    });
});




// LIKE AN IMAGE FUNCTIONALITY 

// Assign variables to symbolize the like button and like count
const likeButton = document.querySelector(`#like-button-${imageId}`);
const likeCount = document.querySelector('#like-count');

// If a user likes, or unlikes an image, update the like count 
likeButton.addEventListener('click', evt =>{
    evt.preventDefault();

    // If a user likes an image, add 1 to "like_count" 
    if (likeButton.innerHTML === 'Like'){
        const url = `/api/user_profile/${imageId}/likes`;
        likeButton.innerHTML = 'Unlike';

        fetch(url) 
        .then(response => response.json())
        .then(responseData => { 
                likeCount.innerHTML = responseData["like_count"];
        });

    // If a user unlikes an image, remove 1 from "like_count"
    }else {
        const url = `/api/user_profile/${imageId}/remove_likes`;
        likeButton.innerHTML = 'Like';

        fetch(url) 
        .then(response => response.json())
        .then(responseData => { 
            likeCount.innerHTML = responseData["like_count"];
        });
    };

});

