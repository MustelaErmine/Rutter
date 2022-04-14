
    let origin = window.location.origin;
    let api_prefix = '/api'
    let username = "{{username}}";

    api_address = function (address) { return origin + api_prefix + address; }

    async function replyToPost(post_id) {
        var text = document.getElementById('textarea' + post_id).value;
        if (text.length == 0)
        {
            return;
        }
        var response = await fetch(api_address("/post"),{method: 'POST', body: JSON.stringify({
            reply: post_id,
            text: text
        })});
        if (response.status == 200) {
            window.location.replace("/post/" + post_id);
        }
        else {
            console.log(document.status);
        }
    }
