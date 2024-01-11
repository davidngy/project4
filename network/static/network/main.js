document.addEventListener("DOMContentLoaded", function () {
  console.log("DOMContentLoaded event fired"); //debug

  document.querySelectorAll(".like").forEach(function (likeButton) {
    likeButton.addEventListener("click", function (event) {
        const postID = event.target.dataset.postId;
        const likeStatus = event.target.dataset.liked === 'true';
        const data = {
            liked: !likeStatus
        };

        updateLikeButton(postID, data);
    });
});

function updateLikeButton(postID, data) {
    fetch(`/likes/${postID}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(like => {
      console.log('Fetch Response:', like);
        const updatedLikeStatus = like.liked ? "Unlike" : "Like";
        const likeButton = document.querySelector(`.like[data-post-id="${postID}"]`)
        likeButton.textContent = updatedLikeStatus;

        const likeCountElement = document.getElementById(`like-count-${postID}`);
        likeCountElement.textContent = like.likes_count;
    });
}

 
// if u click on edit get the id and the content 
document.querySelectorAll(".edit").forEach(function (editButton) {
  editButton.addEventListener("click", function (event) {
    const postID = event.target.dataset.postId;
    const postContent = event.target.dataset.postContent;

    updateEditButton(postID, postContent);
  });
});
//here the right text area appears and you are able to make changes
function updateEditButton(postID, postContent) {
  // declare right value to each variable
  console.log("content:", postContent);
  const editContainer = document.getElementById(`edit-container-${postID}`);
  let textarea = document.getElementById(`edit-textarea-${postID}`);
  const saveChangesButton = document.getElementById(`saveChangesButton-${postID}`);

  document.getElementById(`post-content-${postID}`).style.display = "none";//none

  fetch(`/textarea/${postID}/`)
    .then(response => response.json())
    .then(content => {
      document.getElementById(`edit-textarea-${postID}`).innerHTML = content.postContent;
      editContainer.style.display = "block";
    });
   // so you can see the textarea

  // Store the original content
  let originalContent = postContent; 
  // Update the textarea value
  textarea.value = originalContent;
  //textarea.value = "";
  // here we handle the changes
  saveChangesButton.addEventListener("click", function () {
    // Check if changes have been made
    const updatedContent = textarea.value;
    saveChanges(postID, updatedContent, editContainer);
    
});
}
//here you save the changes to django
function saveChanges(postID, updatedContent, editContainer) {

  console.log('updatedContentBeChange:', updatedContent);
  document.getElementById(`edit-textarea-${postID}`).innerHTML = updatedContent;
  document.getElementById(`post-content-${postID}`).style.display = "block";
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
  // we send a request to our backend to update the content
  fetch(`/edit/${postID}/`, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
      'post_content': updatedContent
    })
  })
    .then(response => response.json())
    .then(updatedPost => {
      document.getElementById(`post-content-${postID}`).innerHTML = updatedPost.post_content;
      editContainer.style.display = "none";
      console.log('updatedContentEnd:', updatedContent);
      //might update the user interface to reflect the changes
    });
}

});
