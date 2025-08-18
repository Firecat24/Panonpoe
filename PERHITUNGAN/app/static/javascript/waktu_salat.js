function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var timezoneOffset = new Date().getTimezoneOffset() / -60;

    fetch('/jadwal_salat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({latitude: latitude, longitude: longitude, timezone: timezoneOffset})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Location data sent:', data);
        updateHTML(data);
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
    });
}

function updateHTML(data) {
    var section = document.querySelector('section');
    var div = document.querySelector('div');
    section.innerHTML = '';
    div.innerHTML = '';

    
    if (data.result && data.result.length > 0) {

        var div1 = document.createElement('div');
        div1.classList.add('container');

        var h2 = document.createElement('h2');
        var teks = 'Jadwal Waktu Salat Bulan '
        tanggal = data.result[0][0];
        var parts = tanggal.split(' ');
        var bulans = parts[2];
        var tahuns = parts[3];
        h2.textContent = teks + bulans + " " + tahuns;
        div1.appendChild(h2);
    
        var tabel = document.createElement('table');
        var thead = document.createElement('thead');
        var teer = document.createElement('tr');

        var hari = document.createElement('th');
        hari.textContent = 'Hari/Tanggal';
        var imsak = document.createElement('th');
        imsak.textContent = 'Imsak';
        var subuh = document.createElement('th');
        subuh.textContent = 'Subuh';
        var duhur = document.createElement('th');
        duhur.textContent = 'Dzuhur';
        var asar = document.createElement('th');
        asar.textContent = 'Asar';
        var magrib = document.createElement('th');
        magrib.textContent = 'Magrib';
        var isya = document.createElement('th');
        isya.textContent = 'Isya';

        teer.appendChild(hari);
        teer.appendChild(imsak);
        teer.appendChild(subuh);
        teer.appendChild(duhur);
        teer.appendChild(asar);
        teer.appendChild(magrib);
        teer.appendChild(isya);

        thead.appendChild(teer);
        tabel.appendChild(thead);
    
        var tbody = document.createElement('tbody');
        
        data.result.forEach(content => {
            var tr = document.createElement('tr');
            var tdtanggal = document.createElement('td');
            tdtanggal.textContent = content[0];
            tr.appendChild(tdtanggal);
            var jam = [content[6], content[1], content[2], content[3], content[4], content[5]];

            for (var i = 0; i < jam.length; i++) {
                var pJam = document.createElement('td');
                pJam.textContent = jam[i];
                tr.appendChild(pJam);
            }
            tbody.appendChild(tr);
        });
        
        tabel.appendChild(tbody);
        div1.appendChild(tabel);
        section.appendChild(div1);

        var div_a = document.createElement('div');

        div_a.classList.add('button-container');

        var kembaliDapatkanData = document.createElement('a');
        kembaliDapatkanData.href = '/jadwal_salat';
        kembaliDapatkanData.classList.add('button_daftar');
        kembaliDapatkanData.textContent = 'Kembali dapatkan data';

        var kembaliKeDashboard = document.createElement('a');
        kembaliKeDashboard.href = '/home';
        kembaliKeDashboard.classList.add('button_daftar');
        kembaliKeDashboard.textContent = 'Kembali ke Dashboard';

        div_a.appendChild(kembaliDapatkanData);
        div_a.appendChild(kembaliKeDashboard);
        div.appendChild(div_a);
        section.appendChild(div);

        var copyrightElement = document.querySelector('.copyright');
        copyrightElement.classList.replace('copyright', 'cupyright');

    } else {
        var h1 = document.createElement('h1');
        h1.textContent = 'No data available';
        section.appendChild(h1);

        var kembaliDapatkanData = document.createElement('a');
        kembaliDapatkanData.href = '/jadwal_salat';
        kembaliDapatkanData.classList.add('button_daftar');
        kembaliDapatkanData.textContent = 'Kembali dapatkan data';

        var kembaliKeDashboard = document.createElement('a');
        kembaliKeDashboard.href = '/home';
        kembaliKeDashboard.classList.add('button_daftar');
        kembaliKeDashboard.textContent = 'Kembali ke Dashboard';

        section.appendChild(kembaliDapatkanData);
        section.appendChild(kembaliKeDashboard);
    }
}