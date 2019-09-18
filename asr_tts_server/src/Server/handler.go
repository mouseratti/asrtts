package Server

type ClientConnectionHandler interface {
	Handle(ClientConnection)
}
