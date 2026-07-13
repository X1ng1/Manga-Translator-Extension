async function translatePageImages() {
    const imageSection = document.querySelector(
        "section.w-full.flex.flex-col.justify-center.items-center.text-accent"
    );

    if (!imageSection) {
        console.error("Couldn't find manga image section.");
        return;
    }

    const images = Array.from(imageSection.querySelectorAll("img"));

    console.log(`Found ${images.length} images.`);

    for (let i = 0; i < images.length; i++) {

        const img = images[i];

        console.log(`===== Image ${i} =====`);

        try {

            console.log("Sending message");

            // const result = await chrome.runtime.sendMessage({
            //     type: "translateImage",
            //     imageUrl: img.currentSrc || img.src
            // });
            // console.log("Received response");

            // wrapImage(img);

            // console.log("Wrapped image");

            // drawTranslations(img, result.translations);

            // console.log("Drew translations");

            // img.dataset.translated = "true";

            // console.log("Finished image");

            chrome.runtime.sendMessage(
                {
                    type: "translateImage",
                    imageUrl: img.currentSrc || img.src
                },
                (result) => {

                    console.log("Callback fired");
                    console.log(result);

                    if (chrome.runtime.lastError) {
                        console.error(chrome.runtime.lastError);
                        return;
                    }

                    if (!result.success) {
                        console.error(result.error);
                        return;
                    }

                    console.log("Received response");

                    wrapImage(img);

                    console.log("Wrapped image");

                    drawTranslations(img, result.translations);

                    console.log("Drew translations");

                    img.dataset.translated = "true";

                    console.log("Finished image");
                }
            );

        } catch (err) {
            console.error(err);
        }
    }
}

function wrapImage(img) {

    if (img.parentElement.classList.contains("manglify-wrapper"))
        return;

    const wrapper = document.createElement("div");

    wrapper.className = "manglify-wrapper";

    wrapper.style.position = "relative";
    wrapper.style.display = "inline-block";

    img.parentNode.insertBefore(wrapper, img);

    wrapper.appendChild(img);
}

function drawTranslations(img, translations) {

    const wrapper = img.parentElement;

    const scaleX = img.clientWidth / img.naturalWidth;
    const scaleY = img.clientHeight / img.naturalHeight;

    for (const bubble of translations) {

        const [x1, y1, x2, y2] = bubble.bbox;

        const overlay = document.createElement("div");

        overlay.className = "manglify-overlay";

        overlay.textContent = bubble.translation;

        overlay.style.position = "absolute";

        overlay.style.left = `${x1 * scaleX}px`;
        overlay.style.top = `${y1 * scaleY}px`;

        overlay.style.width = `${(x2 - x1) * scaleX}px`;
        overlay.style.height = `${(y2 - y1) * scaleY}px`;

        overlay.style.background = "white";
        overlay.style.borderRadius = "10px";

        overlay.style.display = "flex";
        overlay.style.alignItems = "center";
        overlay.style.justifyContent = "center";

        overlay.style.textAlign = "center";

        overlay.style.padding = "4px";

        overlay.style.fontFamily = "Anime Ace";
        overlay.style.fontSize = "16px";

        overlay.style.color = "black";

        wrapper.appendChild(overlay);
    }
}

window.addEventListener("load", () => {

    setTimeout(() => {
        translatePageImages();
    }, 1000);

});
