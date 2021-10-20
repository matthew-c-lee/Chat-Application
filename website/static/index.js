function selectFriend(id) {
    fetch('/select-friend', {
        method: 'POST',
        body: JSON.stringify({id: id})
    }).then((_res) => {
        window.location.href = "/";
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

