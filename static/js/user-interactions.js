
// ADD A COMMENT FUNCTIONALITY
const imageId = document.querySelector('#image-id').value;
const addCommentButton = document.querySelector(`#add-comment-button-${imageId}`);

console.log(imageId);
console.log(addCommentButton);

addCommentButton.addEventListener('click', evt => {
    evt.preventDefault();
    console.log('hello');
    const commentInput = evt.target.value;
    const commentsAdded = document.querySelector('#comment').value;

    const formInputs = {
        new_comment : commentsAdded,
    };

    console.log(commentsAdded);
    console.log(formInputs);

    fetch(`/user_profile/${imageId}/comments`, {
        method : 'POST',
        body: JSON.stringify(formInputs),
        headers : {
            'Content-Type': 'application/json',
        },
    }) 
    .then(response => response.json())
    .then(responseData => {
            document.querySelector('#added-comments').insertAdjacentHTML('beforeend', `<li>${responseData.comment}</li>`)
    });
});