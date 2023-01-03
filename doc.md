## Detection

**POST /detect**

_Json Request:_

`{ "domain": "aosadanxikojdadxa.com" }
`

_Curl Request:_ 

`curl --location --request POST 'http://localhost:5000/detect'
--header 'Content-Type: application/json'
--data-raw '{
    "domain": "aosadanxikojdadxa.com"
}'`

_Sample Response:_

200 OK 7 ms 203 B

    { 
        "DGA": "True",
        "probability": "0.9130" 
    }

**POST /bulk/path**

_Body form-data Request:_

| Key           | Key Type | Value                                     |
|---------------|----------|-------------------------------------------|
| require       | text     | {"plgid": "20468", "Question_Type": "A" } |
| search_keys   | text     | dhost, src_ip, dst_ip                     |
| path          | text     | /path_to_file/x_20468.log                 |
| predict_param | text     | dhost                                     |

_Curl Request:_

`curl --location --request POST 'http://localhost:5000/bulk/path'
--form 'require="{\"plgid\": \"20468\",
\"Question_Type\": \"A\"
}";type=application/json'
--form 'search_keys="dhost, src_ip, dst_ip"'
--form 'path="/path_to_file/x_20468.log"'
--form 'predict_param="dhost"'`

_Sample Response:_

200 OK 1069 ms 186 B

    { 
        "status": "success" 
    }

**POST /bulk/file**


_Body form-data Request:_

| Key           | Key Type | Value                                     |
|---------------|----------|-------------------------------------------|
| require       | text     | {"plgid": "20468", "Question_Type": "A" } |
| search_keys   | text     | dhost, src_ip, dst_ip                     |
| file          | file     | choose file                               |
| predict_param | text     | dhost                                     |

_Curl Request:_

`curl --location --request POST 'http://localhost:5000/bulk/file'
--form 'file=@"/path_to_file/x_20468.log"'
--form 'require="{\"plgid\": \"20468\",
\"Question_Type\": \"A\"
}";type=application/json'
--form 'search_keys="dhost, src_ip, dst_ip"'
--form 'predict_param="dhost"'`

_Sample Response:_

200 OK 1419 ms 186 B

    { 
        "status": "success" 
    }


## Information

**POST /get_labels/path**

_Body form-data Request:_

| Key     | Key Type | Value                                     |
|---------|----------|-------------------------------------------|
| require | text     | {"plgid": "20468", "Question_Type": "A" } |
| path    | text     | /path_to_file/x_20468.log                 |

_Curl Request:_

`curl --location --request POST 'http://localhost:5000/get_labels/path'
--form 'require="{\"plgid\": \"20468\",
\"Question_Type\": \"A\"
}";type=application/json'
--form 'path="/path_to_file/x_20468.log"'
`

_Sample Response:_

200 OK 730 ms 460 B

    [  "plgid",
        "ts",
        "catid",
        "catsvr",
        "date1",
        "Thread_ID",
        "context",
        "Internal_packet_identifier",
        "proto",
        "Send_Receive_indicator",
        "src_ip",
        "dst_ip",
        "dhost" ]

**POST /get_labels/file**

_Body form-data Request:_

| Key     | Key Type | Value                                     |
|---------|----------|-------------------------------------------|
| require | text     | {"plgid": "20468", "Question_Type": "A" } |
| file    | file     | choose file                               |

_Curl Request:_

`curl --location --request POST 'http://localhost:5000/get_labels/file'
--form 'file=@"/path_to_file/x_20468.log"'
--form 'require="{\"plgid\": \"20468\",
\"Question_Type\": \"A\"
}";type=application/json'
`

_Sample Response:_

200 OK 902 ms 460 B

    [ "plgid",
        "ts",
        "catid",
        "catsvr",
        "date1",
        "Thread_ID",
        "context",
        "Internal_packet_identifier",
        "proto",
        "Send_Receive_indicator",
        "src_ip",
        "dst_ip",
        "dhost" ]

**GET /whitelists/list**

_Curl Request:_

`curl --location --request GET 'http://localhost:5000/whitelist/list'`

_Sample Response:_

200 OK 7 ms 200 B

    {
    "White_Lists": [
        "white_list_1654517798.txt",
        "white_list_1654516688.txt",
        "white_list.txt"
        ]
    }

## Configuration

**GET /configuration**

_Curl Request:_

`curl --location --request GET 'http://localhost:5000/whitelist/list'`

_Sample Response:_

    {
        "current_list": "white_list.txt"
    }


**POST /configuration**

_Json Request:_

`{
    "model": "white_list_1654516688.txt"
}`

_Curl Request:_

`curl --location --request POST 'http://localhost:5000/configuration'
--header 'Content-Type: application/json'
--data-raw '{
    "model": "white_list_1654516688.txt"
}'`

_Sample Response:_

    {
        "current_list": "white_list_1654516688.txt",
        "old_list": "white_list.txt"
    }

**GET /whitelist/content**

_Curl Request:_

`curl --location --request GET 'http://localhost:5000/whitelist/content'
--header 'Content-Type: application/json'
--data-raw '{
    "model": "white_list_1654516688.txt"
}'`

_Sample Response:_

    [
        "google.com",
        "akamaiedge.net",
        "facebook.com",
        "youtube.com",
        "gtld-servers.net",
        "netflix.com",
        "microsoft.com",
        "instagram.com",
        "twitter.com",
        "akamai.net",
        "baidu.com",
        "amazonaws.com"
    ]

**POST /set_whitelist/file**

_Body form-data Request:_

| Key  | Key Type | Value       |
|------|----------|-------------|
| file | file     | choose file |

_Curl Request:_

`curl --location --request POST 'http://localhost:5000/set_whitelist/file'
--form 'file=@"/home/suedagulgun/Desktop/white_list_test.txt"'`

_Sample Response:_

    {
        "status": "success"
    }

**POST /set_whitelist/path**

_Body form-data Request:_

| Key  | Key Type | Value                     |
|------|----------|---------------------------|
| path | text     | /path_to_file/x_20468.log |

_Curl Request:_

`
curl --location --request POST 'http://localhost:5000/set_whitelist/path'
--form 'path="/path_to_file/x_20468.log"'
`

_Sample Response:_

    {
        "status": "success"
    }