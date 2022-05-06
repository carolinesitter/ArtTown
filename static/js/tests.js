// Test if the like button can toggle back and forth 
describe('Like/Unlike Increase/Decrease', () => {
    beforeEach(setup);

    // Get our like button as well as our like count
    const button = document.querySelector('#like-button');
    let likeCount = document.querySelector('#like-count');

    it ('should test if the like button toggles to "unlike" when clicked', () => {
        button.innerText = 'Log In';
        button.click();
        
        // When clicked, expect the button to say "Unlike",
        // and for the like count to increase by one
        expect(button).htmlContentsToBe('<button id="login-button">Log Out</button>');
        expect(likeCount).htmlContentsToBe('<p id="like-count"> 1 </p>');
    });
        
    it('should test if the unlike button toggles to "like" when clicked again', () => {
        button.innerText = 'Log Out';
        button.click();
        
        // When clicked again, expect the button to say "Like",
        // and for the like count to decrease by one
        expect(button).htmlContentsToBe('<button id="login-button">Log In</button>');
        expect(likeCount).htmlContentsToBe('<p id="like-count"> 1 </p>');
    });
});

