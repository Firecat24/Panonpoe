import math, pandas, app

from datetime               import datetime


#-----------------------------------------------------------------------------------------------------------#


#PEMANGGILAN DATA
data_nutasi = pandas.read_csv('app/data/nutasi.csv', delimiter=',')
data_obliquity = pandas.read_csv('app/data/obliquity.csv', delimiter=',')
data_earth_L0 = pandas.read_csv('app/data/earth_L0.csv', delimiter=',')
data_earth_L1 = pandas.read_csv('app/data/earth_L1.csv', delimiter=',')
data_earth_L2 = pandas.read_csv('app/data/earth_L2.csv', delimiter=',')
data_earth_L3 = pandas.read_csv('app/data/earth_L3.csv', delimiter=',')
data_earth_L4 = pandas.read_csv('app/data/earth_L4.csv', delimiter=',')
data_earth_L5 = pandas.read_csv('app/data/earth_L5.csv', delimiter=',')
data_earth_R0 = pandas.read_csv('app/data/earth_R0.csv', delimiter=',')
data_earth_R1 = pandas.read_csv('app/data/earth_R1.csv', delimiter=',')
data_earth_R2 = pandas.read_csv('app/data/earth_R2.csv', delimiter=',')
data_earth_R3 = pandas.read_csv('app/data/earth_R3.csv', delimiter=',')
data_earth_R4 = pandas.read_csv('app/data/earth_R4.csv', delimiter=',')
data_earth_B0 = pandas.read_csv('app/data/earth_B0.csv', delimiter=',')
data_earth_B1 = pandas.read_csv('app/data/earth_B1.csv', delimiter=',')
data_longitude_bulan = pandas.read_csv('app/data/longitude_bulan.csv', delimiter=',')
data_ekliptika_bulan = pandas.read_csv('app/data/ekliptika_bulan.csv', delimiter=',')
data_distance_bulan = pandas.read_csv('app/data/distance_bulan.csv', delimiter=',')

#-----------------------------------------------------------------------------------------------------------#


def format_time(jam, menit):
    if menit >= 60:
        jam += menit // 60
        menit = menit % 60
    return "{jam}:{menit}".format(jam=jam, menit=str(menit).zfill(2))


#-----------------------------------------------------------------------------------------------------------#


#LINTANG TEMPAT
def fungsi_lintang_tempat(lintang_detik, lintang_menit, lintang_jam):
    lintang_tempat = lintang_jam + lintang_menit/60 + lintang_detik/3600

    return lintang_tempat


#-----------------------------------------------------------------------------------------------------------#


#BUJUR TEMPAT
def fungsi_bujur_tempat(bujur_detik, bujur_menit, bujur_jam):
    bujur_tempat = bujur_jam + bujur_menit/60 + bujur_detik/3600

    return bujur_tempat


#-----------------------------------------------------------------------------------------------------------#


#CONVERT WAKTU
#DELTA T
def deltaT(tahun, bulan):
    y = tahun + (bulan - 0.5)/12
    if tahun <= -500 :
        u = (tahun-1820)/100
        delta_T = -0 + 32 * u**2
    elif tahun > -500 and tahun <= 500 :
        u = y/100
        delta_T = 10583.6-1014.41*u+33.78311*u**2-5.952053*u**3-0.1798452*u**4-0.005050998*u**5+0.0083572073*u**6
    elif tahun > 500 and tahun <= 1600 :
        u = (y-1000)/100
        delta_T = 1574.2-556.01*u+71.23472*u**2+0.319781*u**3-0.8503463*u**4-0.005050998*u**5+0.0083572073*u**6
    elif tahun > 1940 and tahun <= 1990 :
        u = 0.35 + (tahun - 2000)/100
        delta_T = 36.2 + 74.0*u + 189*u**2 - 140*u**3 - 1883*u**4
    elif tahun > 1990 and tahun <= 2005 :
        t = y - 2000
        delta_T = 63.86 + 0.3345 * t - 0.060374 * t**2 + 0.0017275 * t**3 + 0.000651814 * t**4 + 0.00002373599* t**5
    elif tahun > 2005 and tahun <= 2050 :
        t = y - 2000
        delta_T = 62.92+0.32217*t+0.005589*t**2
    delta_T = delta_T/86400

    return delta_T


#-----------------------------------------------------------------------------------------------------------#

def hasil(Pk):
    jams = math.floor(Pk)
    menit0 = (Pk) - math.floor(Pk)
    menits = round((menit0)*60)
    return jams, menits


def jam_konvert(waktu):
    jam = int(waktu)
    menit = int((abs(waktu)-abs(jam))*60)
    detik = round(((abs(waktu)-abs(jam))*60 - menit)*60)
    if waktu < 0:
        jam = int(waktu)
        if jam == 0 :
            menit = -menit
            
    return jam, menit, detik

def jam_konvert_template(waktu):
    jam_new_moon1 = waktu * 24
    if jam_new_moon1 <= 0:
        jam_new_moon1 += 24

    jam = int(jam_new_moon1)
    menit = int((abs(jam_new_moon1) - abs(jam)) * 60)
    detik = round(((abs(jam_new_moon1) - abs(jam)) * 60 - menit) * 60)

    if menit >= 60:
        jam += menit // 60
        menit = menit % 60

    return "{jam}.{menit}".format(jam=str(jam).zfill(2), menit=str(menit).zfill(2))
    return "{jam}.{menit}".format(jam=str(jam).zfill(2), menit=str(menit).zfill(2))


#-----------------------------------------------------------------------------------------------------------#


#JULIAN DAYS
def JD (d, m, H, D, M, Y, TZ):
    if M <=2 :
        M = M + 12
        Y = Y - 1
        A = int(Y/100)
    else :
        A = int(Y/100)
    if Y <=1582:
        B = 0
    else:
        B = 2 - A + int(A/4)
    jam = H
    menit = m/60
    detik = d/3600
    waktu = (jam + menit + detik)/24
    JD_total = int(365.25*(Y + 4716)) + int(30.6001*(M+1)) + D + B - 1524.5 + waktu - TZ/24
    
    return JD_total


#-----------------------------------------------------------------------------------------------------------#


#SIDEREAL TIME AT GREENWICH
def sidereal(T, JD, delta_nutasi, obliquity, bujur_tempat):
    #dalam jam
    O0 = (6*3600) + (41*60) + 50.54841 + 8640184.812866*T + 0.093104*(T**2) - 0.0000062*(T**3)
    #dalam degress dan decimal
    o0 = 100.46061837 + 36000.770053608*T + 0.000387933*(T**2) - (T**3)/38710000
    GST = ((280.46061837 + 360.98564736629*(JD - 2451545) + 0.000387933*(T**2) - (T**3)/38710000)%360)/15
    GST_nampak = GST + delta_nutasi*math.cos(math.radians(obliquity))/15
    LST_nampak = (GST_nampak + bujur_tempat/15)%24
    
    return O0, o0, GST, GST_nampak, LST_nampak


#-----------------------------------------------------------------------------------------------------------#


#TRANSFORMASI
def transformasi(apparent_longitude, obliquity, latitude, LST_nampak, lintang_tempat):
    #transformasi dari ekliptika ke equatorial latitude nya salah diganti latitude baru
    right_ascension = ((math.degrees(math.atan2((math.sin(math.radians(apparent_longitude))*math.cos(math.radians(obliquity))-math.tan(math.radians(latitude))*math.sin(math.radians(obliquity))), math.cos(math.radians(apparent_longitude)))))%360)
    deklinasi = (math.degrees(math.asin(math.sin(math.radians(latitude))*math.cos(math.radians(obliquity))+math.cos(math.radians(latitude))*math.sin(math.radians(obliquity))*math.sin(math.radians(apparent_longitude)))))
    hour_angel = LST_nampak * 15 - right_ascension

    azimuth = math.degrees(math.atan2(math.sin(math.radians(hour_angel)), math.cos(math.radians(hour_angel))* math.sin(math.radians(lintang_tempat)) - math.tan(math.radians(deklinasi))* math.cos(math.radians(lintang_tempat))))+180
    altitude = math.degrees(math.asin(math.sin(math.radians(lintang_tempat))* math.sin(math.radians(deklinasi))+ math.cos(math.radians(lintang_tempat))* math.cos(math.radians(deklinasi))* math.cos(math.radians(hour_angel))))
    
    return right_ascension, deklinasi, azimuth, altitude, hour_angel


#-----------------------------------------------------------------------------------------------------------#


#NUTASI DAN OBLIQUITY obliquity adalah kemiringan ekliptika
def nutasi_obliquity(Tjd):
    U = Tjd/100
    #D, M, M1, F
    D_true_obliquity = 297.85036 + 445267.111480*Tjd - 0.0019142*(Tjd**2) + (Tjd**3)/189474
    M_true_obliquity = 357.52772 + 35999.050340*Tjd - 0.0001603*(Tjd**2) - (Tjd**3)/300000
    M1_true_obliquity = 134.96298 + 477198.867398*Tjd + 0.0086972*(Tjd**2) + (Tjd**3)/56250
    F_true_obliquity = 93.27191 + 483202.017538*Tjd - 0.0036825*(Tjd**2) + (Tjd**3)/327270
    omega = 125.04 - 1934.136*Tjd

    #gangerti apa ini ???
    #L = 280.4665 + 36000.7698*Tjd
    #L_aksen = 218.3165 + 481267.8813*Tjd
    #delta_nutasi = (-17.20/3600) * math.sin(math.radians(omega))+ (1.32/3600) * math.sin(math.radians(2*L)) - (0.23/3600) * math.sin(math.radians(2*L_aksen)) + (0.21/3600) * math.sin(math.radians(2*omega))
    #delta_obliquity = (9.20/3600) * math.cos(math.radians(omega))+ (0.57/3600) * math.cos(math.radians(2*L)) + (0.10/3600) * math.cos(math.radians(2*L_aksen)) - (0.09/3600) * math.cos(math.radians(2*omega))
    
    #delta obliquity
    hs = 0
    for index, i in data_obliquity.iterrows():
        d = i['D']
        m = i['M']
        m1 = i["M'"]
        f = i['F']
        ome = i['Ω']
        f2 = i['koefisien 1']
        g = i['koefisien 2']
        hasil1 = (f2 + (g*Tjd)) * (math.cos(((math.radians(d*D_true_obliquity)) + (math.radians(m*M_true_obliquity)) + (math.radians(m1*M1_true_obliquity)) + (math.radians(f*F_true_obliquity)) + (math.radians(ome*omega)))))
        hs = hs + hasil1
    
    #delta Nutasi
    hss = 0
    for index, i in data_nutasi.iterrows():
        d = i['D']
        m = i['M']
        m1 = i["M'"]
        f = i['F']
        ome = i['Ω']
        f2 = i['koefisien 1']
        g = i['koefisien 2']
        hasil00 = (f2 + (g*Tjd)) * (math.sin(((math.radians(d*D_true_obliquity)) + (math.radians(m*M_true_obliquity)) + (math.radians(m1*M1_true_obliquity)) + (math.radians(f*F_true_obliquity)) + (math.radians(ome*omega)))))
        hss = hss + hasil00

    delta_nutasi = (hss/10000/3600)
    delta_obliquity = (hs/10000/3600)
    obliquity0 = (((23*3600) + (26*60) + 21.448 - 46.8150*Tjd - 0.00059*Tjd**2 + 0.001813*Tjd**3)/3600)
    #obliquity_nol = ((23*3600) + (26*60) + 21.448 - 4680.93*U - 1.55*(U**2) + 1999.25*(U**3) - 51.38*(U**4) - 249.67*(U**5) - 39.05*(U**6) + 7.12*(U**7) + 27.87*(U**8) + 5.79*(U**9) + 2.45*(U**10))/3600
    obliquity = (delta_obliquity + obliquity0)

    return delta_nutasi, delta_obliquity, obliquity0, obliquity


#-----------------------------------------------------------------------------------------------------------#


#EQUATION OF TIME
def equationoftime (T, right_ascension_high, delta_nutasi, obliquity):
    apparent_longitude = (280.4664567 + 360007.6982779*T + 0.03032028*(T**2) + (T**3)/49931 - (T**4)/15300 - (T**5)/20000000)%360
    equation_of_time = (apparent_longitude - 0.0057183 - right_ascension_high + delta_nutasi * math.cos(math.radians(obliquity)))/15

    return equation_of_time


#-----------------------------------------------------------------------------------------------------------#


def harga_tinggi(tinggi_tempat):
    DIP = 1.76 * math.sqrt(tinggi_tempat) / 60
    semi_diameter = 0.5 * (32/60)
    refraksi = 34.5/60
    h = (DIP + semi_diameter + refraksi)

    return h


#-----------------------------------------------------------------------------------------------------------#


def perhitungan_waktu_magrib(lintang_tempat, deklinasi_hari_ini, h_waktu, e, TZ, bujur_tempat):
    lintang_tempat = math.radians(lintang_tempat)
    deklinasi_hari_ini = math.radians(deklinasi_hari_ini)
    h_waktu = math.radians(-h_waktu)
    t = math.degrees(math.acos(-math.tan(lintang_tempat)* math.tan(deklinasi_hari_ini)+ 1/math.cos(lintang_tempat)* 1/math.cos(deklinasi_hari_ini)* math.sin(h_waktu)))
    t = t/15
    kwd = ((TZ*15) - bujur_tempat)/15
    waktu_magrib = 12 - e + t + kwd

    return waktu_magrib, t


