class Randomizer {
    constructor() {
        this.rom_stats_elem = document.getElementById("rom_status_text");
        this.loadingROM = false
        this.pyCode = null;
    }
    romFileSelect(btn) {
        if (this.loadingROM) return;
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.gbc,.zip';
        input.title = SBT('Sélectionner un fichier ROM', 'Select a ROM file');
        input.onchange = async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            this.loadingROM = true;
            this.rom_stats_elem.textContent = SBT("Chargement de la ROM...", "Loading ROM...");
            const reader = new FileReader();
            reader.onload = async (event) => {
                const arrayBuffer = event.target.result;
                const pyodide = await loadPyodide();
                async function mount_import_files(code, og_file_location = "") {
                    const lines = code.split("\n")
                    for (let i = 0; i < lines.length; i++) {
                        const line = lines[i];
                        if (line.startsWith("from") && line.includes(" import")) {
                            const path = line.split("from ")[1].split(" import")[0].split(".")
                            let file_location = "backend";
                            if (path[0] == "") file_location += `/${og_file_location}`
                            file_location += path.join("/") + ".py";
                            const text = await (await fetch(file_location)).text()
                            const file_path = file_location.split("/")
                            file_path.splice(0, 1)
                            file_path.pop()
                            const dir_path = file_path.join("/")
                            lines[i] = `\n${await mount_import_files(text, dir_path)}`
                        }
                    }
                    return lines.join("\n")
                }
                if (!this.pyCode) {
                    this.rom_stats_elem.textContent = SBT("Chargement de randomizer.py...", "Loading randomizer.py...");
                    this.pyCode = await mount_import_files(await (await fetch("backend/randomizer.py")).text());
                }
                console.log(this.pyCode)
                this.rom_stats_elem.textContent = SBT("Vérification de la ROM...", "Validating ROM...");
                pyodide.FS.writeFile("ages.gbc", new Uint8Array(arrayBuffer));
                pyodide.runPythonAsync(this.pyCode + "\nrando.validate_rom()").then((isValid) => {
                    if (isValid) {
                        document.getElementById("rom_selection_screen").remove()
                        document.getElementById("rando_settings").style.display = "block"
                    } else {
                        this.rom_stats_elem.textContent = (SBT("ROM invalide. Veuillez fournir une ROM Oracle of Ages (US) valide.", "Invalid ROM. Please provide a valid Oracle of Ages (US) ROM."));
                    }
                }).catch((error) => {
                    console.error("Error validating ROM:", error);
                    this.rom_stats_elem.textContent = (SBT("Erreur lors de la validation de la ROM. Veuillez vérifier la console pour plus de détails.", "Error validating ROM. Please check the console for more details."));
                })
                this.loadingROM = false;
            };
            reader.readAsArrayBuffer(file);
        };
        input.click();
    }
}

rando = new Randomizer();