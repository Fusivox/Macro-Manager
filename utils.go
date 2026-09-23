package main

import (
	"os"
	"os/exec"
	"time"

	"github.com/toqueteos/webbrowser"
)

type Action struct {
	action string
	args   map[string]any
}

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
				duration := time.Duration(params["time"].(float32)) * time.Second
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
