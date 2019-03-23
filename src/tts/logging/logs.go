package logging

import (
	"github.com/sirupsen/logrus"
	"os"
)


func GetLogger(level LogLevel) logrus.FieldLogger  {
	file, err := os.OpenFile("/tmp/tts.log",os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		panic("can not open logfile!!!")
	}

	logger := logrus.StandardLogger()
	logger.SetLevel(logrus.Level(level))
	logrus.SetOutput(file)
	return logger
}