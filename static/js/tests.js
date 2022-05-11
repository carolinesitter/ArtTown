// Test if the like button can toggle back and forth 
describe('Like/Unlike Increase/Decrease', () => {
    beforeEach(setup);

    // Get our like button as well as our like count
    const button = document.querySelector('#like-button');
    let likeCount = document.querySelector('#like-count');

    it ('should test if the like button toggles to "unlike" when clicked', () => {
        button.innerText = 'Like';
        button.click();
        
        // When clicked, expect the button to say "Unlike",
        // and for the like count to increase by one
        expect(button).htmlContentsToBe('<button id="like-button">Unlike</button>');
        expect(likeCount).htmlContentsToBe('<p id="like-count">1</p>');
    });
        
    it('should test if the unlike button toggles to "like" when clicked again', () => {
        button.innerText = 'Unlike';
        button.click();
        
        // When clicked again, expect the button to say "Like",
        // and for the like count to decrease by one
        expect(button).htmlContentsToBe('<button id="like-button">Like</button>');
        expect(likeCount).htmlContentsToBe('<p id="like-count">0</p>');
    });
});

// Test that a user can add a comment to an image
// describe('Add a comment', () => {

//     const button = document.querySelector('#add-comment-form');

//     button.click();

//     expect(butt)
// })


// Test that a user can delete a comment
describe('Delete a comment', () => {

    // Get the delete button as well as the comment to be deleted
    const button = document.getElementsByClassName('.Delete');
    let comment = document.getElementsByClassName('.Comment');

    // Click the delete button
    button.click();

    // Expect the comment to be gone 
    expect(comment.text).toBe('');
})


// // Test that a user can edit a comment
// describe('Edit a comment', () => {

//     const button = document.getElementsByClassName('.Save')

// })