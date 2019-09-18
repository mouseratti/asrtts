package Server


type Protocol interface {
	SetHandler(handler ClientConnectionHandler)
	WaitForClientConnection()
}