#-----------------------------------------------------------------------------------------------------------#


#PERHITUNGAN MATAHARI
#LOW ACCURACY
def perhitungan_Low(Tjd):
    U = Tjd/100
    L0 = (280.46646 + (36000.76983*Tjd)+ (0.0003032*(Tjd**2)))%360
    
    #M
    M = (357.52911 + (35999.05029*Tjd)+ (0.0001537*(Tjd**2)))%360
    Mrad = math.radians(M)

    #eksentrisitas
    eksentrisitas = 0.016708634 - (0.000042037*Tjd) - (0.0000001267*(Tjd**2))
    
    #Sun Equation of the Center
    C = ((1.914602-(0.004817*Tjd)- 0.000014*(Tjd**2))* math.sin(Mrad) + (0.019993-(0.000101*Tjd))* math.sin(2*Mrad) + 0.000289 * math.sin(3*Mrad))
    
    #longitude matahari low accuracy
    longitude = L0 + C
    
    #True Anomaly = Anomali Sejati
    v = M + C
    vrad = math.radians(v)

    #center of the sun and the earth = Radius (R) low accuracy
    R = (1.000001018*(1-(eksentrisitas**2)) / (1 + eksentrisitas *math.cos(vrad)))
    
    #omega
    omega = (125.04 - 1934.136*Tjd)
    omegarad = math.radians(omega)
    
    #lamda
    lamda = (longitude - 0.00569 - 0.00478 * math.sin(omegarad))
    lamdarad = math.radians(lamda)

    #obliquity
    epsilon0 = 23 + 26/60 + 21.448/3600 - 46.815*Tjd/3600 - 0.00059*((Tjd**2)/3600) + 0.001813*((Tjd**3)/3600)
    epsilon_delta = 0.00256*math.cos(omegarad)
    obliquity_benar = epsilon0 + epsilon_delta
    obliquity_benarrad = math.radians(obliquity_benar)

    #alpha app (apparent)
    right_ascension_low = (((math.degrees(math.atan2((math.cos(obliquity_benarrad)* math.sin(lamdarad)), math.cos(lamdarad)))))%360)

    #deklinasi
    deklinasi = ((math.degrees(math.asin(math.sin(obliquity_benarrad)* math.sin(lamdarad)))))

    return L0, M, eksentrisitas, C, longitude, R, omega, lamda, right_ascension_low, deklinasi


#-----------------------------------------------------------------------------------------------------------#


#HIGH ACCURACY
def perhitungan_high (T, delta_nutasi):
    #L bumi
    earth_L0 = 0
    earth_L1 = 0
    earth_L2 = 0
    earth_L3 = 0
    earth_L4 = 0
    earth_L5 = 0
    #L0
    for index, i in data_earth_L0.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_L01 = A * math.cos(B + C * T)
        earth_L0 = earth_L0 + hasil_L01
    #L1
    for index, i in data_earth_L1.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_L11 = A * math.cos(B + C * T)
        earth_L1 = earth_L1 + hasil_L11
    #L2
    for index, i in data_earth_L2.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_L21 = A * math.cos(B + C * T)
        earth_L2 = earth_L2 + hasil_L21
    #L3
    for index, i in data_earth_L3.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_L31 = A * math.cos(B + C * T )
        earth_L3 = earth_L3 + hasil_L31
    #L4
    for index, i in data_earth_L4.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_L41 = A * math.cos(B + C * T)
        earth_L4 = earth_L4 + hasil_L41
    #L5
    for index, i in data_earth_L5.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_L51 = A * math.cos(B + C * T)
        earth_L5 = earth_L5 + hasil_L51
    L_gabungan = (earth_L0 + earth_L1*T + earth_L2*T**2 + earth_L3*T**3 + earth_L4*T**4 + earth_L5*T**5)/10**8
    L_earth = ((math.degrees(L_gabungan))%360)

    #B
    earth_B0 = 0
    earth_B1 = 0
    #B0
    for index, i in data_earth_B0.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_B01 = A * math.cos(B + C * T)
        earth_B0 = earth_B0 + hasil_B01
    #B1
    for index, i in data_earth_B1.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_B11 = A * math.cos(B + C * T)
        earth_B1 = earth_B1 + hasil_B11
    B_gabungan = (earth_B0 + earth_B1*T)/100000000
    B1 = math.degrees(B_gabungan)
    B_earth = B1 * 3600

    #R
    earth_R0 = 0
    earth_R1 = 0
    earth_R2 = 0
    earth_R3 = 0
    earth_R4 = 0
    #R0
    for index, i in data_earth_R0.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_R01 = A * math.cos(B + C * T)
        earth_R0 = earth_R0 + hasil_R01
    #R1
    for index, i in data_earth_R1.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_R11 = A * math.cos(B + C * T)
        earth_R1 = earth_R1 + hasil_R11
    #R2
    for index, i in data_earth_R2.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_R21 = A * math.cos(B + C * T)
        earth_R2 = earth_R2 + hasil_R21
    #R3
    for index, i in data_earth_R3.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_R31 = A * math.cos(B + C * T)
        earth_R3 = earth_R3 + hasil_R31
    #R4
    for index, i in data_earth_R4.iterrows():
        A = i['A']
        B = i['B']
        C = i['C']
        hasil_R41 = A * math.cos(B + C * T)
        earth_R4 = earth_R4 + hasil_R41
    R_gabungan = (earth_R0 + earth_R1*T + earth_R2*T**2 + earth_R3*T**3 + earth_R4*T**4)/10**8
    R_earth = R_gabungan
    
    #longitude matahari high accuracy = longitude ha
    longitude_matahari = ((L_earth + 180)%360)

    #latitude
    latitude_matahari = -(B_earth)

    #Conversion to the FK5 system
    #Apparent longitude aksen = AL #T*10 karena T ini sudah dibagi 10 diatas maka dikali 10 disini
    apparent_longitude_aksen = (longitude_matahari - (1.397*(T*10)) - (0.00031*((T*10)**2)))
    delta_longitude = -0.09033/3600
    delta_latitude = +0.03916*(math.cos(math.radians(apparent_longitude_aksen)) - math.sin(math.radians(apparent_longitude_aksen)))
    
    #whence
    longitude_baru = longitude_matahari + delta_longitude
    latitude_baru = latitude_matahari + delta_latitude
    #delta Apperent Longitude
    #delta_AL = 3548.193+118.568*math.sin(math.radians(87.5287+359993.7286*T))+2.476*math.sin(math.radians(85.0561+719987.4571*T))+1.376*math.sin(math.radians(27.8502+4452671.1152*T))+0.119*math.sin(math.radians(73.1375+450368.8564*T))+0.114*math.sin(math.radians(337.2264+329644.6718*T))+0.086*math.sin(math.radians(222.5400+659289.3436*T))+0.078*math.sin(math.radians(162.8136+9224659.7915*T))+0.054*math.sin(math.radians(82.5823+1079981.1857*T))+0.052*math.sin(math.radians(171.5189+225184.4282*T))+0.034*math.sin(math.radians(30.3214+4092677.3866*T))+0.033*math.sin(math.radians(119.8105+337181.4711*T))+0.023*math.sin(math.radians(247.5418+299295.6151*T))+0.023*math.sin(math.radians(325.1526+315559.5560*T))+0.021*math.sin(math.radians(155.1241+675553.2846*T))+7.311*T*math.sin(math.radians(333.4515+359993.7286*T))+0.305*T*math.sin(math.radians(330.9814+719987.4571*T))+0.010*T*math.sin(math.radians(328.5170+1079981.1857*T))+0.309*(T**2)*math.sin(math.radians(241.4518+359993.7286*T))+0.021*(T**2)*math.sin(math.radians(205.0482+719987.4571*T))+0.004*(T**2)*math.sin(math.radians(297.8610+4452671.1152*T))+0.010*(T**3)*math.sin(math.radians(154.7066+359993.7286*T))
    #koreksi besar
    #koreksi_aberration = -0.005775518 * R_earth * delta_AL

    #aberration
    aberration = (-20.4898/(3600*R_earth))

    #Apperent Longitude
    apparent_longitude = (longitude_baru + delta_nutasi + aberration)

    return L_earth, B_earth, R_earth, longitude_matahari, latitude_matahari, apparent_longitude_aksen, delta_longitude, delta_latitude, longitude_baru, latitude_baru, aberration, apparent_longitude


#-----------------------------------------------------------------------------------------------------------#


#PERHITUNGAN BULAN
def perhitungan_posisi_bulan (Tjd, delta_nutasi):
    L_aksen = ((218.3164477 + 481267.88123421*Tjd - 0.0015786 *(Tjd**2) + (Tjd**3)/538841 - (Tjd**4)/65194000)%360)
    D = ((297.8501921 + 445267.1114034*Tjd - 0.0018819*(Tjd**2) + (Tjd**3)/545868 - (Tjd**4)/113065000)%360)
    M = ((357.5291092 + 35999.0502909*Tjd - 0.0001536*(Tjd**2) + (Tjd**3)/24490000)%360)
    M_aksen = ((134.9633964 + 477198.8675055*Tjd + 0.0087414*(Tjd**2) + (Tjd**3)/69699 - (Tjd**4)/14712000)%360)
    F = ((93.2720950 + 483202.0175233*Tjd - 0.0036539*(Tjd**2) - (Tjd**3)/3526000 + (Tjd**4)/863310000)%360)
    A1 = ((119.75 + 131.849*Tjd)%360)
    A2 = ((53.09 + 479264.290*Tjd)%360)
    A3 = ((313.45 + 481266.484*Tjd)%360)
    E = (1 - 0.002516*Tjd - 0.0000074*(Tjd**2))

    longitude_bulan1 = 0
    for index, i in data_longitude_bulan.iterrows():
        Dp = i['D']
        Mp = i['M']
        M_aksenp = i["M'"]
        Fp = i['F']
        f2p = i['koefisien']
        hasil_longitude0 = f2p*(E**(abs(Mp)))* math.sin(((math.radians(D*Dp)) + (math.radians(M*Mp)) + (math.radians(M_aksen*M_aksenp)) + (math.radians(F*Fp))))
        longitude_bulan1 = longitude_bulan1 + hasil_longitude0
    longitude_bulan = ((longitude_bulan1 + 3958 * math.sin(math.radians(A1)) + 1962 * math.sin(math.radians(L_aksen - F)) + 318 * math.sin(math.radians(A2)))/1000000)
    
    latitude_bulan1 = 0
    for index, i in data_ekliptika_bulan.iterrows():
        Dp = i['D']
        Mp = i['M']
        M_aksenp = i["M'"]
        Fp = i['F']
        f2p = i['koefisien']
        hasil_latitude0 = f2p*(E**(abs(Mp)))* math.sin(((math.radians(D*Dp)) + (math.radians(M*Mp)) + (math.radians(M_aksen*M_aksenp)) + (math.radians(F*Fp))))
        latitude_bulan1 = latitude_bulan1 + hasil_latitude0
    latitude_bulan = ((latitude_bulan1 - 2235 * math.sin(math.radians(L_aksen)) + 382 * math.sin(math.radians(A3)) + 175 * math.sin(math.radians(A1 - F)) + 175 * math.sin(math.radians(A1 + F)) + 127 * math.sin(math.radians(L_aksen - M_aksen)) - 115 * math.sin(math.radians(L_aksen + M_aksen)))/1000000)
    
    distance_bulan1 = 0
    for index, i in data_distance_bulan.iterrows():
        Dp = i['D']
        Mp = i['M']
        M_aksenp = i["M'"]
        Fp = i['F']
        f2p = i['koefisien']
        hasil_distance0 = f2p*(E**(abs(Mp)))* math.cos(((math.radians(D*Dp)) + (math.radians(M*Mp)) + (math.radians(M_aksen*M_aksenp)) + (math.radians(F*Fp))))
        distance_bulan1 = distance_bulan1 + hasil_distance0
    distance_bulan = (distance_bulan1/1000)

    apparent_longitude = L_aksen + longitude_bulan
    distance_to_earth = 385000.56 + distance_bulan
    parallax = (math.degrees(math.asin(6378.14/368409.7)))
    apparent_longitude_bulan = (apparent_longitude + delta_nutasi)

    return L_aksen, D, M, M_aksen, F, A1, A2, A3, E, longitude_bulan, latitude_bulan, distance_bulan, apparent_longitude_bulan, distance_to_earth, parallax


#-----------------------------------------------------------------------------------------------------------#


