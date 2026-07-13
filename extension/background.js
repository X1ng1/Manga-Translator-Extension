console.log("Background service worker started");

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    console.log("Received message", message);

    if (message.type !== "translateImage")
        return;

    (async () => {
        try {

            console.log("Downloading image...");

            const imageResponse = await fetch(message.imageUrl);

            console.log("Downloaded image");

            if (!imageResponse.ok)
                throw new Error("Couldn't download image.");

            const blob = await imageResponse.blob();

            console.log("Sending to FastAPI...");

            const formData = new FormData();
            formData.append("image", blob, "page.png");

            const response = await fetch("http://localhost:8000/process", {
                method: "POST",
                body: formData
            });

            console.log("FastAPI returned", response.status);

            if (!response.ok)
                throw new Error(await response.text());

            const data = await response.json();

            sendResponse({
                success: true,
                translations: data.translations
            });

        } catch (err) {

            console.error(err);

            sendResponse({
                success: false,
                error: err.toString()
            });

        }
    })();

    return true;
});