document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(".like-button").forEach(button => {
        button.addEventListener('click', (event) => likePost(event));
        const postId = button.closest('form').querySelector('input[name="post_id"]').value;
        fetch(`/get-liked-state/${postId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    button.style.backgroundColor = '#FF4500'; 
                } else {
                    button.style.backgroundColor = ''; 
                }
            })
            .catch(error => console.error('Error fetching liked state:', error));
    });

    function likePost(event) {
        event.preventDefault();  
        console.log("Like button clicked");

        const postId = event.target.closest('form').querySelector('input[name="post_id"]').value;
        const csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const likeButton = event.target;

        fetch(`/like/${postId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token 
            },
            body: JSON.stringify({
                post_id: postId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.log(data.message);  
                likeButton.innerText = `❤️ ${data.likes}`;       
                if (data.liked) {
                    likeButton.style.backgroundColor = '#FF4500'; 
                } else {
                    likeButton.style.backgroundColor = ''; 
                }
            }
        })
        .catch(error => console.error('Error:', error));
    }
});