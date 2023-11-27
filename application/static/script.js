"use strict";

document.querySelectorAll("#like-btn").forEach(btn => {
    btn.addEventListener("click", function() {
        const btnIcon = btn.querySelector('i');
        const likeCounter = btn.closest('.post').querySelector('.like-counter');

        btnIcon.classList.toggle('fa-heart');
        btnIcon.classList.toggle('fa-heart-o');
        btnIcon.classList.toggle('liked');

        const xhr = new XMLHttpRequest();
        xhr.open('POST', `${window.location.origin}/like`, true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

        xhr.onload = () => {
            if (xhr.status === 200) {
                // const response = JSON.parse(xhr.responseText);
                // console.log(response.status);

                let currentLikes = parseInt(likeCounter.textContent.match(/\d+/)[0]);

                if (btnIcon.classList.contains('liked')) {
                    currentLikes++;
                } else {
                    currentLikes--;
                }

                if (currentLikes === 1) {
                    likeCounter.textContent = '1 like';
                } else {
                    likeCounter.textContent = `${currentLikes} likes`
                }
            }
        }
        const data = JSON.stringify({ 'postId': this.dataset.postId });
        xhr.send(data);
    });
});

const btn = document.querySelector("#follow-btn");
btn?.addEventListener("click", function() {
    const followerCounter = document.querySelectorAll('.stat-value')[1];

    btn.classList.toggle('followed');
    if (btn.classList.contains('followed')) {
        btn.textContent = 'Following';
    } else {
        btn.textContent = 'Follow';
    }

    const xhr = new XMLHttpRequest();
    xhr.open('POST', `${window.location.origin}/follow`, true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

    xhr.onload = () => {
        if (xhr.status === 200) {
            // const response = JSON.parse(xhr.responseText);
            // console.log(response.status);

            let currentFollowers = parseInt(followerCounter.textContent);

            if (btn.classList.contains('followed')) {
                currentFollowers++;
            } else {
                currentFollowers--;
            }
            
            followerCounter.textContent = currentFollowers;
        }
    }
    const data = JSON.stringify({ 'userId': this.dataset.userId });
    xhr.send(data);
});