#PERHITUNGAN new moon
def fase_bulan(month, year, delta_T, TZ):

    # #kabisat & basitoh
    # #basitoh
    # if (month == 1):
    #     year1 = 31/365
    #     year0 = year + year1
    # elif (month == 2 and year % 4 != 0):
    #     year1 = 59/365
    #     year0 = year + year1
    # elif (month == 3 and year % 4 != 0):
    #     year1 = 90/365
    #     year0 = year + year1
    # elif (month == 4 and year % 4 != 0):
    #     year1 = 120/365
    #     year0 = year + year1
    # elif (month == 5 and year % 4 != 0):
    #     year1 = 151/365
    #     year0 = year + year1
    # elif (month == 6 and year % 4 != 0):
    #     year1 = 181/365
    #     year0 = year + year1
    # elif (month == 7 and year % 4 != 0):
    #     year1 = 212/365
    #     year0 = year + year1
    # elif (month == 8 and year % 4 != 0):
    #     year1 = 243/365
    #     year0 = year + year1
    # elif (month == 9 and year % 4 != 0):
    #     year1 = 273/365
    #     year0 = year + year1
    # elif (month == 10 and year % 4 != 0):
    #     year1 = 304/365
    #     year0 = year + year1
    # elif (month == 11 and year % 4 != 0):
    #     year1 = 334/365
    #     year0 = year + year1
    # elif (month == 12 and year % 4 != 0):
    #     year1 = 365/365
    #     year0 = year + year1
    # #kabisat
    # elif (month == 2 and year % 4 == 0):
    #     year1 = 60/366
    #     year0 = year + year1
    # elif (month == 3 and year % 4 == 0):
    #     year1 = 91/366
    #     year0 = year + year1
    # elif (month == 4 and year % 4 == 0):
    #     year1 = 121/366
    #     year0 = year + year1
    # elif (month == 5 and year % 4 == 0):
    #     year1 = 152/366
    #     year0 = year + year1
    # elif (month == 6 and year % 4 == 0):
    #     year1 = 182/366
    #     year0 = year + year1
    # elif (month == 7 and year % 4 == 0):
    #     year1 = 213/366
    #     year0 = year + year1
    # elif (month == 8 and year % 4 == 0):
    #     year1 = 244/366
    #     year0 = year + year1
    # elif (month == 9 and year % 4 == 0):
    #     year1 = 274/366
    #     year0 = year + year1
    # elif (month == 10 and year % 4 == 0):
    #     year1 = 305/366
    #     year0 = year + year1
    # elif (month == 11 and year % 4 == 0):
    #     year1 = 335/366
    #     year0 = year + year1
    # elif (month == 12 and year % 4 == 0):
    #     year1 = 366/366
    #     year0 = year + year1
    # k_fase_bulan = math.floor(((year0 - 2000) * 12.3685))
    # menggunakan perhitungan tanggal hijriyah karena menggunakan jean meeus ada eror di perhitungan bulan juli (7) 2024

    k_fase_bulan = 12 * year + month - 17050
    T_fase_bulan = (k_fase_bulan/1236.85)
    E_bulan = 1 - 0.002516* T_fase_bulan - 0.0000074* T_fase_bulan**2
    JDE_fase_bulan = (2451550.09766 + 29.530588861 * k_fase_bulan + 0.00015437*(T_fase_bulan**2) - 0.000000150*(T_fase_bulan**3) + 0.00000000073*(T_fase_bulan**4))
    M_fase_bulan = ((2.5534 + 29.10535670*k_fase_bulan - 0.0000014*(T_fase_bulan**2) - 0.00000011*(T_fase_bulan**3))%360)
    M_aksen_fase_bulan = ((201.5643 + 385.81693528*k_fase_bulan + 0.0107582*(T_fase_bulan**2) + 0.00001238*(T_fase_bulan**3) - 0.000000058*(T_fase_bulan**4))%360)
    F_fase_bulan = ((160.7108 + 390.67050284*k_fase_bulan - 0.0016118*(T_fase_bulan**2) - 0.00000227*(T_fase_bulan**3) + 0.000000011*(T_fase_bulan**4))%360)
    omega_fase_bulan = ((124.7746 - 1.56375588*k_fase_bulan + 0.0020672*(T_fase_bulan**2) + 0.00000215*(T_fase_bulan**3))%360)
    A1_fase_bulan = 299.77 +  0.107408*k_fase_bulan - 0.009173*(T_fase_bulan**2)
    A2_fase_bulan = 251.88 +  0.016321*k_fase_bulan
    A3_fase_bulan = 251.83 + 26.651886*k_fase_bulan
    A4_fase_bulan = 349.42 + 36.412478*k_fase_bulan
    A5_fase_bulan = 84.66 + 18.206239*k_fase_bulan
    A6_fase_bulan = 141.74 + 53.303771*k_fase_bulan
    A7_fase_bulan = 207.14 +  2.453732*k_fase_bulan
    A8_fase_bulan = 154.84 +  7.306860*k_fase_bulan
    A9_fase_bulan = 34.52 + 27.261239*k_fase_bulan
    A10_fase_bulan = 207.19 +  0.121824*k_fase_bulan
    A11_fase_bulan = 291.34 +  1.844379*k_fase_bulan
    A12_fase_bulan = 161.72 + 24.198154*k_fase_bulan
    A13_fase_bulan = 239.56 + 25.513099*k_fase_bulan
    A14_fase_bulan = 331.55 +  3.592518*k_fase_bulan

    new_moon = (-0.40720*math.sin(math.radians(M_aksen_fase_bulan)) + 0.17241*E_bulan*math.sin(math.radians(M_fase_bulan)) +  0.01608*math.sin(math.radians(2*M_aksen_fase_bulan)) + 0.01039*math.sin(math.radians(2*F_fase_bulan)) + 0.00739*E_bulan*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan)) - 0.00514*E_bulan*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan)) + 0.00208*math.sin(math.radians((E_bulan**2)*(2*M_fase_bulan))) - 0.00111*math.sin(math.radians(M_aksen_fase_bulan-2*F_fase_bulan)) - 0.00057*math.sin(math.radians(M_aksen_fase_bulan+2*F_fase_bulan)) + 0.00056*E_bulan*math.sin(math.radians(2*M_aksen_fase_bulan+M_fase_bulan)) - 0.00042*math.sin(math.radians(3*M_aksen_fase_bulan)) + 0.00042*E_bulan*math.sin(math.radians(M_fase_bulan+2*F_fase_bulan)) + 0.00038*E_bulan*math.sin(math.radians(M_fase_bulan-2*F_fase_bulan)) - 0.00024*E_bulan*math.sin(math.radians(2*M_aksen_fase_bulan-M_fase_bulan)) - 0.00017*math.sin(math.radians(omega_fase_bulan)) - 0.00007*math.sin(math.radians(M_aksen_fase_bulan+2*M_fase_bulan)) + 0.00004*math.sin(math.radians(2*(M_aksen_fase_bulan-F_fase_bulan))) + 0.00004*math.sin(math.radians(3*M_fase_bulan)) + 0.00003*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan-2*F_fase_bulan)) +0.00003*math.sin(math.radians(2*(M_aksen_fase_bulan+F_fase_bulan))) - 0.00003*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan+2*F_fase_bulan)) + 0.00003*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan+2*F_fase_bulan)) - 0.00002*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan-2*F_fase_bulan)) - 0.00002*math.sin(math.radians(3*M_aksen_fase_bulan+M_fase_bulan)) + 0.00002*math.sin(math.radians(4*M_aksen_fase_bulan)))

    correction_all_phase = ((325*math.sin(math.radians(A1_fase_bulan))+165*math.sin(math.radians(A2_fase_bulan))+164*math.sin(math.radians(A3_fase_bulan))+126*math.sin(math.radians(A4_fase_bulan))+110*math.sin(math.radians(A5_fase_bulan))+62*math.sin(math.radians(A6_fase_bulan))+60*math.sin(math.radians(A7_fase_bulan))+ 56*math.sin(math.radians(A8_fase_bulan))+ 47*math.sin(math.radians(A9_fase_bulan))+ 42*math.sin(math.radians(A10_fase_bulan))+ 40*math.sin(math.radians(A11_fase_bulan))+ 37*math.sin(math.radians(A12_fase_bulan))+ 35*math.sin(math.radians(A13_fase_bulan))+ 23*math.sin(math.radians(A14_fase_bulan)))/1000000)

    JDE_fase_bulan_new_blm = (JDE_fase_bulan + new_moon + correction_all_phase)
    JDE_fase_bulan_new = JDE_fase_bulan_new_blm - delta_T + (TZ/24)
    jd = JDE_fase_bulan_new + 0.5
    z = int(jd)
    f = jd - z
    alpha = int((z - 1867216.25)/36524.25)
    if (z<2299161):
        a = z
    else:
        a = z + 1 + alpha - int(alpha/4)
    b = a + 1524
    c = int((b-122.1)/365.25)
    d = int(365.25*c)
    e = int((b-d)/30.6001)
    day_fase_bulan = b - d - int(30.6001*e)+f
    tanggal_fase_bulan = int(day_fase_bulan)
    jam_fase_bulan = (day_fase_bulan - tanggal_fase_bulan)
    if e<14 :
        bulan_fase_bulan = e-1
    else:
        bulan_fase_bulan = e-13
    if (bulan_fase_bulan>2):
        tahun_fase_bulan = c-4716
    else:
        tahun_fase_bulan = c-4715

    return k_fase_bulan, T_fase_bulan, JDE_fase_bulan, M_fase_bulan, M_aksen_fase_bulan, F_fase_bulan, omega_fase_bulan, correction_all_phase, new_moon, JDE_fase_bulan_new, jam_fase_bulan, tanggal_fase_bulan, bulan_fase_bulan, tahun_fase_bulan


#-----------------------------------------------------------------------------------------------------------#


#PERHITUNGAN new moon
def new_moon(month, year, delta_T, TZ):
    k_fase_bulan = 12 * year + month - 17050
    T_fase_bulan = (k_fase_bulan/1236.85)
    E_bulan = 1 - 0.002516* T_fase_bulan - 0.0000074* T_fase_bulan**2
    JDE_fase_bulan = (2451550.09766 + 29.530588861 * k_fase_bulan + 0.00015437*(T_fase_bulan**2) - 0.000000150*(T_fase_bulan**3) + 0.00000000073*(T_fase_bulan**4))
    M_fase_bulan = ((2.5534 + 29.10535670*k_fase_bulan - 0.0000014*(T_fase_bulan**2) - 0.00000011*(T_fase_bulan**3))%360)
    M_aksen_fase_bulan = ((201.5643 + 385.81693528*k_fase_bulan + 0.0107582*(T_fase_bulan**2) + 0.00001238*(T_fase_bulan**3) - 0.000000058*(T_fase_bulan**4))%360)
    F_fase_bulan = ((160.7108 + 390.67050284*k_fase_bulan - 0.0016118*(T_fase_bulan**2) - 0.00000227*(T_fase_bulan**3) + 0.000000011*(T_fase_bulan**4))%360)
    omega_fase_bulan = ((124.7746 - 1.56375588*k_fase_bulan + 0.0020672*(T_fase_bulan**2) + 0.00000215*(T_fase_bulan**3))%360)
    A1_fase_bulan = 299.77 +  0.107408*k_fase_bulan - 0.009173*(T_fase_bulan**2)
    A2_fase_bulan = 251.88 +  0.016321*k_fase_bulan
    A3_fase_bulan = 251.83 + 26.651886*k_fase_bulan
    A4_fase_bulan = 349.42 + 36.412478*k_fase_bulan
    A5_fase_bulan = 84.66 + 18.206239*k_fase_bulan
    A6_fase_bulan = 141.74 + 53.303771*k_fase_bulan
    A7_fase_bulan = 207.14 +  2.453732*k_fase_bulan
    A8_fase_bulan = 154.84 +  7.306860*k_fase_bulan
    A9_fase_bulan = 34.52 + 27.261239*k_fase_bulan
    A10_fase_bulan = 207.19 +  0.121824*k_fase_bulan
    A11_fase_bulan = 291.34 +  1.844379*k_fase_bulan
    A12_fase_bulan = 161.72 + 24.198154*k_fase_bulan
    A13_fase_bulan = 239.56 + 25.513099*k_fase_bulan
    A14_fase_bulan = 331.55 +  3.592518*k_fase_bulan

    new_moon = (-0.40720*math.sin(math.radians(M_aksen_fase_bulan)) + 0.17241*E_bulan*math.sin(math.radians(M_fase_bulan)) +  0.01608*math.sin(math.radians(2*M_aksen_fase_bulan)) + 0.01039*math.sin(math.radians(2*F_fase_bulan)) + 0.00739*E_bulan*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan)) - 0.00514*E_bulan*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan)) + 0.00208*math.sin(math.radians((E_bulan**2)*(2*M_fase_bulan))) - 0.00111*math.sin(math.radians(M_aksen_fase_bulan-2*F_fase_bulan)) - 0.00057*math.sin(math.radians(M_aksen_fase_bulan+2*F_fase_bulan)) + 0.00056*E_bulan*math.sin(math.radians(2*M_aksen_fase_bulan+M_fase_bulan)) - 0.00042*math.sin(math.radians(3*M_aksen_fase_bulan)) + 0.00042*E_bulan*math.sin(math.radians(M_fase_bulan+2*F_fase_bulan)) + 0.00038*E_bulan*math.sin(math.radians(M_fase_bulan-2*F_fase_bulan)) - 0.00024*E_bulan*math.sin(math.radians(2*M_aksen_fase_bulan-M_fase_bulan)) - 0.00017*math.sin(math.radians(omega_fase_bulan)) - 0.00007*math.sin(math.radians(M_aksen_fase_bulan+2*M_fase_bulan)) + 0.00004*math.sin(math.radians(2*(M_aksen_fase_bulan-F_fase_bulan))) + 0.00004*math.sin(math.radians(3*M_fase_bulan)) + 0.00003*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan-2*F_fase_bulan)) +0.00003*math.sin(math.radians(2*(M_aksen_fase_bulan+F_fase_bulan))) - 0.00003*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan+2*F_fase_bulan)) + 0.00003*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan+2*F_fase_bulan)) - 0.00002*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan-2*F_fase_bulan)) - 0.00002*math.sin(math.radians(3*M_aksen_fase_bulan+M_fase_bulan)) + 0.00002*math.sin(math.radians(4*M_aksen_fase_bulan)))

    correction_all_phase = ((325*math.sin(math.radians(A1_fase_bulan))+165*math.sin(math.radians(A2_fase_bulan))+164*math.sin(math.radians(A3_fase_bulan))+126*math.sin(math.radians(A4_fase_bulan))+110*math.sin(math.radians(A5_fase_bulan))+62*math.sin(math.radians(A6_fase_bulan))+60*math.sin(math.radians(A7_fase_bulan))+ 56*math.sin(math.radians(A8_fase_bulan))+ 47*math.sin(math.radians(A9_fase_bulan))+ 42*math.sin(math.radians(A10_fase_bulan))+ 40*math.sin(math.radians(A11_fase_bulan))+ 37*math.sin(math.radians(A12_fase_bulan))+ 35*math.sin(math.radians(A13_fase_bulan))+ 23*math.sin(math.radians(A14_fase_bulan)))/1000000)

    JDE_fase_bulan_new_blm = (JDE_fase_bulan + new_moon + correction_all_phase)
    JDE_fase_bulan_new = JDE_fase_bulan_new_blm - delta_T + (TZ/24)
    jd = JDE_fase_bulan_new + 0.5
    z = int(jd)
    f = jd - z
    alpha = int((z - 1867216.25)/36524.25)
    if (z<2299161):
        a = z
    else:
        a = z + 1 + alpha - int(alpha/4)
    b = a + 1524
    c = int((b-122.1)/365.25)
    d = int(365.25*c)
    e = int((b-d)/30.6001)
    day_fase_bulan = b - d - int(30.6001*e)+f
    tanggal_fase_bulan = int(day_fase_bulan)
    jam_fase_bulan = (day_fase_bulan - tanggal_fase_bulan)
    if e<14 :
        bulan_fase_bulan = e-1
    else:
        bulan_fase_bulan = e-13
    if (bulan_fase_bulan>2):
        tahun_fase_bulan = c-4716
    else:
        tahun_fase_bulan = c-4715

    return jam_fase_bulan, tanggal_fase_bulan, bulan_fase_bulan, tahun_fase_bulan


