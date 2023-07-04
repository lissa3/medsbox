const sendAvaUpdate = function(url,avatar) {
    let log = console.log;
    const fd = new FormData();
    fd.append("csrfmiddlewaretoken",getCookie("csrftoken"));
    fd.append('avatar',avatar)
    fetch(url,{
      method:"POST",
      body:fd
      }).then((resp)=>resp.json())
        .then((data)=>{
        log(data);
        if(data.status_code ===200){
              log("data",data.resp);
              log("reloading")
              window.location.reload();
          }
          else if(data.status_code ===404){
            log("code 404; upload failed")
            jsErr.classList.remove("visually-hidden");
            jsErr.textContent = "Failed upload avatar";
            data.err.avatar.forEach((err)=>{
              let div = document.createElement("div")
              div.classList.add("errorlist");
              print("div is ",div)
              div.innerHTML = `${err}`;
              errDiv.appendChild(div)
            });
             throw new Error(message="Custom error: upload failed");
            }
        })
        .catch((err)=>{
          log(err["message"]);
  })
}
