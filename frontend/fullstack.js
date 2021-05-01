
console.log("Fullstack frontend loaded");

var images = [
    "https://static.wikia.nocookie.net/mlp/images/b/b2/Pinkie_Pie_ID_S4E11.png",
    "https://media.karousell.com/media/photos/products/2017/02/02/lego_batman_lobster_figure_1486041715_4eed985e.jpg",
    "https://static.dw.com/image/18463014_303.jpg",
    "https://static.wikia.nocookie.net/mlp/images/b/b2/Pinkie_Pie_ID_S4E11.png"
]

var users = []

function load_copter(){
    var copter_img = "https://www.puppentoys.com/WebRoot/ce_es/Shops/940395445/5320/45C4/8DBF/84BC/3270/C0A8/8010/C606/A5935-2.jpg"
    var nocopter_img = "http://www.skyblue-pink.com/wp-content/uploads/2013/08/sadbatman.jpg"
    row = this.parentElement.parentElement;
    copter = Boolean(users[row.id - 1][2]);
    console.log(`Loading copter for ${row.id}. Has ponycopter? ${users[row.id - 1][2]}`);
    var h_img = row.querySelector(".card-image");
    h_img.src = copter ? copter_img : nocopter_img;
}

function render_users(data){
    console.log(`Rendering ${data}`)
    var h_list = document.getElementById("user_list");
    var h_row1 = document.getElementById("first_row");
    console.log(`My DOM list: ${h_list}`)
    for (i in data){
        users[i] = data[i];
        [id, n, copter] = data[i];

        var cloned_row = h_row1.cloneNode(true);
        cloned_row.id = id;

        var h_title = cloned_row.querySelector(".card-title");
        h_title.innerHTML =  id.toString() + ". Name: " + n;
        
        var h_img = cloned_row.querySelector(".card-image");
        h_img.src = images[id - 1];

        var h_btn = cloned_row.querySelector(".btn");
        h_btn.onclick = load_copter;
        console.log(`Added onclick: ${h_btn.onclick}`)

        console.log(`ID: ${id}, Name: ${n}, Copter? ${Boolean(copter)}`);
        h_list.appendChild(cloned_row);

    }
    h_row1.remove();
}

fetch("./api/users")
    .then(response => response.json())
    .then(data => render_users(data));

console.log("Fetch in progress");