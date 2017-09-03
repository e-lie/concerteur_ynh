from flask import current_app, render_template, request, url_for, jsonify, redirect
from contextlib import closing
from .. import db, bootstrap
from ..models import Question, User, Message
from .forms import AddQuestionForm, AddMessageForm
from ..acapelaVaas import get_acapela_sound
from . import main

import shutil
import parse
import re
import os


@main.route('/')
def concerteur_home():
    #print(main.template_folder)
    #print(main.static_folder)
    return render_template('home.html')

@main.route('/add-question', methods=['GET', 'POST'])
def add_question():
    question = None
    form = AddQuestionForm()
    if form.validate_on_submit():
        #change current question to false before adding the new current question
        currQuestion = db.session.query(Question).filter(Question.current==True).first()
        if currQuestion:
            currQuestion.current = False
            db.session.add(currQuestion)
        question = Question(title=form.title.data, text=form.text.data, current=True)

        form.title.data = ''
        form.text.data = ''

        db.session.add(question)
        db.session.commit()

        #name is <id>_<title>_<timestamp_iso>
        name = '{}_{}_{}'.format(question.id, question.title, question.time_created.isoformat())
        #remove problematic characters because this is a path
        question.archive_name = re.sub('[^\w\-_\.]', '-', name)

        #create archive directory
        dirpath = '{}/{}'.format(current_app.config['QUESTION_ARCHIVE_DIR'], question.archive_name)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        question.audio_path = re.sub('[^\w\-_\.]', '-', name) + '.mp3'

        mp3_path = current_app.config['MP3_DIR'] + '/' + question.audio_path
        mp3_archive_path = "{}/{}".format(dirpath, question.audio_path)
        messages_archive_file = '{}/{}/{}'.format( current_app.config['QUESTION_ARCHIVE_DIR'], question.archive_name, current_app.config['MESSAGES_ARCHIVE_FILENAME'])

        mp3_sound = get_acapela_sound(message=question.text, voice_id='Celine')
        with open(mp3_path, 'wb+') as mp3:
            mp3.write(mp3_sound)
        with open(mp3_archive_path, 'wb+') as archive_mp3:
            archive_mp3.write(mp3_sound)

        with open(messages_archive_file, 'a') as messages_file:
            messages_file.write('Question : {}\n\n{}\n\n{}\n------\n'.format(question.title, question.audio_path, question.text))

        archive_dirpath = '{}/{}'.format(current_app.config['QUESTION_ARCHIVE_DIR'], question.archive_name)
        messages_archive_file = '{}/{}'.format( archive_dirpath, current_app.config['MESSAGES_ARCHIVE_FILENAME'])
        zippath = current_app.config['ZIP_DIR']+'/'+question.archive_name
        shutil.make_archive(zippath,'zip',archive_dirpath)

        db.session.commit()
        return redirect(url_for('.messages'))

    return render_template('add_question.html', form=form )

    
@main.route('/messages')
def messages():
    questions = db.session.query(Question).order_by(Question.time_created.desc()).all()
    return render_template('messages.html', questions=questions)
    
@main.route('/trash')
def trash():
    questions = db.session.query(Question).order_by(Question.time_created.desc()).all()
    return render_template('trash.html', questions=questions)


