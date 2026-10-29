function romFileSelect() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.gbc,.zip';
    input.title = SBT('Sélectionner un fichier ROM', 'Select a ROM file');
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = async (event) => {
            const arrayBuffer = event.target.result;
            const pyodide = await loadPyodide();
            fetch("backend/randomizer.py").then(response => response.text()).then(code => {
                pyodide.FS.writeFile("ages.gbc", new Uint8Array(arrayBuffer));
                pyodide.runPythonAsync(code)
                pyodide.runPythonAsync(`rando.validate_rom()`).then((isValid) => {
                    if (isValid) {
                        document.getElementById("rom_selection_screen").remove()
                    } else {
                        alert(SBT("ROM invalide. Veuillez fournir une ROM Oracle of Ages (US) valide.", "Invalid ROM. Please provide a valid Oracle of Ages (US) ROM."));
                    }
                }).catch((error) => {
                    console.error("Error validating ROM:", error);
                    alert(SBT("Erreur lors de la validation de la ROM. Veuillez vérifier la console pour plus de détails.", "Error validating ROM. Please check the console for more details."));
                })
            })
        };
        reader.readAsArrayBuffer(file);
    };
    input.click();
}