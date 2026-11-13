class Randomizer {
    constructor() {
        this.rom_stats_elem = document.getElementById("rom_status_text");
        this.rando_status_elem = document.getElementById("rando_status_text")
        this.loadingROM = false
        this.pyCode = null;
        this.rando_settings = {
            locations: {}
        }
        this.initPresets()
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
    async initPresets() {
        if (!localStorage.rando_presets) localStorage.setItem("rando_presets", JSON.stringify({}));
        this.local_randoPresets = JSON.parse(localStorage.rando_presets)
        this.rando_presets = Object.assign(JSON.parse(await (await fetch("rando_presets.json")).text()), this.local_randoPresets)
        return 67
    }
    async romFileSelect(btn) {
        if (this.loadingROM) return;
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.gbc,.zip';
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
                            const array = []
                            const split_filelocations = file_location.split("/")
                            for (let i = 0; i < split_filelocations.length; i++) {
                                const loc = split_filelocations[i]
                                if (loc != "") array.push(loc);
                                if (loc.startsWith("..")) {
                                    array.splice(i, 1)
                                    for (let x = loc.length; x > 0; x--) array.splice(i - (loc.length - 1), 1)
                                }
                            }
                            file_location = array.join("/")
                            console.log(file_location)
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
                console.log(this.pyCode)
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
                                if (settings[c][o].options) {
                                    settings_elem.insertAdjacentHTML("beforeend", "<br>")
                                    input_elem = document.createElement("select")
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
                                            option_elem.textContent = Array.isArray(info[p]) ? SBT(info[p][0], info[p][1]) : info[p]
                                            elem.appendChild(option_elem)
                                        }
                                    }
                                } else switch (typeof settings[c][o].default) {
                                    case "number": {
                                        if (settings[c][o].min) input_elem.min = settings[c][o].min
                                        if (settings[c][o].max) input_elem.max = settings[c][o].max
                                        input_elem.setAttribute("type", "number")
                                    } case "string": {
                                        input_elem.setAttribute("required", "")
                                        if (typeof settings[c][o].default != "number") input_elem.setAttribute("type", "text")
                                        input_elem.defaultValue = settings[c][o].default
                                        break
                                    } case "boolean": {
                                        input_elem.type = "checkbox"
                                        input_first = true
                                        input_elem.defaultChecked = settings[c][o].default
                                        break;
                                    }
                                }
                                input_elem.setAttribute("onchange", "rando.changeSettingsSeed()")
                                input_elem.id = o
                                input_elem.title = SBT(settings[c][o].description[0], settings[c][o].description[1])
                                if (settings[c][o].disabled) input_elem.disabled = true
                                label_elem.setAttribute("for", o)
                                label_elem.title = input_elem.title
                                const en_label = o.split("_").map(a => {
                                    const rest = a.substring(1)
                                    return a.split(rest)[0].toUpperCase() + rest
                                }).join(" ")
                                for (let i = 0; i < 2; i++) {
                                    if (input_first) settings_elem.insertAdjacentHTML("beforeend", `${i == 1 ? ":" : ""} ${input_elem.outerHTML}`);
                                    else label_elem.textContent = " " + SBT(settings[c][o].fr || en_label, en_label), settings_elem.appendChild(label_elem)
                                    input_first = !input_first
                                }
                            }
                            settings_elem.insertAdjacentHTML("beforeend", "<br>")
                        }
                        this.changeSettingsSeed(true)
                        this.rando_presets.default = {
                            settings: Object.assign({}, this.rando_settings),
                            preset_title: "Default",
                            preset_desc: "",
                            preset_creators: "This Website"
                        }
                        this.loadPresets()
                        document.getElementById("rom_selection_screen").remove()
                        document.getElementById("rando_settings_change_screen").style.display = "block"
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
    openPresetSaveDialog() {
        if (!this.uploaded_preset_settings) document.getElementById('preset_save_dialog').showModal();
        else {
            const riskingLooseUploadedPresetSettings = confirm(SBT(
                "Vous disposez encore des préréglages que vous avez importés et que vous n'avez pas encore enregistrés. Êtes-vous sûr de vouloir vraiment perdre ces préréglages ?",
                "You still have your uploaded preset settings that you have yet to save. Are you sure that you really want to loose your uploaded settings?"
            ))
            if (riskingLooseUploadedPresetSettings) {
                delete this.uploaded_preset_settings
                this.loadingROM = false
                this.openPresetSaveDialog()
            }
        }
    }
    uploadPreset() {
        if (this.uploaded_preset_settings) {
            document.getElementById('preset_save_dialog').showModal()
            return
        }
        if (this.loadingROM) return
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            this.loadingROM = true
            this.rando_status_elem.textContent = SBT("Mise en ligne du journal des spoilers de « Gulls Of Life »...", "Uploading Gulls Of Life Spoiler Log...")
            const reader = new FileReader()
            reader.addEventListener("loadend", h => {
                try {
                    const settings = JSON.parse(h.target.result)
                    let propsIncluded = settings.seed && settings.patch_data
                    if (propsIncluded) for (const p in this.rando_settings) {
                        if (
                            typeof settings.patch_data[p] != "undefined"
                            && typeof this.rando_settings[p] == typeof settings.patch_data[p]
                        ) propsIncluded = true
                        else {
                            propsIncluded = false
                            break
                        }
                    }
                    if (!propsIncluded) {
                        this.rando_status_elem.textContent = SBT("Votre fichier journal des spoilers de « Gulls of Life » n'est pas valide. Veuillez essayer de télécharger un fichier journal de spoilers de « Gulls of Life » valide.", "Your gulls of life spoiler log file is not valid. Please try uploading a valid gulls of life spoiler log.")
                        this.loadingROM = false
                    } else {
                        const includeLocations = Object.keys(settings.patch_data.locations).length != 0 && confirm(SBT("Souhaitez-vous inclure vos emplacements aléatoires dans votre préréglage?", "Do you want to include your randomized locations inside your preset?"))
                        if (!includeLocations) settings.patch_data.locations = {}
                        let settingsSame = ["", false]
                        for (const p in this.rando_presets) {
                            if (JSON.stringify(this.rando_presets[p].settings) == JSON.stringify(settings.patch_data)) {
                                settingsSame = [
                                    this.rando_presets[p].preset_title,
                                    true
                                ]
                                break
                            }
                        }
                        if (settingsSame[1]) {
                            this.loadingROM = false
                            this.rando_status_elem.textContent = SBT(`Votre fichier journal « Gulls of Life » contient les mêmes paramètres que le préréglage ${settingsSame[0]}. Veuillez essayer de télécharger un autre fichier journal « Gulls of Life » comportant des paramètres différents.`, `Your gulls of life spoiler log contains the same settings as the ${settingsSame[0]} preset. Please try uploading a different gulls of life spoiler log with the different settings on it.`)
                            return
                        }
                        const preset_stuff = document.getElementById('preset_save_dialog')
                        this.uploaded_preset_settings = settings.patch_data
                        this.rando_status_elem.textContent = ""
                        preset_stuff.showModal()
                        this.loadingROM = false
                    }
                } catch (e) {
                    console.error("Error uploading JSON file", e)
                    this.rando_status_elem.textContent = SBT("Impossible de télécharger votre journal de spoilers sur « Gulls of Life ». Veuillez consulter la console développeur pour plus de détails.", "Could not upload your gulls of life spoiler log. Please check the developer console for more details.")
                    this.loadingROM = false
                }
            })
            reader.readAsText(file)
        }
        input.click()
    }
    loadPresets(savedPreset = false, deletedPreset = false) {
        const rando_presets_elem = document.getElementById("rando_presets");
        rando_presets_elem.innerHTML = ""
        for (const p in this.rando_presets) {
            const option = document.createElement("option")
            if (p == "default" && !savedPreset) option.setAttribute("selected", "")
            option.value = p
            option.title = this.rando_presets[p].preset_desc + "\n\nCreator(s): " + this.rando_presets[p].preset_creators
            option.textContent = this.rando_presets[p].preset_title
            rando_presets_elem.appendChild(option)
        }
        if (!savedPreset) this.changePreset("default", deletedPreset);
        document.getElementById("del_all_presets_btn").style.display = Object.keys(this.local_randoPresets).length == 0 ? "none" : "block"
    }
    savePreset(form) {
        const preset_stuff = {
            settings: Object.assign({}, this.uploaded_preset_settings || this.rando_settings)
        }
        const preset_save_modalClose_elem = document.getElementById("preset_save_closeModal_btn")
        if (this.uploaded_preset_settings) {
            preset_save_modalClose_elem.setAttribute("disabled", "")
            delete this.uploaded_preset_settings
        }
        const preset_save_status_elem = document.getElementById("preset_save_status")
        preset_save_status_elem.textContent = SBT("Enregistrement du préréglage...", "Saving Preset...")
        for (const elem of form.children) {
            if (!elem.id) continue;
            preset_stuff[elem.id] = elem.value
        }
        const p = preset_stuff.preset_title.split(" ").join("_")
        this.local_randoPresets[p] = preset_stuff
        Object.assign(this.rando_presets, this.local_randoPresets)
        this.loadPresets(true)
        localStorage.setItem("rando_presets", JSON.stringify(this.local_randoPresets))
        preset_save_status_elem.textContent = SBT("Votre préréglage a été enregistré avec succès!", "Your Preset was saved successfully!")
        setTimeout(() => {
            if (preset_save_modalClose_elem.hasAttribute("disabled")) {
                preset_save_modalClose_elem.removeAttribute("disabled")
                document.getElementById('preset_save_dialog').close()
            }
            preset_save_status_elem.textContent = "";
        }, 3000)
    }
    changePreset(preset, deletedPreset = false) {
        const randoPresets_copy = Object.assign({}, this.rando_presets)
        delete randoPresets_copy.default
        document.getElementById("presetDownload").href = `data:application/json;base64,${btoa(JSON.stringify(randoPresets_copy, null, "\t"))}`
        document.getElementById("loadedPreset").textContent = this.rando_presets[preset].preset_title
        document.getElementById("preset_mgr_btn").style.display = this.local_randoPresets[preset] ? "block" : "none"
        if (!deletedPreset) {
            document.getElementById('rando_seed').value = btoa(JSON.stringify(this.rando_presets[preset].settings))
            this.changeSettingsFromSeed()
        }
    }
    deletePreset() {
        const deletingPreset = document.getElementById("loadedPreset").textContent;
        const val = document.getElementById("rando_presets").value
        if (confirm(SBT(
            `Êtes-vous sûr de vouloir supprimer ${deletingPreset} ? Cette action est irréversible ! Vous pouvez toutefois annuler la suppression si vous conservez les paramètres actuellement sélectionnés et que vous les enregistrez en tant que nouveau préréglage.`,
            `Are you sure that you want to delete ${deletingPreset}? There is no going back if you do this! You can however undo the deletion if you keep your currently selected settings and save those as a new preset.`
        ))) {
            document.getElementById("loadedPreset").textContent = "Deleting..."
            delete this.local_randoPresets[val]
            localStorage.setItem("rando_presets", JSON.stringify(this.local_randoPresets))
            delete this.rando_presets[val]
            this.loadPresets(false, true)
            document.getElementById("preset_save_btn").style.display = "block"
            alert(`${deletingPreset} was removed successfully!`);
            document.getElementById("preset_manager").close()
        }
    }
    deleteAllPresets() {
        if (confirm(SBT(
            "Êtes-vous sûr de vouloir supprimer tous vos préréglages ? Une fois cette opération effectuée, vous ne pourrez plus revenir en arrière !", 
            `Are you sure that you want to delete all of your presets? There is no going back if you do this!`
        ))) {
            localStorage.clear()
            this.rando_status_elem.textContent = SBT("Suppression des préréglages...", "Deleting Presets...")
            const default_preset = Object.assign({}, this.rando_presets.default)
            this.initPresets().then(() => {
                this.rando_presets.default = default_preset
                this.loadPresets(false, true)
                document.getElementById("preset_save_btn").style.display = "block"
                alert(`All of your presets were removed successfully!`);
                this.rando_status_elem.textContent = ""
            })
        }
    }
    changeSettingsSeed(firstTime = false) {
        for (const elem of document.getElementById("rando_settings").children) {
            if (!elem.id) continue
            if (elem.id == "romhack_version") {
                if (this.rando_settings[elem.id] != elem.value) this.rando_settings.locations = {}
                this.actionOnRomhackVersionChange(elem.value)
            }
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
        if (!firstTime) this.checkShowSavePresetBtn();
    }
    actionOnRomhackVersionChange(v) {
        for (
            const e of ["disable_dream_timer", "max_out_dream_timer", "dream_timer"]
        ) {
            const elem = document.getElementById(e)
            if (v == "0.2" || v == "0.1") elem.setAttribute("disabled", "");
            else if (elem.hasAttribute("disabled")) elem.removeAttribute("disabled");
        }
    }
    changeSettingsFromSeed() {
        try {
            this.rando_settings = JSON.parse(atob(document.getElementById("rando_seed").value))
            for (const i in this.rando_settings) {
                if (i == "locations") continue;
                if (i == "romhack_version") this.actionOnRomhackVersionChange(this.rando_settings[i])
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
        this.checkShowSavePresetBtn()
    }
    checkShowSavePresetBtn() {
        document.getElementById('preset_save_btn').style.display = document.getElementById('rando_seed').value == btoa(
            JSON.stringify(this.rando_presets[document.getElementById("rando_presets").value].settings)
        ) ? "none" : "block"
    }
    async generateSeed() {
        if (this.loadingROM) return;
        document.getElementById("rando_options").style.display = "none";
        this.loadingROM = (
            this.rando_settings.romhack_version == "0.2"
            || this.rando_settings.romhack_version == "0.1"
        ) || (this.rando_settings.dream_timer > 9 ? confirm(SBT([
            "Attends un peu, on dirait que tu as réglé la durée de ton rêve sur plus de 9 secondes.",
            "Cette fenêtre de confirmation s'affiche car le jeu ne t'indiquera pas le temps écoulé au-delà de ce seuil pendant ton rêve;",
            "elle sert à s'assurer que tu te souviendras bien de la modification que tu as apportée à ce paramètre avant de lancer le jeu en mode aléatoire.",
            "Es-tu sûr de vouloir continuer?"
        ].join(" "), [
            "Whoa there, it seems like you have configured your dream timer setting to be above 9 seconds.",
            "You are getting this confirmation box because the game will not show you your seconds past this point during your dream,",
            "and it is to make sure that you will remember the change you made to this setting before randomizing the game.\nAre you sure you want to go about this?"
        ].join(" "))) : true);
        if (this.loadingROM) {
            this.rando_status_elem.textContent = SBT("Changement d'emplacement...", "Shuffling Locations...")
            if (this.fileExists("/home/pyodide/rando_settings.py")) this.pyodide.FS.unlink("/home/pyodide/rando_settings.py")
            this.pyodide.FS.writeFile(
                "/home/pyodide/rando_settings.py", `import json\ndef get():\n\treturn json.loads('${JSON.stringify(this.rando_settings)}')`
            )
            this.pyodide.runPythonAsync(this.pyCode + `\nimport rando_settings\nrando.generate_seed(rando_settings.get())`).then(async patch_data => {
                this.rando_status_elem.textContent = SBT("Modification de la ROM...", "Patching ROM...")
                for (const ext of ["bps", "sym", "txt", "json"]) {
                    if (!this.loadingROM) {
                        document.getElementById('rando_options').style.display = 'block'
                        break;
                    }
                    if (this.fileExists(`/home/pyodide/romhack.${ext}`)) continue
                    const romhack_builds_base = `romhack_builds/${this.rando_settings.romhack_version}`
                    const fetchStats = await fetch(romhack_builds_base + `/ages.${ext}`)
                    if (fetchStats.status == 200 || fetchStats.status == 304) {
                        if (ext == "bps") {
                            if (this.fileExists("/home/pyodide/romhack.gbc")) continue
                            const patchFile=new BinFile(await fetchStats.bytes());
                            patchFile.fileName="ages.bps";
                            const patch=RomPatcher.parsePatchFile(patchFile);
                            if (patch) try {
                                this.pyodide.FS.writeFile("/home/pyodide/romhack.gbc", RomPatcher.applyPatch(this.romFile, patch, {})._u8array);
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
                            if (this.rando_settings.vanilaize_rom || this.fileExists("/home/pyodide/romhack_bugfixes.txt")) continue
                            const bgp = "/home/pyodide/bugfixes";
                            const fixes = await fetchStats.text()
                            this.pyodide.FS.writeFile("/home/pyodide/romhack_bugfixes.txt", fixes);
                            this.pyodide.FS.mkdir(bgp)
                            for (const line of fixes.split("\n")) {
                                if (line.trim() == "") continue;
                                this.pyodide.FS.writeFile(`${bgp}/${line.trim()}`, await (await fetch(romhack_builds_base + `/bugfixes/${line.trim()}`)).bytes())
                            }
                        }
                        else this.pyodide.FS.writeFile(`/home/pyodide/romhack.${ext}`, await fetchStats.text());
                    }
                }
                if (this.loadingROM) this.pyodide.runPythonAsync(this.pyCode + `\nimport json\nrando.patch_rom(json.loads('${JSON.stringify(Object.assign(JSON.parse(patch_data), {
                    "apply_fr_lang": this.lang_index == 0
                }))}'))`).then(i => {
                    const rom_info = JSON.parse(i)
                    if (rom_info.patched) {
                        this.showRandoScreen(true)
                        document.getElementById("spoilerLogDownload").setAttribute("href", `data:application/json;base64,${btoa(JSON.stringify({
                            seed: btoa(patch_data),
                            patch_data: JSON.parse(patch_data),
                        }, null, "\t"))}`);
                        const romhackFile = new BinFile(this.pyodide.FS.readFile("romhack.gbc"))
                        const patch = RomPatcher.createPatch(this.romFile, romhackFile, "bps", {})
                        document.getElementById("randoRomDownload").setAttribute("href", `data:application/octet-stream;base64,${romhackFile._u8array.toBase64()}`);
                        document.getElementById("patchFileDownload").setAttribute("href", `data:application/octet-stream;base64,${patch.export('my_patch')._u8array.toBase64()}`);
                        document.getElementById('rando_options').style.display = 'block'
                    }
                }).catch((error) => {
                    this.loadingROM = false
                    document.getElementById('rando_options').style.display = 'block'
                    console.error("Error patching ROM:", error);
                    this.rando_status_elem.textContent = (SBT("Erreur lors de la patching de la ROM. Veuillez vérifier la console pour plus de détails.", "Error patching ROM. Please check the console for more details."));
                })
            }).catch((error) => {
                this.loadingROM = false
                document.getElementById('rando_options').style.display = 'block'
                console.error("Error running the randomizer:", error);
                this.rando_status_elem.textContent = (SBT("Erreur lors de l'exécution du générateur aléatoire. Veuillez vérifier la console pour plus de détails.", "Error running the randomizer. Please check the console for more details."));
            })
        }
    }
    fileExists(path) {
        try {
            this.pyodide.FS.stat(path)
            return true
        } catch {
            return false
        }
    }
    showRandoScreen(preOrPost = false) {
        this.rando_status_elem.textContent = ""
        this.loadingROM = false
        document.getElementById("prerando").style.display = preOrPost ? "none" : "block";
        document.getElementById("postrando").style.display = preOrPost ? "block" : "none";
    }
    async newPlandoSession() {
        if (this.loadingROM) return;
        this.loadingROM = true
        this.rando_status_elem.textContent ||= SBT("Lancement de Plandomizer...", "Opening Plandomizer...")
        this.plando_modal ||= document.getElementById("plandomizer")
        this.plando_locations = Object.assign({}, this.rando_settings.locations)
        this.plando_config ||= document.getElementById("game_locations_plando")
        if (Object.keys(this.plando_locations).length == 0) await new Promise(async res => {
            this.plando_locations = {}
            const locations_data = JSON.parse(await this.pyodide.runPythonAsync(this.pyCode + "\nrando.stringify_locations()"))
            for (const location in locations_data) {
                if (
                    (
                        locations_data[location]?.not_compatiable_versions 
                        && locations_data[location].not_compatiable_versions.includes(this.rando_settings.romhack_version)
                    ) || (
                        locations_data[location]?.compatiable_versions 
                        && !locations_data[location].compatiable_versions.includes(this.rando_settings.romhack_version)
                    )
                ) continue
                this.plando_locations[location] = locations_data[location]
            }
            res()
        });
        else {
            const new_locations = {}
            for (const location in this.plando_locations) {
                new_locations[location] = {"vanila_item": this.plando_locations[location]}
            }
            this.plando_locations = new_locations
        }
        this.plando_config.innerHTML = ""
        const game_items = JSON.parse(await this.pyodide.runPythonAsync(this.pyCode + "\nrando.stringify_items()"))
        for (const location in this.plando_locations) {
            const label = document.createElement("label")
            label.textContent = location + ": "
            label.classList.add("hearts")
            label.for = location.split(" ").join("_")
            this.plando_config.appendChild(label)
            const select = document.createElement("select")
            select.id = label.for
            select.setAttribute("onchange", "rando.savePlandoLocation()")
            for (const item in game_items) {
                if (game_items[item].hidden) continue
                const option = document.createElement("option")
                option.value = item
                if (item == this.plando_locations[location].vanila_item) option.setAttribute("selected", "");
                option.textContent = item
                select.appendChild(option)
            }
            this.plando_config.appendChild(select)
            this.plando_config.insertAdjacentHTML("beforeend", "<br>")
        }
        this.plando_modal.showModal()
        this.rando_status_elem.textContent = ""
        this.loadingROM = false
    }
    savePlandoLocation() {
        for (const elem of this.plando_config.children) {
            if (elem.id) this.rando_settings.locations[elem.id.split("_").join(" ")] = elem.value
        }
        this.changeSettingsSeed()
    }
    clearPlandoLocations() {
        this.rando_settings.locations = {}
        this.closePlando()
        this.rando_status_elem.textContent = SBT("Nettoyage des emplacements planifiés...", "Clearing Plandomized Locations...")
        this.newPlandoSession()
        const i = setInterval(() => {
            if (!this.loadingROM) {
                clearInterval(i)
                alert(SBT('Les emplacements Plando ont été effacés avec succès !', 'Plando Locations were cleared successfully!')) 
            }
        })
    }
    closePlando() {
        this.plando_modal.close()
    }
    shuffleArray(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }
    shufflePlandoLocations() {
        let array = []
        for (const elem of this.plando_config.children) {
            if (!elem.id) continue
            array.push(elem.value)
        }
        array = this.shuffleArray(array)
        let count = 0
        for (const elem of this.plando_config.children) {
            if (!elem.id) continue
            elem.value = array[count]
            count++
        }
    }
}

rando = new Randomizer();