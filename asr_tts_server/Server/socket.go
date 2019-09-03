package Server

type NetSocket struct {
	host Host
	port Port
}

func (this *NetSocket) Pass() {
	panic("implement me")
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