
// ADD A COMMENT FUNCTIONALITY

// Assign variables to symbolize the image id and comment button
let imageId = document.querySelector('#image').dataset.id;

const addCommentButton = document.querySelector(`#add-comment-form`);

// Check if a user has added a comment 
addCommentButton.addEventListener('submit', evt => {
    evt.preventDefault();

    const commentInput = evt.target.querySelector("input").value;

    // Get the values from our server and add updated values to the DOM
    fetch(`/user_profile/${imageId}/comments`, {
        method : 'POST',
        body: JSON.stringify( {
            new_comment : commentInput,
        }),
        headers : {
            'Content-Type': 'application/json',
        },
    }) 
    .then(response => response.json())
    .then(responseData => {

            // Assign a new variable that will create a div element in our HTML 
            // and set the variable to hold username and comment info
            const newCommentDiv = document.createElement('div');
            newCommentDiv.innerHTML = `${responseData.username} : ${responseData.comment}`;

            // Create a delete button and set its attributes to delete the 
            // comment on the browser
            const deleteButton = document.createElement('button');
            deleteButton.setAttribute("class", "Delete");
            deleteButton.setAttribute("type","button");
            deleteButton.setAttribute("data-comment-id", `${responseData.comment_id}`);
            deleteButton.innerHTML = "Delete";

            // When the delete button is clicked, delete the comment
            deleteButton.addEventListener('click', deleteComment);

            // Ensure that the comment button is added to each div 
            // where the user who left the comment is in session
            newCommentDiv.appendChild(deleteButton);

            // Add the value of the new div to the user comments section 
            document.querySelector('#user-comments').insertAdjacentElement('beforeend', newCommentDiv)
                            
    });
});

// DELETE A COMMENT FUNCTIONALITY

// Assign a variable to symbolize the delete comment button


function deleteComment (evt) {
    evt.preventDefault();


    // Get the updated comment values from the server and add changes to the DOM
    fetch(`/api/user_profile/${imageId}/delete_comment`, {
        method : 'POST',
        body: JSON.stringify({
            comment_id : evt.target.dataset.commentId,
            }),
        headers : {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(responseData => {
            if (responseData["status"] === "OK"){                
                evt.target.parentElement.remove()
                console.log("OK");
            }
    });
}

// For each delete button on the page, if it is clicked, delete the comment
for (button of document.querySelectorAll(`.Delete`)) {
    button.addEventListener('click', deleteComment);
};



// LIKE AN IMAGE FUNCTIONALITY 

// Assign variables to symbolize the like button and like count
const likeButton = document.querySelector('#like-button');
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

