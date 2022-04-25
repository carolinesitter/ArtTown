
// ADD A COMMENT FUNCTIONALITY

document.querySelector('#comment').addEventListener('click', evt => {
    evt.preventDefault();

    const commentInput = document.querySelector('#comment').value;

    console.log(commentInput);
});