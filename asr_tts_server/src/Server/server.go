package Server

type Server interface {
	Start()
	AddProtocol(Protocol)
	AddHandler(handler ClientConnectionHandler)
}


type ServerImpl struct {
	protocol Protocol
	handler ClientConnectionHandler
}

func (this *ServerImpl) AddHandler(handler ClientConnectionHandler) {
	this.handler = handler
}

func (this *ServerImpl) AddProtocol(protocol Protocol) {
	protocol.SetHandler(this.handler)
	this.protocol = protocol
}


func (this *ServerImpl) Start() {
	if this.protocol == nil {
		panic("protocols are not specified!")
	}
	this.protocol.WaitForClientConnection()
}


func GetServer() Server {
	return new(ServerImpl)
}
