import { getCookie } from "./utils";
const sendAvaUpdate = function(url,avatar) {
    const fd = new FormData();
      fd.append("csrfmiddlewaretoken",getCookie("csrftoken"));
      fd.append('avatar',avatar)
      fetch(url,{
        method:"POST",
        headers:{ "x-requested-with": "XMLHttpRequest"},
        body:fd
        }).then((resp)=>resp.json())
          .then((data)=>{
            if(data.status_code ===200){
              setTimeout(
                window.location.reload(),3000
              )
            }
            else if(data.status_code ===404){
              jsErr.classList.remove("visually-hidden");
              jsErr.textContent = "Failed upload avatar";
              data.err.avatar.forEach((err)=>{
                let div = document.createElement("div")
                div.classList.add("errorlist");
                div.innerHTML = `${err}`;
                errDiv.appendChild(div)
              });
               throw new Error(message="Custom error: upload failed");
              }
          })
          .catch((err)=>{
            console.log(err["message"]);
    })
  }

  export {sendAvaUpdate}
