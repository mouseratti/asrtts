package logging

type LogLevel uint64

const (
	Panic LogLevel = iota
	Fatal
	Error
	Warning
	Info
	Debug
)
