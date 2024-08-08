# Guide about API endpoint

## admin credential

- username: `davanntet`
- email: `davanntet@gmail.com`
- password: `Cb.u<shq='?6_j5@QZna#9`

## Authentication

### login

- api/auth/login/ : (`POST`)<-(username,password)

### generate secret key to use for access chatbot api

- /api/secretkey/ : (`POST`)<-(name),(`DELETE`)<-(id),(`PUT`)<-(id,name)

## How to use Authentication

### Use Token

Authorization: Token `replace your_token here`

- Example: Authorization = `Token bb706e779ee7455a0670b0c0c897d952feb3ee20`

### Use Secret-Key for API chatbot

Authorization: `replace secret_key here`

- Example: Authorization = `=awqh*9(s8m62anda-%pp1j3k$!v7(m#wx1z)p2um7c*7ykp&j`

## Manage data for training model

### upload data

- api/data : (`POST`)

### list data

- api/data : (`GET`)

### download data

- api/data/download?filename=`file_name` : (`GET`)
- Example: api/data/download?filename=`admission_1718196024.9245794.csv`

### delete data

- api/data??filename=`file_name` : (`DELETE`)

## Manage Model

### List all models

- api/model/manage : `GET`

### Upload the model

- api/model/upload : `POST`<-(file:attach a file,module_type)

### Delete the model

- api/model/delete?filename=`name of model want to delete` : `DELETE`

### Change model for response

- api/model/change : `POST`<-(modelname)
