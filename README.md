# Demo
http://ec2-35-157-225-167.eu-central-1.compute.amazonaws.com/
# Usage
``` docker-compose up ```
# Methods:
```
POST: /api/post_link/
DATA: {"url": url}
RETURN: {"guid": guid} or error {"message": message}
```
```
GET: /api/<guid>
RETURN: {"guid": guid, "state": state, 'info': info}
```