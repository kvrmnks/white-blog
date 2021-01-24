// Get the modal


const modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
const img = document.getElementsByTagName("img");
const modalImg = document.getElementById("img01");
// const captionText = document.getElementById("caption");
let init_scale = 1;
const handle = (event)=>{

    console.log( event)
    if(event.deltaY < 0){
        init_scale = init_scale - 0.2 > 0.5 ? init_scale - 0.2 : init_scale;
        modalImg.style.transform = 'scale(' + init_scale + ')';
    }else{
        init_scale = init_scale + 0.2 < 1.5 ? init_scale + 0.2 : init_scale;
        modalImg.style.transform = 'scale(' + init_scale + ')';
    }
    event.preventDefault();
}

for(let i=0;i<img.length;i++){
    img[i].onclick = function (){
          modal.style.display = "block";
          modalImg.src = this.src;
          modalImg.style.transform = 'scale(1)'
          // captionText.innerHTML = this.alt;
          init_scale = 1;
          document.addEventListener('wheel',handle, {passive: false})
    }
}







// Get the <span> element that closes the modal
const span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
  init_scale = 1;
  document.removeEventListener('wheel', handle, {passive: false})
}