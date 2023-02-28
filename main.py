import matplotlib.pyplot
import matplotlib.animation
import socket
import struct
import typing


class Sensor(typing.NamedTuple):
    ip_address: str
    port: int


def read_data(sensor: Sensor, sock: socket.socket) -> bytes:
    buffer = 2048
    command = bytes.fromhex("30020d60")
    sock.sendto(command, sensor)
    response, _ = sock.recvfrom(buffer)
    return response

def unpack(data: bytes):
    _, value = struct.unpack(">HI", data)
    return value

def main():
    sensor1 = Sensor("192.168.1.100", 5011)
    sensor2 = Sensor("192.168.1.101", 5011)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    x_data = list()
    y_data = list()

    figure = matplotlib.pyplot.figure()
    line, = matplotlib.pyplot.plot(x_data, y_data, '-')

    def update(frame):

        data1 = read_data(sensor1, sock)
        data2 = read_data(sensor2, sock)
        value1 = unpack(data1)
        value2 = unpack(data2)

        difference = value2 - value1
        difference /= 1_000_000

        if 0 < difference < 20:
            x_data.append(frame)
            y_data.append(difference)
            line.set_data(x_data, y_data)
        figure.gca().relim()
        figure.gca().autoscale_view()
        return line,

    animation = matplotlib.animation.FuncAnimation(figure, update, interval=50)

    matplotlib.pyplot.show()


if __name__ == "__main__":
    main()