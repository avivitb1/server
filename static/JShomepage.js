   
     function ButtonFunction() {
      var txt;
      if (confirm("תאשרו שאתם מעל גיל 16")) {
        txt = "You pressed OK!";
      } else {
        txt = "You pressed Cancel!";
      }
      document.getElementById("demo").innerHTML = txt;
    }
    
      window.onload = function(){

        const homepage = window.location.pathname;
        console.log(homepage);
        
         document.querySelectorAll('a').forEach(link => {    
          if(link.href.includes(`${homepage}`)){
            link.classList.add('markURL');
          }
        });
        
        }
        
    