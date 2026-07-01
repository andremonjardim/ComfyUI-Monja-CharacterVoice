import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Monja.CharacterVoice",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "LoadCharacterVoice") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Espera 10ms para garantir que os widgets existam
                setTimeout(() => {
                    const charWidget = this.widgets?.find(w => w.name === "character");
                    const voiceWidget = this.widgets?.find(w => w.name === "voice_name");

                    if (charWidget && voiceWidget) {
                        console.log("✅ [Monja JS] Nó detectado e configurado!");
                        
                        charWidget.callback = async () => {
                            const resp = await fetch(`/monja/get_voices?character=${encodeURIComponent(charWidget.value)}`);
                            if (resp.ok) {
                                const voices = await resp.json();
                                voiceWidget.options.values = voices;
                                if (!voices.includes(voiceWidget.value)) {
                                    voiceWidget.value = voices[0];
                                }
                            }
                        };
                        // Sincroniza ao criar
                        charWidget.callback();
                    }
                }, 10);
                return r;
            };
        }
    }
});