function home() {
    location.href = "/";
}

function lone() {
    location.href = "/guide/1"
}

function ltwo() {
    location.href = "/guide/2"
}

function lthree() {
    location.href  = "/guide/3"
}

function caas() {
    location.href = "/guide/4"
}

function assessments() {
    location.href = "/guide/5"
}

function exams() {
    location.href = "/guide/6"
}

function endorsements() {
    location.href = "/guide/7"
}

function tipsandtricks() {
    location.href = "/guide/8"
}

function rules() {
    location.href = "/guide/9"
}

function faq() {
    location.href = "/guide/10"
}

function forum() {
    location.href = "/forum"
}

function login() {
    location.href = "/login"
}

function signup() {
    location.href = "/signup"
}

function logout() {
    location.href = "/logout"
}

function search() {
    location.href = "/search"
}

function create_post() {
    location.href = "/forum/create_post"
}



function open_share() {
    document.getElementById("share_overlay").style.display = "flex";
    document.getElementById("body").style.overflow = "hidden";
};

function close_share() {
    document.getElementById("share_overlay").style.display = "none";
    document.getElementById("body").style.overflow = "auto";
}

function copy_link() {
    var url = document.getElementById("share_link_box");
    url.select();
    url.setSelectionRange(0, 99999);
    navigator.clipboard.writeText(url.value);
    document.getElementById("share_overlay").style.display = "none";
    document.getElementById("body").style.overflow = "auto";
};