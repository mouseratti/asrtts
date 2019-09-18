package Server

import "fmt"

type NetSocket struct {
	host Host
	port Port
}

func (this *NetSocket) AsString()  string{
	return fmt.Sprintf("%v:%v", this.host, this.port)
}

func (this *NetSocket) GetHost() Host  {
	return this.host
}

func (this *NetSocket) GetPort() Port  {
	return this.port
}


func GetSocket(host Host, port Port) Socket {
	return &NetSocket{host, port}
}