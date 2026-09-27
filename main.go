package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path"
	"runtime"
)

type Macro struct {
	Keys    string   `json:"keys"`
	Actions []Action `json:"actions"`
	Task    any      `json:"tasked"`
	Comment string   `json:"comment"`
}

type Action struct {
	action string
	args   map[string]any
}

type Abbreviation struct {
	Source string `json:"source"`
	Text   string `json:"text"`
}

type Settings struct {
	Lang     string `json:"lang"`
	Fallback string `json:"fallback"`
	Gui      bool   `json:"GUI on launch"`
}

var appdata string
var macros map[int]Macro
var abbreviation map[int]Abbreviation
var settings Settings
var osName string

func main() {
	osName = runtime.GOOS

	if osName == "windows" {
		appdata = path.Join(os.Getenv("APPDATA"), "Macro Manager")
	} else {
		if os.Geteuid() != 0 {
			fmt.Println("You have to be root to run this programm")
			return
		}
		appdata = path.Join(os.Getenv("HOME"), ".config", "Macro Manager")
	}

	macroByte, err := os.ReadFile(path.Join(appdata, "data.json"))
	if err != nil {
		panic(err)
	}

	json.Unmarshal(macroByte, &macros)

	abbByte, err := os.ReadFile(path.Join(appdata, "abbreviation.json"))
	if err != nil {
		panic(err)
	}

	json.Unmarshal(abbByte, &abbreviation)

	settingsByte, err := os.ReadFile(path.Join(appdata, "settings.json"))
	if err != nil {
		panic(err)
	}

	json.Unmarshal(settingsByte, &settings)

}
