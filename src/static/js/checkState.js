const checkInp = (checkbox,inp)=>{
    /*
    func for upload image:
    1.should help to send only one state to the server:
    either remove avatar or update the old one;
    2.toggle class 'disabled' on submit button
     */
    if(checkbox){
        console.log("checkbox in DOM; line 9")
        // checkbox(remove avatar) present in DOM:
        // checked vs unchecked
        checkbox.addEventListener("change",(e)=>{
        if(checkbox.checked){
            // checkbox checked = avatar should be removed
          inp.value = null //
          butSubmit.classList.remove("disabled")
         }
         else{
          butSubmit.classList.add("disabled")
        }

       });
       inp.addEventListener("change",()=>{
        if(inp.value){
          checkbox.checked = false;
          butSubmit.classList.remove("disabled")

        }else{
          butSubmit.classList.add("disabled");
        }
      })

    }
    else{
        // checkbox present in DOM but not
        // state can contain either "remove img"
        // or "attach img" but not both
        if(checkbox!=null){
          // remove existed avatar (clear image input if user attached img occasionally);
          console.log("checkbox NOT null; line 40")
          checkbox.addEventListener("change",(e)=>{
          if(checkbox.checked){
            inp.value = null
            butSubmit.classList.remove("disabled")
          }else{
            butSubmit.classList.add("disabled")
          }
          });
        inp.addEventListener("change",()=>{
          if(inp.value){
            checkbox.checked = false;
            butSubmit.classList.remove("disabled");
          }else{
            butSubmit.classList.add("disabled");
          }
        })
        }else{
       console.log("initial default state;line 58")
       // checkbox NOT in DOM (avatar == default static image)
        inp.addEventListener("change",()=>{
        // toggle class 'disabled' on submit button
          if(inp.value){
            butSubmit.classList.remove("disabled")
          }else{
            butSubmit.classList.add("disabled")

          }
        })

      }
    }
}

