const mangaImg = document.querySelector("img");

const response = await fetch(mangaImg.src);
const blob = await response.blob();

const formData = new FormData();
formData.append("image", blob);

await fetch("http://localhost:8000/process-page", {
    method: "POST",
    body: formData
});