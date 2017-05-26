import imaplib, email
from parse import parse
from urllib import urlencode
from urllib2 import urlopen
import quopri
from email.header import decode_header

IMAP_USER = 'concerteur'
IMAP_PWD = 'concerteur007'
IMAP_SERVER = 'pharmakonpc.fr'

conn = imaplib.IMAP4_SSL(IMAP_SERVER)


try:
    (retcode, capabilities) = conn.login(IMAP_USER, IMAP_PWD)
except:
    print sys.exc_info()[1]
    sys.exit(1)

conn.select('INBOX') # Select inbox or default namespace
(retcode, messages) = conn.search(None, '(UNSEEN)')
if retcode == 'OK':
    message_ids = messages[0].split()
    for message_id in message_ids:
        params = {}
        conn.store(message_id,'+FLAGS','\SEEN')
        print(message_id)
        #result, data = conn.uid('STORE', '3', '+FLAGS', '\SEEN')



        (retcode, data) = conn.fetch(message_id,'(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                subject = msg['subject']
                num = int(parse("{} +{:d}{}",subject)[1])
                params['num'] = num



        (retcode, data) = conn.fetch(message_id,'(UID BODY[TEXT])')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1]).get_payload(decode=True)
                msg = quopri.decodestring(msg)
                lines = [line for line in msg.split('\n') if not (
                    line.startswith('---=')
                    or line.startswith('Content')
                    or line.startswith('Received')
                    or line.startswith('\r')
                    or line.startswith('--=\r')
                    or line.startswith('--\r')
                    )]

                text = "\n".join(lines)
                params['text'] = text
    
        print(params)
        #Local POST request to the flask app using a custom port
        url = 'https://pharmakonpc.fr/add-message'

        # Encode the query string
        querystring = urlencode(params)

        # Make a POST request and read the response
        req = urlopen(url, querystring.encode('utf-8'))

        #conn.store(message_id, '+FLAGS', '\\Deleted')
    #conn.expunge()



conn.close()
