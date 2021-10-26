function selectFriend(id) {
    fetch('/select-friend', {
        method: 'POST',
        body: JSON.stringify({id: id})
    }).then((_res) => {
        window.location.href = "/";
    })
}

// function friendSearch(username) {
//     fetch('/friend-search', {
//         method: 'POST',
//         body: JSON.stringify({username: username})
//     }).then((_res) => {
//         window.location.href = "/search/" + username;
//     })
// }
function addFriend(id) {
    fetch('/add-friend', {
        method: 'POST',
        body: JSON.stringify({id: id})
    }).then((_res) => {
        window.location.href = ""
    })
}


function deleteMessage(messageId) {
    fetch('/delete-message', {
        method: 'POST',
        body: JSON.stringify({messageId: messageId})
    }).then((_res) => {
        window.location.href = "/";
    })
}

