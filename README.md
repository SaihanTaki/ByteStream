# File Sharing over TCP

A basic server-client model for sharing file over TCP implemented using socket.

## Usage

Run the `server.py` and `client.py` in two different directories to avoid filename conflict.

### Runnig the server

```
$ python server.py <send|recv> <file name>
```

### Runnig the client

```
$ python client.py <send|recv> <file name>
```

### Sending a file to the server

```
$ python server.py recv <file name>
```

```
$ python client.py send <file name>
```

### Receiving a file from the server

```
$ python server.py send <file name>
```

```
$ python client.py recv <file name>
```

## Things To Do

1.Handling multiple clients  
2.Handling multiple servers
