
// ADD A COMMENT FUNCTIONALITY

const addCommentButton = document.querySelector('#comment');
// const imageId = 

addCommentButton.addEventListener('submit', evt => {
    evt.preventDefault();

    const commentInput = evt.target.value;
    const commentsAdded = document.querySelector('#added-comments');

    const formInputs = {
        comment : commentInput,
        new_comment : commentsAdded,
    };

    fetch(`/user_profile/${image_id}/comments`, {
        method : 'POST',
        body: JSON.stringify(formInputs),
        headers : {
            'Content-Type': 'application/json',
        },
    }) 
    .then(response => response.json())
    .then(responseData => {
        addCommentButton.addEventListener('click', () => {
            commentsAdded.insertAdjacentHTML('beforeend', `<li>Comments</li>`)
        })
    });
});