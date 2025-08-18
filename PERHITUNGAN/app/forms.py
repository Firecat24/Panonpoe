from flask_wtf              import FlaskForm
from wtforms                import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators     import DataRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file         import FileField, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=12), Regexp(r'^[a-zA-Z0-9_]+$', message="Username hanya boleh mengandung huruf, angka, dan garis bawah.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), Regexp('^[^\s]+$', message="Password tidak boleh mengandung spasi")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Password tidak sama")])
    submit = SubmitField('Daftarkan Sekarang !!')

class login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=12)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

class lupa_password(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Kirim Link')

class recovery_password(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), Regexp('^[^\s]+$', message="Password tidak boleh mengandung spasi")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Password tidak sama")])
    submit = SubmitField('Ganti Password')

class hasil_pengamatan(FlaskForm):
    judul = StringField('Judul', validators=[DataRequired(), Length(min=2, max=20)])
    deskripsi = TextAreaField('Deskripsi', validators=[DataRequired()])
    lokasi = StringField('Lokasi', validators=[DataRequired()])
    gambar = FileField('Gambar', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    kategori = SelectField('Kategori Gambar', validators=[DataRequired()], choices=[('benda_langit', 'Benda Langit'),('planet', 'Planet'),('bintang', 'Bintang'),('hilal', 'Hilal'),('fajar', 'Fajar'),('matahari', 'Matahari')])
    submit = SubmitField('Kirim Postingan')

class edit_hasil_pengamatan(FlaskForm):
    judul = StringField('Judul', validators=[DataRequired(), Length(min=2, max=20)])
    deskripsi = TextAreaField('Deskripsi', validators=[DataRequired()])
    lokasi = StringField('Lokasi', validators=[DataRequired()])
    gambar = FileField('Gambar', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    kategori = SelectField('Kategori Gambar', validators=[DataRequired()], choices=[('benda_langit', 'Benda Langit'),('planet', 'Planet'),('bintang', 'Bintang'),('hilal', 'Hilal'),('fajar', 'Fajar'),('matahari', 'Matahari')])
    submit = SubmitField('Edit Postingan')
