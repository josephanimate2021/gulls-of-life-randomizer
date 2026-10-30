class Randomizer {
    constructor() {
        this.rom_stats_elem = document.getElementById("rom_status_text");
        this.loadingROM = false
        this.pyCode = null;
        this.rando_settings = {
            locations: {}
        }
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
                const imported_files = []
                async function mount_import_files(code, og_file_location = "") {
                    const lines = code.split("\n")
                    for (let i = 0; i < lines.length; i++) {
                        const line = lines[i];
                        if (line.startsWith("from") && line.includes(" import")) {
                            const path = line.split("from ")[1].split(" import")[0].split(".")
                            let file_location = "backend";
                            const blank_paths = path.filter(i => i == "")
                            if (blank_paths.length > 0) file_location += `/${og_file_location}`
                            if (blank_paths.length > 1) {
                                file_location += "/"
                                let c = 0
                                for (const _ of blank_paths) {
                                    if (c == 2) file_location += "/", c = -1;
                                    else file_location += "."
                                    c++
                                }
                            }
                            const file = path.join("/") + ".py"
                            if (blank_paths.length == 0) file_location += "/"
                            file_location += file;
                            if (imported_files.includes(file_location)) {
                                lines[i] = ""
                                continue
                            }
                            const fetchStats = await fetch(file_location)
                            if (fetchStats.status == 200 || fetchStats.status == 304) {
                                imported_files.push(file_location)
                                const file_path = file_location.split("/")
                                file_path.splice(0, 1)
                                file_path.pop()
                                lines[i] = `\n${await mount_import_files(await fetchStats.text(), file_path.join("/"))}`
                            }
                        } else if (line.startsWith("import ")) {
                            if (imported_files.includes(line.trim())) {
                                lines[i] = ""
                                continue
                            }
                            imported_files.push(line.trim())
                            let l = line.split("import ")[1].trim()
                            if (l.includes(" as")) l = l.split(" as")[0]
                            const fetchStats = await fetch(`backend/${og_file_location}/${l}.py`)
                            if (fetchStats.status == 200 || fetchStats.status == 304) pyodide.FS.writeFile(`/home/pyodide/${l}.py`, await fetchStats.text())
                        }
                    }
                    return lines.join("\n")
                }
                if (!this.pyCode) {
                    this.rom_stats_elem.textContent = SBT("Chargement de randomizer.py...", "Loading randomizer.py...");
                    this.pyCode = await mount_import_files(await (await fetch("backend/randomizer.py")).text());
                }
                this.pyodide = pyodide
                this.pyodide.FS.writeFile(`/home/pyodide/__init__.py`, "")
                await this.pyodide.runPythonAsync('import os\nprint(__package__)')
                this.rom_stats_elem.textContent = SBT("Vérification de la ROM...", "Validating ROM...");
                this.pyodide.FS.writeFile("ages.gbc", new Uint8Array(arrayBuffer));
                this.pyodide.runPythonAsync(this.pyCode + "\nrando.validate_rom()").then((isValid) => {
                    if (isValid) {
                        document.getElementById("rom_selection_screen").remove()
                        document.getElementById("rando_settings_change_screen").style.display = "block"
                        this.changeSettingsSeed()
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
    changeSettingsSeed() {
        const rando_seed_elem = document.getElementById("rando_seed")
        for (const elem of document.getElementById("rando_settings").children) {
            if (!elem.id) continue
            switch (elem.getAttribute("type")) {
                case "checkbox": {
                    this.rando_settings[elem.id] = elem.checked
                    break;
                } default: {
                    this.rando_settings[elem.id] = elem.value
                }
            }
        }
        rando_seed_elem.value = btoa(JSON.stringify(this.rando_settings))
    }
    changeSettingsFromSeed() {
        try {
            this.rando_settings = JSON.parse(atob(document.getElementById("rando_seed").value))
            for (const i in this.rando_settings) {
                if (i == "locations") continue;
                const elem = document.getElementById(i)
                switch (elem.getAttribute("type")) {
                    case "checkbox": {
                        elem.checked = this.rando_settings[i]
                        break;
                    } default: {
                        elem.value = this.rando_settings[i]
                    }
                }
            }
        } catch (e) {
            console.warn("Changing settings from seed failed.", e)
            this.changeSettingsSeed()
        }
    }
    async generateSeed(btn) {
        if (this.loadingROM) return;
        this.loadingROM = true
        this.rando_status_elem = document.getElementById("rando_status_text")
        this.rando_status_elem.textContent = SBT("Changement d'emplacement...", "Shuffling Locations...")
        const rando_settings = {}
        for (const i in this.rando_settings) {
            const elem = document.getElementById(i)
            if (!elem || elem.getAttribute("disabled") == null) rando_settings[i] = this.rando_settings[i]
        }
        for (const ext of ["bps", "sym", "txt"]) {
            const fetchStats = await fetch(`romhack_builds/${rando_settings.romhack_version}/ages.${ext}`)
            if (fetchStats.status == 200 || fetchStats.status == 304) {
                if (ext == "bps") this.pyodide.FS.writeFile("romhack.bps", await fetchStats.bytes());
                else if (ext == "txt") this.pyodide.FS.writeFile("romhack_bugfixes.txt", await fetchStats.text());
                else this.pyodide.FS.writeFile("romhack.txt", await fetchStats.text());
            }
        }
        this.pyodide.runPythonAsync(this.pyCode + `\nrando.generate_seed('${JSON.stringify(rando_settings)}')`).then(locations => {
            this.rando_status_elem.textContent = SBT("Modification de la ROM...", "Patching ROM...")
            console.log(locations)
        })
    }
}

rando = new Randomizer();