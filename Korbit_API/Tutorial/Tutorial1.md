#Korbit API Tutorial
--------------------
    Warning: Before you start, Read following Link
    https://bitbucket.org/korbit/korbit-api/wiki/Home
>##How to Start
>1. Create API Key
>Public API는 로그인 없이 사용 가능하지만, 기능이 제한적(시세 조회 등)이므로 실제 거래를 하기 위해서는 Private Key를 생성하여 Private API를 이용할 수 있어야 한다. 이를 위한 API Key 생성법을 설명한다.
>>A. 일단 아래의 사이트에 로그인 한 후 API 키를 신청한다.
>>B. 신청이 완료되면 아래 그림과 같이 Key 및 Secret를 얻을 수 있다.
>>![Figure 1](http://likevinci.iptime.org/everybody/Haroo/Figure%201_API%20Key%20and%20Secret.JPG)
>2. Getting Access Key
>API Key, Secret를 모두 얻었다면 실제 API를 이용한 거래를 하기 위하여 Access Token을 얻어야 한다. 이 때 얻은 Access Token은 얻은 후 1시간 후에 만료되므로 1시간 이내에 Refresh Token을 사용하여 Access Token을 갱신하여야 한다.
>Access Token은 아래의 URL에 접속하여 획득 가능하다.
>
	POST https://api.korbit.co.kr/v1/oauth2/access_token

>이 경우 POST로 아래 데이터를 추가로 제공하여야 한다.
>
    client_id=<CLIENT ID>&client_secret=<CLIENT SECRET>&username=<이메일주소&password=<암호>&grant_type=password
>
>Client ID는 API Key를, Client Secret은 API Secret을, username은 로그인시 사용하는 사용자 ID를, password는 로그인 Password를 말한다.
>
>이를 Python 코드로 간단히 나타내면 아래와 같다.
>API KEY : fG4rUqTg
>Secret : 9m4GImYJHHxBHiEvQu7sY1pPZn9
>ID : ABC@korea.ac.kr
>PW : veryhardpassword
>로 가정하였다.
>
    conn = httplib.HTTPSConnection("api.korbit.co.kr")
	par = "client_id=" + "fG4rUqTg" + "&client_secret=" + "9m4GImYJHHxBHiEvQu7sY1pPZn9" + "&username=" + "ABC@korea.ac.kr" + "&password=" + "veryhardpassword" + "&grant_type=password"
	hdr = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn.request("POST","/v1/oauth2/access_token",par,hdr)
    resp = conn.getresponse()

>이제 여기서 얻은 Access Token을 이용하여 거래를 수행할 수 있다.