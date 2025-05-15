from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UserSettingsForm(FlaskForm):
    discord_channel_id = StringField('Discord Channel ID', validators=[DataRequired()])
    tiktok_username = StringField('TikTok Username', validators=[DataRequired()])
    submit = SubmitField('Save Settings')