#TODO add authentification for security
@main.route('/add-message', methods=['GET', 'POST'])
def add_sms():

    form = AddMessageForm()
    if request.method == 'GET':
        return render_template('add_message.html', form=form)

    else:
        question = db.session.query(Question).filter(Question.current==True).first()

        if question:
            #FIXME install hashlib and use sha1 for this hash
            hashNum = hash(request.form['num'])
            message = Message(text=request.form['text'], question_id=question.id)
            user = db.session.query(User).filter(User.numHash==hashNum).first()
            if not user:
                user = User(hashNum, message)
            else:
                user.messages.append(message)

            db.session.add(user)
            db.session.add(message)
            db.session.commit()
            
            #create a unique filename (id + timestamp + hash of the sender number)
            #to link the "message" entry to a mp3 file on the server
            mp3_name = message.id.__str__() + '_' + message.time_created.isoformat() + '_' + user.numHash.__str__() + '.mp3'
            mp3_path = current_app.config['MP3_DIR'] + '/' + mp3_name
            mp3_archive_path = '{}/{}/{}'.format( current_app.config['QUESTION_ARCHIVE_DIR'], question.archive_name, mp3_name)
            messages_archive_file = '{}/{}/{}'.format( current_app.config['QUESTION_ARCHIVE_DIR'], question.archive_name, current_app.config['MESSAGES_ARCHIVE_FILENAME'])

            message.audio_path = mp3_name

            #synthesize the sound using acapela voice as a service
            # and create the file at that mp3 path
            num = current_app.config['CREDENTIAL_NUM']
            loginUser = current_app.config['CREDENTIALS'][num]['loginUser']
            loginPassword = current_app.config['CREDENTIALS'][num]['loginPassword']

            #rotate against multiple credentials saved in list in config
            if num < len(current_app.config['CREDENTIALS']):
                current_app.config['CREDENTIAL_NUM'] = min(current_app.config['CREDENTIAL_NUM']+1,len(current_app.config['CREDENTIALS'])-1)
            else:
                current_app.config['CREDENTIAL_NUM'] = 0

            mp3_sound = get_acapela_sound(message=message.text, voice_id='Mathieu')
            with open(mp3_path, 'wb+') as mp3:
                mp3.write(mp3_sound)
            with open(mp3_archive_path, 'wb+') as archive_mp3:
                archive_mp3.write(mp3_sound)

            with open(messages_archive_file, 'a') as messages_file:
                messages_file.write('{}\n\n{}\n------\n'.format(message.audio_path, message.text))

            archive_dirpath = '{}/{}'.format(current_app.config['QUESTION_ARCHIVE_DIR'], question.archive_name)
            zippath = current_app.config['ZIP_DIR']+'/'+question.archive_name
            shutil.make_archive(zippath,'zip',archive_dirpath)

            db.session.add(message)
            db.session.commit()
            
            #return "<h1>{}: {}</h1>".format(hashNum, request.form['text'])
            return redirect(url_for('.messages'))

        else:
            erreur = "Erreur : pas de question disponible pour ajouter des messages"
            print( erreur )
            return erreur


@main.route('/change_question/<message_num>', methods=['GET'])
def change_question(message_num):
    new_question = db.session.query(Question).filter(Question.id == int(message_num)).first()
    old_question = db.session.query(Question).filter(Question.current == True).first()
    if new_question:
        new_question.current = True
        old_question.current = False
        db.session.add(new_question)
        db.session.add(old_question)
        db.session.commit()

    return redirect(url_for('.messages'))


@main.route('/trash-message/<message_num>', methods=['GET'])
def trash_message(message_num):
    message = db.session.query(Message).filter(Message.id == message_num).first()
    message.trashed = True
    db.session.add(message)
    db.session.commit()
    #return 'Message {} mis à la poubelle. <br> <a href="{}">retour</a>'.format(message_num, url_for('.messages'))
    return redirect(url_for('.messages'))



@main.route('/untrash-message/<message_num>', methods=['GET'])
def untrash_message(message_num):
    message = db.session.query(Message).filter(Message.id == message_num).first()
    message.trashed = False
    db.session.add(message)
    db.session.commit()
    return redirect(url_for('.trash'))
    


@main.route('/del-message/<message_num>', methods=['GET'])
def del_message(message_num):
    message = db.session.query(Message).filter(Message.id == message_num).first()

    db.session.delete(message)
    db.session.commit()

    if message.audio_path:
        mp3_path = current_app.config['MP3_DIR'] + '/' +  message.audio_path
        os.remove(mp3_path)

    #return 'Message {} supprimé. <br> <a href="{}">retour</a>'.format(message_num, url_for('.trash'))
    return redirect(url_for('.trash'))



@main.route('/update-status', methods=['POST'])
def update_status():
    print(current_app.config['UPDATE_STATUS'])
    signature = request.form['signature']
    if (current_app.config['UPDATE_STATUS'] and
            signature not in current_app.config['CLIENT_STACK']):
        current_app.config['CLIENT_STACK'].append(signature)
        if len(current_app.config['CLIENT_STACK']) >= current_app.config['CLIENT_NUMBER']:
            current_app.config['UPDATE_STATUS'] = False
            current_app.config['CLIENT_STACK'] = []
        data = { 'update_status': True }
    else:
        data = { 'update_status': False }
    return jsonify(data)



