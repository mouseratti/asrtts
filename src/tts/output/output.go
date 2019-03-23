package output

import "encoding/json"

type Output struct {
	Filename string `json:"filename"`
}

func FormatOutput(filename string) (result string, e error) {
	output := Output{filename}
	jsoned, e := json.Marshal(output)
	if e != nil {
		return
	}
	result = string(jsoned)
	return
}

