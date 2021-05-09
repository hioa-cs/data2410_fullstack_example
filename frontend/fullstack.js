
console.log("Fullstack frontend loaded");

var users = []
var logged_in = null
var h_row1 = null

var copter_img = "https://www.puppentoys.com/WebRoot/ce_es/Shops/940395445/5320/45C4/8DBF/84BC/3270/C0A8/8010/C606/A5935-2.jpg"
var nocopter_img = "http://www.skyblue-pink.com/wp-content/uploads/2013/08/sadbatman.jpg"

function load_copter(){
    row = this.parentElement.parentElement;
    user_id = row.id;
    user = users[user_id];
    console.log(`Loading copter for user ${user_id}`)
    copter = Boolean(user[3]);
    var h_img = row.querySelector(".card-image");
    h_img.src = copter ? copter_img : nocopter_img;
}

function remove_users(){
    var h_list = document.getElementById("user_list");
    var rows = h_list.querySelectorAll(".row");
    console.log(`Removign users: ${rows}`);
    rows.forEach(node => {
        console.log(`removing row ${node.id}`);
        node.remove();
    });
}

function render_users(data){
    console.log(`Rendering ${data}`)

    var h_list = document.getElementById("user_list");
    if (h_row1 == null) {
        h_row1 = document.getElementById("first_row");
    }
    console.log(`My DOM list: ${h_list}`)
    console.log(`data length: ${data.length} data: ${data}`)

    for (var i = 0; i < data.length; i++){
        console.log(`Rendering element ${data[i]}\n\n`);

        // NOTE: This is very brittle - objects with named keys are better
        [id, n, email, copter, access, img] = data[i];

        /*  Add information from the google profile if this is
            the logged in user */
        if (logged_in && email == logged_in.getEmail()){
            n = logged_in.getName();
            img = logged_in.getImageUrl();
            // Google has a nice API for resizing images
            // from https://developers.google.com/people/image-sizing
            img = img.split("=")[0]+"=s300";
        }

        console.log(`Image: ${img}`)

        var cloned_row = h_row1.cloneNode(true);
        cloned_row.id = i;

        var h_title = cloned_row.querySelector(".card-title");
        h_title.innerHTML =  id.toString() + ". Name: " + n;

        var h_img = cloned_row.querySelector(".card-image");
        h_img.src = img

        var h_btn = cloned_row.querySelector(".btn");
        h_btn.onclick = load_copter;
        console.log(`Added onclick`)
        console.log(`ID: ${id}, Name: ${n}, Copter? ${Boolean(copter)}`);

        if(logged_in && logged_in.getEmail() == email){
            h_list.insertBefore(cloned_row, h_list.querySelector(".row"))
        } else {
            h_list.appendChild(cloned_row);
        }

    }
    h_row1.remove();
}

function load_users(){
    users = []
    fetch("./api/users")
        .then(response => response.json())
        .then(data => {
            users = data;

            if (h_row1 != null){
                remove_users();
            }
            render_users(data)
        });

    console.log("Fetch in progress");
}

load_users();

// Google sign-on
console.log("Signin javascript loading");

var id_token = null;

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

    id_token = googleUser.getAuthResponse().id_token;
    console.log(`ID Token to pass to server: ${id_token}`)

    logged_in = profile;

    // Render again to get the logged in users card
    // updated from the google profile
    remove_users();
    render_users(users);
}

console.log("Adding signOut function");
function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
      logged_in = null;
      remove_users();
      load_users();
    });
    id_token = null;
}


function danger_return(data){
    console.log("Authenticated request returned");
    console.log(data);
    remove_users();
    render_users(data);
}

function danger(){
    console.log("Danger!");
    if (id_token == null) {
        alert("ILLEGAL ACCESS ATTEMPT REGISTERED");
        return;
    }

    fetch("./api/users", {
        headers: {
            'Authorization' : id_token
        }
    }).then(response => response.json())
    .then(data => danger_return(data));

}

