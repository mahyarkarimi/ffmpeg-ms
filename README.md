# FFMPEG microservice developed in python fastapi

<hr />
A microservice for conversion of any sort of media using FFMPEG.

## Quick start

### Deploy using docker

<hr />

```bash
docker run --rm -p 8000:8000 ffmpeg-ms:0.1.0
```

### Deploy with docker-compose.yml

<hr />

```yml
version: '3'

services:
    api:
        image: ffmpeg-ms:0.1.0
        restart: unless-stopped
        ports:
            - 8000:8000
        volumes:
            - ./.htpasswd:/app/.htpasswd
```

## Features

<hr />

1. Convert any media with given ffmpeg style output format.
2. Stream output from `/convert` endpoint.
3. File based download from `/convert-file` endpoint.
4. Has rate limit for calling each endpoint based on user (default 5 requests per minute).
5. Can have basic authentication based on `/app/.htpasswd` file generated by htpasswd of apache2-utils. password must be encrypted with the bcrypt algorithm.

## Generate .htpasswd file

<hr />

In order to activate authentication, generate `.htpasswd` file using `apache2-utils`.
Install `apache2-utils` on debian/ubuntu:

```bash
sudo apt-get install apache2-utils
```

To create user run the following command in terminal (replace \<username\> and \<password\> with your desired credentials):

```bash
htpasswd -B -cb .htpasswd <username> <password> 
```

## API Documentation

<hr />

<iframe>
<body>
<link rel="stylesheet" type="text/css" href="https://github.com/swagger-api/swagger-ui/blob/master/dist/swagger-ui.css">

<script>
window.onload = function() {
  const ui = SwaggerUIBundle({
    url: "opennapi.json",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ]
  })

  window.ui = ui
}
</script>
<script src="https://github.com/swagger-api/swagger-ui/blob/master/dist/swagger-ui-bundle.js" ></script>
<script src="https://github.com/swagger-api/swagger-ui/blob/master/dist/swagger-ui-standalone-preset.js" ></script>
</body>
</iframe>


FFMPEG file conversion microservice API documentation

## Version: 0.1.0

**Contact information:**  
mahyarkarimi@rocketmail.com  

**License:** [MIT](https://opensource.org/license/mit/)

### /convert

#### POST
##### Summary:

Convert a media file (video or audio) and get response as stream

##### Description:

Convert a media file and return as stream

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful operation |
| 413 | file to convert is larger than upload size limit |
| 422 | Unprocessable entity when either file in body or action in query parameters is not available |

### /convert-file

#### POST
##### Summary:

Convert a media file (video or audio) and get response as file

##### Description:

Convert a media file and return as file

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful operation |
| 413 | file to convert is larger than upload size limit |
| 422 | Unprocessable entity when either file in body or action in query parameters is not available |
