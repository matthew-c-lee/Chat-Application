function selectFriend(id) {
    fetch('/select-friend', {
        method: 'POST',
        body: JSON.stringify({id: id})
    }).then((_res) => {
        window.location.href = "/";
    })
}

setInterval(                               //Periodically 
    function()
    {
       $.getJSON(                            //Get some values from the server
          $SCRIPT_ROOT + '/get_values',      // At this URL
          {},                                // With no extra parameters
          function(data)                     // And when you get a response
          {
            $("#result").text(data.result);  // Write the results into the 
                                             // #result element
          });
    },
    500);                                    // And do it every 500ms

// function friendSearch(username) {
//     fetch('/friend-search', {
//         method: 'POST',
//         body: JSON.stringify({username: username})
//     }).then((_res) => {
//         window.location.href = "/search/" + username;
//     })
// }
// function addFriend(id) {
//     fetch('/add-friend', {
//         method: 'POST',
//         body: JSON.stringify({id: id})
//     }).then((_res) => {
//         window.location.href = ""
//     })
// }

function addMember(id, group) {
    fetch('/add-member', {
        method: 'POST',
        body: JSON.stringify({id: id, group: group})
    }).then((_res) => {
        window.location.href = ""
    })
}


function deleteMessage(messageId) {
    fetch('/delete-message', {
        method: 'POST',
        body: JSON.stringify({messageId: messageId})
    }).then((_res) => {
        window.location.href = "";
    })
}

