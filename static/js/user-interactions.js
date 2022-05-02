
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
            newCommentDiv.setAttribute("data-comment-id", `${responseData.comment_id}`);
            newCommentDiv.setAttribute("class", "Comment");
            newCommentDiv.innerHTML = `${responseData.username}`;
            
            const commentParagraph = document.createElement('p');
            commentParagraph.setAttribute("id", `para-comment-${responseData.comment_id}`);
            commentParagraph.innerHTML = `${responseData.comment}`;

            newCommentDiv.appendChild(commentParagraph);

            // Create a div for edited comments
            const editCommentDiv = document.createElement('div');
            editCommentDiv.setAttribute("id", `hidden-comment-${responseData.comment_id}`);
            editCommentDiv.setAttribute("hidden", true);

            const input = document.createElement('input');
            input.setAttribute("value", `${responseData.comment}`);

            editCommentDiv.appendChild(input);
            
            const saveButton = document.createElement('button');
            saveButton.setAttribute("class", "Save");
            saveButton.setAttribute("type", "button");
            saveButton.setAttribute("id", `save-id-${responseData.comment_id}`);
            saveButton.innerHTML = 'Save';

            editCommentDiv.appendChild(saveButton);

            saveButton.addEventListener('click', saveCommentEdit);

            const cancelButton = document.createElement('button');
            cancelButton.setAttribute("class", "Cancel");
            cancelButton.setAttribute("type", "button");
            cancelButton.setAttribute("id", `cancel-id-${responseData.comment_id}`);
            cancelButton.innerHTML = 'Cancel';

            editCommentDiv.appendChild(cancelButton);

            cancelButton.addEventListener('click', cancelCommentEdit);

            // Create a delete button and set its attributes to delete the 
            // comment on the browser
            const deleteButton = document.createElement('button');
            deleteButton.setAttribute("class", "Delete");
            deleteButton.setAttribute("type","button");
            deleteButton.innerHTML = "Delete";

            // When the delete button is clicked, delete the comment
            deleteButton.addEventListener('click', deleteComment);

            // Create an edit button and set its attributes to edit
            // the comment on the browser
            const editButton = document.createElement('button');
            editButton.setAttribute("class", "Hidden");
            editButton.setAttribute("type", "button");
            editButton.setAttribute("id", `button-id-${responseData.comment_id}`);
            editButton.innerHTML = "Edit";

            // When the edit button is clicked, edit the comment
            editButton.addEventListener('click', unhideEdit);

            // Ensure that the delete button is rendered for each 
            // comment that the logged in user made
            newCommentDiv.appendChild(editButton);

            newCommentDiv.appendChild(editCommentDiv);

            // Ensure that the delete button is added to each div 
            // where the user who left the comment is in session
            newCommentDiv.appendChild(deleteButton);


            // Add the value of the new div to the user comments section 
            document.querySelector('#user-comments').insertAdjacentElement('beforeend', newCommentDiv)
                            
    });
});

//addCommentButton.addEventListener('submit', createComment);

// DELETE A COMMENT FUNCTIONALITY

// Assign a variable to symbolize the delete comment button


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

// Unhide the edit div in image_details
function unhideEdit (evt) {

    console.log('evt target id: ', evt.target.id) //button

    const buttonInfo = evt.target.id;
    const buttonIdArray = buttonInfo.split('-');
    const buttonId = buttonIdArray[2];

    console.log(document.querySelector(`#hidden-comment-${buttonId}`));
    if (buttonId) {
    document.querySelector(`#hidden-comment-${buttonId}`).removeAttribute("hidden");
    //console.log(document.querySelector(`#hidden-comment-${buttonId}`));
    };
}

// Save the edited comment and update the web page 
function saveCommentEdit(evt) {
    evt.preventDefault();

    console.log('EVT TARGET:' ,  evt.target);

    const commentButtonInfo = evt.target.id;
    const commentButtonArray = commentButtonInfo.split('-');
    const commentButtonId = commentButtonArray[2];
    //console.log('ENTERED SAVECOMMENTEDIT: ', commentButtonId);

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

    const cancelButtonInfo = evt.target.id;
    const cancelButtonArray = cancelButtonInfo.split('-');
    const cancelButtonId = cancelButtonArray[2];

    // Hide the edit box by setting the parent div to hidden
    document.querySelector(`#hidden-comment-${cancelButtonId}`).setAttribute("hidden", "");
}





// // LIKE AN IMAGE FUNCTIONALITY 

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
    }

})