package Server

type ClientConnection interface {
	Read() (ClientMessage, error)
	Write(message ClientMessage) error
}
