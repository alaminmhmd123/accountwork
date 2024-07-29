document.addEventListener('DOMContentLoaded', function() {
    var galleryImages = document.querySelectorAll('.gallery-image');

    galleryImages.forEach(function(img) {
        img.addEventListener('click', function() {
            var src = this.src;
            var caption = this.getAttribute('data-caption');
            openModal(src, caption);
        });
    });
});

function openModal(src, caption) {
    var modal = document.getElementById("myModal");
    var modalImg = document.getElementById("modalImage");
    var modalCaption = document.getElementById("modalCaption");
    modal.style.display = "flex";
    modalImg.src = src;
    modalCaption.textContent = caption;
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

window.addEventListener('click', function(event) {
    var modal = document.getElementById("myModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
});