#-----------------------------------------------------------------------------------------------------------#


#PERHITUNGAN QUARTAL PERTAMA
def quartal_pertama(month, year, delta_T, TZ):
    k_fase_bulan = (12 * year + month - 17050) + 0.25
    T_fase_bulan = (k_fase_bulan/1236.85)
    E_bulan = 1 - 0.002516* T_fase_bulan - 0.0000074* T_fase_bulan**2
    JDE_fase_bulan = (2451550.09766 + 29.530588861 * k_fase_bulan + 0.00015437*(T_fase_bulan**2) - 0.000000150*(T_fase_bulan**3) + 0.00000000073*(T_fase_bulan**4))
    M_fase_bulan = ((2.5534 + 29.10535670*k_fase_bulan - 0.0000014*(T_fase_bulan**2) - 0.00000011*(T_fase_bulan**3))%360)
    M_aksen_fase_bulan = ((201.5643 + 385.81693528*k_fase_bulan + 0.0107582*(T_fase_bulan**2) + 0.00001238*(T_fase_bulan**3) - 0.000000058*(T_fase_bulan**4))%360)
    F_fase_bulan = ((160.7108 + 390.67050284*k_fase_bulan - 0.0016118*(T_fase_bulan**2) - 0.00000227*(T_fase_bulan**3) + 0.000000011*(T_fase_bulan**4))%360)
    omega_fase_bulan = ((124.7746 - 1.56375588*k_fase_bulan + 0.0020672*(T_fase_bulan**2) + 0.00000215*(T_fase_bulan**3))%360)
    A1_fase_bulan = 299.77 +  0.107408*k_fase_bulan - 0.009173*(T_fase_bulan**2)
    A2_fase_bulan = 251.88 +  0.016321*k_fase_bulan
    A3_fase_bulan = 251.83 + 26.651886*k_fase_bulan
    A4_fase_bulan = 349.42 + 36.412478*k_fase_bulan
    A5_fase_bulan = 84.66 + 18.206239*k_fase_bulan
    A6_fase_bulan = 141.74 + 53.303771*k_fase_bulan
    A7_fase_bulan = 207.14 +  2.453732*k_fase_bulan
    A8_fase_bulan = 154.84 +  7.306860*k_fase_bulan
    A9_fase_bulan = 34.52 + 27.261239*k_fase_bulan
    A10_fase_bulan = 207.19 +  0.121824*k_fase_bulan
    A11_fase_bulan = 291.34 +  1.844379*k_fase_bulan
    A12_fase_bulan = 161.72 + 24.198154*k_fase_bulan
    A13_fase_bulan = 239.56 + 25.513099*k_fase_bulan
    A14_fase_bulan = 331.55 +  3.592518*k_fase_bulan

    new_moon = (-62801 * math.sin(math.radians(M_aksen_fase_bulan)) + 17172 * E_bulan * math.sin(math.radians(M_fase_bulan)) - 1183 * E_bulan * math.sin(math.radians(M_aksen_fase_bulan + M_fase_bulan))+ 862 * math.sin(math.radians(2 * M_aksen_fase_bulan)) + 804 * math.sin(math.radians(2 * F_fase_bulan))+ 454 * E_bulan * math.sin(math.radians(M_aksen_fase_bulan - M_fase_bulan)) + 204 * E_bulan**2 * math.sin(math.radians(2 * M_fase_bulan))- 180 * math.sin(math.radians(M_aksen_fase_bulan - 2 * F_fase_bulan)) - 70 * math.sin(math.radians(M_aksen_fase_bulan + 2 * F_fase_bulan)) - 40 * math.sin(math.radians(3 * M_aksen_fase_bulan))- 34 * E_bulan * math.sin(math.radians(2 * M_aksen_fase_bulan - M_fase_bulan)) + 32 * E_bulan * math.sin(math.radians(M_fase_bulan + 2 * F_fase_bulan)) + 32 * E_bulan * math.sin(math.radians(M_fase_bulan - 2 * F_fase_bulan)) - 28 * E_bulan**2 * math.sin(math.radians(M_aksen_fase_bulan + 2 * M_fase_bulan)) + 27 * E_bulan * math.sin(math.radians(2 * M_aksen_fase_bulan + M_fase_bulan)) - 17 * math.sin(math.radians(omega_fase_bulan))- 5 * math.sin(math.radians(M_aksen_fase_bulan - M_fase_bulan - 2 * F_fase_bulan)) + 4 * math.sin(math.radians(2 * (M_aksen_fase_bulan + F_fase_bulan)))- 4 * math.sin(math.radians(M_aksen_fase_bulan + M_fase_bulan + 2 * F_fase_bulan)) + 4 * math.sin(math.radians(M_aksen_fase_bulan - 2 * M_fase_bulan)) + 3 * math.sin(math.radians(3 * M_fase_bulan)) + 3 * math.sin(math.radians(M_aksen_fase_bulan + M_fase_bulan - 2 * F_fase_bulan)) + 2 * math.sin(math.radians(2 * (M_aksen_fase_bulan - F_fase_bulan))) + 2 * math.sin(math.radians(M_aksen_fase_bulan - M_fase_bulan + 2 * F_fase_bulan)) - 2 * math.sin(math.radians(3 * M_aksen_fase_bulan + M_fase_bulan))+ 306 - 38 * E_bulan * math.cos(math.radians(M_fase_bulan)) + 26 * math.cos(math.radians(M_aksen_fase_bulan)) - 2 * math.cos(math.radians(M_aksen_fase_bulan - M_fase_bulan)) + 2 * math.cos(math.radians(M_aksen_fase_bulan + M_fase_bulan)) + 2 * math.cos(math.radians(2 * F_fase_bulan))) / 100000

    correction_all_phase = ((325*math.sin(math.radians(A1_fase_bulan))+165*math.sin(math.radians(A2_fase_bulan))+164*math.sin(math.radians(A3_fase_bulan))+126*math.sin(math.radians(A4_fase_bulan))+110*math.sin(math.radians(A5_fase_bulan))+62*math.sin(math.radians(A6_fase_bulan))+60*math.sin(math.radians(A7_fase_bulan))+ 56*math.sin(math.radians(A8_fase_bulan))+ 47*math.sin(math.radians(A9_fase_bulan))+ 42*math.sin(math.radians(A10_fase_bulan))+ 40*math.sin(math.radians(A11_fase_bulan))+ 37*math.sin(math.radians(A12_fase_bulan))+ 35*math.sin(math.radians(A13_fase_bulan))+ 23*math.sin(math.radians(A14_fase_bulan)))/1000000)

    JDE_fase_bulan_new_blm = (JDE_fase_bulan + new_moon + correction_all_phase)
    JDE_fase_bulan_new = JDE_fase_bulan_new_blm - delta_T + (TZ/24)
    jd = JDE_fase_bulan_new + 0.5
    z = int(jd)
    f = jd - z
    alpha = int((z - 1867216.25)/36524.25)
    if (z<2299161):
        a = z
    else:
        a = z + 1 + alpha - int(alpha/4)
    b = a + 1524
    c = int((b-122.1)/365.25)
    d = int(365.25*c)
    e = int((b-d)/30.6001)
    day_fase_bulan = b - d - int(30.6001*e)+f
    tanggal_fase_bulan = int(day_fase_bulan)
    jam_fase_bulan = (day_fase_bulan - tanggal_fase_bulan)
    if e<14 :
        bulan_fase_bulan = e-1
    else:
        bulan_fase_bulan = e-13
    if (bulan_fase_bulan>2):
        tahun_fase_bulan = c-4716
    else:
        tahun_fase_bulan = c-4715

    return jam_fase_bulan, tanggal_fase_bulan, bulan_fase_bulan, tahun_fase_bulan


#-----------------------------------------------------------------------------------------------------------#


