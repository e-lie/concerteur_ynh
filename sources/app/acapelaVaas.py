from urllib import request, parse


def get_acapela_sound(message, url='http://vaas.acapela-group.com/Services/Synthesizer',
                    loginType='EVAL_VAAS', loginUser='EVAL_7824973',
                    loginPassword='dbhukc6j', voice='anais22k', requestType='SOUND'):

    params = {
    'cl_login' : loginType,
    'cl_app' : loginUser,
    'cl_pwd' : loginPassword,
    'req_voice' : voice,
    'req_text' : message,
    'req_asw_type' : requestType  
    }


    # Encode the query string
    querystring = parse.urlencode(params)

    # Make a POST request and read the response
    u = request.urlopen(url, querystring.encode('ascii'))
    mp3Response = u.read()

    return mp3Response



if __name__ == "__main__":
    
    with open('lastmessage.txt', 'r') as sms:
        mp3Response = getAcapelaSound(message=sms.read())

    with open('message_anais.mp3', 'wb') as f:
        f.write(mp3Response)
