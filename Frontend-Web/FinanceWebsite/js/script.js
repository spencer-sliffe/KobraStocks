function toggleContent(id) {
    var content = document.getElementById(id);
    if (content.classList.contains('show')) {
        content.classList.remove('show');
    } else {
        content.classList.add('show');
    }
}

function submitAnswer(questionId) {
    var textarea = document.getElementById(questionId);
    if (textarea.value.trim() === '') {
        alert('Please provide your thoughts before submitting.');
    } else {
        alert('Thank you for your response!');
        textarea.value = ''; // Clear the textarea after submission
    }
}

function submitPost() {
    var contentArea = document.getElementById('postContent');
    var content = contentArea.value.trim();
    if (content === '') {
        alert('Please write something before posting.');
        return;
    }
    
    var postsSection = document.getElementById('posts');
    var newPost = document.createElement('div');
    newPost.classList.add('post');
    newPost.textContent = content;
    
    postsSection.insertBefore(newPost, postsSection.firstChild.nextSibling);
    
    contentArea.value = '';
}