
// ADD A COMMENT FUNCTIONALITY

// Assign variables to symbolize the image id and comment button
let imageId = document.querySelector('#image').dataset.id;

console.log(imageId);

// if (imageId) {
//     imageId = imageId.value;
// }

const addCommentButton = document.querySelector(`#add-comment-form`);

// Check if a user has added a comment 
addCommentButton.addEventListener('submit', evt => {
    evt.preventDefault();

    const commentInput = evt.target.querySelector("input").value;
    // const commentsAdded = document.querySelector('#comment').value;


    // const formInputs =;

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

            const newCommentDiv = document.createElement('div');
            newCommentDiv.innerHTML = `${responseData.username} : ${responseData.comment}`;

            const deleteButton = document.createElement('button');
            deleteButton.setAttribute("class", "Delete");
            deleteButton.setAttribute("type","button");
            deleteButton.setAttribute("data-comment-id", `${responseData.comment_id}`);
            deleteButton.innerHTML = "Delete";

            deleteButton.addEventListener('click', deleteComment);
            newCommentDiv.appendChild(deleteButton)
            // <button type="button" id="delete-comment-button-${imageId}">Delete</button>`;

            document.querySelector('#user-comments').insertAdjacentElement('beforeend', newCommentDiv)
                            
    });
});

// DELETE A COMMENT FUNCTIONALITY

// Assign a variable to symbolize the delete comment button


function deleteComment (evt) {
    evt.preventDefault();


    // const commentsAdded = evt.target.dataset.comment-id;

    // const formInputs = ;

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



            // document.querySelector('#user-comments').insertAdjacentHTML('beforeend',
            //                     `<div>${responseData.username} : ${responseData.comment}</div>
            //                     <button type="button" id="delete-comment-button-${imageId}">Delete</button>`)
    });
}

for (button of document.querySelectorAll(`.Delete`)) {
    button.addEventListener('click', deleteComment);
}



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

