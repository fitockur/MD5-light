# MD5_light
App for calculating MD5-hash of file through its url. It can send the results on your email address.

*POST request for **/submit** with url and email address (optional);*

*GET request for **/check** with id parameter*

## Installation

### Download the necessary files
```bash
$ git clone https://github.com/fitockur/MD5-light.git
$ cd MD5-light
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### Set DataBase
```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
```

### Add information on your mail server:
```bash
$ export MAIL_SERVER=<server>
$ export MAIL_PORT=<port>
$ export MAIL_USE_TLS=<tls>
$ export MAIL_USERNAME=<your username>
$ export MAIL_PASSWORD=<your password>
```

Example for gmail.com:
```bash
$ export MAIL_SERVER=smtp.googlemail.com
$ export MAIL_PORT=587
$ export MAIL_USE_TLS=1
```
### Start your server
```bash
$ flask run
```

## Example
```bash
$ curl -X POST -d "email=nikitosik981@gmail.com&url=https://students.bmstu.ru/static/images/eulogo-lite.png" http://localhost:5000/submit

> {"id":"997a75d5-2630-4fc1-a42d-c27b2e79d232"}

$ curl -X GET http://localhost:5000/check?id=997a75d5-2630-4fc1-a42d-c27b2e79d232

> {"md5":"1dc831b23a0d38434a99975cb2bcc874","status":"done","url":"https://students.bmstu.ru/static/images/eulogo-lite.png"}
```

If you want to sync another DBMS, change the url:
```bash
$ export SQLALCHEMY_DATABASE_URI=<your-url>
```