let canvas,ctx,avatar,newImgUrl,serverErrMsg;
  const WIDTH = 600;
  const form = document.getElementById("upForm");
  const url = form.getAttribute("action");
  const checkbox = document.querySelector("#avatar-clear_id");
  const inp = document.querySelector("#imgInp");
  const butSubmit = document.querySelector("#butSubmit");
  const errDiv = document.querySelector("#errDiv");
  let jsErr = document.querySelector("#jsErr");
  // func to toggle class on inputs
  checkInp(checkbox,inp);

  document.addEventListener("DOMContentLoaded",init);
  function init(){
    canvas = document.createElement("canvas");
    ctx = canvas.getContext('2d');
    form.addEventListener("submit",upload);
  }
  async function upload(e){
    e.preventDefault()
    let file = inp.files[0];
    if(file){
      // file attached
      let userFileName = file.name;
      let initialSize = file.size;
      let humanSize = formatFileSize(file.size);
      let userFileExt = userFileName.split(".").at(-1).toLowerCase();
      console.log("file detected")
      if(!checkExt(userFileExt)){
      // show error msg for 3 sec; clean file input and quit
          jsErr.classList.remove("visually-hidden");
          jsErr.textContent = "Only '.png/.jpeg/.jpg' file's extentions allowed";
          inp.value = null;
          setTimeout(()=>{
              jsErr.classList.add("visually-hidden");
              jsErr.textContent = "";
          },3000)
        return;
      }
      const res = await fileToDataUri(file) // base64 encoded
      if(res){
      // console.log("res is",res)
        let img = new Image();
        img.src = res // base64 encoded
      // console.log("img created",img.src)
        img.onload = function(e){

          let initialWidth = img.width;
          let initialHeight = img.height;
          if(initialSize <300000)  {
      // file(less 300KB) without resizing
      // console.log("size is small",img)
      //console.log("file is rel small; upload as it is");
            sendAvaUpdate(url,avatar=file)
          }
          else if(initialWidth <WIDTH)  {
            // file (w < 600) without resizing
            sendAvaUpdate(url,avatar=file)
          }
          else{
      // resize the image
            console.log("try to resize")
            let scaleFactor = WIDTH/initialWidth;
            canvas.width = WIDTH;
            canvas.height = img.height * scaleFactor;
            ctx.drawImage(img,0,0,canvas.width,canvas.height);
            let newImgUrl = ctx.canvas.toDataURL("image/jpeg",0.9);
            avatar = helpUtil(newImgUrl,userFileName);
            sendAvaUpdate(url,avatar=avatar)
          }
        }
      }else{
      // error during reader file load
        console.log("line 128 ")
        jsErr.textContent = "Something went wrong; uplaod file failed"
        }
      }
      else{
      //file detached; remove existing avatar
      console.log("file detached; removing exisitnig avatar")
      sendAvaUpdate(url,avatar=false);
    }

}
