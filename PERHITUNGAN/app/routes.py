import math, mysql.connector, time, os, uuid, random, requests

from itsdangerous           import SignatureExpired, BadSignature
from werkzeug.utils         import secure_filename
from werkzeug.security      import generate_password_hash, check_password_hash
from calendar               import monthrange, calendar
from datetime               import datetime, timedelta
from flask                  import render_template, request, redirect, session, send_file, url_for, flash, jsonify
from flask_login            import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app                    import app, util, config, db, auth, forms
from hijri_converter        import convert
from flask_mail             import Message


#-----------------------------------------------------------------------------------------------------------#


@app.route("/", methods=["get"])
def index():
    session.clear ()

    return redirect("/home")


#-----------------------------------------------------------------------------------------------------------#


#ADMIN AREA
@app.route("/anonymous", methods=["get"])
def anonymous():
        return redirect("/home")


#-----------------------------------------------------------------------------------------------------------#


#HOME
@app.route("/home", methods=["get", "post"])
def home():
    if request.method == "POST" and 'lintangjson' not in session:
        #ambil data
        data = request.get_json()
        lintang = data.get('lintang')
        bujur = data.get('bujur')
        zona_waktu1 = data.get("timezone")
        geocode_url = f'https://nominatim.openstreetmap.org/reverse?lat={lintang}&lon={bujur}&format=json'

        headers = {'User-Agent': 'labfalak/1.0 (landahcuu@gmail.com)'}
        response = requests.get(geocode_url, headers=headers)
        geolocation_data = response.json()
        prov = geolocation_data.get('address', {}).get('city', 'Unknown')
        kota = kota = geolocation_data.get('address', {}).get('city') or geolocation_data.get('address', {}).get('county') or 'Unknown'
        negara = geolocation_data.get('address', {}).get('country', 'Unknown')

        #perhitungan salat
        now = datetime.now()
        Tahun = now.year
        Bulan = now.month
        day = now.day
        zona_waktu = zona_waktu1 * 15

        KWD = ((zona_waktu - bujur)/15) 
        date = datetime(Tahun, Bulan, day)
        tanggal = util.convert_date(date)

        pk, pk1, pk2, pk3, pk4 = util.waktu_salat_fardhu_dan_lain(day, Bulan, Tahun, lintang, bujur, KWD)

        jams, menits = util.hasil(pk)
        subuh = util.format_time(jams, menits)

        jams, menits = util.hasil(pk)
        total_menits = jams * 60 + menits - 10
        new_jams = total_menits // 60
        new_menits = total_menits % 60
        imsak = util.format_time(new_jams, new_menits)

        jams, menits = util.hasil(pk1)
        zuhur = util.format_time(jams, menits)

        jams, menits = util.hasil(pk2)
        asar = util.format_time(jams, menits)

        jams, menits = util.hasil(pk3)
        magrib = util.format_time(jams, menits)

        jams, menits = util.hasil(pk4)
        isya = util.format_time(jams, menits)

        #perhitungan umum
        #perhitungan delta T
        delta_T = util.deltaT(Tahun, Bulan)

        #konversi tanggal
        hijriah = convert.Gregorian(Tahun, Bulan, day).to_hijri()
        hijriah1 = (f"{hijriah.day} {hijriah.month_name()} {hijriah.year} H")

        #fungsi new moon
        jam_bulan_baru, tanggal_bulan_baru, bulan_bulan_baru, tahun_bulan_baru = util.new_moon(hijriah.month, hijriah.year, delta_T, zona_waktu1)

        tanggal0 = datetime(tahun_bulan_baru, bulan_bulan_baru, tanggal_bulan_baru)

        tanggal_bulan_baru = util.convert_date(tanggal0)
        waktu_bulan_baru = util.jam_konvert_template(jam_bulan_baru)

        #fungsi quartal 1
        jam_quartal1, tanggal_quartal1, bulan_quartal1, tahun_quartal1 = util.quartal_pertama(hijriah.month, hijriah.year, delta_T, zona_waktu1)

        tanggal1 = datetime(tahun_quartal1, bulan_quartal1, tanggal_quartal1)

        tanggal_quartal1 = util.convert_date(tanggal1)
        waktu_quartal1 = util.jam_konvert_template(jam_quartal1)

        #fungsi full moon
        jam_bulan_purnama, tanggal_bulan_purnama, bulan_bulan_purnama, tahun_bulan_purnama = util.full_moon(hijriah.month, hijriah.year, delta_T, zona_waktu1)

        tanggal2 = datetime(tahun_bulan_purnama, bulan_bulan_purnama, tanggal_bulan_purnama)

        tanggal_bulan_purnama = util.convert_date(tanggal2)
        waktu_bulan_purnama = util.jam_konvert_template(jam_bulan_purnama)

        #fungsi quartal 3
        jam_quartal3, tanggal_quartal3, bulan_quartal3, tahun_quartal3 = util.quartal_akhir(hijriah.month, hijriah.year, delta_T, zona_waktu1)

        tanggal3 = datetime(tahun_quartal3, bulan_quartal3, tanggal_quartal3)

        tanggal_quartal3 = util.convert_date(tanggal3)
        waktu_quartal3 = util.jam_konvert_template(jam_quartal3)

        session['lintangjson'] = lintang
        session['bujurjson'] = bujur
        session['zona_waktu1json'] = zona_waktu1
        session['kotajson'] = kota
        session['provjson'] = prov
        session['negarajson'] = negara
        session['tanggaljson'] = tanggal
        session['tanggal_quartal1json'] = tanggal_quartal1
        session['waktu_quartal1json'] = waktu_quartal1
        session['tanggal_quartal3json'] = tanggal_quartal3
        session['waktu_quartal3json'] = waktu_quartal3
        session['tanggal_bulan_purnamajson'] = tanggal_bulan_purnama
        session['waktu_bulan_purnamajson'] = waktu_bulan_purnama
        session['tanggal_bulan_barujson'] = tanggal_bulan_baru
        session['tanggal_hijriahjson'] = hijriah1
        session['waktu_bulan_barujson'] = waktu_bulan_baru
        session['imsakjson'] = imsak
        session['subuhjson'] = subuh
        session['zuhurjson'] = zuhur
        session['asarjson'] = asar
        session['magribjson'] = magrib
        session['isyajson'] = isya

        return jsonify(({"prov" : prov, "city": kota, "country": negara, "tanggal": tanggal, "tanggal_quartal1" : tanggal_quartal1, "waktu_quartal1" : waktu_quartal1, "tanggal_bulan_baru" : tanggal_bulan_baru, "waktu_bulan_baru" : waktu_bulan_baru, "tanggal_quartal3" : tanggal_quartal3, "waktu_quartal3" : waktu_quartal3, "tanggal_bulan_purnama" : tanggal_bulan_purnama, "waktu_bulan_purnama" : waktu_bulan_purnama, "tanggal_hijriah" : hijriah1, "imsak":imsak, "subuh":subuh, "zuhur":zuhur,"asar":asar, "magrib":magrib, "isya":isya}))

    elif 'lintangjson' in session:
        lintang = session['lintangjson']
        bujur = session['bujurjson']
        zona_waktu1 = session['zona_waktu1json']
        kota = session['kotajson']
        prov = session['provjson']
        negara = session['negarajson']
        tanggal = session['tanggaljson']
        waktu_quartal1 = session['waktu_quartal1json']
        waktu_quartal3 = session['waktu_quartal3json']
        waktu_bulan_baru = session['waktu_bulan_barujson']
        waktu_bulan_purnama = session['waktu_bulan_purnamajson']
        tanggal_quartal1 = session['tanggal_quartal1json']
        tanggal_quartal3 = session['tanggal_quartal3json']
        tanggal_bulan_baru = session['tanggal_bulan_barujson']
        tanggal_bulan_purnama = session['tanggal_bulan_purnamajson']
        hijriah1 = session['tanggal_hijriahjson']
        imsak = session['imsakjson']
        subuh = session['subuhjson']
        zuhur = session['zuhurjson']
        asar = session['asarjson']
        magrib = session['magribjson']
        isya = session['isyajson']

        if 'username' in session:
            username = session['username']
            c = db.koneksi_database()
            cursor = c.cursor(dictionary=True)
            cursor.execute("SELECT gambar FROM galeri")
            gambar = cursor.fetchall()
            cursor.close()
            c.close()
            gambar = random.choice(gambar)['gambar']

            return render_template("dashboard.html", username=username, gambar = gambar, imsak=imsak,subuh=subuh,zuhur=zuhur,asar=asar,magrib=magrib,isya=isya, kota=kota, negara=negara, prov = prov, tanggal=tanggal, tanggal_quartal1 = tanggal_quartal1, waktu_quartal1 = waktu_quartal1, tanggal_bulan_baru = tanggal_bulan_baru, waktu_bulan_baru = waktu_bulan_baru, tanggal_quartal3 = tanggal_quartal3, waktu_quartal3 = waktu_quartal3, tanggal_bulan_purnama = tanggal_bulan_purnama, waktu_bulan_purnama = waktu_bulan_purnama, tanggal_hijriah = hijriah1)

        else:
            c = db.koneksi_database()
            cursor = c.cursor(dictionary=True)
            cursor.execute("SELECT gambar FROM galeri")
            gambar = cursor.fetchall()
            cursor.close()
            c.close()
            gambar = random.choice(gambar)['gambar']

            return render_template("dashboard.html", gambar = gambar, imsak=imsak,subuh=subuh,zuhur=zuhur,asar=asar,magrib=magrib,isya=isya, kota=kota, negara=negara, prov = prov, tanggal=tanggal, tanggal_quartal1 = tanggal_quartal1, waktu_quartal1 = waktu_quartal1, tanggal_bulan_baru = tanggal_bulan_baru, waktu_bulan_baru = waktu_bulan_baru, tanggal_quartal3 = tanggal_quartal3, waktu_quartal3 = waktu_quartal3, tanggal_bulan_purnama = tanggal_bulan_purnama, waktu_bulan_purnama = waktu_bulan_purnama, tanggal_hijriah = hijriah1)

    else:
        lintang = -7.15
        bujur = 112.45
        zona_waktu1 = 7
        kota = "Surabaya"
        prov = "Jawa Timur"
        negara = "Indonesia"

        #perhitungan salat
        now = datetime.now()
        Tahun = now.year
        Bulan = now.month
        day = now.day
        zona_waktu = zona_waktu1 * 15

        KWD = ((zona_waktu - bujur)/15) 
        date = datetime(Tahun, Bulan, day)
        tanggal = util.convert_date(date)

        pk, pk1, pk2, pk3, pk4 = util.waktu_salat_fardhu_dan_lain(day, Bulan, Tahun, lintang, bujur, KWD)

        jams, menits = util.hasil(pk)
        subuh = util.format_time(jams, menits)

        jams, menits = util.hasil(pk)
        total_menits = jams * 60 + menits - 10
        new_jams = total_menits // 60
        new_menits = total_menits % 60
        imsak = util.format_time(new_jams, new_menits)

        jams, menits = util.hasil(pk1)
        zuhur = util.format_time(jams, menits)

        jams, menits = util.hasil(pk2)
        asar = util.format_time(jams, menits)

        jams, menits = util.hasil(pk3)
        magrib = util.format_time(jams, menits)

        jams, menits = util.hasil(pk4)
        isya = util.format_time(jams, menits)

        #perhitungan umum
        #perhitungan delta T
        delta_T = util.deltaT(Tahun, Bulan)

        #konversi tanggal
        hijriah = convert.Gregorian(Tahun, Bulan, day).to_hijri()
        hijriah1 = (f"{hijriah.day} {hijriah.month_name()} {hijriah.year} H")

        #fungsi new moon
        jam_bulan_baru, tanggal_bulan_baru, bulan_bulan_baru, tahun_bulan_baru = util.new_moon(hijriah.month, hijriah.year, delta_T, zona_waktu1)

        tanggal0 = datetime(tahun_bulan_baru, bulan_bulan_baru, tanggal_bulan_baru)

        tanggal_bulan_baru = util.convert_date(tanggal0)
        waktu_bulan_baru = util.jam_konvert_template(jam_bulan_baru)

        #fungsi quartal 1
        jam_quartal1, tanggal_quartal1, bulan_quartal1, tahun_quartal1 = util.quartal_pertama(hijriah.month, hijriah.year, delta_T, zona_waktu1)

        tanggal1 = datetime(tahun_quartal1, bulan_quartal1, tanggal_quartal1)

        tanggal_quartal1 = util.convert_date(tanggal1)
        waktu_quartal1 = util.jam_konvert_template(jam_quartal1)

        #fungsi full moon
        jam_bulan_purnama, tanggal_bulan_purnama, bulan_bulan_purnama, tahun_bulan_purnama = util.full_moon(hijriah.month, hijriah.year, delta_T, zona_waktu1)

        tanggal2 = datetime(tahun_bulan_purnama, bulan_bulan_purnama, tanggal_bulan_purnama)

        tanggal_bulan_purnama = util.convert_date(tanggal2)
        waktu_bulan_purnama = util.jam_konvert_template(jam_bulan_purnama)

        #fungsi quartal 3
        jam_quartal3, tanggal_quartal3, bulan_quartal3, tahun_quartal3 = util.quartal_akhir(hijriah.month, hijriah.year, delta_T, zona_waktu1)

        tanggal3 = datetime(tahun_quartal3, bulan_quartal3, tanggal_quartal3)

        tanggal_quartal3 = util.convert_date(tanggal3)
        waktu_quartal3 = util.jam_konvert_template(jam_quartal3)


        if 'username' in session:
            username = session['username']
            c = db.koneksi_database()
            cursor = c.cursor(dictionary=True)
            cursor.execute("SELECT gambar FROM galeri")
            gambar = cursor.fetchall()
            cursor.close()
            c.close()
            gambar = random.choice(gambar)['gambar']

            return render_template("dashboard.html", username=username, gambar = gambar, imsak=imsak,subuh=subuh,zuhur=zuhur,asar=asar,magrib=magrib,isya=isya, kota=kota, negara=negara, prov = prov, tanggal=tanggal, tanggal_quartal1 = tanggal_quartal1, waktu_quartal1 = waktu_quartal1, tanggal_bulan_baru = tanggal_bulan_baru, waktu_bulan_baru = waktu_bulan_baru, tanggal_quartal3 = tanggal_quartal3, waktu_quartal3 = waktu_quartal3, tanggal_bulan_purnama = tanggal_bulan_purnama, waktu_bulan_purnama = waktu_bulan_purnama, tanggal_hijriah = hijriah1)

        else:
            c = db.koneksi_database()
            cursor = c.cursor(dictionary=True)
            cursor.execute("SELECT gambar FROM galeri")
            gambar = cursor.fetchall()
            cursor.close()
            c.close()
            gambar = random.choice(gambar)['gambar']

            return render_template("dashboard.html", gambar = gambar, imsak=imsak,subuh=subuh,zuhur=zuhur,asar=asar,magrib=magrib,isya=isya, kota=kota, negara=negara, prov = prov, tanggal=tanggal, tanggal_quartal1 = tanggal_quartal1, waktu_quartal1 = waktu_quartal1, tanggal_bulan_baru = tanggal_bulan_baru, waktu_bulan_baru = waktu_bulan_baru, tanggal_quartal3 = tanggal_quartal3, waktu_quartal3 = waktu_quartal3, tanggal_bulan_purnama = tanggal_bulan_purnama, waktu_bulan_purnama = waktu_bulan_purnama, tanggal_hijriah = hijriah1)


