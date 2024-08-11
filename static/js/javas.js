async function uploadImage(event) {
	event.preventDefault(); // منع إرسال النموذج بالطريقة التقليدية
	const formData = new FormData(document.getElementById("upload-form"));
	try {
		const response = await fetch('/upload', {
		method: 'POST',
		body: formData
		});
		const result = await response.json();

		// عرض رسالة بناءً على النتيجة
		if (result.status === 'success') {
			alert(result.message);
		} else {
			alert(result.message);
		}
		} catch (error) {
			console.error('Error:', error);
			alert('An error occurred while uploading the image.');
           }
        }

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

// script.js

function validateForm() {
	const fileInput = document.getElementById("file-input");
	if (fileInput.files.length === 0) {
		alert("Please select a file to upload.");
		return false;
		}
	return true;
   }

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


            function updateImages() {
                fetch('/update-images')
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('تم تحديث الصور بنجاح!');
                            location.reload(); // إعادة تحميل الصفحة لتحديث المعرض
                        } else {
                            alert('فشل في تحديث الصور.');
                        }
                    })
                    .catch(error => {
                        console.error('خطأ:', error);
                    });
            }

            function updateAvailableImages() {
                fetch('/update-available-images')
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('تم تحديث الصور بنجاح!');
                            location.reload(); // إعادة تحميل الصفحة لتحديث المعرض
                        } else {
                            alert('فشل في تحديث الصور.');
                        }
                    })
                    .catch(error => {
                        console.error('خطأ:', error);
                    });
            }

            function updatePriceImages() {
                fetch('/update-price-images')
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('تم تحديث الصور بنجاح!');
                            location.reload(); // إعادة تحميل الصفحة لتحديث المعرض
                        } else {
                            alert('فشل في تحديث الصور.');
                        }
                    })
                    .catch(error => {
                        console.error('خطأ:', error);
                    });
            }

function openDeleteModal() {
    document.getElementById("deleteModal").style.display = "block";
}

function closeDeleteModal() {
    document.getElementById("deleteModal").style.display = "none";
}

async function deleteImage(event) {
    event.preventDefault();
    const imageName = document.getElementById("imageSelect").value;

    try {
        const response = await fetch(`/delete_image?name=${imageName}`, { method: 'DELETE' });
        const result = await response.json();

        if (result.success) {
            alert('تم حذف الصورة بنجاح');
            location.reload(); // لإعادة تحميل الصفحة بعد الحذف
        } else {
            alert('حدث خطأ أثناء حذف الصورة');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('حدث خطأ أثناء حذف الصورة');
    }
}
