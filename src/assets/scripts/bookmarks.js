import { getCookie } from "./utils";
// bookmarks
const jsBox = document.getElementById("jsBox");
const bmarkDiv = document.getElementById("bmarkDiv");
const formBook = document.querySelector("#bookmark");
if(bmarkDiv){
const fd = new FormData();
fd.append("csrfmiddlewaretoken",getCookie("csrftoken"))
formBook.addEventListener("submit",(e)=>{
  e.preventDefault();
  const url = formBook.getAttribute("action");
  fd.append("post_uuid",formBook.post_uuid.value),
  fd.append("user_id",formBook.user_id.value)

  fetch(url,{
    method:"POST",
    headers:{ "x-requested-with": "XMLHttpRequest"},
    body:fd
    }).then((resp)=>resp.json())
      .then((data)=>{
        if(data.status_code ===200){
          let msg = data.msg;
          jsBox.classList.add("green","slide");
          jsBox.textContent=  msg;
          if(data.del_button){
            bmarkDiv.remove();
          }
        }
        else if(data.status_code ===404){
          //  add error flash msg
            jsBox.classList.add("red","slide");
            jsBox.textContent= "Failed to add to bookmarks";
           throw new Error(message="Failed to add to bookmarks");
          }
      })
      .catch((err)=>{
        console.log(err["message"]);
      })
})
}
