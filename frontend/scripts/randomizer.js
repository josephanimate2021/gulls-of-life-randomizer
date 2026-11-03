class Randomizer {
    constructor() {
        this.rom_stats_elem = document.getElementById("rom_status_text");
        this.loadingROM = false
        this.pyCode = null;
        this.rando_settings = {
            locations: {}
        }
        for (const SCRIPT_PATH of [
            'modules/BinFile.js',
            'modules/HashCalculator.js',
            'modules/RomPatcher.format.ips.js',
            'modules/RomPatcher.format.ups.js',
            'modules/RomPatcher.format.aps_n64.js',
            'modules/RomPatcher.format.aps_gba.js',
            'modules/RomPatcher.format.bps.js',
            'modules/RomPatcher.format.rup.js',
            'modules/RomPatcher.format.ppf.js',
            'modules/RomPatcher.format.bdf.js',
            'modules/RomPatcher.format.pmsr.js',
            'modules/RomPatcher.format.vcdiff.js',
            'modules/zip.js/zip.min.js',
            'RomPatcher.js'
        ]) {
            const script = document.createElement('script');
            script.src = "https://www.marcrobledo.com/RomPatcher.js/rom-patcher-js/" + SCRIPT_PATH;
            script.type = 'text/javascript';
            document.head.appendChild(script);
        }
    }
    async romFileSelect(btn) {
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
            this.romFile = new BinFile(file, async (binFile) => {
                const pyodide = await loadPyodide().catch(e => {
                    console.error(e);
                    this.loadingROM = false;
                    this.rom_stats_elem.textContent = SBT("Échec du chargement de la ROM. Pyodide n'a pas pu être chargé pour une raison inconnue. Veuillez vérifier votre code.", "Loading ROM failed. Pyodide could not be loaded for some reason. please check your code.");
                });
                if (!this.loadingROM) return;
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
                this.rom_stats_elem.textContent = SBT("Vérification de la ROM...", "Validating ROM...");
                this.pyodide.FS.writeFile("ages.gbc", binFile._u8array);
                this.pyodide.runPythonAsync(this.pyCode + "\nrando.validate_rom()").then(async (isValid) => {
                    if (isValid) {
                        this.rom_stats_elem.textContent = SBT("Chargement des paramètres du générateur aléatoire...", "Loading randomizer settings...");
                        const code = await (await fetch("backend/rando_settings.py")).text()
                        this.lang_index = document.getElementById('lang').textContent.endsWith("FR") ? 1 : 0;
                        const settings = JSON.parse(await this.pyodide.runPythonAsync(code + `\nstringify_settings(${this.lang_index})`))
                        const settings_elem = document.getElementById("rando_settings");
                        for (const c in settings) {
                            settings_elem.insertAdjacentHTML("beforeend", "<br>")
                            const center = document.createElement("center")
                            const cat_elem = document.createElement("h3");
                            cat_elem.textContent = c
                            center.appendChild(cat_elem)
                            settings_elem.appendChild(center)
                            for (const o in settings[c]) {
                                let input_first = false
                                const label_elem = document.createElement("label")
                                let input_elem = document.createElement("input")
                                input_elem.setAttribute("onclick", "rando.changeSettingsSeed()")
                                if (typeof settings[c][o].default == "boolean") {
                                    input_elem.type = "checkbox"
                                    input_first = true
                                    input_elem.defaultChecked = settings[c][o].default
                                } else if (settings[c][o].options) {
                                    settings_elem.insertAdjacentHTML("beforeend", "<br>")
                                    input_elem = document.createElement("select")
                                    input_elem.setAttribute("onchange", "rando.changeSettingsSeed()")
                                    for (const c2 in settings[c][o].options) {
                                        if (typeof settings[c][o].options[c2] == "object" && !Array.isArray(settings[c][o].options[c2])) {
                                            const optgroup = document.createElement("optgroup")
                                            optgroup.label = c2
                                            for (const p in settings[c][o].options[c2]) appendOption(optgroup, settings[c][o].options[c2], p)
                                            input_elem.appendChild(optgroup)
                                        } else appendOption(input_elem, {[c2]: settings[c][o].options[c2]}, c2)
                                        function appendOption(elem, info, p) {
                                            const option_elem = document.createElement("option")
                                            option_elem.value = p
                                            if (settings[c][o].default == p) option_elem.setAttribute("selected", "")
                                            option_elem.textContent = SBT(info[p][0], info[p][1])
                                            elem.appendChild(option_elem)
                                        }
                                    }
                                }
                                input_elem.id = o
                                if (settings[c][o].disabled) input_elem.disabled = true
                                label_elem.setAttribute("for", o)
                                for (let i = 0; i < 2; i++) {
                                    if (input_first) settings_elem.insertAdjacentHTML("beforeend", `${i == 1 ? ":" : ""} ${input_elem.outerHTML}`);
                                    else label_elem.textContent = " " + SBT(settings[c][o].fr, o.split("_").map(a => {
                                        const rest = a.substring(1)
                                        return a.split(rest)[0].toUpperCase() + rest
                                    }).join(" ")), settings_elem.appendChild(label_elem)
                                    input_first = !input_first
                                }
                            }
                            settings_elem.insertAdjacentHTML("beforeend", "<br>")
                        }
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
            });
        };
        input.click();
    }
    changeSettingsSeed() {
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
        document.getElementById("rando_seed").value = btoa(JSON.stringify(this.rando_settings))
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
        this.pyodide.FS.writeFile("/home/pyodide/rando_settings.py", `import json\ndef get():\n\treturn json.loads('${JSON.stringify(this.rando_settings)}')`)
        this.pyodide.runPythonAsync(this.pyCode + `\nimport rando_settings\nrando.generate_seed(rando_settings.get())`).then(async patch_data => {
            this.rando_status_elem.textContent = SBT("Modification de la ROM...", "Patching ROM...")
            for (const ext of ["bps", "sym", "txt"]) {
                if (!this.loadingROM) break;
                const romhack_builds_base = `romhack_builds/${this.rando_settings.romhack_version}`
                const fetchStats = await fetch(romhack_builds_base + `/ages.${ext}`)
                if (fetchStats.status == 200 || fetchStats.status == 304) {
                    if (ext == "bps") {
                        const patchFile=new BinFile(await fetchStats.bytes());
                        patchFile.fileName="ages.bps";
                        const patch=RomPatcher.parsePatchFile(patchFile);
                        if (patch) try {
                            this.pyodide.FS.writeFile("romhack.gbc", RomPatcher.applyPatch(this.romFile, patch, {})._u8array);
                        } catch (e) {
                            console.error(e.message);
                            this.rando_status_elem.textContent = SBT("Échec de l'application du patch. Veuillez vérifier la console pour plus de détails.", "Failed to apply patch. Please check the console for more details.");
                            this.loadingROM = false
                        }
                        else {
                            console.error("Invalid patch file was provided.");
                            this.rando_status_elem.textContent = SBT("Échec de l'application du patch. Veuillez vérifier la console pour plus de détails.", "Failed to apply patch. Please check the console for more details.");
                            this.loadingROM = false
                        }
                    }
                    else if (ext == "txt") {
                        const fixes = await fetchStats.text()
                        this.pyodide.FS.writeFile("romhack_bugfixes.txt", fixes);
                        this.pyodide.FS.mkdir("/home/pyodide/bugfixes")
                        for (const line of fixes.split("\n")) {
                            if (line.trim() == "") continue;
                            this.pyodide.FS.writeFile(`/home/pyodide/bugfixes/${line.trim()}`, await (await fetch(romhack_builds_base + `/bugfixes/${line.trim()}`)).bytes())
                        }
                    }
                    else this.pyodide.FS.writeFile("romhack.sym", await fetchStats.text());
                }
            }
            if (this.loadingROM) this.pyodide.runPythonAsync(this.pyCode + `\nimport json\nrando.patch_rom(json.loads('${patch_data}'))`).then(i => {
                const rom_info = JSON.parse(i)
                if (rom_info.patched) {
                    this.showRandoScreen(true)
                    console.log(patch_data)
                    document.getElementById("spoilerLogDownload").setAttribute("href", `data:application/json;base64,${btoa(JSON.stringify({
                        seed: btoa(patch_data),
                        locations: JSON.parse(patch_data).locations,
                    }, null, "\t"))}`);
                    document.getElementById("randoRomDownload").setAttribute("href", `data:application/octet-stream;base64,${this.pyodide.FS.readFile("romhack.gbc").toBase64()}`);
                }
            })
        })
    }
    showRandoScreen(preOrPost = false) {
        document.getElementById("prerando").style.display = preOrPost ? "none" : "block";
        document.getElementById("postrando").style.display = preOrPost ? "block" : "none";
    }
}

rando = new Randomizer();