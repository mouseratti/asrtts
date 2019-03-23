package main

import (
	"fmt"
	"github.com/satori/go.uuid"
	"gopkg.in/alecthomas/kingpin.v2"
	"os"
	"tts/logging"
	"tts/output"
	"tts/translation"
)
type args struct {
	outputDirectory string
	phrase          string
	debug bool
}


func main() {
	defer func() {
		if r:= recover(); r != nil {
			fmt.Println(r)
			os.Exit(8)
		}
	}()
	level := logging.Info
	cliArgs := parseArgs()
	if cliArgs.debug {
		level = logging.Debug
	}
	log := logging.GetLogger(level)
	log.Debug(fmt.Sprintf("run with cliArgs: %+v", cliArgs))
	converted, err := translation.Convert(cliArgs.phrase)
	if err != nil {
		log.Errorf("error on conversion %v", err)
		os.Exit(7)
	}
	filename := getFileName(cliArgs.outputDirectory)
	log.Debug("filename is ", filename)
	err = translation.Export(converted, filename)
	if err != nil {
		log.Errorf("error on export to %v:  %v", filename, err)
		os.Exit(7)
	}
	if jsoned, err := output.FormatOutput(filename); err != nil {
		log.Error("error on serialising output: ", err)
		os.Exit(7)
	} else {
		fmt.Println(jsoned)
	}
}


func parseArgs() args {
	phrase:= kingpin.Arg("phrase", "phrase to translate").Required().String()
	dir :=  kingpin.Flag("dir", "output directory").Required().String()
	debug :=  kingpin.Flag("debug", "debug").Short('d').Bool()
	kingpin.Parse()
	return args{*dir, *phrase, *debug}
}


func getFileName(directory string) string {
	uidv4 := uuid.NewV4()
	return fmt.Sprintf("%v/%v.raw", directory, uidv4.String())
}