#PERHITUNGAN FULL MOON
def full_moon(month, year, delta_T, TZ):
    k_fase_bulan = (12 * year + month - 17050) + 0.50
    T_fase_bulan = (k_fase_bulan/1236.85)
    E_bulan = 1 - 0.002516* T_fase_bulan - 0.0000074* T_fase_bulan**2
    JDE_fase_bulan = (2451550.09766 + 29.530588861 * k_fase_bulan + 0.00015437*(T_fase_bulan**2) - 0.000000150*(T_fase_bulan**3) + 0.00000000073*(T_fase_bulan**4))
    M_fase_bulan = ((2.5534 + 29.10535670*k_fase_bulan - 0.0000014*(T_fase_bulan**2) - 0.00000011*(T_fase_bulan**3))%360)
    M_aksen_fase_bulan = ((201.5643 + 385.81693528*k_fase_bulan + 0.0107582*(T_fase_bulan**2) + 0.00001238*(T_fase_bulan**3) - 0.000000058*(T_fase_bulan**4))%360)
    F_fase_bulan = ((160.7108 + 390.67050284*k_fase_bulan - 0.0016118*(T_fase_bulan**2) - 0.00000227*(T_fase_bulan**3) + 0.000000011*(T_fase_bulan**4))%360)
    omega_fase_bulan = ((124.7746 - 1.56375588*k_fase_bulan + 0.0020672*(T_fase_bulan**2) + 0.00000215*(T_fase_bulan**3))%360)
    A1_fase_bulan = 299.77 +  0.107408*k_fase_bulan - 0.009173*(T_fase_bulan**2)
    A2_fase_bulan = 251.88 +  0.016321*k_fase_bulan
    A3_fase_bulan = 251.83 + 26.651886*k_fase_bulan
    A4_fase_bulan = 349.42 + 36.412478*k_fase_bulan
    A5_fase_bulan = 84.66 + 18.206239*k_fase_bulan
    A6_fase_bulan = 141.74 + 53.303771*k_fase_bulan
    A7_fase_bulan = 207.14 +  2.453732*k_fase_bulan
    A8_fase_bulan = 154.84 +  7.306860*k_fase_bulan
    A9_fase_bulan = 34.52 + 27.261239*k_fase_bulan
    A10_fase_bulan = 207.19 +  0.121824*k_fase_bulan
    A11_fase_bulan = 291.34 +  1.844379*k_fase_bulan
    A12_fase_bulan = 161.72 + 24.198154*k_fase_bulan
    A13_fase_bulan = 239.56 + 25.513099*k_fase_bulan
    A14_fase_bulan = 331.55 +  3.592518*k_fase_bulan

    new_moon = (-0.40720*math.sin(math.radians(M_aksen_fase_bulan)) + 0.17241*E_bulan*math.sin(math.radians(M_fase_bulan)) +  0.01608*math.sin(math.radians(2*M_aksen_fase_bulan)) + 0.01039*math.sin(math.radians(2*F_fase_bulan)) + 0.00739*E_bulan*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan)) - 0.00514*E_bulan*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan)) + 0.00208*math.sin(math.radians((E_bulan**2)*(2*M_fase_bulan))) - 0.00111*math.sin(math.radians(M_aksen_fase_bulan-2*F_fase_bulan)) - 0.00057*math.sin(math.radians(M_aksen_fase_bulan+2*F_fase_bulan)) + 0.00056*E_bulan*math.sin(math.radians(2*M_aksen_fase_bulan+M_fase_bulan)) - 0.00042*math.sin(math.radians(3*M_aksen_fase_bulan)) + 0.00042*E_bulan*math.sin(math.radians(M_fase_bulan+2*F_fase_bulan)) + 0.00038*E_bulan*math.sin(math.radians(M_fase_bulan-2*F_fase_bulan)) - 0.00024*E_bulan*math.sin(math.radians(2*M_aksen_fase_bulan-M_fase_bulan)) - 0.00017*math.sin(math.radians(omega_fase_bulan)) - 0.00007*math.sin(math.radians(M_aksen_fase_bulan+2*M_fase_bulan)) + 0.00004*math.sin(math.radians(2*(M_aksen_fase_bulan-F_fase_bulan))) + 0.00004*math.sin(math.radians(3*M_fase_bulan)) + 0.00003*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan-2*F_fase_bulan)) +0.00003*math.sin(math.radians(2*(M_aksen_fase_bulan+F_fase_bulan))) - 0.00003*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan+2*F_fase_bulan)) + 0.00003*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan+2*F_fase_bulan)) - 0.00002*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan-2*F_fase_bulan)) - 0.00002*math.sin(math.radians(3*M_aksen_fase_bulan+M_fase_bulan)) + 0.00002*math.sin(math.radians(4*M_aksen_fase_bulan)))

    correction_all_phase = ((325*math.sin(math.radians(A1_fase_bulan))+165*math.sin(math.radians(A2_fase_bulan))+164*math.sin(math.radians(A3_fase_bulan))+126*math.sin(math.radians(A4_fase_bulan))+110*math.sin(math.radians(A5_fase_bulan))+62*math.sin(math.radians(A6_fase_bulan))+60*math.sin(math.radians(A7_fase_bulan))+ 56*math.sin(math.radians(A8_fase_bulan))+ 47*math.sin(math.radians(A9_fase_bulan))+ 42*math.sin(math.radians(A10_fase_bulan))+ 40*math.sin(math.radians(A11_fase_bulan))+ 37*math.sin(math.radians(A12_fase_bulan))+ 35*math.sin(math.radians(A13_fase_bulan))+ 23*math.sin(math.radians(A14_fase_bulan)))/1000000)

    JDE_fase_bulan_new_blm = (JDE_fase_bulan + new_moon + correction_all_phase)
    JDE_fase_bulan_new = JDE_fase_bulan_new_blm - delta_T + (TZ/24)
    jd = JDE_fase_bulan_new + 0.5
    z = int(jd)
    f = jd - z
    alpha = int((z - 1867216.25)/36524.25)
    if (z<2299161):
        a = z
    else:
        a = z + 1 + alpha - int(alpha/4)
    b = a + 1524
    c = int((b-122.1)/365.25)
    d = int(365.25*c)
    e = int((b-d)/30.6001)
    day_fase_bulan = b - d - int(30.6001*e)+f
    tanggal_fase_bulan = int(day_fase_bulan)
    jam_fase_bulan = (day_fase_bulan - tanggal_fase_bulan)
    if e<14 :
        bulan_fase_bulan = e-1
    else:
        bulan_fase_bulan = e-13
    if (bulan_fase_bulan>2):
        tahun_fase_bulan = c-4716
    else:
        tahun_fase_bulan = c-4715

    return jam_fase_bulan, tanggal_fase_bulan, bulan_fase_bulan, tahun_fase_bulan


#-----------------------------------------------------------------------------------------------------------#


#PERHITUNGAN QUARTAL AKHIR
def quartal_akhir(month, year, delta_T, TZ):
    k_fase_bulan = (12 * year + month - 17050) + 0.75
    T_fase_bulan = (k_fase_bulan/1236.85)
    E_bulan = 1 - 0.002516* T_fase_bulan - 0.0000074* T_fase_bulan**2
    JDE_fase_bulan = (2451550.09766 + 29.530588861 * k_fase_bulan + 0.00015437*(T_fase_bulan**2) - 0.000000150*(T_fase_bulan**3) + 0.00000000073*(T_fase_bulan**4))
    M_fase_bulan = ((2.5534 + 29.10535670*k_fase_bulan - 0.0000014*(T_fase_bulan**2) - 0.00000011*(T_fase_bulan**3))%360)
    M_aksen_fase_bulan = ((201.5643 + 385.81693528*k_fase_bulan + 0.0107582*(T_fase_bulan**2) + 0.00001238*(T_fase_bulan**3) - 0.000000058*(T_fase_bulan**4))%360)
    F_fase_bulan = ((160.7108 + 390.67050284*k_fase_bulan - 0.0016118*(T_fase_bulan**2) - 0.00000227*(T_fase_bulan**3) + 0.000000011*(T_fase_bulan**4))%360)
    omega_fase_bulan = ((124.7746 - 1.56375588*k_fase_bulan + 0.0020672*(T_fase_bulan**2) + 0.00000215*(T_fase_bulan**3))%360)
    A1_fase_bulan = 299.77 +  0.107408*k_fase_bulan - 0.009173*(T_fase_bulan**2)
    A2_fase_bulan = 251.88 +  0.016321*k_fase_bulan
    A3_fase_bulan = 251.83 + 26.651886*k_fase_bulan
    A4_fase_bulan = 349.42 + 36.412478*k_fase_bulan
    A5_fase_bulan = 84.66 + 18.206239*k_fase_bulan
    A6_fase_bulan = 141.74 + 53.303771*k_fase_bulan
    A7_fase_bulan = 207.14 +  2.453732*k_fase_bulan
    A8_fase_bulan = 154.84 +  7.306860*k_fase_bulan
    A9_fase_bulan = 34.52 + 27.261239*k_fase_bulan
    A10_fase_bulan = 207.19 +  0.121824*k_fase_bulan
    A11_fase_bulan = 291.34 +  1.844379*k_fase_bulan
    A12_fase_bulan = 161.72 + 24.198154*k_fase_bulan
    A13_fase_bulan = 239.56 + 25.513099*k_fase_bulan
    A14_fase_bulan = 331.55 +  3.592518*k_fase_bulan

    new_moon = (-62801 * math.sin(math.radians(M_aksen_fase_bulan)) + 17172 * E_bulan * math.sin(math.radians(M_fase_bulan)) - 1183 * E_bulan * math.sin(math.radians(M_aksen_fase_bulan + M_fase_bulan))+ 862 * math.sin(math.radians(2 * M_aksen_fase_bulan)) + 804 * math.sin(math.radians(2 * F_fase_bulan))+ 454 * E_bulan * math.sin(math.radians(M_aksen_fase_bulan - M_fase_bulan)) + 204 * E_bulan**2 * math.sin(math.radians(2 * M_fase_bulan))- 180 * math.sin(math.radians(M_aksen_fase_bulan - 2 * F_fase_bulan)) - 70 * math.sin(math.radians(M_aksen_fase_bulan + 2 * F_fase_bulan)) - 40 * math.sin(math.radians(3 * M_aksen_fase_bulan))- 34 * E_bulan * math.sin(math.radians(2 * M_aksen_fase_bulan - M_fase_bulan)) + 32 * E_bulan * math.sin(math.radians(M_fase_bulan + 2 * F_fase_bulan)) + 32 * E_bulan * math.sin(math.radians(M_fase_bulan - 2 * F_fase_bulan)) - 28 * E_bulan**2 * math.sin(math.radians(M_aksen_fase_bulan + 2 * M_fase_bulan)) + 27 * E_bulan * math.sin(math.radians(2 * M_aksen_fase_bulan + M_fase_bulan)) - 17 * math.sin(math.radians(omega_fase_bulan))- 5 * math.sin(math.radians(M_aksen_fase_bulan - M_fase_bulan - 2 * F_fase_bulan)) + 4 * math.sin(math.radians(2 * (M_aksen_fase_bulan + F_fase_bulan)))- 4 * math.sin(math.radians(M_aksen_fase_bulan + M_fase_bulan + 2 * F_fase_bulan)) + 4 * math.sin(math.radians(M_aksen_fase_bulan - 2 * M_fase_bulan)) + 3 * math.sin(math.radians(3 * M_fase_bulan)) + 3 * math.sin(math.radians(M_aksen_fase_bulan + M_fase_bulan - 2 * F_fase_bulan)) + 2 * math.sin(math.radians(2 * (M_aksen_fase_bulan - F_fase_bulan))) + 2 * math.sin(math.radians(M_aksen_fase_bulan - M_fase_bulan + 2 * F_fase_bulan)) - 2 * math.sin(math.radians(3 * M_aksen_fase_bulan + M_fase_bulan)) - (306 - 38 * E_bulan * math.cos(math.radians(M_fase_bulan)) + 26 * math.cos(math.radians(M_aksen_fase_bulan)) - 2 * math.cos(math.radians(M_aksen_fase_bulan - M_fase_bulan)) + 2 * math.cos(math.radians(M_aksen_fase_bulan + M_fase_bulan)) + 2 * math.cos(math.radians(2 * F_fase_bulan)))) / 100000

    correction_all_phase = ((325*math.sin(math.radians(A1_fase_bulan))+165*math.sin(math.radians(A2_fase_bulan))+164*math.sin(math.radians(A3_fase_bulan))+126*math.sin(math.radians(A4_fase_bulan))+110*math.sin(math.radians(A5_fase_bulan))+62*math.sin(math.radians(A6_fase_bulan))+60*math.sin(math.radians(A7_fase_bulan))+ 56*math.sin(math.radians(A8_fase_bulan))+ 47*math.sin(math.radians(A9_fase_bulan))+ 42*math.sin(math.radians(A10_fase_bulan))+ 40*math.sin(math.radians(A11_fase_bulan))+ 37*math.sin(math.radians(A12_fase_bulan))+ 35*math.sin(math.radians(A13_fase_bulan))+ 23*math.sin(math.radians(A14_fase_bulan)))/1000000)

    JDE_fase_bulan_new_blm = (JDE_fase_bulan + new_moon + correction_all_phase)
    JDE_fase_bulan_new = JDE_fase_bulan_new_blm - delta_T + (TZ/24)
    jd = JDE_fase_bulan_new + 0.5
    z = int(jd)
    f = jd - z
    alpha = int((z - 1867216.25)/36524.25)
    if (z<2299161):
        a = z
    else:
        a = z + 1 + alpha - int(alpha/4)
    b = a + 1524
    c = int((b-122.1)/365.25)
    d = int(365.25*c)
    e = int((b-d)/30.6001)
    day_fase_bulan = b - d - int(30.6001*e)+f
    tanggal_fase_bulan = int(day_fase_bulan)
    jam_fase_bulan = (day_fase_bulan - tanggal_fase_bulan)
    if e<14 :
        bulan_fase_bulan = e-1
    else:
        bulan_fase_bulan = e-13
    if (bulan_fase_bulan>2):
        tahun_fase_bulan = c-4716
    else:
        tahun_fase_bulan = c-4715

    return jam_fase_bulan, tanggal_fase_bulan, bulan_fase_bulan, tahun_fase_bulan

#-----------------------------------------------------------------------------------------------------------#


###############################################     PERHITUNGAN HILAL     ####################################################################

