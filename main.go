package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path"
	"runtime"
)

type Macro struct {
	Keys    string         `json:"keys"`
	Actions []Action       `json:"actions"`
	Task    map[string]any `json:"tasked"`
	Comment string         `json:"comment"`
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

func init_background() {
	for nb := range macros {
		keys := macros[nb].Keys
		actions := macros[nb].Actions
		task := macros[nb].Task
		callback := make_callback(actions)

		fmt.Println(callback)

		if keys != "" {
			// keyboard.add_hotkey(keys, callback)
			fmt.Println(">Debug : new hotkey", keys, ", do", actions)
		} else {
			fmt.Println(">Debug: New action that has no keys :", actions)
		}

		if task["active"] == true {
			// sched.add_job(callback, max_instances=1, **task["kwargs"])
			fmt.Println(">Debug : new tasked macro with trigger", task["kwargs"], "do", actions)
		}
	}
	for nb := range abbreviation {
		source := abbreviation[nb].Source
		text := abbreviation[nb].Text
		// keyboard.add_abbreviation(source, text)
		fmt.Println(">Debug : New abbreviation", source, ", replaced by", text)
	}
}
