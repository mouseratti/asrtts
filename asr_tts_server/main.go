package main

import (
	"./Server"

)

func main() {
	server := Server.GetServer()
	socket := Server.GetSocket(Server.Host("0.0.0.0"), Server.Port(8080))
	server.Listen(socket)
}
