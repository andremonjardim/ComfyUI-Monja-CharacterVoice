import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Monja.CharacterVoice",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "LoadCharacterVoice") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

                // Localiza os menus (widgets)
                const charWidget = this.widgets.find(w => w.name === "character");
                const voiceWidget = this.widgets.find(w => w.name === "voice_name");

                if (charWidget && voiceWidget) {
                    // Função que busca as vozes no servidor (Python)
                    const updateVoices = async () => {
                        const character = charWidget.value;
                        const response = await fetch(`/monja/get_voices?character=${encodeURIComponent(character)}`);
                        if (response.ok) {
                            const voices = await response.json();
                            
                            // Atualiza a lista de opções do menu
                            voiceWidget.options.values = voices;

                            // SE A VOZ ATUAL NÃO PERTENCE AO PERSONAGEM NOVO, MUDA NA HORA
                            if (!voices.includes(voiceWidget.value)) {
                                voiceWidget.value = voices[0] || "Principal";
                            }
                        }
                    };

                    // Ativa a atualização sempre que você clicar no Personagem
                    charWidget.callback = updateVoices;

                    // Roda uma vez ao carregar o nó para garantir que comece certo
                    setTimeout(updateVoices, 100);
                }
                return r;
            };
        }
    }
});