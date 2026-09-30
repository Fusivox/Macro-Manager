package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path"
	"runtime"
	"strings"

	"golang.design/x/hotkey"
	"golang.design/x/hotkey/mainthread"
)

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

	mainthread.Init(init_background)

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

			parseHotkey(keys)

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

func parseHotkey(s string) (*hotkey.Hotkey, error) {
	parts := strings.Split(strings.ToLower(s), "+")
	for i := range parts {
		parts[i] = strings.TrimSpace(parts[i])
	}

	// le dernier élément est la touche, les autres sont les modificateurs
	keyName := parts[len(parts)-1]
	key, ok := keyMap[keyName]
	if !ok {
		return nil, fmt.Errorf("touche inconnue : %q", keyName)
	}

	var mods []hotkey.Modifier
	for _, m := range parts[:len(parts)-1] {
		mod, ok := modMap[m]
		if !ok {
			return nil, fmt.Errorf("modificateur inconnu : %q", m)
		}
		mods = append(mods, mod)
	}

	return hotkey.New(mods, key), nil
}
