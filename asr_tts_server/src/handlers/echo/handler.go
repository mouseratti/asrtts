package echo

import (
	"Server"
	"fmt"
)

type handler struct {

}

func (h *handler) Handle(conn Server.ClientConnection) {
	msg, err := conn.Read()
	if err != nil {
		fmt.Println("error")
	}
	conn.Write(msg)
}

func GetHandler() Server.ClientConnectionHandler {
	return new(handler)
}