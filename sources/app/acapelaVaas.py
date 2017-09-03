from urllib import request, parse
from boto3 import client
import boto3
from contextlib import closing


def get_acapela_sound(message, end_point='us-east-1', output_format='mp3', voice_id='Celine'):

    #params = {
    #'cl_login' : loginType,
    #'cl_app' : loginUser,
    #'cl_pwd' : loginPassword,
    #'req_voice' : voice,
    #'req_text' : message,
    #'req_asw_type' : requestType  
    #}

    polly = client("polly", end_point )
    response = polly.synthesize_speech(
        Text=message,
        OutputFormat=output_format,
        VoiceId=voice_id)

    print(response["AudioStream"])
    data = ''
    with closing(response["AudioStream"]) as stream:
        data = stream.read()

    return data

    #if "AudioStream" in response:
    #with closing(response["AudioStream"]) as stream:
    #data = stream.read()
    #fo = open("pollytest.mp3", "wb+")
    #fo.write( data )
    #fo.close()


    ## Encode the query string
    #querystring = parse.urlencode(params)

    ## Make a POST request and read the response
    #u = request.urlopen(url, querystring.encode('ascii'))
    #mp3Response = u.read()

    #return mp3Response



if __name__ == "__main__":
    
    with open('lastmessage.txt', 'r') as sms:
        mp3Response = getAcapelaSound(message=sms.read())

    with open('message_anais.mp3', 'wb') as f:
        f.write(mp3Response)
