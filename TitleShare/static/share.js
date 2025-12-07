class PresetFetchException extends Error {
  constructor(status, errorMessage) {
    super(`Failed to fetch preset (${status}): ${errorMessage}`)
    this.name = this.constructor.name;
    this.status = status;
    this.errorMessage = errorMessage;
  }
}

var presetPromise = null;

async function copyPresetToClipboard(code) {
    const copyButton = document.getElementById("copy-button");
    copyButton.disabled = true;
    console.log("Copying preset code to clipboard:", code);
    if (!presetPromise) {
        presetPromise = getPresetPromise(code);
    }
    setStatusMessage("Fetching preset data...");
    try {
        let data = await presetPromise;
        await navigator.clipboard.writeText(data);
        setSuccessMessage("Preset data copied to clipboard!");
    }
    catch (error) {
        console.error("Failed to copy preset to clipboard.", error);
        if (error instanceof DOMException) {
            setErrorMessage("Failed to copy preset data to clipboard. Please try again.");
        }
        else if (error instanceof PresetFetchException) {
            setErrorMessage(`Failed to fetch preset data. Error ${error.status}: ${error.errorMessage}.`);
        }
        else {
            setErrorMessage("An unexpected error occurred. " + error.toString());
        }
    }
    copyButton.disabled = false;
}

async function getPresetPromise(code) {
    let response = await fetch(`/share/file/${code}`);
    if (!response.ok) {
        let errorMessage = response.statusText;
        try {
            const data = await response.json();
            if (data.error)
            errorMessage = data.error;
        } catch {}
        throw new PresetFetchException(response.status, errorMessage);
    }
    return response.text();
}

function setErrorMessage(message) {
    setStatusMessage(message, "error");
}

function setSuccessMessage(message) {
    setStatusMessage(message, "success");
}

function setStatusMessage(message, status = "info") {
    const statusDiv = document.getElementById("status-message");
    if (statusDiv) {
        statusDiv.textContent = message;
        statusDiv.classList.remove("info", "error", "success");
        statusDiv.classList.add(status);
    }
}