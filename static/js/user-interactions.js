// Assign variables to symbolize the image id and comment button
let imageId = document.querySelector('#image').dataset.id;
const addCommentButton = document.querySelector(`#add-comment-form`);

// Allow the user to create a new comment
function createComment (evt) {
    evt.preventDefault();

    // Get the comment the user created on the browser
    const commentInput = evt.target.querySelector('input').value;

    // Get the values from our server and add updated values to the DOM
    fetch(`/api/user_profile/${imageId}/comments`, {
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
            // for our new comments
            const newCommentDiv = document.createElement('div');
            newCommentDiv.setAttribute("data-comment-id", `${responseData.comment_id}`);
            newCommentDiv.setAttribute("class", "Comment");
            newCommentDiv.innerHTML = `${responseData.username}:`;
            
            // Create the paragraph div in our HTML that holds the new comment
            const commentParagraph = document.createElement('p');
            commentParagraph.setAttribute("id", `para-comment-${responseData.comment_id}`);
            commentParagraph.innerHTML = `${responseData.comment}`;

            // Append the paragraph to the new comment div
            newCommentDiv.appendChild(commentParagraph);

            // Create a div for edited comments
            const editCommentDiv = document.createElement('div');
            editCommentDiv.setAttribute("id", `hidden-comment-${responseData.comment_id}`);
            editCommentDiv.setAttribute("hidden", true);

            // Create a div to take the input value for the edited comment
            const input = document.createElement('input');
            input.setAttribute("value", `${responseData.comment}`);

            // Append the input to the edited comments div
            editCommentDiv.appendChild(input);
            
            // Create a save button in our HTML
            const saveButton = document.createElement('button');
            saveButton.classList.add("Save");
            saveButton.classList.add("btn-outline-success");
            saveButton.setAttribute("type", "button");
            saveButton.setAttribute("id", `save-id-${responseData.comment_id}`);
            saveButton.innerHTML = 'Save';

            // Add the save button to the edited comments div
            editCommentDiv.appendChild(saveButton);

            // When clicked, ensure that the edited comment is saved
            saveButton.addEventListener('click', saveCommentEdit);

            // Create a cancel edits button in our HTML
            const cancelButton = document.createElement('button');
            cancelButton.classList.add("Cancel"); 
            cancelButton.classList.add("btn-outline-dark");
            cancelButton.setAttribute("type", "button");
            cancelButton.setAttribute("id", `cancel-id-${responseData.comment_id}`);
            cancelButton.innerHTML = 'Cancel';

            // Append the cancel button to our edit comments div
            editCommentDiv.appendChild(cancelButton);

            // When clicked, ensure that the option to edit a comment disappears,
            // and that the original comment itself is not changed in any way
            cancelButton.addEventListener('click', cancelCommentEdit);

            // Create a delete button and set its attributes to delete the 
            // comment on the browser
            const deleteButton = document.createElement('button');
            deleteButton.classList.add("Delete");
            deleteButton.classList.add("btn-outline-danger");
            deleteButton.setAttribute("type","button");
            deleteButton.innerHTML = "Delete";

            // When the delete button is clicked, delete the comment
            deleteButton.addEventListener('click', deleteComment);

            // Create an edit button and set its attributes to edit
            // the comment on the browser
            const editButton = document.createElement('button');
            editButton.classList.add("Hidden");
            editButton.classList.add("btn-outline-dark");
            editButton.setAttribute("type", "button");
            editButton.setAttribute("id", `button-id-${responseData.comment_id}`);
            editButton.innerHTML = "Edit";

            // When the edit button is clicked, edit the comment
            editButton.addEventListener('click', unhideEdit);

            // Ensure that the edit button is rendered for each 
            // comment that the logged in user made
            newCommentDiv.appendChild(editButton);

            // Add the edited comment div as a sub-div to the new comment div
            newCommentDiv.appendChild(editCommentDiv);

            // Ensure that the delete button is added to each div 
            // where the user who left the comment is in session
            newCommentDiv.appendChild(deleteButton);


            // Add the value of the new div to the user comments section 
            document.querySelector('#user-comments').insertAdjacentElement('afterbegin', newCommentDiv);
                            
    });
};

// When the post button is clicked, create a comment
addCommentButton.addEventListener('submit', createComment);


// Allow the user to delete their comment
function deleteComment (evt) {
    evt.preventDefault();


    // Get the updated comment values from the server and add changes to the DOM
    fetch(`/api/user_profile/${imageId}/delete_comment`, {
        method : 'POST',
        body: JSON.stringify({
            comment_id : evt.target.parentElement.dataset.commentId,
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

// For each comment the user makes, give them the option to edit or delete
for (button of document.querySelectorAll(`.Comment`)) {
    button.querySelector('.Delete').addEventListener('click', deleteComment);
    button.querySelector('.Hidden').addEventListener('click', unhideEdit);
    button.querySelector('.Save').addEventListener('click', saveCommentEdit);
    button.querySelector('.Cancel').addEventListener('click', cancelCommentEdit);
};

// If the user decides to edit a comment, allow them to edit
// by opening up the comment div
function unhideEdit (evt) {

    // Get the edit button id by splitting the event id object
    const buttonInfo = evt.target.id;
    const buttonIdArray = buttonInfo.split('-');
    const buttonId = buttonIdArray[2];

    // Remove the hidden attribute in the comment div so that users can
    // interact with their comment
    if (buttonId) {
    document.querySelector(`#hidden-comment-${buttonId}`).removeAttribute("hidden");
    };
}

// Save the user's edited comment and update the web page accordingly
function saveCommentEdit(evt) {
    evt.preventDefault();

    // Get the save button id by splitting the target event id object
    const commentButtonInfo = evt.target.id;
    const commentButtonArray = commentButtonInfo.split('-');
    const commentButtonId = commentButtonArray[2];

    // Pass the updated comment information to the server and update the database
    fetch(`/api/user_profile/${imageId}/edit_comments`, {
        method: 'POST',
        body: JSON.stringify({
            comment_id : evt.target.parentElement.parentElement.dataset.commentId,
            comment_text : evt.target.parentElement.querySelector('input').value,
        }),
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json()) 
    .then (responseData => {
            if (responseData["status"] === "OK"){
                evt.target.parentElement.querySelector('input').value = responseData["comment"];
                document.querySelector(`#para-comment-${commentButtonId}`).innerHTML = responseData["comment"];
                evt.target.parentElement.setAttribute("hidden", "");
            }
            console.log(responseData);
    });    
    
}

// Allow the user to cancel making changes to their comment
function cancelCommentEdit (evt) {

    // Extract the cancel button's id from the event object
    const cancelButtonInfo = evt.target.id;
    const cancelButtonArray = cancelButtonInfo.split('-');
    const cancelButtonId = cancelButtonArray[2];

    // Hide the edit box by setting the parent div to hidden
    document.querySelector(`#hidden-comment-${cancelButtonId}`).setAttribute("hidden", "");
}

// Assign variables to symbolize the like button and like count
const likeButton = document.querySelector('#like-button');
const likeCount = document.querySelector('#like-count');

// If a user likes, or unlikes an image, update the like count 
function likeAnImage (evt){
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

    // If a user unlikes an image, subtract 1 from "like_count"
    }else {
        const url = `/api/user_profile/${imageId}/remove_likes`;
        likeButton.innerHTML = 'Like';

        fetch(url) 
        .then(response => response.json())
        .then(responseData => { 
            likeCount.innerHTML = responseData["like_count"];
        });
    }

};

// When the like button is clicked/unclicked, call the function to like
// or unlike an image
likeButton.addEventListener('click', likeAnImage);