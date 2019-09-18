package Server

type ClientMessage interface {
	GetType() MessageType
}

type MessageType int

const (
	_ MessageType = iota
	TTS
	ASR
)

