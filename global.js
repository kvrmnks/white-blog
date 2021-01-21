// Get the modal
const modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
const img = document.getElementsByTagName("img");
const modalImg = document.getElementById("img01");
const captionText = document.getElementById("caption");
for(let i=0;i<img.length;i++){
    img[i].onclick = function (){
          modal.style.display = "block";
          // modal.style.maxWidth =
          modalImg.src = this.src;
          captionText.innerHTML = this.alt;
    }
}

// Get the <span> element that closes the modal
const span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}