def perhitungan_hilal(detik, menit, hours, day, month, year, TZ, lintang_tempat, bujur_tempat, tinggi_tempat, delta_T):

    def jam(waktu):
        jam = int(waktu)
        menit = int((abs(waktu)-abs(jam))*60)
        detik = round(((abs(waktu)-abs(jam))*60 - menit)*60)
        if waktu <= 0:
            jam = int(waktu)
            if jam == 0 :
                menit = -menit

        return jam, menit, detik

    def JD (d, m, H, D, M, Y, TZ):
        if M <=2 :
            M = M + 12
            Y = Y - 1
            A = int(Y/100)
        else :
            A = int(Y/100)
        if Y <=1582:
            B = 0
        else:
            B = 2 - A + int(A/4)
        jam = H
        menit = m/60
        detik = d/3600
        waktu = (jam + menit + detik)/24
        JD_total = int(365.25*(Y + 4716)) + int(30.6001*(M+1)) + D + B - 1524.5 + waktu - TZ/24
        
        return JD_total

    def transformasi(apparent_longitude, obliquity, latitude, LST_nampak, lintang_tempat):
        #transformasi dari ekliptika ke equatorial latitude nya salah diganti latitude baru
        right_ascension = ((math.degrees(math.atan2((math.sin(math.radians(apparent_longitude))*math.cos(math.radians(obliquity))-math.tan(math.radians(latitude))*math.sin(math.radians(obliquity))), math.cos(math.radians(apparent_longitude)))))%360)
        deklinasi = (math.degrees(math.asin(math.sin(math.radians(latitude))*math.cos(math.radians(obliquity))+math.cos(math.radians(latitude))*math.sin(math.radians(obliquity))*math.sin(math.radians(apparent_longitude)))))
        hour_angel = LST_nampak * 15 - right_ascension
        azimuth = math.degrees(math.atan2(math.sin(math.radians(hour_angel)), math.cos(math.radians(hour_angel))* math.sin(math.radians(lintang_tempat)) - math.tan(math.radians(deklinasi))* math.cos(math.radians(lintang_tempat))))+180
        altitude = math.degrees(math.asin(math.sin(math.radians(lintang_tempat))* math.sin(math.radians(deklinasi))+ math.cos(math.radians(lintang_tempat))* math.cos(math.radians(deklinasi))* math.cos(math.radians(hour_angel))))
        
        return right_ascension, deklinasi, azimuth, altitude

    def sidereal(T, JD, delta_nutasi, obliquity, bujur_tempat):
        #dalam jam
        O0 = (6*3600) + (41*60) + 50.54841 + 8640184.812866*T + 0.093104*(T**2) - 0.0000062*(T**3)
        #dalam degress dan decimal
        o0 = 100.46061837 + 36000.770053608*T + 0.000387933*(T**2) - (T**3)/38710000
        GST = ((280.46061837 + 360.98564736629*(JD - 2451545) + 0.000387933*(T**2) - (T**3)/38710000)%360)/15
        GST_nampak = GST + delta_nutasi*math.cos(math.radians(obliquity))/15
        LST_nampak = (GST_nampak + bujur_tempat/15)%24
        return O0, o0, GST, GST_nampak, LST_nampak

    def nutasi_obliquity(Tjd):
        U = Tjd/100
        #D, M, M1, F
        D_true_obliquity = 297.85036 + 445267.111480*Tjd - 0.0019142*(Tjd**2) + (Tjd**3)/189474
        M_true_obliquity = 357.52772 + 35999.050340*Tjd - 0.0001603*(Tjd**2) - (Tjd**3)/300000
        M1_true_obliquity = 134.96298 + 477198.867398*Tjd + 0.0086972*(Tjd**2) + (Tjd**3)/56250
        F_true_obliquity = 93.27191 + 483202.017538*Tjd - 0.0036825*(Tjd**2) + (Tjd**3)/327270
        omega = 125.04 - 1934.136*Tjd

        #gangerti apa ini ???
        #L = 280.4665 + 36000.7698*Tjd
        #L_aksen = 218.3165 + 481267.8813*Tjd
        #delta_nutasi = (-17.20/3600) * math.sin(math.radians(omega))+ (1.32/3600) * math.sin(math.radians(2*L)) - (0.23/3600) * math.sin(math.radians(2*L_aksen)) + (0.21/3600) * math.sin(math.radians(2*omega))
        #delta_obliquity = (9.20/3600) * math.cos(math.radians(omega))+ (0.57/3600) * math.cos(math.radians(2*L)) + (0.10/3600) * math.cos(math.radians(2*L_aksen)) - (0.09/3600) * math.cos(math.radians(2*omega))
        
        #delta obliquity
        hs = 0
        for index, i in data_obliquity.iterrows():
            d = i['D']
            m = i['M']
            m1 = i["M'"]
            f = i['F']
            ome = i['Ω']
            f2 = i['koefisien 1']
            g = i['koefisien 2']
            hasil1 = (f2 + (g*Tjd)) * (math.cos(((math.radians(d*D_true_obliquity)) + (math.radians(m*M_true_obliquity)) + (math.radians(m1*M1_true_obliquity)) + (math.radians(f*F_true_obliquity)) + (math.radians(ome*omega)))))
            hs = hs + hasil1
        
        #delta Nutasi
        hss = 0
        for index, i in data_nutasi.iterrows():
            d = i['D']
            m = i['M']
            m1 = i["M'"]
            f = i['F']
            ome = i['Ω']
            f2 = i['koefisien 1']
            g = i['koefisien 2']
            hasil00 = (f2 + (g*Tjd)) * (math.sin(((math.radians(d*D_true_obliquity)) + (math.radians(m*M_true_obliquity)) + (math.radians(m1*M1_true_obliquity)) + (math.radians(f*F_true_obliquity)) + (math.radians(ome*omega)))))
            hss = hss + hasil00

        delta_nutasi = (hss/10000/3600)
        delta_obliquity = (hs/10000/3600)
        obliquity0 = (((23*3600) + (26*60) + 21.448 - 46.8150*Tjd - 0.00059*Tjd**2 + 0.001813*Tjd**3)/3600)
        #obliquity_nol = ((23*3600) + (26*60) + 21.448 - 4680.93*U - 1.55*(U**2) + 1999.25*(U**3) - 51.38*(U**4) - 249.67*(U**5) - 39.05*(U**6) + 7.12*(U**7) + 27.87*(U**8) + 5.79*(U**9) + 2.45*(U**10))/3600
        obliquity = delta_obliquity + obliquity0
        return delta_nutasi, delta_obliquity, obliquity0, obliquity

    def perhitungan_high (T, delta_nutasi):
        #L bumi
        earth_L0 = 0
        earth_L1 = 0
        earth_L2 = 0
        earth_L3 = 0
        earth_L4 = 0
        earth_L5 = 0
        #L0
        for index, i in data_earth_L0.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_L01 = A * math.cos(B + C * T)
            earth_L0 = earth_L0 + hasil_L01
        #L1
        for index, i in data_earth_L1.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_L11 = A * math.cos(B + C * T)
            earth_L1 = earth_L1 + hasil_L11
        #L2
        for index, i in data_earth_L2.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_L21 = A * math.cos(B + C * T)
            earth_L2 = earth_L2 + hasil_L21
        #L3
        for index, i in data_earth_L3.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_L31 = A * math.cos(B + C * T )
            earth_L3 = earth_L3 + hasil_L31
        #L4
        for index, i in data_earth_L4.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_L41 = A * math.cos(B + C * T)
            earth_L4 = earth_L4 + hasil_L41
        #L5
        for index, i in data_earth_L5.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_L51 = A * math.cos(B + C * T)
            earth_L5 = earth_L5 + hasil_L51
        L_gabungan = (earth_L0 + earth_L1*T + earth_L2*T**2 + earth_L3*T**3 + earth_L4*T**4 + earth_L5*T**5)/10**8
        L_earth = ((math.degrees(L_gabungan))%360)

        #B
        earth_B0 = 0
        earth_B1 = 0
        #B0
        for index, i in data_earth_B0.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_B01 = A * math.cos(B + C * T)
            earth_B0 = earth_B0 + hasil_B01
        #B1
        for index, i in data_earth_B1.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_B11 = A * math.cos(B + C * T)
            earth_B1 = earth_B1 + hasil_B11
        B_gabungan = (earth_B0 + earth_B1*T)/100000000
        B1 = math.degrees(B_gabungan)
        B_earth = B1 * 3600

        #R
        earth_R0 = 0
        earth_R1 = 0
        earth_R2 = 0
        earth_R3 = 0
        earth_R4 = 0
        #R0
        for index, i in data_earth_R0.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_R01 = A * math.cos(B + C * T)
            earth_R0 = earth_R0 + hasil_R01
        #R1
        for index, i in data_earth_R1.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_R11 = A * math.cos(B + C * T)
            earth_R1 = earth_R1 + hasil_R11
        #R2
        for index, i in data_earth_R2.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_R21 = A * math.cos(B + C * T)
            earth_R2 = earth_R2 + hasil_R21
        #R3
        for index, i in data_earth_R3.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_R31 = A * math.cos(B + C * T)
            earth_R3 = earth_R3 + hasil_R31
        #R4
        for index, i in data_earth_R4.iterrows():
            A = i['A']
            B = i['B']
            C = i['C']
            hasil_R41 = A * math.cos(B + C * T)
            earth_R4 = earth_R4 + hasil_R41
        R_gabungan = (earth_R0 + earth_R1*T + earth_R2*T**2 + earth_R3*T**3 + earth_R4*T**4)/10**8
        R_earth = R_gabungan
        
        #longitude matahari high accuracy = longitude ha
        longitude_matahari = ((L_earth + 180)%360)

        #latitude
        latitude_matahari = -(B_earth)

        #Conversion to the FK5 system
        #Apparent longitude aksen = AL #T*10 karena T ini sudah dibagi 10 diatas maka dikali 10 disini
        apparent_longitude_aksen = (longitude_matahari - (1.397*(T*10)) - (0.00031*((T*10)**2)))
        delta_longitude = -0.09033/3600
        delta_latitude = +0.03916*(math.cos(math.radians(apparent_longitude_aksen)) - math.sin(math.radians(apparent_longitude_aksen)))
        
        #whence
        longitude_baru = longitude_matahari + delta_longitude
        latitude_baru = latitude_matahari + delta_latitude
        #delta Apperent Longitude
        #delta_AL = 3548.193+118.568*math.sin(math.radians(87.5287+359993.7286*T))+2.476*math.sin(math.radians(85.0561+719987.4571*T))+1.376*math.sin(math.radians(27.8502+4452671.1152*T))+0.119*math.sin(math.radians(73.1375+450368.8564*T))+0.114*math.sin(math.radians(337.2264+329644.6718*T))+0.086*math.sin(math.radians(222.5400+659289.3436*T))+0.078*math.sin(math.radians(162.8136+9224659.7915*T))+0.054*math.sin(math.radians(82.5823+1079981.1857*T))+0.052*math.sin(math.radians(171.5189+225184.4282*T))+0.034*math.sin(math.radians(30.3214+4092677.3866*T))+0.033*math.sin(math.radians(119.8105+337181.4711*T))+0.023*math.sin(math.radians(247.5418+299295.6151*T))+0.023*math.sin(math.radians(325.1526+315559.5560*T))+0.021*math.sin(math.radians(155.1241+675553.2846*T))+7.311*T*math.sin(math.radians(333.4515+359993.7286*T))+0.305*T*math.sin(math.radians(330.9814+719987.4571*T))+0.010*T*math.sin(math.radians(328.5170+1079981.1857*T))+0.309*(T**2)*math.sin(math.radians(241.4518+359993.7286*T))+0.021*(T**2)*math.sin(math.radians(205.0482+719987.4571*T))+0.004*(T**2)*math.sin(math.radians(297.8610+4452671.1152*T))+0.010*(T**3)*math.sin(math.radians(154.7066+359993.7286*T))
        #koreksi besar
        #koreksi_aberration = -0.005775518 * R_earth * delta_AL

        #aberration
        aberration = (-20.4898/(3600*R_earth))

        #Apperent Longitude
        apparent_longitude = (longitude_baru + delta_nutasi + aberration)

        return latitude_baru, apparent_longitude

    def bulan (Tjd, delta_nutasi):
        L_aksen = ((218.3164477 + 481267.88123421*Tjd - 0.0015786 *(Tjd**2) + (Tjd**3)/538841 - (Tjd**4)/65194000)%360)
        D = ((297.8501921 + 445267.1114034*Tjd - 0.0018819*(Tjd**2) + (Tjd**3)/545868 - (Tjd**4)/113065000)%360)
        M = ((357.5291092 + 35999.0502909*Tjd - 0.0001536*(Tjd**2) + (Tjd**3)/24490000)%360)
        M_aksen = ((134.9633964 + 477198.8675055*Tjd + 0.0087414*(Tjd**2) + (Tjd**3)/69699 - (Tjd**4)/14712000)%360)
        F = ((93.2720950 + 483202.0175233*Tjd - 0.0036539*(Tjd**2) - (Tjd**3)/3526000 + (Tjd**4)/863310000)%360)
        A1 = ((119.75 + 131.849*Tjd)%360)
        A2 = ((53.09 + 479264.290*Tjd)%360)
        A3 = ((313.45 + 481266.484*Tjd)%360)
        E = (1 - 0.002516*Tjd - 0.0000074*(Tjd**2))

        longitude_bulan1 = 0
        for index, i in data_longitude_bulan.iterrows():
            Dp = i['D']
            Mp = i['M']
            M_aksenp = i["M'"]
            Fp = i['F']
            f2p = i['koefisien']
            hasil_longitude0 = f2p*(E**(abs(Mp)))* math.sin(((math.radians(D*Dp)) + (math.radians(M*Mp)) + (math.radians(M_aksen*M_aksenp)) + (math.radians(F*Fp))))
            longitude_bulan1 = longitude_bulan1 + hasil_longitude0
        longitude_bulan = ((longitude_bulan1 + 3958 * math.sin(math.radians(A1)) + 1962 * math.sin(math.radians(L_aksen - F)) + 318 * math.sin(math.radians(A2)))/1000000)
        
        latitude_bulan1 = 0
        for index, i in data_ekliptika_bulan.iterrows():
            Dp = i['D']
            Mp = i['M']
            M_aksenp = i["M'"]
            Fp = i['F']
            f2p = i['koefisien']
            hasil_latitude0 = f2p*(E**(abs(Mp)))* math.sin(((math.radians(D*Dp)) + (math.radians(M*Mp)) + (math.radians(M_aksen*M_aksenp)) + (math.radians(F*Fp))))
            latitude_bulan1 = latitude_bulan1 + hasil_latitude0
        latitude_bulan = ((latitude_bulan1 - 2235 * math.sin(math.radians(L_aksen)) + 382 * math.sin(math.radians(A3)) + 175 * math.sin(math.radians(A1 - F)) + 175 * math.sin(math.radians(A1 + F)) + 127 * math.sin(math.radians(L_aksen - M_aksen)) - 115 * math.sin(math.radians(L_aksen + M_aksen)))/1000000)
        
        distance_bulan1 = 0
        for index, i in data_distance_bulan.iterrows():
            Dp = i['D']
            Mp = i['M']
            M_aksenp = i["M'"]
            Fp = i['F']
            f2p = i['koefisien']
            hasil_distance0 = f2p*(E**(abs(Mp)))* math.cos(((math.radians(D*Dp)) + (math.radians(M*Mp)) + (math.radians(M_aksen*M_aksenp)) + (math.radians(F*Fp))))
            distance_bulan1 = distance_bulan1 + hasil_distance0
        distance_bulan = (distance_bulan1/1000)

        apparent_longitude = L_aksen + longitude_bulan
        distance_to_earth = 385000.56 + distance_bulan
        parallax = (math.degrees(math.asin(6378.14/368409.7)))
        apparent_longitude_bulan = (apparent_longitude + delta_nutasi)

        return E, latitude_bulan, apparent_longitude_bulan

    def equationoftime (T, right_ascension_high, delta_nutasi, obliquity):
        apparent_longitude = (280.4664567 + 360007.6982779*T + 0.03032028*(T**2) + (T**3)/49931 - (T**4)/15300 - (T**5)/20000000)%360
        equation_of_time = (apparent_longitude - 0.0057183 - right_ascension_high + delta_nutasi * math.cos(math.radians(obliquity)))/15
        return equation_of_time

    def fase_bulan(month, year, E_bulan, delta_T, TZ):
        #kabisat & basitoh
        #basitoh
        if (month == 1):
            year1 = 31/365
            year0 = year + year1
        elif (month == 2 and year % 4 != 0):
            year1 = 59/365
            year0 = year + year1
        elif (month == 3 and year % 4 != 0):
            year1 = 90/365
            year0 = year + year1
        elif (month == 4 and year % 4 != 0):
            year1 = 120/365
            year0 = year + year1
        elif (month == 5 and year % 4 != 0):
            year1 = 151/365
            year0 = year + year1
        elif (month == 6 and year % 4 != 0):
            year1 = 181/365
            year0 = year + year1
        elif (month == 7 and year % 4 != 0):
            year1 = 212/365
            year0 = year + year1
        elif (month == 8 and year % 4 != 0):
            year1 = 243/365
            year0 = year + year1
        elif (month == 9 and year % 4 != 0):
            year1 = 273/365
            year0 = year + year1
        elif (month == 10 and year % 4 != 0):
            year1 = 304/365
            year0 = year + year1
        elif (month == 11 and year % 4 != 0):
            year1 = 334/365
            year0 = year + year1
        elif (month == 12 and year % 4 != 0):
            year1 = 365/365
            year0 = year + year1
        #kabisat
        elif (month == 2 and year % 4 == 0):
            year1 = 60/366
            year0 = year + year1
        elif (month == 3 and year % 4 == 0):
            year1 = 91/366
            year0 = year + year1
        elif (month == 4 and year % 4 == 0):
            year1 = 121/366
            year0 = year + year1
        elif (month == 5 and year % 4 == 0):
            year1 = 152/366
            year0 = year + year1
        elif (month == 6 and year % 4 == 0):
            year1 = 182/366
            year0 = year + year1
        elif (month == 7 and year % 4 == 0):
            year1 = 213/366
            year0 = year + year1
        elif (month == 8 and year % 4 == 0):
            year1 = 244/366
            year0 = year + year1
        elif (month == 9 and year % 4 == 0):
            year1 = 274/366
            year0 = year + year1
        elif (month == 10 and year % 4 == 0):
            year1 = 305/366
            year0 = year + year1
        elif (month == 11 and year % 4 == 0):
            year1 = 335/366
            year0 = year + year1
        elif (month == 12 and year % 4 == 0):
            year1 = 366/366
            year0 = year + year1

        k_fase_bulan = math.floor(((year0 - 2000) * 12.3685))
        T_fase_bulan = (k_fase_bulan/1236.85)
        JDE_fase_bulan = (2451550.09766 + 29.530588861 * k_fase_bulan + 0.00015437*(T_fase_bulan**2) - 0.000000150*(T_fase_bulan**3) + 0.00000000073*(T_fase_bulan**4))
        M_fase_bulan = ((2.5534 + 29.10535670*k_fase_bulan - 0.0000014*(T_fase_bulan**2) - 0.00000011*(T_fase_bulan**3))%360)
        M_aksen_fase_bulan = ((201.5643 + 385.81693528*k_fase_bulan + 0.0107582*(T_fase_bulan**2) + 0.00001238*(T_fase_bulan**3) - 0.000000058*(T_fase_bulan**4))%360)
        F_fase_bulan = ((160.7108 + 390.67050284*k_fase_bulan - 0.0016118*(T_fase_bulan**2) - 0.00000227*(T_fase_bulan**3) + 0.000000011*(T_fase_bulan**4))%360)
        omega_fase_bulan = ((124.7746 - 1.56375588*k_fase_bulan + 0.0020672*(T_fase_bulan**2) + 0.00000215*(T_fase_bulan**3))%360)
        A1_fase_bulan = 299.77 +  0.107408*k_fase_bulan - 0.009173*(T_fase_bulan**2)
        A2_fase_bulan = 251.88 +  0.016321*k_fase_bulan
        A3_fase_bulan = 251.83 + 26.651886*k_fase_bulan
        A4_fase_bulan = 349.42 + 36.412478*k_fase_bulan
        A5_fase_bulan = 84.66 + 18.206239*k_fase_bulan
        A6_fase_bulan = 141.74 + 53.303771*k_fase_bulan
        A7_fase_bulan = 207.14 +  2.453732*k_fase_bulan
        A8_fase_bulan = 154.84 +  7.306860*k_fase_bulan
        A9_fase_bulan = 34.52 + 27.261239*k_fase_bulan
        A10_fase_bulan = 207.19 +  0.121824*k_fase_bulan
        A11_fase_bulan = 291.34 +  1.844379*k_fase_bulan
        A12_fase_bulan = 161.72 + 24.198154*k_fase_bulan
        A13_fase_bulan = 239.56 + 25.513099*k_fase_bulan
        A14_fase_bulan = 331.55 +  3.592518*k_fase_bulan

        new_moon =  (-0.40720*math.sin(math.radians(M_aksen_fase_bulan)) + 0.17241*E_bulan*math.sin(math.radians(M_fase_bulan)) +  0.01608*math.sin(math.radians(2*M_aksen_fase_bulan)) + 0.01039*math.sin(math.radians(2*F_fase_bulan)) + 0.00739*E_bulan*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan)) - 0.00514*E_bulan*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan)) + 0.00208*math.sin(math.radians((E_bulan**2)*(2*M_fase_bulan))) - 0.00111*math.sin(math.radians(M_aksen_fase_bulan-2*F_fase_bulan)) - 0.00057*math.sin(math.radians(M_aksen_fase_bulan+2*F_fase_bulan)) + 0.00056*E_bulan*math.sin(math.radians(2*M_aksen_fase_bulan+M_fase_bulan)) - 0.00042*math.sin(math.radians(3*M_aksen_fase_bulan)) + 0.00042*E_bulan*math.sin(math.radians(M_fase_bulan+2*F_fase_bulan)) + 0.00038*E_bulan*math.sin(math.radians(M_fase_bulan-2*F_fase_bulan)) - 0.00024*E_bulan*math.sin(math.radians(2*M_aksen_fase_bulan-M_fase_bulan)) - 0.00017*math.sin(math.radians(omega_fase_bulan)) - 0.00007*math.sin(math.radians(M_aksen_fase_bulan+2*M_fase_bulan)) + 0.00004*math.sin(math.radians(2*(M_aksen_fase_bulan-F_fase_bulan))) + 0.00004*math.sin(math.radians(3*M_fase_bulan)) + 0.00003*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan-2*F_fase_bulan)) +0.00003*math.sin(math.radians(2*(M_aksen_fase_bulan+F_fase_bulan))) - 0.00003*math.sin(math.radians(M_aksen_fase_bulan+M_fase_bulan+2*F_fase_bulan)) + 0.00003*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan+2*F_fase_bulan)) - 0.00002*math.sin(math.radians(M_aksen_fase_bulan-M_fase_bulan-2*F_fase_bulan)) - 0.00002*math.sin(math.radians(3*M_aksen_fase_bulan+M_fase_bulan)) + 0.00002*math.sin(math.radians(4*M_aksen_fase_bulan)))
        correction_all_phase = ((325*math.sin(math.radians(A1_fase_bulan))+165*math.sin(math.radians(A2_fase_bulan))+164*math.sin(math.radians(A3_fase_bulan))+126*math.sin(math.radians(A4_fase_bulan))+110*math.sin(math.radians(A5_fase_bulan))+62*math.sin(math.radians(A6_fase_bulan))+60*math.sin(math.radians(A7_fase_bulan))+ 56*math.sin(math.radians(A8_fase_bulan))+ 47*math.sin(math.radians(A9_fase_bulan))+ 42*math.sin(math.radians(A10_fase_bulan))+ 40*math.sin(math.radians(A11_fase_bulan))+ 37*math.sin(math.radians(A12_fase_bulan))+ 35*math.sin(math.radians(A13_fase_bulan))+ 23*math.sin(math.radians(A14_fase_bulan)))/1000000)

        #the true New Moon
        JDE_fase_bulan_new = (JDE_fase_bulan + new_moon + correction_all_phase)
        jd = JDE_fase_bulan_new + 0.5 - delta_T + (TZ/24)
        z = int(jd)
        f = jd - z
        alpha = int((z - 1867216.25)/36524.25)
        if (z<2299161):
            a = z
        else:
            a = z + 1 + alpha - int(alpha/4)
        b = a + 1524
        c = int((b-122.1)/365.25)
        d = int(365.25*c)
        e = int((b-d)/30.36001)
        day_fase_bulan = b - d - int(30.6001*e)+f
        tanggal_fase_bulan = int(day_fase_bulan)
        jam_fase_bulan = (day_fase_bulan - tanggal_fase_bulan)
        if e<14 :
            bulan_fase_bulan = e-1
        else:
            bulan_fase_bulan = e-13
        if (bulan_fase_bulan>2):
            tahun_fase_bulan = c-4716
        else:
            tahun_fase_bulan = c-4715
        return tanggal_fase_bulan, bulan_fase_bulan, tahun_fase_bulan
    
    def harga_tinggi(tinggi_tempat):
        DIP = 1.76 * math.sqrt(tinggi_tempat) / 60
        semi_diameter = 0.5 * (32/60)
        refraksi = 34.5/60
        h = (DIP + semi_diameter + refraksi)
        return h

    def perhitungan_waktu_magrib(lintang_tempat, deklinasi_hari_ini, h_waktu, e, TZ, bujur_tempat):
        lintang_tempat = math.radians(lintang_tempat)
        deklinasi_hari_ini = math.radians(deklinasi_hari_ini)
        h_waktu = math.radians(-h_waktu)
        t = math.degrees(math.acos(-math.tan(lintang_tempat)* math.tan(deklinasi_hari_ini)+ 1/math.cos(lintang_tempat)* 1/math.cos(deklinasi_hari_ini)* math.sin(h_waktu)))
        t = t/15
        kwd = ((TZ*15) - bujur_tempat)/15
        waktu_magrib = 12 - e + t + kwd
        return waktu_magrib, t



    ##################
    #julian day normal
    Julian_day1 = JD (detik, menit, hours, day, month, year, TZ)
    Julian_day = Julian_day1 + delta_T
    Tjd = (Julian_day-2451545)/36525
    Tjd2 = (Julian_day1-2451545)/36525
    Tjde = (Julian_day-2451545)/365250

    #semua fungsi dipanggil
    nutasi_obliquity_hilal = nutasi_obliquity(Tjd)
    siderial_time_hilal = sidereal(Tjde, Julian_day1, nutasi_obliquity_hilal[0], nutasi_obliquity_hilal[3], bujur_tempat)

    #tanggal
    perhitungan_bulan_hilal = bulan(Tjd, nutasi_obliquity_hilal[0])
    tanggal_hilal = fase_bulan(month, year, perhitungan_bulan_hilal[0], delta_T, TZ)


    #################
    #julian day jam 0
    Julian_day2 = JD (0, 0, 11, tanggal_hilal[0], tanggal_hilal[1], tanggal_hilal[2], 0)
    Julian_day_jam_0 = Julian_day2
    Tjd_jam_0 = (Julian_day_jam_0-2451545)/36525
    Tjde_jam_0 = (Julian_day_jam_0-2451545)/365250

    #####$$$####
    nutasi_obliquity_hilal_jam0 = nutasi_obliquity(Tjd_jam_0)
    siderial_time_hilal_jam0 = sidereal(Tjde_jam_0, Julian_day2, nutasi_obliquity_hilal_jam0[0], nutasi_obliquity_hilal_jam0[3], bujur_tempat)

    #waktu
    perhitungan_high_hilal = perhitungan_high (Tjde_jam_0, nutasi_obliquity_hilal_jam0[0])
    equatorial_high_hilal = transformasi(perhitungan_high_hilal[1], nutasi_obliquity_hilal_jam0[3], perhitungan_high_hilal[0], siderial_time_hilal_jam0[4], lintang_tempat)

    #kemenag waktu tenggelam
    equation_of_time = equationoftime (Tjde_jam_0, equatorial_high_hilal[0], nutasi_obliquity_hilal_jam0[0], nutasi_obliquity_hilal_jam0[3])
    h = harga_tinggi(tinggi_tempat)
    waktu_magrib, t = perhitungan_waktu_magrib(lintang_tempat, equatorial_high_hilal[1], h, equation_of_time, TZ, bujur_tempat)
    waktu_matahari_tenggelam = jam(waktu_magrib)
    #jean meeus waktu tenggelam
    # waktu_matahari_tenggelam1 = terbit_transit_tenggelam (lintang_tempat, bujur_tempat, equatorial_high_hilal[0], equatorial_high_hilal[1], siderial_time_hilal_jam0[1], TZ)
    # waktu_matahari_tenggelam = jam(waktu_matahari_tenggelam1)


    ##########################################
    #julian day jam tenggelam tanggal new moon
    Julian_day3 = JD (waktu_matahari_tenggelam[2], waktu_matahari_tenggelam[1], waktu_matahari_tenggelam[0], tanggal_hilal[0], tanggal_hilal[1], tanggal_hilal[2], TZ)
    Julian_day_jam = Julian_day3 + delta_T
    Tjd_jam = (Julian_day_jam - 2451545)/36525
    Tjde_jam = (Julian_day_jam - 2451545)/365250

    #perhitungan posisi pada saat tanggal new moon tenggelam
    nutasi_obliquity_hilal_jam = nutasi_obliquity(Tjd_jam)
    siderial_time_hilal_jam = sidereal(Tjde_jam, Julian_day3, nutasi_obliquity_hilal_jam[0], nutasi_obliquity_hilal_jam[3], bujur_tempat)

    #####$$$#####
    perhitungan_high_hilal2 = perhitungan_high (Tjde_jam, nutasi_obliquity_hilal_jam[0])
    equatorial_high_hilal2 = transformasi(perhitungan_high_hilal2[1], nutasi_obliquity_hilal_jam[3], perhitungan_high_hilal2[0], siderial_time_hilal_jam[4], lintang_tempat)
    perhitungan_bulan_hilal = bulan (Tjd_jam, nutasi_obliquity_hilal_jam[0])
    equatorial_bulan_hilal = transformasi(perhitungan_bulan_hilal[2], nutasi_obliquity_hilal_jam[3], perhitungan_bulan_hilal[1], siderial_time_hilal_jam[4], lintang_tempat)

    # matahari
    latitude_ekliptika_matahari_pada_saat_magrib = perhitungan_high_hilal2[0]
    longitude_ekliptika_matahari_pada_saat_magrib = jam(perhitungan_high_hilal2[1])
    asensiorekta_matahari_pada_saat_magrib = jam(equatorial_high_hilal2[0])
    deklinasi_matahari_pada_saat_magrib = jam(equatorial_high_hilal2[1])
    azimuth_matahari_pada_saat_magrib = jam(equatorial_high_hilal2[2])
    altitude_matahari_pada_saat_magrib = jam(equatorial_high_hilal2[3])

    # bulan
    latitude_ekliptika_bulan_pada_saat_magrib = perhitungan_bulan_hilal[1]
    longitude_ekliptika_bulan_pada_saat_magrib = jam(perhitungan_bulan_hilal[2])
    asensiorekta_bulan_pada_saat_magrib = jam(equatorial_bulan_hilal[0])
    deklinasi_bulan_pada_saat_magrib = jam(equatorial_bulan_hilal[1])
    azimuth_bulan_pada_saat_magrib = jam(equatorial_bulan_hilal[2])
    altitude_bulan_pada_saat_magrib = jam(equatorial_bulan_hilal[3])

    # Elongasi Bulan Matahari
    azimuth_matahari_bulan = abs(equatorial_bulan_hilal[2] - equatorial_high_hilal2[2])
    altitude_matahari_bulan = abs(equatorial_bulan_hilal[3] - equatorial_high_hilal2[3])
    elongasi1 = math.sqrt(azimuth_matahari_bulan**2 + altitude_matahari_bulan**2)
    elongasi = jam(elongasi1)

    return tanggal_hilal, waktu_matahari_tenggelam, altitude_matahari_pada_saat_magrib, azimuth_matahari_pada_saat_magrib, asensiorekta_matahari_pada_saat_magrib, deklinasi_matahari_pada_saat_magrib, longitude_ekliptika_matahari_pada_saat_magrib, latitude_ekliptika_matahari_pada_saat_magrib, altitude_bulan_pada_saat_magrib, azimuth_bulan_pada_saat_magrib, asensiorekta_bulan_pada_saat_magrib, deklinasi_bulan_pada_saat_magrib, longitude_ekliptika_bulan_pada_saat_magrib, latitude_ekliptika_bulan_pada_saat_magrib, elongasi


