async function sendGeolocation() {
    if (navigator.geolocation) {
        
        if (sessionStorage.getItem("geolocationFetched") === "true") {
            console.log("Geolocation already fetched");
            return;
        }

        navigator.geolocation.getCurrentPosition(async (position) => {
            const timezoneOffset = new Date().getTimezoneOffset() / -60;
            const data = {
                lintang: position.coords.latitude,
                bujur: position.coords.longitude,
                timezone: timezoneOffset
            };
            try {
                const response = await fetch("/home", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    const result = await response.json();
                    document.getElementById("city").innerText = result.city;
                    document.getElementById("country").innerText = result.country;
                    document.getElementById("prov").innerText = result.prov;
                    document.getElementById("tanggal").innerText = result.tanggal;
                    document.getElementById("subuh").innerText = result.subuh;
                    document.getElementById("imsak").innerText = result.imsak;
                    document.getElementById("zuhur").innerText = result.zuhur;
                    document.getElementById("asar").innerText = result.asar;
                    document.getElementById("magrib").innerText = result.magrib;
                    document.getElementById("isya").innerText = result.isya;
                    document.getElementById("waktu_quartal1").innerText = result.waktu_quartal1;
                    document.getElementById("waktu_bulan_purnama").innerText = result.waktu_bulan_purnama;
                    document.getElementById("waktu_bulan_baru").innerText = result.waktu_bulan_baru;
                    document.getElementById("waktu_quartal3").innerText = result.waktu_quartal1;
                    document.getElementById("tanggal_quartal1").innerText = result.tanggal_quartal3;
                    document.getElementById("tanggal_bulan_purnama").innerText = result.tanggal_bulan_purnama;
                    document.getElementById("tanggal_bulan_baru").innerText = result.tanggal_bulan_baru;
                    document.getElementById("tanggal_quartal3").innerText = result.tanggal_quartal3;

                    sessionStorage.setItem("geolocationFetched", "true");
                } else {
                    console.error("Failed to fetch geolocation data.");
                }
            } catch (error) {
                console.error("Error:", error);
            }
        }, (error) => {
            console.error("Geolocation error:", error);
        });
    }
}

document.addEventListener("visibilitychange", function() {
    if (!document.hidden) {
        sendGeolocation();
    }
});

window.onload = sendGeolocation;
