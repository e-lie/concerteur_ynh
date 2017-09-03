from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import Required

class AddQuestionForm(Form):
    title = StringField('Titre de la question', validators=[Required()])
    text = TextAreaField('Texte de la question', validators=[Required()])
    submit = SubmitField('Submit')

class AddMessageForm(Form):
    num = StringField("numéro de téléphone de l'émetteur (33634354637 pour un portable)", validators=[Required()])
    text = TextAreaField('Texte du message', validators=[Required()])
    submit = SubmitField('Submit')
