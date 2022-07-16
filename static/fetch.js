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

function createUsersList(users){
      const user = users
       const curr_main = document.querySelector("main");
         const section = document.createElement('section');
         section.innerHTML = `
        <br>
         <img src="${user.avatar}" alt="Profile Picture"/>
         <div>
            <span>${user.first_name} ${user.last_name}</span>
               console.log(users)
            <br>
            <br>
             <a href="mailto:${user.email}">Send Email</a>
        </div>
        <br>
        <br>
        `;
         curr_main.appendChild(section);
}


