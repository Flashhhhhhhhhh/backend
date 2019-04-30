### Installation
Clone this repo to a working directory on your Linux server and run backend/install/FlashInstall.sh with root privs

### Start server
If your OS is using systemd use:
`sudo systemctl start FlashCapstone.service`

otherwise:
`python server.py`

This server was created using [this python tutorial.](https://codeburst.io/this-is-how-easy-it-is-to-create-a-rest-api-8a25122ab1f3)

### query API
Use postman or whatever querying technology you want to hit the endpoints:
http://127.0.0.1:5000/test/test
