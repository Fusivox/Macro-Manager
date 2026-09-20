package main

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

				case "explorer":

				default:

				}

			case "wait":

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
