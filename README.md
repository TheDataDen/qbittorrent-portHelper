# qbittorrent-portHelper

Sets the port used for incoming connections in qBittorrent from a file containing the port. Best to be used with the thrnz/docker-wireguard-pia Docker container, but can be used with any other setup as long as the port is provided via a file.

This script is currently setup to only run within the provided Docker container but could be easily modified to run on its own.

## Usage

### Docker Compose

1. Clone this repository:

```bash
git clone https://github.com/TheDataDen/qbittorrent-portHelper.git
cd qbittorrent-portHelper
```

2. Edit the `docker-compose.yml` file to set the environment variables and volumes as needed. Check the [Configuration](#configuration) section for more details.

3. Run the container:

```bash
docker-compose up -d
```

> [!NOTE]
> If you are running qBittorrent in a docker container (like qBittorrent-nox) you can add this container to your existing docker-compose.yml file.

### Docker Run

```bash
docker run -d \
  --name qbittorrent-porthelper \
  --restart unless-stopped \
  -e QBITTORRENT_HOST=127.0.0.1 \
  -e QBITTORRENT_PORT=8080 \
  -e QBITTORRENT_USERNAME=admin \
  -e QBITTORRENT_PASSWORD=adminadmin \
  -e QBITTORRENT_UPDATE_TIME_SECONDS=60 \
  -e PIA_PORT_FILE_NAME=port.txt \
  -v /PATH/TO/DIR/CONTAINING/PORT/FILE:/pia_port \
  strenkml/qbittorrent-porthelper
```

### Pull the Image

```bash
docker pull strenkml/qbittorrent-porthelper
```

## Configuration

### Environment Variables

The container can be configured using the following environment variables:

| Variable Name                     | Required | Default | Description                                      |
| --------------------------------- | -------- | ------- | ------------------------------------------------ |
| `QBITTORRENT_HOST`                | Yes      |         | Hostname or IP address of the qBittorrent WebUI. |
| `QBITTORRENT_PORT`                | Yes      |         | Port of the qBittorrent WebUI.                   |
| `QBITTORRENT_USERNAME`            | Yes      |         | Username of the qBittorrent WebUI.               |
| `QBITTORRENT_PASSWORD`            | Yes      |         | Password of the qBittorrent WebUI.               |
| `PIA_PORT_FILE_NAME`              | Yes      |         | Name of the file containing the port.            |
| `QBITTORRENT_UPDATE_TIME_SECONDS` | No       | `60`    | How often the port is checked in seconds.        |

### Volumes

The container expects a single volume to be mounted at `/pia_port` containing the port file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please open an issue in this repository.
