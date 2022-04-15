let posts_parent = document.getElementById('articles')
let last_obj = "";

async function update_posts(offset=0) {
    var response = await fetch(api_address("/posts/" + username + '/' + offset));
    var data = await response.json();
    //posts_parent.innerHTML = "";
    for (var i = 0; i < data.posts.length; i++) {
        var text = await (await fetch(origin + "/post-card/" + data.posts[i])).text();
        posts_parent.innerHTML += text;
        last_obj = data.posts[i];
    }
    return data.length == 10;
}

var offset = 0;

var cont = update_posts(offset);
offset += 10;

window.addEventListener('scroll', async function() {
	var element = document.querySelector('#post' + last_obj);
	console.log(last_obj);
	var position = element.getBoundingClientRect();
/*
	// checking whether fully visible
	if(position.top >= 0 && position.bottom <= window.innerHeight) {
		console.log('Element is fully visible in screen');
	}
*/
	// checking for partial visibility
	if(position.top < window.innerHeight && position.bottom >= 0) {
	    if (cont) {
	        cont = await update_posts(offset);
	        offset += 10;
	    }
	}
});

async function save_bio() {
    var text = document.getElementById('bioEdit').value;
    var res = await fetch('/api/user/bio', {method: 'PUT', body: text});
    var body = await res.text();
    if (res.status != 200) {
        console.log(body);
    }
}

async function add_post() {
    var text = document.getElementById('newPost').value;
    if (text.length == 0) return;
    var res = await fetch('/api/post', {method: 'POST', body: '{"text": "' + text + '"}'});
    var body = await res.text();
    if (res.status != 200) {
        console.log(body);
    }
    else {
        window.location.reload();
    }
}