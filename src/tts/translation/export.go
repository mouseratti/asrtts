package translation

import (
	"io/ioutil"
)

func Export(content AudioContent, filename string) error {
	err := ioutil.WriteFile(filename, content, 0777)
	return err
}
