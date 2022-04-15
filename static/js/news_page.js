let posts_parent = document.getElementById('articles')
let last_obj = "";

async function update_posts(offset=0) {
    var response = await fetch(api_address("/posts/news/" + offset));
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