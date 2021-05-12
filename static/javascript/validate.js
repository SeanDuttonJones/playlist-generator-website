var success = window.location.href.search("access_token");
if(success != -1) {
    var start = window.location.href.search('=') + 1; // +1 to exclude the '=' from the start
    var end = window.location.href.search('&');
    var access_token = window.location.href.substring(start, end);

    localStorage.setItem("access_token", access_token);
} else {
    localStorage.setItem("access_token", "error");
}

window.close();