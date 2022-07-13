function myFunction() {
    let num =  document.getElementById("loll").value
    fetch(`https://reqres.in/api/users/${num}`).then(
        response => response.json()
    ).then(
        responseOBJECT => createUsersList(responseOBJECT.data)
    ).catch(
        err => console.log(err)
    );
}


function createUsersList(response){
    const user = users
    const currMain = document.querySelector("main")
    const section = document.createElement('section')
    section.innerHTML = `
            <img src="${user.avatar}" alt="Profile Picture"/>
            <div>
                <span>${user.name} ${user.last_name}</span>
                <br>
                <a href="mailto:${user.email}">Send Email</a>
            </div>
    `
    currMain.appendChild(section)
}

