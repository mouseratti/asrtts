package Server

import (
	"fmt"
	"time"
)

type ServerImpl int16

func (this *ServerImpl) Listen(socket Socket) {
	for {
		fmt.Println("server is listening! ", socket )
		time.Sleep(2 * time.Second)

	}

}

func (this *ServerImpl) Handle(c Connection) {

}

func GetServer() Server {
	server := ServerImpl(1)
	return &server
}
