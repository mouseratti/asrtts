package main

import (
	"Server"
	"handlers/echo"
	//"protocols/tcp"
)

func main() {
	server := Server.GetServer()
	server.AddHandler(echo.GetHandler())
	//server.AddProtocol(tcp.g)
	server.Start()
}
