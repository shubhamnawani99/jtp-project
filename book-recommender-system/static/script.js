var e = document.getElementById("book-choice");
function show(){
    var value = e.options[e.selectedIndex].id;
    var image_url = e.options[e.selectedIndex].getAttribute('data-img-url');
    document.getElementsByClassName("book-cover")[0].id = value;
    document.getElementsByClassName("book-cover")[0].src = image_url;
}
e.onchange=show;
show();
