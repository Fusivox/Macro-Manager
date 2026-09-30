package main

import (
	"compress/gzip"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path"
	"strings"
	"time"

	"github.com/toqueteos/webbrowser"
)

func make_callback(actions []Action) func() {

	callback := func() {

		for _, a := range actions {

			action, params := a.action, a.args

			switch action {
			case "open":
				switch params["window"] {
				case "gui":

				case "cmd", "shell":
					folder := params["folder"].(string)

					cmd := exec.Command("cmd.exe", folder)
					cmd.Stdin, cmd.Stdout, cmd.Stderr = os.Stdin, os.Stdout, os.Stderr

					if err := cmd.Start(); err != nil {
						cmd = exec.Command("xterm", folder)

						if err := cmd.Start(); err != nil {
							cmd = exec.Command("konsole", folder)

							if err := cmd.Start(); err != nil {
								panic(err)
							}
						}
					}

				case "explorer":
					path := params["folder"].(string)

					file := exec.Command("explorer", path)
					if err := file.Start(); err != nil {

						file = exec.Command("Dolphin", path)
						if err := file.Start(); err != nil {

							panic(err)
						}
					}

				default:
					path := params["window"].(string)

					file := exec.Command(path)

					if err := file.Start(); err != nil {
						webbrowser.Open(path)
					}
				}

			case "wait":
				duration := time.Duration(params["time"].(float64)) * time.Second
				time.Sleep(duration)

			case "write":

			case "click":

			case "moveto":

			case "move":

			case "press":

			case "scroll":

			case "dragto":

			case "drag":

			case "hold":

			case "release":

			case "hotkeys":

			case "screenshot":

			}
		}

	}

	return callback
}

func actualise(data map[int]Macro, settings Settings, abbreviation map[int]Abbreviation) {
	if data != nil {
		databyte, err := json.Marshal(data)
		if err != nil {
			fmt.Println(err)
			return
		}
		err = os.WriteFile(path.Join(appdata, "data.json"), databyte, 0644)
	}
	if settings.Lang != "" {
		settingsbyte, err := json.Marshal(settings)
		if err != nil {
			fmt.Println(err)
			return
		}
		err = os.WriteFile(path.Join(appdata, "settings.json"), settingsbyte, 0644)
	}
	if abbreviation != nil {
		abbbyte, err := json.Marshal(abbreviation)
		if err != nil {
			fmt.Println(err)
			return
		}
		err = os.WriteFile(path.Join(appdata, "settings.json"), abbbyte, 0644)
	}
}

func add_mcr(keys, comment string, actions []Action) {

	macros[len(macros)] = Macro{Keys: keys, Comment: comment, Actions: actions, Task: map[string]any{"active": false}}
}

func add_abb(source, text string) {

	abbreviation[len(abbreviation)] = Abbreviation{Source: source, Text: text}
}

func remove(data map[int]any, nb int) {

	delete(data, nb)
}

func export_mcr(input Macro, outputPath string) bool {

	if outputPath == "" {
		outputPath = "macros.mcr"
	} else if !strings.HasSuffix(outputPath, ".mcr") {
		outputPath += ".mcr"
	}

	f_out, err := os.Create(outputPath)
	if err != nil {
		return false
	}
	defer f_out.Close()

	gz := gzip.NewWriter(f_out)
	defer gz.Close()

	encoder := json.NewEncoder(gz)
	if err := encoder.Encode(input); err != nil {
		return false
	}
	return true
}

func import_mcr(inputPath string) Macro {

	file, _ := os.Open(inputPath)
	defer file.Close()

	gz, _ := gzip.NewReader(file)
	defer gz.Close()

	var macro Macro
	json.NewDecoder(gz).Decode(&macro)
	return macro
}
