package tcp

import (
	"Server"
	"fmt"
	"net"
)

type Protocol struct {
	handler Server.ClientConnectionHandler
}

func (this *Protocol) SetHandler(handler Server.ClientConnectionHandler) {
	this.handler = handler
}

func (this *Protocol) WaitForClientConnection() {
	listener, err := net.Listen("tcp", "0.0.0.0:8080")
	if err != nil {
		panic("error on starting server")
	}
	fmt.Println("start listening ", listener.Addr())
	for {
		conn, e := listener.Accept()
		go this.handler.Handle(fromConn(conn), e)
	}
}
