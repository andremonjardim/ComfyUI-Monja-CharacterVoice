import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Monja.CharacterVoice",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "LoadCharacterVoice") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);
                
                const charWidget = this.widgets.find(w => w.name === "character");
                const voiceWidget = this.widgets.find(w => w.name === "voice_name");

                charWidget.callback = async () => {
                    const response = await fetch(`/monja/get_voices?character=${encodeURIComponent(charWidget.value)}`);
                    const voices = await response.json();
                    
                    voiceWidget.options.values = voices;
                    if (!voices.includes(voiceWidget.value)) {
                        voiceWidget.value = voices[0];
                    }
                };
                // Dispara uma vez ao criar o nó para popular o menu
                charWidget.callback();
            };
        }
    }
});