#-----------------------------------------------------------------------------------------------------------#


#gambar looping
@app.route('/get_image')
def get_data():
    c = db.koneksi_database()
    cursor = c.cursor(dictionary=True)
    cursor.execute('SELECT gambar FROM galeri')
    gambar = cursor.fetchall()
    c.close()
    gambar = random.choice(gambar)['gambar']
    return jsonify({'gambar': gambar})


#-----------------------------------------------------------------------------------------------------------#


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.login()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        c = db.koneksi_database()
        cursor = c.cursor(dictionary=True)
        cursor.execute("SELECT * FROM data_login WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        c.close()
        if user:
            if not user['isVerified']:
                token_verifikasi_email = config.keamanan_token.dumps(user['uuid'], salt='verifikasi_email')
                link_verifikasi = request.url_root + 'verifikasi_email/' + token_verifikasi_email
                print(link_verifikasi)
                # msg = Message("Verifikasi Email", recipients=[email])
                # msg.body = f"Tekan link untuk verifikasi emailmu: {link_verifikasi}"
                # config.mail.send(msg)
                flash("Kamu belum memverifikasi emailmu, check emailmu Di Bagian **SPAM**")
                return redirect(url_for('login'))
            if check_password_hash(user['password'], password) and user['isVerified']:
                user_obj = auth.User(id=user['id'], username=user['username'], password=user['password'])
                login_user(user_obj, remember = remember)
                session['username'] = username
                session['uuid'] = user['uuid']
                flash("Berhasil login")
                return redirect(url_for('home'))
            else:
                flash("Password salah, Silahkan coba kembali")
                return redirect(url_for('login'))
        else:
            flash("Username tidak ditemukan")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


#-----------------------------------------------------------------------------------------------------------#


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('uuid', None)
    logout_user()
    return redirect(url_for('home'))


#-----------------------------------------------------------------------------------------------------------#


@app.route('/daftar_login', methods=['GET', 'POST'])
def daftar_login():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.lower()
        email = form.email.data.lower()
        password = form.password.data

        # Koneksi ke database
        c = db.koneksi_database()
        cursor = c.cursor()

        try:
            # Cek apakah username atau email sudah ada
            query = "SELECT COUNT(*) FROM data_login WHERE username = %s OR email = %s"
            cursor.execute(query, (username, email))
            result = cursor.fetchone()

            if result[0] > 0:
                flash("Username atau email sudah ada yang memakai")
                return redirect(url_for('daftar_login'))

            # Jika belum ada, tambahkan pengguna baru
            uuid_user = str(uuid.uuid4())
            hashed_password = generate_password_hash(password)

            tambah_data = """
                INSERT INTO data_login (username, password, email, uuid, isVerified)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(tambah_data, (username, hashed_password, email, uuid_user, False))
            c.commit()

            # Kirim email verifikasi
            token_verifikasi_email = config.keamanan_token.dumps(uuid_user, salt='verifikasi_email')
            link_verifikasi = request.url_root + 'verifikasi_email/' + token_verifikasi_email
            print(link_verifikasi)
            # msg = Message("Verifikasi Email", recipients=[email])
            # msg.body = f"Tekan link untuk verifikasi emailmu: {link_verifikasi}"
            # config.mail.send(msg)

            flash("Silakan cek email Anda (termasuk folder SPAM) untuk verifikasi.")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Terjadi kesalahan: {e}")
            return redirect(url_for('daftar_login'))
        finally:
            # Tutup koneksi database
            cursor.close()
            c.close()

    return render_template('daftar_login.html', form=form)


#-----------------------------------------------------------------------------------------------------------#


@app.route('/verifikasi_email/<token_verifikasi_email>', methods=['GET'])
def verifikasi_email(token_verifikasi_email):
    c = db.koneksi_database()
    cursor = c.cursor(dictionary=True)
    try:
        email = config.keamanan_token.loads(token_verifikasi_email, salt = 'verifikasi_email', max_age=3600)
        cursor.execute("SELECT * FROM data_login WHERE uuid = %s", (email,))
        user = cursor.fetchone()
        update_data = "UPDATE data_login SET isVerified = %s, updatedAt = %s WHERE id = %s"
        cursor.execute(update_data, (True, datetime.now(), user['id']))
        c.commit()
        flash("Email Anda telah berhasil diverifikasi")
    except SignatureExpired:
        flash("Link verifikasi sudah kedaluwarsa!")
    except BadSignature:
        flash("Token tidak valid!")
    cursor.close()
    c.close()

    return redirect(url_for('login'))


#-----------------------------------------------------------------------------------------------------------#
#masuk ke halaman pengajuan lupa password sekalian kirim email lupa password

@app.route('/lupa_password', methods=['GET', 'POST'])
def lupa_password():
    form = forms.lupa_password()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        c = db.koneksi_database()
        cursor = c.cursor()
        cursor.execute("SELECT uuid FROM data_login WHERE username = %s AND email = %s", (username, email))
        password_record = cursor.fetchone()
        cursor.close()
        c.close()

        if password_record:
            token_reset_password = config.keamanan_token.dumps(password_record, salt='reset_password')
            link_verifikasi = request.url_root + 'recovery_password/' + token_reset_password
            print(link_verifikasi)
            # msg = Message("Reset Password", recipients=[email])
            # msg.body = f"Tekan link untuk mereset password anda: {link_verifikasi}"
            # config.mail.send(msg)

            flash("Silakan cek email Anda (termasuk folder SPAM) untuk reset password anda.")
        else:
            flash("Username tidak ditemukan")

        return redirect(url_for('login'))

    return render_template('lupa_password.html', form=form)


#-----------------------------------------------------------------------------------------------------------#


@app.route('/recovery_password/<token_reset_password>', methods=['GET','POST'])
def recovery_password(token_reset_password):
    try:
        uuid_password = config.keamanan_token.loads(token_reset_password, salt = 'reset_password', max_age=3600)
        form = forms.recovery_password()
        if form.validate_on_submit():
            c = db.koneksi_database()
            cursor = c.cursor(dictionary=True)
            ne_password = form.password.data
            new_password = generate_password_hash(ne_password)
            cursor.execute("UPDATE data_login SET password = %s WHERE uuid = %s",(new_password, uuid_password[0]))
            c.commit() 
            cursor.close()
            c.close()
            flash("Password Anda berhasil direset. Jangan lupa untuk menjaga keamanan akun Anda.")
            return redirect(url_for('login'))
        return render_template('lupa_password_recovery.html', form=form)
    except SignatureExpired:
        flash("Link sudah kedaluwarsa!")
        return redirect(url_for('lupa_password'))
    except BadSignature:
        flash("Token tidak valid!")
        return redirect(url_for('lupa_password'))


#-----------------------------------------------------------------------------------------------------------#


#peta visibilitas hilal
@app.route("/peta_visibilitas_hilal", methods=["get"])
def peta_visibilitas_hilal():

    return render_template("peta_visibilitas_hilal.html")


#-----------------------------------------------------------------------------------------------------------#


#peta elongasi
@app.route("/peta_elongasi", methods=["get"])
def peta_elongasi():

    return render_template("peta_elongasi.html")


#-----------------------------------------------------------------------------------------------------------#


#hasil pengamatan
@app.route("/hasil_pengamatan", methods=["get", "POST"])
def hasil_pengamatan():
    if 'username' in session:
        username = session['username']
        c = db.koneksi_database()
        cursor = c.cursor(dictionary=True)

        cursor.execute('SELECT * FROM galeri ORDER BY waktu DESC')
        posts = cursor.fetchall()

        cursor.execute('SELECT * FROM data_login WHERE username = %s', (username,))
        user = cursor.fetchone()

        cursor.close()
        c.close()
        return render_template("hasil_pengamatan.html", posts = posts, username = username, user=user)

    else:
        username = ""
        user = ""
        c = db.koneksi_database()
        cursor = c.cursor(dictionary=True)
        cursor.execute('SELECT * FROM galeri ORDER BY waktu DESC')
        posts = cursor.fetchall()
        cursor.close()
        c.close()

        return render_template("hasil_pengamatan.html", posts = posts, username = username, user=user)


#-----------------------------------------------------------------------------------------------------------#


#lihat postingan
@app.route("/lihat_postingan/<int:post_id>", methods=["GET","POST"])
def lihat_postingan(post_id):
    if 'username' in session:
        username = session['username']
    else:
        username = ""

    c = db.koneksi_database()
    cursor = c.cursor(dictionary=True)
    cursor.execute('SELECT * FROM galeri WHERE id = %s', (post_id,))
    posts = cursor.fetchone()
    cursor.execute('SELECT * FROM data_login WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    c.close()

    return render_template("lihat_postingan.html", posts = posts, username = username, user=user)


#-----------------------------------------------------------------------------------------------------------#


#tambah_postingan
@app.route("/tambah_postingan", methods=["get", "POST"])
@login_required
def tambah_postingan():
    if  'username' in session:
        form = forms.hasil_pengamatan()
        username = session['username']
        user_uuid = session['uuid']
        session['spam'] = session.get('spam', 0)

        waktu_terakhir_upload = session.get('waktu_terakhir_upload')
        if waktu_terakhir_upload:
            waktu_terakhir_upload = waktu_terakhir_upload.replace(tzinfo=None)

        if waktu_terakhir_upload and datetime.now() < waktu_terakhir_upload + timedelta(seconds=20):
            waktu_tunggu = (waktu_terakhir_upload + timedelta(seconds=20) - datetime.now()).total_seconds()
            if session['spam'] == 2:
                flash(f"sabar oiiiiiiii")
                session['spam'] = 0
                return redirect(url_for('hasil_pengamatan'))
            flash(f'Anda harus menunggu {int(waktu_tunggu)} detik sebelum mengunggah postingan lagi.')
            session['spam'] +=1
            return redirect(url_for('hasil_pengamatan'))
        if form.validate_on_submit():
            judul = form.judul.data
            deskripsi = form.deskripsi.data
            lokasi = form.lokasi.data
            gambar = form.gambar.data
            kategori = form.kategori.data
            waktu = datetime.now()
            gambar.seek(0, os.SEEK_END)
            file_length = gambar.tell()
            gambar.seek(0, 0)
            if file_length > 50 * 1024 * 1024:
                flash('Ukuran file maksimal adalah 50MB')
                return redirect(request.url)

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            secure_nama = secure_filename(gambar.filename)
            filename = f"{timestamp}_{secure_nama}"

            gambar_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            gambar.save(gambar_path)


            c = db.koneksi_database()
            cursor = c.cursor()
            cursor.execute('''
                INSERT INTO galeri (judul, waktu, deskripsi, lokasi, gambar, user_uuid, kategori, username)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (judul, waktu, deskripsi, lokasi, filename, user_uuid, kategori, username))
            c.commit()
            cursor.close()
            c.close()
            session['waktu_terakhir_upload'] = datetime.now()
            flash('postingan anda telah ditambahkan')
            return redirect(url_for('hasil_pengamatan'))

        return render_template("tambah_postingan.html", form = form, username = username)
        


#-----------------------------------------------------------------------------------------------------------#


#edit hasil pengamatan
@app.route("/edit_postingan/<int:post_id>", methods=["GET","POST"])
@login_required
def edit_postingan(post_id):
    username = session['username']
    c = db.koneksi_database()
    cursor = c.cursor(dictionary=True)
    cursor.execute('SELECT * FROM galeri WHERE id = %s', (post_id,))
    post = cursor.fetchone()
    post_uuid = post['user_uuid']
    cursor.close()
    c.close()
    if 'uuid' in session and (session['uuid'] == post_uuid or session['uuid'] == '31102001' or session['uuid'] == '24012002'):
        form = forms.edit_hasil_pengamatan()
        if request.method == 'GET':
            form.deskripsi.data = post['deskripsi']
            form.judul.data = post['judul']
            form.lokasi.data = post['lokasi']
            form.kategori.data = post['kategori']
        if form.validate_on_submit():
            judul = form.judul.data
            deskripsi = form.deskripsi.data
            lokasi = form.lokasi.data
            kategori = form.kategori.data
            waktu = datetime.now()
            print(judul)
            filename = post['gambar'] if 'gambar' in post else None

            if 'gambar' in request.files:
                file = request.files['gambar']
                file.seek(0, os.SEEK_END)
                file_length = file.tell()
                file.seek(0, 0)
                if file_length > 50 * 1024 * 1024:
                    flash('Ukuran file maksimal adalah 50MB')
                    return redirect(request.url)
                if file.filename != '':
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    secure_nama = secure_filename(file.filename)
                    filename = f"{timestamp}_{secure_nama}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    if 'gambar' in post and post['gambar'] != filename:
                        path_to_image = os.path.join(app.root_path, 'static', 'gambar_upload', post['gambar'])
                        if os.path.exists(path_to_image):
                            os.remove(path_to_image)
                    file.save(file_path)

            c = db.koneksi_database()
            cursor = c.cursor(dictionary=True)
            cursor.execute('UPDATE galeri SET judul = %s, waktu = %s, deskripsi = %s, lokasi=%s, gambar = %s, kategori= %s WHERE id = %s',
                           (judul, waktu, deskripsi, lokasi, filename, kategori, post_id))
            c.commit()
            cursor.close()
            c.close()
            flash("Postingan Telah Diupdate")
            return redirect(url_for("hasil_pengamatan"))

        return render_template("edit_postingan.html", post=post, form=form, username=username)
            
    flash("KAMU SIAPA KOK BISA BISANYA MAU EDIT POSTINGAN ORANG")
    return redirect(url_for("hasil_pengamatan"))


#-----------------------------------------------------------------------------------------------------------#


# hapus hasil pengamatan
@app.route("/hapus_postingan/<int:post_id>", methods=["GET","POST"])
@login_required
def hapus_postingan(post_id):
    c = db.koneksi_database()
    cursor = c.cursor(dictionary=True)
    cursor.execute('SELECT * FROM galeri WHERE id = %s', (post_id,))
    post = cursor.fetchone()
    post_uuid = post['user_uuid']
    cursor.close()
    c.close()
    if 'uuid' in session and (session['uuid'] == post_uuid or session['uuid'] == '31102001' or session['uuid'] == '24012002'):
        c = db.koneksi_database()
        cursor = c.cursor(dictionary=True)
        if post:
            path_to_image = os.path.join(app.root_path, 'static', 'gambar_upload', post['gambar'])
            if os.path.exists(path_to_image):
                    os.remove(path_to_image)
        if 'username' in session:
            cursor.execute('DELETE FROM galeri WHERE id = %s', (post_id,))
            c.commit()
            cursor.close()
            c.close()
            flash("Postingan Telah Dihapus")
            return redirect(url_for("hasil_pengamatan"))
            
    flash("KAMU SIAPA KOK BISA BISANYA MAU HAPUS POSTINGAN ORANG")
    return redirect(url_for("hasil_pengamatan"))


#-----------------------------------------------------------------------------------------------------------#


#jadwal sholat
@app.route("/jadwal_salat", methods=["get","post"])
def jadwal_salat():
    if request.method == "POST":
        results = []
        data = request.json
        lintang = data.get('latitude')
        bujur = data.get('longitude')
        zona_waktu1 = data.get('timezone')
        now = datetime.now()
        Tahun = now.year
        Bulan = now.month
        Hari = 1
        zona_waktu = zona_waktu1 * 15
        datenow = datetime(Tahun, Bulan, Hari)
        max_day = monthrange(datenow.year, datenow.month)[1]
        for day in range(1, max_day+1):
            result = []

            KWD = ((zona_waktu - bujur)/15) 
            date = datetime(Tahun, Bulan, day)
            tanggal = util.convert_date(date)

            pk, pk1, pk2, pk3, pk4 = util.waktu_salat_fardhu_dan_lain(day, Bulan, Tahun, lintang, bujur, KWD)

            jams, menits = util.hasil(pk)
            Subuh = util.format_time(jams, menits)

            jams, menits = util.hasil(pk)
            total_menits = jams * 60 + menits - 10
            new_jams = total_menits // 60
            new_menits = total_menits % 60
            imsak = util.format_time(new_jams, new_menits)

            jams, menits = util.hasil(pk1)
            Zuhur = util.format_time(jams, menits)

            jams, menits = util.hasil(pk2)
            Asar = util.format_time(jams, menits)

            jams, menits = util.hasil(pk3)
            Magrib = util.format_time(jams, menits)

            jams, menits = util.hasil(pk4)
            Isya = util.format_time(jams, menits)
            result.append(tanggal)
            result.append(Subuh)
            result.append(Zuhur)
            result.append(Asar)
            result.append(Magrib)
            result.append(Isya)
            result.append(imsak)
            results.append(result)
            tupled = tuple(results)
        return jsonify(result = results)
    
    return render_template("salat.html")


#-----------------------------------------------------------------------------------------------------------#


#website kalkulator hilal
@app.route("/kalkulator_hilal", methods=["GET","POST"])
def main_menu():
    if request.method == "GET":
        if 'username' in session:
            username = session['username']
        else:
            username = ""
        waktu_tanggal_UTC = datetime.utcnow()
        waktu_tanggal = datetime.now()
        if 'zona_waktu_now' in session:
            zona_waktu_now = session['zona_waktu_now']
        else:
            zona_waktu_now = waktu_tanggal.hour - waktu_tanggal_UTC.hour
        if 'detik_now' in session:
            detik_now = session['detik_now']
        else:
            detik_now = waktu_tanggal.second
        if 'menit_now' in session:
            menit_now = session['menit_now']
        else:
            menit_now = waktu_tanggal.minute
        if 'jam_now' in session:
            jam_now = session['jam_now']
        else:
            jam_now = waktu_tanggal.hour
        if 'tanggal_now' in session:
            tanggal_now = session['tanggal_now']
        else:
            tanggal_now = waktu_tanggal.day
        if 'bulan_now' in session:
            bulan_now = session['bulan_now']
        else:
            bulan_now = waktu_tanggal.month
        if 'tahun_now' in session:
            tahun_now = session['tahun_now']
        else:
            tahun_now = waktu_tanggal.year
        if 'lintang_detik' in session:
            lintang_detik = session['lintang_detik']
        else:
            lintang_detik = ""
        if 'lintang_menit' in session:
            lintang_menit = session['lintang_menit']
        else:
            lintang_menit = ""
        if 'lintang_jam' in session:
            lintang_jam = session['lintang_jam']
        else:
            lintang_jam = ""
        if 'bujur_detik' in session:
            bujur_detik = session['bujur_detik']
        else:
            bujur_detik = ""
        if 'bujur_menit' in session:
            bujur_menit = session['bujur_menit']
        else:
            bujur_menit = ""
        if 'bujur_jam' in session:
            bujur_jam = session['bujur_jam']
        else:
            bujur_jam = ""
        if 'tinggi_tempat' in session:
            tinggi_tempat = session['tinggi_tempat']
        else:
            tinggi_tempat = ""

        return render_template("perhitungan_posisi_hilal.html",tinggi_tempat = tinggi_tempat, lintang_detik=lintang_detik, lintang_menit=lintang_menit, lintang_jam=lintang_jam, bujur_detik=bujur_detik, bujur_menit=bujur_menit, bujur_jam=bujur_jam, detik_now=detik_now, menit_now=menit_now, jam_now=jam_now, tanggal_now=tanggal_now, bulan_now=bulan_now, tahun_now=tahun_now, zona_waktu_now=zona_waktu_now, username = username)

    elif request.method == "POST":
        if 'username' in session:
            username = session['username']
        else:
            username = ""
        detik = int(request.form["detik_waktu"])
        session['detik_now'] = detik
        menit = int(request.form["menit_waktu"])
        session['menit_now'] = menit
        jam = int(request.form["jam_waktu"])
        session['jam_now'] = jam
        tanggal = int(request.form["tanggal_waktu"])
        session['tanggal_now'] = tanggal
        bulan = int(request.form["bulan_waktu"])
        session['bulan_now'] = bulan
        tahun = int(request.form["tahun_waktu"])
        session['tahun_now'] = tahun
        zona_waktu = int(request.form["zona_waktu"])
        session['zona_waktu_now'] = zona_waktu
        lintang_detik = int(request.form["lintang_detik"])
        session['lintang_detik'] = lintang_detik
        lintang_menit = int(request.form["lintang_menit"])
        session['lintang_menit'] = lintang_menit
        lintang_jam = int(request.form["lintang_jam"])
        session['lintang_jam'] = lintang_jam
        bujur_detik = int(request.form["bujur_detik"])
        session['bujur_detik'] = bujur_detik
        bujur_menit = int(request.form["bujur_menit"])
        session['bujur_menit'] = bujur_menit
        bujur_jam = int(request.form["bujur_jam"])
        session['bujur_jam'] = bujur_jam
        tinggi_tempat = int(request.form["tinggi_tempat"])
        session['tinggi_tempat'] = tinggi_tempat
        lintang_arah = request.form["lintang_arah"]
        session['lintang_arah'] = lintang_arah
        bujur_arah = request.form["bujur_arah"]
        session['bujur_arah'] = bujur_arah

        return redirect(url_for("main_menu_dua_direct"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/cek_data", methods=["GET","POST"])
def main_menu_dua_direct():
    if 'username' in session:
        username = session['username']
    else:
        username = ""
    if 'detik_now' in session:
        if request.method == "GET":
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']
            tinggi_tempat = session['tinggi_tempat']
            #tempat eksekusi semua perhitungan dan input-an
            if lintang_arah == "U":
                lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            elif lintang_arah == "S":
                lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            if bujur_arah == "E":
                bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            elif bujur_arah == "W":
                bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            
            #perhitungan
            delta_T = util.deltaT(tahun, bulan)
            Julian_day1 = util.JD (detik, menit, jam, tanggal, bulan, tahun, zona_waktu)
            Julian_day = Julian_day1 + delta_T
            Tjd = (Julian_day-2451545)/36525
            Tjde = (Julian_day-2451545)/365250

            #panggil fungsi
            delta_nutasi, delta_obliquity, obliquity0, obliquity = util.nutasi_obliquity(Tjd)
            O0, o0, GST, GST_nampak, LST_nampak = util.sidereal(Tjde, Julian_day1, delta_nutasi, obliquity, bujur_tempat)

            return render_template("perhitungan_posisi_hilal.html",tinggi_tempat = tinggi_tempat, O0 =O0, o0 =o0, GST = GST, GST_nampak = GST_nampak, LST_nampak = LST_nampak ,delta_nutasi = delta_nutasi, delta_obliquity = delta_obliquity, obliquity0 = obliquity0, obliquity = obliquity, lintang_tempat = lintang_tempat, bujur_tempat = bujur_tempat, Tjd = Tjd, Tjde = Tjde, JD_total =Julian_day, jam_now = jam, menit_now = menit, detik_now = detik, zona_waktu_now = zona_waktu, tanggal_now = tanggal, bulan_now = bulan, tahun_now = tahun, lintang_detik = lintang_detik, lintang_menit = lintang_menit, lintang_jam = lintang_jam, bujur_detik = bujur_detik, bujur_jam = bujur_jam, bujur_menit = bujur_menit, username = username)
    else:
        return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/hasil_perhitungan_matahari_high", methods=["GET","POST"])
def matahari_high():
    if request.method == "POST":

        return redirect(url_for("matahari_high_direct"))

    return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/data_matahari", methods=["GET"])
def matahari_high_direct():
    if 'detik_now' in session:
        if request.method == "GET":
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']

            #tempat eksekusi semua perhitungan dan input-an
            if lintang_arah == "U":
                lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            elif lintang_arah == "S":
                lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            if bujur_arah == "E":
                bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            elif bujur_arah == "W":
                bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            
            #perhitungan
            delta_T = util.deltaT(tahun, bulan)
            Julian_day1 = util.JD (detik, menit, jam, tanggal, bulan, tahun, zona_waktu)
            Julian_day = Julian_day1 + delta_T
            Tjd = (Julian_day-2451545)/36525
            Tjde = (Julian_day-2451545)/365250

            #panggil fungsi
            delta_nutasi, delta_obliquity, obliquity0, obliquity = util.nutasi_obliquity(Tjd)
            O0, o0, GST, GST_nampak, LST_nampak = util.sidereal(Tjde, Julian_day1, delta_nutasi, obliquity, bujur_tempat)
            L_earth, B_earth, R_earth, longitude_matahari, latitude_matahari, apparent_longitude_aksen, delta_longitude, delta_latitude, longitude_baru, latitude_baru, aberration, apparent_longitude = util.perhitungan_high (Tjde, delta_nutasi)
            right_ascension_high, deklinasi_high, azimuth_high, altitude_high, hour_angle_high = util.transformasi(apparent_longitude, obliquity, (latitude_baru/3600), LST_nampak, lintang_tempat)
            jam_azimuth_high, menit_azimuth_high, detik_azimuth_high = util.jam_konvert(azimuth_high)
            jam_altitude_high, menit_altitude_high, detik_altitude_high = util.jam_konvert(altitude_high)
            
            return render_template("hasil_perhitungan_high_accuracy.html",jam_altitude_high = jam_altitude_high, menit_altitude_high = menit_altitude_high, detik_altitude_high = detik_altitude_high, right_ascension_high = right_ascension_high, deklinasi_high = deklinasi_high, jam_azimuth_high = jam_azimuth_high, menit_azimuth_high = menit_azimuth_high, detik_azimuth_high = detik_azimuth_high, hour_angle_high = hour_angle_high, L_earth = L_earth, B_earth = B_earth, R_earth = R_earth, longitude_matahari = longitude_matahari, latitude_matahari = latitude_matahari, apparent_longitude_aksen = apparent_longitude_aksen, delta_longitude = delta_longitude, delta_latitude = delta_latitude, longitude_baru = longitude_baru, latitude_baru = latitude_baru, aberration = aberration, apparent_longitude = apparent_longitude)
    else:
        return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/hasil_perhitungan_matahari_high_kedua", methods=["GET","POST"])
def matahari_high_kedua():
    if request.method == "POST":
        jumlah_pengulangan_high_accuracy = int(request.form["pengulangan_high_accuracy"])
        session['jumlah_pengulangan_high_accuracy'] = jumlah_pengulangan_high_accuracy
        if 'jumlah_pengulangan_high_accuracy' in session:
            jumlah_pengulangan_high_accuracy = session['jumlah_pengulangan_high_accuracy']
        else:
            jumlah_pengulangan_high_accuracy = ""

        return redirect(url_for("matahari_high_kedua_direct"))

    return redirect(url_for("main_menu"))
    

#-----------------------------------------------------------------------------------------------------------#


@app.route("/hasil_perhitungan_matahari_high_kedua_perulangan", methods=["GET"])
def matahari_high_kedua_direct():
    if 'detik_now' in session:
        if request.method == "GET":
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']
            jumlah_pengulangan_high_accuracy = session['jumlah_pengulangan_high_accuracy']

            # #tempat eksekusi semua perhitungan dan input-an
            # if lintang_arah == "U":
            #     lintang_tempat = fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            # elif lintang_arah == "S":
            #     lintang_tempat = -fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            # if bujur_arah == "E":
            #     bujur_tempat = fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            # elif bujur_arah == "W":
            #     bujur_tempat = -fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            
            # #perhitungan
            # delta_T = deltaT(tahun, bulan)
            # Julian_day1 = JD (detik, menit, jam, tanggal, bulan, tahun, zona_waktu)
            # Julian_day = Julian_day1 + delta_T
            # Tjd = (Julian_day-2451545)/36525
            # Tjde = (Julian_day-2451545)/365250

            # #panggil fungsi
            # delta_nutasi, delta_obliquity, obliquity0, obliquity = nutasi_obliquity(Tjd)
            # O0, o0, GST, GST_nampak, LST_nampak = sidereal(Tjde, Julian_day1, delta_nutasi, obliquity, bujur_tempat)
            # L_earth, B_earth, R_earth, longitude_matahari, latitude_matahari, apparent_longitude_aksen, delta_longitude, delta_latitude, longitude_baru, latitude_baru, aberration, apparent_longitude = perhitungan_high (Tjde, delta_nutasi)
            # right_ascension_high, deklinasi_high, azimuth_high, altitude_high, hour_angle_high = transformasi(apparent_longitude, obliquity, (latitude_baru/3600), LST_nampak, lintang_tempat)
            # jam_azimuth_high, menit_azimuth_high, detik_azimuth_high = jam_konvert(azimuth_high)
            # jam_altitude_high, menit_altitude_high, detik_altitude_high = jam_konvert(altitude_high) 
            # ,jam_altitude_high = jam_altitude_high, menit_altitude_high = menit_altitude_high, detik_altitude_high = detik_altitude_high, right_ascension_high = right_ascension_high, deklinasi_high = deklinasi_high, jam_azimuth_high = jam_azimuth_high, menit_azimuth_high = menit_azimuth_high, detik_azimuth_high = detik_azimuth_high, hour_angle_high = hour_angle_high, L_earth = L_earth, B_earth = B_earth, R_earth = R_earth, longitude_matahari = longitude_matahari, latitude_matahari = latitude_matahari, apparent_longitude_aksen = apparent_longitude_aksen, delta_longitude = delta_longitude, delta_latitude = delta_latitude, longitude_baru = longitude_baru, latitude_baru = latitude_baru, aberration = aberration, apparent_longitude = apparent_longitude

            return render_template("hasil_perhitungan_high_accuracy_kedua.html",jam = jam, tanggal = tanggal, bulan = bulan, tahun = tahun, jumlah_pengulangan_high_accuracy = jumlah_pengulangan_high_accuracy)
    else:
       return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route('/download_text_high_accuracy')
def download_text_high_accuracy():
    if 'detik_now' in session:
        with open(config.posisi_matahari, "w") as file:
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']
            jumlah_pengulangan_high_accuracy = session['jumlah_pengulangan_high_accuracy']
            #tempat eksekusi semua perhitungan dan input-an
            if lintang_arah == "U":
                lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            elif lintang_arah == "S":
                lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            if bujur_arah == "E":
                bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            elif bujur_arah == "W":
                bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            
            results=[]
            #perhitungan
            for i in range(jumlah_pengulangan_high_accuracy):
                result=[]
                if jam == 24:
                    tanggal = tanggal + 1
                    jam = 0
                delta_T = util.deltaT(tahun, bulan)
                Julian_day1 = util.JD (0, 0 , jam, tanggal, bulan, tahun, zona_waktu)
                Julian_day = Julian_day1 + delta_T
                Tjd = (Julian_day-2451545)/36525
                Tjde = (Julian_day-2451545)/365250

                #panggil fungsi
                delta_nutasi, delta_obliquity, obliquity0, obliquity = util.nutasi_obliquity(Tjd)
                O0, o0, GST, GST_nampak, LST_nampak = util.sidereal(Tjde, Julian_day1, delta_nutasi, obliquity, bujur_tempat)
                L_earth, B_earth, R_earth, longitude_matahari, latitude_matahari, apparent_longitude_aksen, delta_longitude, delta_latitude, longitude_baru, latitude_baru, aberration, apparent_longitude = util.perhitungan_high (Tjde, delta_nutasi)
                right_ascension_high, deklinasi_high, azimuth_high, altitude_high, hour_angle_high = util.transformasi(apparent_longitude, obliquity, (latitude_baru/3600), LST_nampak, lintang_tempat)
                # jam_azimuth_high, menit_azimuth_high, detik_azimuth_high = jam_konvert(azimuth_high)
                # jam_altitude_high, menit_altitude_high, detik_altitude_high = jam_konvert(altitude_high)
                # jam_right_ascension_high, menit_right_ascension_high, detik_right_ascension_high = jam_konvert(right_ascension_high)
                # jam_deklinasi_high, menit_deklinasi_high, detik_deklinasi_high = jam_konvert(deklinasi_high)
                # jam_latitude_baru_high, menit_latitude_baru_high, detik_latitude_baru_high = jam_konvert(latitude_baru)
                # jam_apparent_longitude_high, menit_apparent_longitude_high, detik_apparent_longitude_high = jam_konvert(apparent_longitude)
                # result.append(detik_altitude_high)
                # result.append(menit_altitude_high)
                # result.append(jam_altitude_high)
                # result.append(detik_azimuth_high)
                # result.append(menit_azimuth_high)
                # result.append(jam_azimuth_high)
                # result.append(jam)
                # result.append(tanggal)
                # result.append(bulan)
                # result.append(tahun)
                # result.append(jam_right_ascension_high)
                # result.append(menit_right_ascension_high)
                # result.append(detik_right_ascension_high)
                # result.append(jam_deklinasi_high)
                # result.append(menit_deklinasi_high)
                # result.append(detik_deklinasi_high)
                # result.append(jam_latitude_baru_high)
                # result.append(menit_latitude_baru_high)
                # result.append(detik_latitude_baru_high)
                # result.append(jam_apparent_longitude_high)
                # result.append(menit_apparent_longitude_high)
                # result.append(detik_apparent_longitude_high)
                # results.append(result)
                result.append(round(altitude_high,2))
                result.append(round(azimuth_high,2))
                result.append(jam)
                result.append(tanggal)
                result.append(bulan)
                result.append(tahun)
                result.append(round(right_ascension_high,2))
                result.append(round(deklinasi_high,2))
                result.append(round(latitude_baru,2))
                result.append(round(apparent_longitude,2))
                results.append(result)
                jam = jam + 1
                i+=1
            file.write("jam   tanggal      alt         az          ar          dek       lat          long\n")
            for item in results:
                file.write(f"""{str(item[2]):>2}   {str(item[3])+"/"+str(item[4])+"/"+str(item[5]):<12}{str(item[0]):<12}{str(item[1]):<12}{str(item[6]):<12}{str(item[7]):<12}{str(item[8]):<12}{str(item[9]):<12}\n""")
                # file.write(f"""{str(item[6]):>2}   {str(item[7])+":"+str(item[8])+":"+str(item[9]):<12}{str(item[2])+":"+str(item[1])+":"+str(item[0]):<12}{str(item[5])+":"+str(item[4])+":"+str(item[3]):<12}{str(item[10])+":"+str(item[11])+":"+str(item[12]):<12}{str(item[13])+":"+str(item[14])+":"+str(item[15]):<12}{str(item[16])+":"+str(item[17])+":"+str(item[18]):<12}{str(item[19])+":"+str(item[20])+":"+str(item[21]):<12}\n""")

        return send_file("static/files/posisi_matahari.txt", as_attachment=True, download_name="posisi_matahari.txt")
    else:
        return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/hasil_perhitungan_matahari_low", methods=["GET","POST"])
def matahari_low():
    if request.method == "GET":
        return redirect("/kalkulator_hilal")
    elif request.method == "POST":
        detik = session['detik_now']
        menit = session['menit_now']
        jam = session['jam_now']
        tanggal = session['tanggal_now']
        bulan = session['bulan_now']
        tahun = session['tahun_now']
        zona_waktu = session['zona_waktu_now']
        lintang_detik = session['lintang_detik']
        lintang_menit = session['lintang_menit']
        lintang_jam = session['lintang_jam']
        bujur_detik = session['bujur_detik']
        bujur_menit = session['bujur_menit']
        bujur_jam = session['bujur_jam']
        lintang_arah = session['lintang_arah']
        bujur_arah = session['bujur_arah']

        #tempat eksekusi semua perhitungan dan input-an
        if lintang_arah == "U":
            lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
        elif lintang_arah == "S":
            lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
        if bujur_arah == "E":
            bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
        elif bujur_arah == "W":
            bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
        
        #perhitungan
        delta_T = util.deltaT(tahun, bulan)
        Julian_day1 = util.JD (detik, menit, jam, tanggal, bulan, tahun, zona_waktu)
        Julian_day = Julian_day1 + delta_T
        Tjd = (Julian_day-2451545)/36525
        Tjde = (Julian_day-2451545)/365250

        #panggil fungsi
        delta_nutasi, delta_obliquity, obliquity0, obliquity = util.nutasi_obliquity(Tjd)
        L0, M, eksentrisitas, C, longitude, R, omega, lamda, right_ascension_low, deklinasi = util.perhitungan_Low(Tjd)

        return render_template("hasil_perhitungan_low_accuracy.html", L0 = L0, M = M, eksentrisitas = eksentrisitas, C = C, longitude = longitude, R = R, omega = omega, lamda = lamda, right_ascension_low = right_ascension_low, deklinasi = deklinasi)


#-----------------------------------------------------------------------------------------------------------#


@app.route("/posisi_bulan", methods=["GET","POST"])
def posisi_bulan_jean_meeus():
    if request.method == "POST":

        return redirect(url_for("posisi_bulan_jean_meeus_direct"))

    return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/data_bulan", methods=["GET","POST"])
def posisi_bulan_jean_meeus_direct():
    if 'detik_now' in session:
        if request.method == "GET":
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']

            #tempat eksekusi semua perhitungan dan input-an
            if lintang_arah == "U":
                lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            elif lintang_arah == "S":
                lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            if bujur_arah == "E":
                bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            elif bujur_arah == "W":
                bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            
            #perhitungan
            delta_T = util.deltaT(tahun, bulan)
            Julian_day1 = util.JD (detik, menit, jam, tanggal, bulan, tahun, zona_waktu)
            Julian_day = Julian_day1 + delta_T
            Tjd = (Julian_day-2451545)/36525
            Tjde = (Julian_day-2451545)/365250

            #panggil fungsi
            delta_nutasi, delta_obliquity, obliquity0, obliquity = util.nutasi_obliquity(Tjd)
            O0, o0, GST, GST_nampak, LST_nampak = util.sidereal(Tjde, Julian_day1, delta_nutasi, obliquity, bujur_tempat)
            L_aksen, D, M, M_aksen, F, A1, A2, A3, E, longitude_bulan, latitude_bulan, distance_bulan, apparent_longitude_bulan, distance_to_earth, parallax = util.perhitungan_posisi_bulan (Tjd, delta_nutasi)
            right_ascension_bulan, deklinasi_bulan, azimuth_bulan, altitude_bulan, hour_angle_bulan = util.transformasi(apparent_longitude_bulan, obliquity, latitude_bulan, LST_nampak, lintang_tempat)
            jam_azimuth_bulan, menit_azimuth_bulan, detik_azimuth_bulan = util.jam_konvert(azimuth_bulan)
            jam_altitude_bulan, menit_altitude_bulan, detik_altitude_bulan = util.jam_konvert(altitude_bulan)

            return render_template("hasil_perhitungan_posisi_bulan.html",jam_altitude_bulan = jam_altitude_bulan, menit_altitude_bulan = menit_altitude_bulan, detik_altitude_bulan = detik_altitude_bulan, jam_azimuth_bulan = jam_azimuth_bulan, menit_azimuth_bulan = menit_azimuth_bulan, detik_azimuth_bulan = detik_azimuth_bulan, right_ascension_bulan = right_ascension_bulan, deklinasi_bulan = deklinasi_bulan, hour_angle_bulan = hour_angle_bulan, L_aksen = L_aksen, D = D, M = M, M_aksen = M_aksen, F = F, A1 = A1, A2 = A2, A3 = A3, E = E, longitude_bulan = longitude_bulan, latitude_bulan = latitude_bulan, distance_bulan = distance_bulan, apparent_longitude_bulan = apparent_longitude_bulan, distance_to_earth = distance_to_earth, parallax = parallax)
    else:
        return redirect(url_for("main_menu"))

#-----------------------------------------------------------------------------------------------------------#


@app.route("/posisi_bulan_kedua", methods=["GET","POST"])
def posisi_bulan_jean_meeus_kedua():
    if request.method == "POST":
        jumlah_pengulangan_posisi_bulan = int(request.form["pengulangan_posisi_bulan"])
        session['jumlah_pengulangan_posisi_bulan'] = jumlah_pengulangan_posisi_bulan
        if 'jumlah_pengulangan_posisi_bulan' in session:
            jumlah_pengulangan_posisi_bulan = session['jumlah_pengulangan_posisi_bulan']
        else:
            jumlah_pengulangan_posisi_bulan = ""

        return redirect(url_for("posisi_bulan_jean_meeus_kedua_direct"))

    return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/posisi_bulan_kedua_perulangan", methods=["GET"])
def posisi_bulan_jean_meeus_kedua_direct():
    if 'detik_now' in session:
        if request.method == "GET":
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']
            jumlah_pengulangan_posisi_bulan = session['jumlah_pengulangan_posisi_bulan']

            # #tempat eksekusi semua perhitungan dan input-an
            # if lintang_arah == "U":
            #     lintang_tempat = fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            # elif lintang_arah == "S":
            #     lintang_tempat = -fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            # if bujur_arah == "E":
            #     bujur_tempat = fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            # elif bujur_arah == "W":
            #     bujur_tempat = -fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            
            # #perhitungan
            # delta_T = deltaT(tahun, bulan)
            # Julian_day1 = JD (detik, menit, jam, tanggal, bulan, tahun, zona_waktu)
            # Julian_day = Julian_day1 + delta_T
            # Tjd = (Julian_day-2451545)/36525
            # Tjde = (Julian_day-2451545)/365250

            # #panggil fungsi
            # delta_nutasi, delta_obliquity, obliquity0, obliquity = nutasi_obliquity(Tjd)
            # O0, o0, GST, GST_nampak, LST_nampak = sidereal(Tjde, Julian_day1, delta_nutasi, obliquity, bujur_tempat)
            # L_aksen, D, M, M_aksen, F, A1, A2, A3, E, longitude_bulan, latitude_bulan, distance_bulan, apparent_longitude_bulan, distance_to_earth, parallax = perhitungan_posisi_bulan (Tjd, delta_nutasi)
            # right_ascension_bulan, deklinasi_bulan, azimuth_bulan, altitude_bulan, hour_angle_bulan = transformasi(apparent_longitude_bulan, obliquity, latitude_bulan, LST_nampak, lintang_tempat)
            # jam_azimuth_bulan, menit_azimuth_bulan, detik_azimuth_bulan = jam_konvert(azimuth_bulan)
            # jam_altitude_bulan, menit_altitude_bulan, detik_altitude_bulan = jam_konvert(altitude_bulan)
            # ,jam_altitude_bulan = jam_altitude_bulan, menit_altitude_bulan = menit_altitude_bulan, detik_altitude_bulan = detik_altitude_bulan, jam_azimuth_bulan = jam_azimuth_bulan, menit_azimuth_bulan = menit_azimuth_bulan, detik_azimuth_bulan = detik_azimuth_bulan, right_ascension_bulan = right_ascension_bulan, deklinasi_bulan = deklinasi_bulan, hour_angle_bulan = hour_angle_bulan, L_aksen = L_aksen, D = D, M = M, M_aksen = M_aksen, F = F, A1 = A1, A2 = A2, A3 = A3, E = E, longitude_bulan = longitude_bulan, latitude_bulan = latitude_bulan, distance_bulan = distance_bulan, apparent_longitude_bulan = apparent_longitude_bulan, distance_to_earth = distance_to_earth, parallax = parallax

            return render_template("hasil_perhitungan_posisi_bulan_kedua.html",jam = jam ,tanggal=tanggal, bulan=bulan, tahun=tahun, jumlah_pengulangan_posisi_bulan = jumlah_pengulangan_posisi_bulan)
    else:
        return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route('/download_text_posisi_bulan')
def download_text_posisi_bulan():
    if 'detik_now' in session:
        with open(config.posisi_bulan, "w") as file:
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']
            jumlah_pengulangan_posisi_bulan = session['jumlah_pengulangan_posisi_bulan']
            #tempat eksekusi semua perhitungan dan input-an
            if lintang_arah == "U":
                lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            elif lintang_arah == "S":
                lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            if bujur_arah == "E":
                bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            elif bujur_arah == "W":
                bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            
            results=[]
            #perhitungan
            for i in range(jumlah_pengulangan_posisi_bulan):
                result=[]
                if jam == 24:
                    tanggal = tanggal + 1
                    jam = 0
                delta_T = util.deltaT (tahun, bulan)
                Julian_day1 = util.JD (0, 0 , jam, tanggal, bulan, tahun, zona_waktu)
                Julian_day = Julian_day1 + delta_T
                Tjd = (Julian_day-2451545)/36525
                Tjde = (Julian_day-2451545)/365250

                #panggil fungsi
                delta_nutasi, delta_obliquity, obliquity0, obliquity = util.nutasi_obliquity(Tjd)
                O0, o0, GST, GST_nampak, LST_nampak = util.sidereal(Tjde, Julian_day1, delta_nutasi, obliquity, bujur_tempat)
                L_aksen, D, M, M_aksen, F, A1, A2, A3, E, longitude_bulan, latitude_bulan, distance_bulan, apparent_longitude_bulan, distance_to_earth, parallax = util.perhitungan_posisi_bulan (Tjd, delta_nutasi)
                right_ascension_bulan, deklinasi_bulan, azimuth_bulan, altitude_bulan, hour_angle_bulan = util.transformasi(apparent_longitude_bulan, obliquity, latitude_bulan, LST_nampak, lintang_tempat)
                # jam_azimuth_bulan, menit_azimuth_bulan, detik_azimuth_bulan = jam_konvert(azimuth_bulan)
                # jam_altitude_bulan, menit_altitude_bulan, detik_altitude_bulan = jam_konvert(altitude_bulan)
                # jam_right_ascension_bulan, menit_right_ascension_bulan, detik_right_ascension_bulan = jam_konvert(right_ascension_bulan)
                # jam_deklinasi_bulan, menit_deklinasi_bulan, detik_deklinasi_bulan = jam_konvert(deklinasi_bulan)
                # jam_latitude_bulan, menit_latitude_bulan, detik_latitude_bulan = jam_konvert(latitude_bulan)
                # jam_apparent_longitude_bulan, menit_apparent_longitude_bulan, detik_apparent_longitude_bulan = jam_konvert(apparent_longitude_bulan)
                # result.append(detik_altitude_bulan)
                # result.append(menit_altitude_bulan)
                # result.append(jam_altitude_bulan)
                # result.append(detik_azimuth_bulan)
                # result.append(menit_azimuth_bulan)
                # result.append(jam_azimuth_bulan)
                # result.append(jam)
                # result.append(tanggal)
                # result.append(bulan)
                # result.append(tahun)
                # result.append(jam_right_ascension_bulan)
                # result.append(menit_right_ascension_bulan)
                # result.append(detik_right_ascension_bulan)
                # result.append(jam_deklinasi_bulan)
                # result.append(menit_deklinasi_bulan)
                # result.append(detik_deklinasi_bulan)
                # result.append(jam_latitude_bulan)
                # result.append(menit_latitude_bulan)
                # result.append(detik_latitude_bulan)
                # result.append(jam_apparent_longitude_bulan)
                # result.append(menit_apparent_longitude_bulan)
                # result.append(detik_apparent_longitude_bulan)
                # results.append(result)
                result.append(round(altitude_bulan,2))
                result.append(round(azimuth_bulan,2))
                result.append(jam)
                result.append(tanggal)
                result.append(bulan)
                result.append(tahun)
                result.append(round(right_ascension_bulan,2))
                result.append(round(deklinasi_bulan,2))
                result.append(round(latitude_bulan,2))
                result.append(round(apparent_longitude_bulan,2))
                results.append(result)
                jam = jam + 1
                i+=1
            file.write("jam   tanggal      alt          az          ar          dek        lat        long\n")
            for item in results:
                file.write(f"""{str(item[2]):>2}   {str(item[3])+"/"+str(item[4])+"/"+str(item[5]):<12}{str(item[0]):<12}{str(item[1]):<12}{str(item[6]):<12}{str(item[7]):<12}{str(item[8]):<12}{str(item[9]):<12}\n""")
                # file.write(f"""{str(item[6]):>2}   {str(item[7])+":"+str(item[8])+":"+str(item[9]):<12}{str(item[2])+":"+str(item[1])+":"+str(item[0]):<12}{str(item[5])+":"+str(item[4])+":"+str(item[3]):<12}{str(item[10])+":"+str(item[11])+":"+str(item[12]):<12}{str(item[13])+":"+str(item[14])+":"+str(item[15]):<12}{str(item[16])+":"+str(item[17])+":"+str(item[18]):<12}{str(item[19])+":"+str(item[20])+":"+str(item[21]):<12}\n""")

        return send_file("static/files/posisi_bulan.txt", as_attachment=True, download_name="posisi_bulan.txt")
    
    else:
        return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/fase_bulan", methods=["GET","POST"])
def fase_bulan_jean_meeus():
    if request.method == "POST":

        return redirect(url_for("fase_bulan_jean_meeus_perulangan_direct"))

    return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/data_fase_bulan", methods=["GET"])
def fase_bulan_jean_meeus_perulangan_direct():
    if 'detik_now' in session:
        if request.method == "GET":
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']

            #tempat eksekusi semua perhitungan dan input-an
            # if lintang_arah == "U":
            #     lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            # elif lintang_arah == "S":
            #     lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            # if bujur_arah == "E":
            #     bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            # elif bujur_arah == "W":
            #     bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            
            #perhitungan
            delta_T = util.deltaT(tahun, bulan)

            #konversi tanggal
            hijriah = convert.Gregorian(tahun, bulan, tanggal).to_hijri()

            #panggil fungsi
            k_fase_bulan, T_fase_bulan, JDE_fase_bulan, M_fase_bulan, M_aksen_fase_bulan, F_fase_bulan, omega_fase_bulan, correction_all_phase, new_moon, JDE_fase_bulan_new, jam_new_moon, tanggal_fase_bulan, bulan_fase_bulan, tahun_fase_bulan = util.fase_bulan (hijriah.month, hijriah.year, delta_T, zona_waktu)
            
            #opsional
            jam_new_moon1 = jam_new_moon*24
            if jam_new_moon1 <= 0:
                jam_new_moon1 = jam_new_moon1 + 24
            jam_new_moon_baru, menit_new_moon, detik_new_moon = util.jam_konvert(jam_new_moon1)

            return render_template("hasil_perhitungan_fase_bulan.html", k_fase_bulan = k_fase_bulan, T_fase_bulan = T_fase_bulan, JDE_fase_bulan = JDE_fase_bulan, M_fase_bulan = M_fase_bulan, M_aksen_fase_bulan = M_aksen_fase_bulan, F_fase_bulan = F_fase_bulan, omega_fase_bulan = omega_fase_bulan, correction_all_phase = correction_all_phase, new_moon = new_moon, JDE_fase_bulan_new = JDE_fase_bulan_new, jam_new_moon_baru = jam_new_moon_baru, menit_new_moon = menit_new_moon, detik_new_moon = detik_new_moon, tanggal_fase_bulan = tanggal_fase_bulan, bulan_fase_bulan = bulan_fase_bulan, tahun_fase_bulan = tahun_fase_bulan)
    else:
        return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/fase_bulan_dua", methods=["GET","POST"])
def fase_bulan_jean_meeus_perulangan():
    if request.method == "POST":
        jumlah_pengulangan_fase_bulan = int(request.form["pengulangan_fase_bulan"])
        session['jumlah_pengulangan_fase_bulan'] = jumlah_pengulangan_fase_bulan
        if 'jumlah_pengulangan_fase_bulan' in session:
            jumlah_pengulangan_fase_bulan = session['jumlah_pengulangan_fase_bulan']
        else:
            jumlah_pengulangan_fase_bulan = ""

        return redirect(url_for("fase_bulan_jean_meeus_perulangan_kedua_direct"))
    return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/fase_bulan_dua_perulangan", methods=["GET"])
def fase_bulan_jean_meeus_perulangan_kedua_direct():
    if 'detik_now' in session:
        if request.method == "GET":
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']
            jumlah_pengulangan_fase_bulan = session['jumlah_pengulangan_fase_bulan']
            
            #tempat eksekusi semua perhitungan dan input-an
            if lintang_arah == "U":
                lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            elif lintang_arah == "S":
                lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            if bujur_arah == "E":
                bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            elif bujur_arah == "W":
                bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)

            #fungsi pengulangan
            results =[]
            bulan = bulan - 1
            if bulan == 0:
                bulan = 12
                tahun = tahun - 1
            for i in range(jumlah_pengulangan_fase_bulan):
                bulan = bulan + 1
                if bulan == 13:
                    bulan = 1
                    tahun = tahun + 1
                result =[]
                delta_T = util.deltaT(tahun, bulan)
                #konversi tanggal
                hijriah = convert.Gregorian(tahun, bulan, tanggal).to_hijri()

                #panggil fungsi
                k_fase_bulan, T_fase_bulan, JDE_fase_bulan, M_fase_bulan, M_aksen_fase_bulan, F_fase_bulan, omega_fase_bulan, correction_all_phase, new_moon, JDE_fase_bulan_new, jam_new_moon, tanggal_fase_bulan, bulan_fase_bulan, tahun_fase_bulan = util.fase_bulan (hijriah.month, hijriah.year, delta_T, zona_waktu)
                jam_new_moon1 = jam_new_moon*24
                if jam_new_moon1 <= 0:
                        jam_new_moon1 = jam_new_moon1 + 24
                jam_new_moon_baru, menit_new_moon, detik_new_moon = util.jam_konvert(jam_new_moon1)
                jam_new_moon_local = jam_new_moon_baru + zona_waktu
                if jam_new_moon_local >= 24:
                    jam_new_moon_local = 0
                    tanggal_fase_bulan = tanggal_fase_bulan
                bulan_konvert = calendar.month_name[bulan_fase_bulan]
                result.append(detik_new_moon)
                result.append(menit_new_moon)
                result.append(jam_new_moon_baru)
                result.append(tanggal_fase_bulan)
                result.append(bulan_konvert)
                result.append(tahun_fase_bulan)
                results.append(result)
                i=+1
                
            return render_template("hasil_perhitungan_fase_bulan_kedua.html", jumlah_pengulangan_fase_bulan = jumlah_pengulangan_fase_bulan, result = results, k_fase_bulan = k_fase_bulan, T_fase_bulan = T_fase_bulan, JDE_fase_bulan = JDE_fase_bulan, M_fase_bulan = M_fase_bulan, M_aksen_fase_bulan = M_aksen_fase_bulan, F_fase_bulan = F_fase_bulan, omega_fase_bulan = omega_fase_bulan, correction_all_phase = correction_all_phase, new_moon = new_moon, JDE_fase_bulan_new = JDE_fase_bulan_new, jam_new_moon_baru = jam_new_moon_baru, menit_new_moon = menit_new_moon, detik_new_moon = detik_new_moon, tanggal_fase_bulan = tanggal_fase_bulan, bulan_fase_bulan = bulan_fase_bulan, tahun_fase_bulan = tahun_fase_bulan)
    else:
        return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route('/download_text_fase_bulan_dua')
def download_text_fase_bulan_dua():
    if 'detik_now' in session:
        detik = session['detik_now']
        menit = session['menit_now']
        jam = session['jam_now']
        tanggal = session['tanggal_now']
        bulan = session['bulan_now']
        tahun = session['tahun_now']
        zona_waktu = session['zona_waktu_now']
        lintang_detik = session['lintang_detik']
        lintang_menit = session['lintang_menit']
        lintang_jam = session['lintang_jam']
        bujur_detik = session['bujur_detik']
        bujur_menit = session['bujur_menit']
        bujur_jam = session['bujur_jam']
        lintang_arah = session['lintang_arah']
        bujur_arah = session['bujur_arah']
        jumlah_pengulangan_fase_bulan = session['jumlah_pengulangan_fase_bulan']

        #tempat eksekusi semua perhitungan dan input-an
        if lintang_arah == "U":
            lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
        elif lintang_arah == "S":
            lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
        if bujur_arah == "E":
            bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
        elif bujur_arah == "W":
            bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)

        #fungsi pengulangan
        bulan = bulan - 1
        if bulan == 0:
            bulan = 12
            tahun = tahun - 1
        with open(config.fase_bulan, "w") as file:
            for i in range(jumlah_pengulangan_fase_bulan):
                bulan = bulan + 1
                if bulan == 13:
                    bulan = 1
                    tahun = tahun + 1
                delta_T = util.deltaT(tahun, bulan)
                k_fase_bulan, T_fase_bulan, JDE_fase_bulan, M_fase_bulan, M_aksen_fase_bulan, F_fase_bulan, omega_fase_bulan, correction_all_phase, new_moon, JDE_fase_bulan_new, jam_new_moon, tanggal_fase_bulan, bulan_fase_bulan, tahun_fase_bulan = util.fase_bulan (bulan, tahun, delta_T, zona_waktu)
                jam_new_moon1 = jam_new_moon*24
                if jam_new_moon1 <= 0:
                        jam_new_moon1 = jam_new_moon1 + 24
                jam_new_moon_baru, menit_new_moon, detik_new_moon = util.jam_konvert(jam_new_moon1)
                jam_new_moon_local = jam_new_moon_baru + zona_waktu
                if jam_new_moon_local >= 24:
                    jam_new_moon_local = 0
                    tanggal_fase_bulan = tanggal_fase_bulan + 1

                file.write(f"""{str(i)}.  {str(tanggal_fase_bulan).zfill(2)}/{str(bulan_fase_bulan).zfill(2)}/{str(tahun_fase_bulan):<10}{str(jam_new_moon_baru).zfill(2)}.{str(menit_new_moon).zfill(2)}.{str(detik_new_moon).zfill(2)}\n""")
                i=+1

        return send_file("static/files/fase_bulan.txt", as_attachment=True, download_name="fase_bulan.txt")
    else:
        return redirect(url_for("main_menu"))


#-----------------------------------------------------------------------------------------------------------#


@app.route("/informasi_hilal", methods=["GET","POST"])
def posisi_hilal():
    if request.method == "GET":
        return redirect("/kalkulator_hilal")
    elif request.method == "POST":
        detik = session['detik_now']
        menit = session['menit_now']
        jam = session['jam_now']
        tanggal = session['tanggal_now']
        bulan = session['bulan_now']
        tahun = session['tahun_now']
        zona_waktu = session['zona_waktu_now']
        lintang_detik = session['lintang_detik']
        lintang_menit = session['lintang_menit']
        lintang_jam = session['lintang_jam']
        bujur_detik = session['bujur_detik']
        bujur_menit = session['bujur_menit']
        bujur_jam = session['bujur_jam']
        lintang_arah = session['lintang_arah']
        bujur_arah = session['bujur_arah']
        tinggi_tempat = session['tinggi_tempat']

        #tempat eksekusi semua perhitungan dan input-an
        if lintang_arah == "U":
            lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
        elif lintang_arah == "S":
            lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
        if bujur_arah == "E":
            bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
        elif bujur_arah == "W":
            bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)

        #perhitungan
        delta_T = util.deltaT(tahun, bulan)
        
        #panggil fungsi
        informasi_hilal_seluruhnya = util.perhitungan_hilal(detik, menit, jam, tanggal, bulan, tahun, zona_waktu, lintang_tempat, bujur_tempat, tinggi_tempat, delta_T)   

        return render_template("hasil_perhitungan_posisi_hilal.html", informasi_hilal_seluruhnya = informasi_hilal_seluruhnya)


#-----------------------------------------------------------------------------------------------------------#


@app.route('/download_text_hilal')
def download_text():
    if 'detik_now' in session:
        with open(config.posisi_hilal, "w") as file:
            detik = session['detik_now']
            menit = session['menit_now']
            jam = session['jam_now']
            tanggal = session['tanggal_now']
            bulan = session['bulan_now']
            tahun = session['tahun_now']
            zona_waktu = session['zona_waktu_now']
            lintang_detik = session['lintang_detik']
            lintang_menit = session['lintang_menit']
            lintang_jam = session['lintang_jam']
            bujur_detik = session['bujur_detik']
            bujur_menit = session['bujur_menit']
            bujur_jam = session['bujur_jam']
            lintang_arah = session['lintang_arah']
            bujur_arah = session['bujur_arah']
            tinggi_tempat = session['tinggi_tempat']

            #tempat eksekusi semua perhitungan dan input-an
            if lintang_arah == "U":
                lintang_tempat = util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            elif lintang_arah == "S":
                lintang_tempat = -util.fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam)
            if bujur_arah == "E":
                bujur_tempat = util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)
            elif bujur_arah == "W":
                bujur_tempat = -util.fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam)

            #perhitungan
            delta_T = util.deltaT(tahun, bulan)
            
            #panggil fungsi
            informasi_hilal_seluruhnya = util.perhitungan_hilal(detik, menit, jam, tanggal, bulan, tahun, zona_waktu, lintang_tempat, bujur_tempat, tinggi_tempat, delta_T)   

            file.write(
    f"""Tanggal New Moon = {str(informasi_hilal_seluruhnya[0][0]).zfill(2)}/{str(informasi_hilal_seluruhnya[0][1]).zfill(2)}/{str(informasi_hilal_seluruhnya[0][2])}     Waktu Matahari Tenggelam = {str(informasi_hilal_seluruhnya[1][0]).zfill(2)}.{str(informasi_hilal_seluruhnya[1][1]).zfill(2)}.{str(informasi_hilal_seluruhnya[1][2]).zfill(2)}
                        
                                Data Matahari

        Azimuth         = {str(informasi_hilal_seluruhnya[3][0]).zfill(3)}:{str(informasi_hilal_seluruhnya[3][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[3][2]).zfill(2):<12}        Altitude          = {str(informasi_hilal_seluruhnya[2][0]).zfill(3)}:{str(informasi_hilal_seluruhnya[2][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[2][2]).zfill(2):<12}
        Asensiorekta    = {str(informasi_hilal_seluruhnya[4][0]).zfill(3)}:{str(informasi_hilal_seluruhnya[4][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[4][2]).zfill(2):<12}        Deklinasi         = {str(informasi_hilal_seluruhnya[5][0]).zfill(2)}:{str(informasi_hilal_seluruhnya[5][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[5][2]).zfill(2):<13}
        Bujur Ekliptika = {str(informasi_hilal_seluruhnya[6][0]).zfill(3)}:{str(informasi_hilal_seluruhnya[6][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[6][2]).zfill(2):<12}        Lintang Ekliptika = {str(informasi_hilal_seluruhnya[7]):<15}   
                    
                    
                                Data Hilal

        Azimuth         = {str(informasi_hilal_seluruhnya[9][0]).zfill(3)}:{str(informasi_hilal_seluruhnya[9][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[9][2]).zfill(2):<9}        Altitude          = {str(informasi_hilal_seluruhnya[8][0]).zfill(3)}:{str(informasi_hilal_seluruhnya[8][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[8][2]).zfill(2):<12}
        Asensiorekta    = {str(informasi_hilal_seluruhnya[10][0]).zfill(3)}:{str(informasi_hilal_seluruhnya[10][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[10][2]).zfill(2):<12}     Deklinasi         = {str(informasi_hilal_seluruhnya[11][0]).zfill(2)}:{str(informasi_hilal_seluruhnya[11][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[11][2]).zfill(2):<15}
        Bujur Ekliptika = {str(informasi_hilal_seluruhnya[12][0]).zfill(3)}:{str(informasi_hilal_seluruhnya[12][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[12][2]).zfill(2):<12}     Lintang Ekliptika = {str(informasi_hilal_seluruhnya[13]):<15}   
        Elongasi        = {str(informasi_hilal_seluruhnya[14][0]).zfill(2)}:{str(informasi_hilal_seluruhnya[14][1]).zfill(2)}:{str(informasi_hilal_seluruhnya[14][2]).zfill(2)}
                            """)

        return send_file("static/files/posisi_hilal.txt", as_attachment=True, download_name="posisi_hilal.txt")
    else:
        return redirect(url_for("main_menu"))


    #-----------------------------------------------------------------------------------------------------------#