#-----------------------------------------------------------------------------------------------------------#

def waktu_salat_fardhu_dan_lain (day, Bulan, Tahun, lintang1, bujur, KWD):
    
    def perhitungan_equation (Tahun, Bulan, B, Dzuhur):
        JD = 1720994.5 + math.floor(365.25*Tahun)+ math.floor(30.6001*(Bulan+1))+ (B) + (Dzuhur)
        T = (JD - 2451545)/36525
        L00 = 280.46607 + (36000.7698*T)
        L01 = math.floor((280.46607 + (36000.7698*T))/360)
        L02 = L01 * 360
        L0 =  L00 - L02
        L0R = math.radians (L0)
        EoT = (-(1789 + 237 * T)* math.sin (L0R) - (7146 - 62*T)* math.cos (L0R) + (9934 - 14*T)* math.sin(2*L0R)- (29 + 5*T)* math.cos(2*L0R) + (74 + 10*T)* math.sin(3*L0R) + (320 - 4*T)* math.cos(3*L0R) - 212* math.sin(4*L0R))/1000
        Jam = 0
        Menit = math.floor(EoT)
        detik0 = EoT - math.floor(EoT)
        detik = math.floor((detik0)*60)
        eot = Jam + (Menit/60) + (detik/3600)
        U = T/100
        L0 = 280.46646 + (36000.76983*T)+ (0.0003032*(T**2))
        while L0 < 0:
            L0 += 360
        while L0 > 360:
            L0 -= 360
        M = 357.52911 + (35999.05029*T)+ (0.0001537*(T**2))
        while M < 0:
            M += 360
        while M > 360:
            M -= 360
        Mrad = math.radians(M)
        eksentrisitas = 0.016708634 - (0.000042037*T) - (0.0000001267*(T**2))
        C = (1.914602-(0.004817*T)- 0.000014*(T**2))* math.sin(Mrad) + (0.019993-(0.000101*T))* math.sin(2*Mrad) + 0.000289 * math.sin(3*Mrad)
        longitude = L0 + C
        longituderad = math.radians(longitude)
        v = M + C
        vrad = math.radians(v)
        R = 1.000001018*(1-(eksentrisitas**2)) / (1 + eksentrisitas *math.cos(vrad))
        omega = 125.04452 - 1934.136261*T + 0.0020708*(T**2) + ((T**3)/450000)
        omegarad = math.radians(omega)
        lamda = longitude - 0.00569 - 0.00478 * math.sin(omegarad)
        L = 280.4665 + 36000.7698*T
        Lrad = math.radians(L)
        L1 = 218.3165 + 481267.8813*T
        L1rad = math.radians(L1)
        #sampek sini delta_obliquity memakai rumus low accuracy 
        delta_obliquity1 = ((9.20/3600) * math.cos(omegarad)) + (0.57/3600)* math.cos(2*Lrad) + (0.10/3600)*math.cos(2*L1rad) - (0.09/3600)*math.cos(2*omegarad)
        epsilon0 = (23*3600) + (26*60) + 21.448 - 4680.93*U - 1.55*(U**2) + 1999.25*(U**3) - 51.38*(U**4) - 249.67*(U**5) - 39.05*(U**6) + 7.12*(U**7) + 27.87*(U**8) + 5.79*(U**9) + 2.45*(U**10)
        obliquity = epsilon0/3600
        obliquity_benar = obliquity + delta_obliquity1
        obliquity_benarrad = math.radians(obliquity_benar)
        alpha = math.degrees(math.atan2((math.cos(obliquity_benarrad)* math.sin(longituderad)), math.cos(longituderad)))
        while alpha < 0:
            alpha += 360
        while alpha > 360:
            alpha -= 360
        deklinasi = math.degrees(math.asin(math.sin(obliquity_benarrad)* math.sin(longituderad)))
        return deklinasi, eot
    
    def perhitungan_degree(rlintang, rdeklinasi, rtinggi):
        t = math.degrees(math.acos(-math.tan(rlintang)* math.tan(rdeklinasi)+ 1/math.cos(rlintang)* 1/math.cos(rdeklinasi)* math.sin (rtinggi)))
        return t

    if Bulan <=2 :
        Bulan = Bulan + 12
        Tahun = Tahun - 1
        A = math.floor (Tahun/100)
    else :
        A = math.floor (Tahun/100)
    if Tahun <=1582:
        B = 0
    elif Tahun >1582:
        B = 2 + math.floor (A/4) - A

    lintang = math.radians(lintang1)
    Dsubuh = (day-1) + (((21 * 3600)+(0 * 60)+ 0)/86400)
    Dzuhur = day + (((5 * 3600)+(0 * 60)+ 0)/86400)
    Dasar = day + (((8 * 3600)+(0 * 60)+ 0)/86400)
    Dmagrib = day + (((11 * 3600)+(0 * 60)+ 0)/86400)
    Disya = day + (((12 * 3600)+(0 * 60)+ 0)/86400)

    deklinasi_zuhur, eot = perhitungan_equation(Tahun, Bulan, B, Dzuhur)
    EoT_zuhur = eot
    rdeklinasi_zuhur = math.radians(deklinasi_zuhur)
    deklinasi_subuh, eot = perhitungan_equation(Tahun, Bulan, B, Dsubuh)
    EoT_subuh = eot
    rdeklinasi_subuh = math.radians(deklinasi_subuh)
    deklinasi_asar, eot = perhitungan_equation(Tahun, Bulan, B, Dasar)
    EoT_asar = eot
    rdeklinasi_asar = math.radians(deklinasi_asar)
    deklinasi_magrib, eot = perhitungan_equation(Tahun, Bulan, B, Dmagrib)
    EoT_magrib = eot
    rdeklinasi_magrib = math.radians(deklinasi_magrib)
    deklinasi_isya, eot = perhitungan_equation(Tahun, Bulan, B, Disya)
    EoT_isya = eot
    rdeklinasi_isya = math.radians(deklinasi_isya)

    i = 2/60

    # subuh
    tinggi_subuh= -20
    rtinggi_subuh= math.radians(tinggi_subuh)

    # asar
    
    deklinasi_2 = deklinasi_asar
    tinggi_asar0= math.radians(abs(lintang1 - deklinasi_2))
    tinggi_asar= math.degrees(math.atan(1/((math.tan(tinggi_asar0))+1)))
    rtinggi_asar= math.radians(tinggi_asar)

    # magrib
    rtinggi_magrib= math.radians(-1)
    
    # isya
    rtinggi_isya= math.radians(-18)

    # perhitungan
    # perhitungan waktu subuh
    t_subuh = perhitungan_degree(lintang, rdeklinasi_subuh, rtinggi_subuh)
    t_selesai_subuh = (t_subuh)/15
    subuh = 12-(EoT_subuh)-(t_selesai_subuh)+(KWD)+(i)
    # perhitungan waktu zuhur
    zuhur = 12-(EoT_zuhur)+(KWD)+(i)
    # perhitungan waktu asar
    t_asar = perhitungan_degree(lintang, rdeklinasi_asar, rtinggi_asar)
    t_selesai_asar = (t_asar)/15
    asar = 12-(EoT_asar)+(t_selesai_asar)+(KWD)+(i)
    # perhitungan waktu magrib
    t_magrib = perhitungan_degree(lintang, rdeklinasi_magrib, rtinggi_magrib)
    t_selesai_magrib = (t_magrib)/15
    magrib = 12-(EoT_magrib)+(t_selesai_magrib)+(KWD)+(i)
    # perhitungan waktu isya
    t_isya=  perhitungan_degree(lintang, rdeklinasi_isya, rtinggi_isya)
    t_selesai_isya = (t_isya)/15
    isya = 12-(EoT_isya)+(t_selesai_isya)+(KWD)+(i)

    return subuh, zuhur, asar, magrib, isya

#-----------------------------------------------------------------------------------------------------------#


def convert_date(date_conversion):
    if isinstance(date_conversion, datetime):
        hari_mapping = {
            "Monday": "Senin",
            "Tuesday": "Selasa",
            "Wednesday": "Rabu",
            "Thursday": "Kamis",
            "Friday": "Jumat",
            "Saturday": "Sabtu",
            "Sunday": "Minggu"
        }
        
        bulan_mapping = {
            "January": "Januari",
            "February": "Februari",
            "March": "Maret",
            "April": "April",
            "May": "Mei",
            "June": "Juni",
            "July": "Juli",
            "August": "Agustus",
            "September": "September",
            "October": "Oktober",
            "November": "November",
            "December": "Desember"
        }
        
        date_converted = f"{date_conversion:%A, %d %B %Y}"
        
        for eng, indo in hari_mapping.items():
            if eng in date_converted:
                date_converted = date_converted.replace(eng, indo)
                
        for eng, indo in bulan_mapping.items():
            if eng in date_converted:
                date_converted = date_converted.replace(eng, indo)
                
        return date_converted


#-----------------------------------------------------------------------------------------------------------#