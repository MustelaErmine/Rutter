let post_p = document.getElementById('parent_post');
let posts_parent = document.getElementById('articles');
let last_obj = "";

async function update_posts(offset=0) {
    var response = await fetch(api_address("/post/" + post_id));
    var data = await response.json();
    //posts_parent.innerHTML = "";

    post_p.innerHTML = await (await fetch(origin + "/post-card/" + post_id)).text();

    for (var i = 0; i < data.replies.length; i++) {
        var text = await (await fetch(origin + "/post-card/" + data.replies[i])).text();
        posts_parent.innerHTML += text;
        last_obj = data.replies[i];
    }
    return data.length == 10;
}

async function post_page_main() {

var offset = 0;

var cont = await update_posts(offset);
offset += 10;

window.addEventListener('scroll', async function() {
	var element = document.querySelector('#post' + last_obj);
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
}

post_page_main();