@main.route('/set-refresh', methods=['GET'])
def set_refresh():
    current_app.config['UPDATE_STATUS'] = True
    return redirect(url_for('.messages'))



@main.route('/activate-question', methods=['GET'])
def activate_question():
    current_app.config['QUESTION_ACTIVE'] = 1
    return redirect(url_for('.messages'))



@main.route('/deactivate-question', methods=['GET'])
def deactivate_question():
    current_app.config['QUESTION_ACTIVE'] = 0
    return redirect(url_for('.messages'))



@main.route('/get-sound-list', methods=['POST'])
def get_sound_list():
    
    refresh = request.form['refresh']
    if refresh == "True":
        refresh = True
    else:
        refresh = False
    current_question = db.session.query(Question).filter(Question.current==True).first()
    message_ids = [int(message.id) for message in current_question.messages] 

    lastfilename = request.form['lastFilename']
    if lastfilename:
        message_id = int(parse.parse("{}_{}_{}",lastfilename)[0])
    else:
        message_id = 1

    if refresh or (message_id not in message_ids): 
        filename_list = [message.audio_path for message in current_question.messages]
        if filename_list:
            data = { 'filenames':filename_list, 'lastfilename':filename_list[-1], 'refresh': True,
                     'question_active':current_app.config['QUESTION_ACTIVE'], 'question_filename':current_question.audio_path}
        else:
            data = { 'filenames':filename_list, 'lastfilename':lastfilename, 'refresh': True,
                     'question_active':current_app.config['QUESTION_ACTIVE'], 'question_filename':current_question.audio_path}
    else:
        messages_ids_to_dl = [i for i in message_ids if i > message_id]
        filenames_to_dl = [message.audio_path for message in current_question.messages if message.id in messages_ids_to_dl]
        if filenames_to_dl:
            data = { 'filenames':filenames_to_dl, 'lastfilename':filenames_to_dl[-1], 'refresh': False,
                     'question_active':current_app.config['QUESTION_ACTIVE'], 'question_filename':''}
        else:
            data = { 'filenames':filenames_to_dl, 'lastfilename':lastfilename, 'refresh': False,
                     'question_active':current_app.config['QUESTION_ACTIVE'], 'question_filename':''}

    return jsonify(data)


   # if int(message_id) < 0:
   #     message_id = 1

   # print("get_sound_list -> message_id : " + str(message_id))

   # max_id = int(db.session.query(Message.id).order_by(Message.id.desc()).first()[0])

   # print("get_sound_list -> max_id : " + str(max_id))
   # if int(message_id) > max_id:
   #     message_id = 1
   #     filename = "{}_mfoaiezjfamozife_moiefamoiezjf".format(max_id)

   # question_elem = db.session.query(Message.question_id).filter(Message.id == message_id).first()
   # question_id = -1
   # if question_elem:
   #     question_id = int(question_elem[0])
   # current_question = db.session.query(Question).filter(Question.current==True).first()

   # print(current_question.id)
   # print(question_id)
   # if question_id < current_question.id:
   #     new_question = True
   #     filename_list = [message.audio_path for message in current_question.messages]
   # else:
   #     new_question = False
   #     filename_tuples = db.session.query(Message.audio_path).filter(Message.id > message_id).all()
   #     filename_list = [tupl[0] for tupl in filename_tuples]
   #     print(filename_list)

   # 
   # if filename_list:
   #     data = { 'new_question':new_question, 'filenames':filename_list, 'lastfilename':filename_list[-1]}
   # else:
   #     data = { 'new_question':new_question, 'filenames':filename_list, 'lastfilename':filename}
   #     print(jsonify(data))
   # return jsonify(data)

@main.route('/get-sound', methods=['POST'])
def get_sound():
    filename = request.form['soundname']
    mp3Url = 'mp3' + '/' + filename
    return main.send_static_file(mp3Url)

