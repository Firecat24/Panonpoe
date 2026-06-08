<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link rel="stylesheet" href="css/plugins/bootstrap.min.css">
        <link rel="stylesheet" href="css/plugins/magnific-popup.css">
        <link rel="stylesheet" href="css/plugins/font-awesome.min.css">
        <link rel="stylesheet" href="css/plugins/animate.css">
        <link href="https://fonts.googleapis.com/css?family=Rubik:300,400,500,700,900" rel="stylesheet">
        <link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
        <link rel="stylesheet" href="css/main.css">
        
        <link rel="stylesheet" href="css/archive-style.css">
        
        <link rel="icon" type="image/x-icon" href="img/eksternal/logo_4.ico">
        <title>Panonpoe LIVE CAMERA</title>
    </head>
    <body>
        <div class="se-pre-con"></div>
        <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
            <div class="container">
                <a class="navbar-brand" href="https://www.panonpoe.id/"><img src="img/eksternal/logo_3.png" alt="logo"></a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
                    <span class="custom-toggler">
                        <span></span><span></span><span></span>
                    </span>
                </button>
            
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ml-auto">
                        <li class="nav-item"><a class="nav-link" href="https://www.panonpoe.id/">Home</a></li>
                        <li class="nav-item"><a class="nav-link" href="https://produk.panonpoe.id/">Produk</a></li>
                        <li class="nav-item"><a class="nav-link" href="https://publisher.panonpoe.id/">Publisher</a></li>
                        <li class="nav-item"><a class="nav-link" href="https://labfalak.panonpoe.id/home/">Labfalak</a></li>
                        <li class="nav-item"><a class="nav-link" href="https://jurnal.panonpoe.id/jurnal/index.php/matahari">Jurnal</a></li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="slider" id="home">
            <div id="particles-js"></div>
            <div class="live-hero-content">
                <span class="live-label">● LIVE OBSERVATORY</span>
                <h1>Panonpoe Live Camera</h1>
                <p>Pantau kondisi langit dan observasi secara realtime dari Bandung, Indonesia.</p>
                <div class="live-camera-box">
                    <img id="allsky-cam" src="image.jpg" alt="Live Camera">
                    <div class="camera-status-bar">
                        <div class="status-item"><span class="dot-live"></span>LIVE</div>
                        <div class="status-item">Bandung, Indonesia</div>
                        <div class="status-item">Updated realtime</div>
                    </div>
                </div>
            </div>
        </div>

        <section class="observation-archive">
            <div class="container">
                <div class="archive-heading text-center">
                    <span>OBSERVATION ARCHIVE</span>
                    <h2>Explore The Sky Archive</h2>
                    <p>Jelajahi hasil observasi langit dari kamera Panonpoe, mulai dari timelapse harian, startrail, hingga keogram realtime.</p>
                </div>

                <div class="archive-tabs">
                    <button class="archive-btn active" data-target="timelapse-content">Timelapse</button>
                    <button class="archive-btn" data-target="startrail-content">Startrail</button>
                    <button class="archive-btn" data-target="keogram-content">Keogram</button>
                </div>

                <div class="archive-content-wrap">
                    
                    <div class="archive-content active" id="timelapse-content">
                        <div class="archive-folder-grid">
                            <?php
                            $dirTimelapse = "videos/";
                            if (is_dir($dirTimelapse)) {
                                $files = glob($dirTimelapse . "*.{mp4,mkv,mov,avi,webm,jpg,jpeg,png,gif,webp}", GLOB_BRACE);
                                
                                if ($files !== false) {
                                    arsort($files);
                                    $totalFiles = count($files);

                                    // Pengaturan Pagination Timelapse (4 ke kanan, 2 ke bawah = 8 item)
                                    $limit = 8; 
                                    $page = isset($_GET['p_timelapse']) ? (int)$_GET['p_timelapse'] : 1;
                                    $page = ($page < 1) ? 1 : $page;
                                    $start = ($page - 1) * $limit;
                                    $totalPages = ceil($totalFiles / $limit);

                                    $pagedFiles = array_slice($files, $start, $limit);

                                    if ($totalFiles > 0) {
                                        foreach ($pagedFiles as $file) {
                                            $filename = basename($file);
                                            $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
                                            $fileNoExt = pathinfo($filename, PATHINFO_FILENAME);
                                            $cleanTitle = str_replace(['_', '-'], ' ', $fileNoExt);
                                            
                                            $fileType = in_array($ext, ['jpg','jpeg','png','gif','webp']) ? 'image' : 'video';
                                            
                                            if ($fileType === 'image') {
                                                $thumbnail = $file;
                                                $icon = "🔍";
                                            } else {
                                                $possibleCover = $dirTimelapse . $fileNoExt . ".jpg";
                                                $thumbnail = file_exists($possibleCover) ? $possibleCover : "img/livecam/thumb-timelapse.jpg";
                                                $icon = "▶";
                                            }

                                            echo '
                                            <div class="video-item-card" data-file-src="' . $file . '" data-file-type="' . $fileType . '">
                                                <div class="video-thumbnail-wrapper">
                                                    <img src="' . $thumbnail . '" alt="' . $cleanTitle . '">
                                                    <div class="play-overlay-icon"><i class="play-icon">' . $icon . '</i></div>
                                                </div>
                                                <span class="video-title">' . ucwords($cleanTitle) . '</span>
                                            </div>';
                                        }
                                    } else { 
                                        echo '<p class="text-muted text-center w-100">Belum ada dokumen arsip timelapse.</p>'; 
                                    }
                                }
                            } else { echo '<p class="text-muted text-center w-100">Folder videos/ tidak ditemukan.</p>'; }
                            ?>
                        </div>

                        <?php if (isset($totalPages) && $totalPages > 1): ?>
                            <div class="pagination-nav text-center mt-4">
                                <?php for ($i = 1; $i <= $totalPages; $i++): ?>
                                    <a href="?p_timelapse=<?php echo $i; ?>" class="btn-page <?php echo ($page == $i) ? 'active' : ''; ?>">
                                        <?php echo $i; ?>
                                    </a>
                                <?php endfor; ?>
                            </div>
                        <?php endif; ?>
                    </div>        

                    <div class="archive-content" id="startrail-content">
                        <div class="archive-folder-grid">
                            <?php
                            $dirStartrail = "startrail/";
                            if (is_dir($dirStartrail)) {
                                $files = glob($dirStartrail . "*.{mp4,mkv,mov,avi,webm,jpg,jpeg,png,gif,webp}", GLOB_BRACE);
                                
                                if ($files !== false) {
                                    arsort($files); // Urutkan file terbaru di atas
                                    $totalFiles = count($files);

                                    // ==========================================
                                    // CONFIGURATION PAGINATION (PENGATURAN HALAMAN)
                                    // ==========================================
                                    $limit = 8; // Mengatur 4 ke kanan, 2 ke bawah (Maksimal 8 item per halaman)
                                    $page = isset($_GET['p_startrail']) ? (int)$_GET['p_startrail'] : 1;
                                    $page = ($page < 1) ? 1 : $page;
                                    $start = ($page - 1) * $limit;
                                    $totalPages = ceil($totalFiles / $limit);

                                    // Memotong array file sesuai halaman aktif
                                    $pagedFiles = array_slice($files, $start, $limit);

                                    if ($totalFiles > 0) {
                                        foreach ($pagedFiles as $file) {
                                            $filename = basename($file);
                                            $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
                                            $fileNoExt = pathinfo($filename, PATHINFO_FILENAME);
                                            $cleanTitle = str_replace(['_', '-'], ' ', $fileNoExt);
                                            
                                            $fileType = in_array($ext, ['jpg','jpeg','png','gif','webp']) ? 'image' : 'video';
                                            
                                            if ($fileType === 'image') {
                                                $thumbnail = $file;
                                                $icon = "🔍";
                                            } else {
                                                $possibleCover = $dirStartrail . $fileNoExt . ".jpg";
                                                $thumbnail = file_exists($possibleCover) ? $possibleCover : "img/livecam/startrail.jpg";
                                                $icon = "▶";
                                            }

                                            echo '
                                            <div class="video-item-card" data-file-src="' . $file . '" data-file-type="' . $fileType . '">
                                                <div class="video-thumbnail-wrapper">
                                                    <img src="' . $thumbnail . '" alt="' . $cleanTitle . '">
                                                    <div class="play-overlay-icon"><i class="play-icon">' . $icon . '</i></div>
                                                </div>
                                                <span class="video-title">' . ucwords($cleanTitle) . '</span>
                                            </div>';
                                        }
                                    } else { 
                                        echo '<p class="text-muted text-center w-100">Belum ada dokumen arsip.</p>'; 
                                    }
                                }
                            }
                            ?>
                        </div>

                        <?php if (isset($totalPages) && $totalPages > 1): ?>
                            <div class="pagination-nav text-center mt-4">
                                <?php for ($i = 1; $i <= $totalPages; $i++): ?>
                                    <a href="?p_startrail=<?php echo $i; ?>" class="btn-page <?php echo ($page == $i) ? 'active' : ''; ?>">
                                        <?php echo $i; ?>
                                    </a>
                                <?php endfor; ?>
                            </div>
                        <?php endif; ?>
                    </div>

                    <div class="archive-content" id="keogram-content">
                        <div class="archive-folder-grid">
                            <?php
                            $dirKeogram = "keogram/";
                            if (is_dir($dirKeogram)) {
                                $files = glob($dirKeogram . "*.{mp4,mkv,mov,avi,webm,jpg,jpeg,png,gif,webp}", GLOB_BRACE);
                                
                                if ($files !== false) {
                                    arsort($files);
                                    $totalFiles = count($files);

                                    // Pengaturan Pagination Keogram (4 ke kanan, 2 ke bawah = 8 item)
                                    $limit = 8; 
                                    $page = isset($_GET['p_keogram']) ? (int)$_GET['p_keogram'] : 1;
                                    $page = ($page < 1) ? 1 : $page;
                                    $start = ($page - 1) * $limit;
                                    $totalPages = ceil($totalFiles / $limit);

                                    $pagedFiles = array_slice($files, $start, $limit);

                                    if ($totalFiles > 0) {
                                        foreach ($pagedFiles as $file) {
                                            $filename = basename($file);
                                            $ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
                                            $fileNoExt = pathinfo($filename, PATHINFO_FILENAME);
                                            $cleanTitle = str_replace(['_', '-'], ' ', $fileNoExt);
                                            
                                            $fileType = in_array($ext, ['jpg','jpeg','png','gif','webp']) ? 'image' : 'video';
                                            
                                            if ($fileType === 'image') {
                                                $thumbnail = $file;
                                                $icon = "🔍";
                                            } else {
                                                $possibleCover = $dirKeogram . $fileNoExt . ".jpg";
                                                $thumbnail = file_exists($possibleCover) ? $possibleCover : "img/livecam/keogram.jpg";
                                                $icon = "▶";
                                            }

                                            echo '
                                            <div class="video-item-card" data-file-src="' . $file . '" data-file-type="' . $fileType . '">
                                                <div class="video-thumbnail-wrapper">
                                                    <img src="' . $thumbnail . '" alt="' . $cleanTitle . '">
                                                    <div class="play-overlay-icon"><i class="play-icon">' . $icon . '</i></div>
                                                </div>
                                                <span class="video-title">' . ucwords($cleanTitle) . '</span>
                                            </div>';
                                        }
                                    } else { 
                                        echo '<p class="text-muted text-center w-100">Belum ada dokumen arsip keogram.</p>'; 
                                    }
                                }
                            } else { echo '<p class="text-muted text-center w-100">Folder keogram/ tidak ditemukan.</p>'; }
                            ?>
                        </div>

                        <?php if (isset($totalPages) && $totalPages > 1): ?>
                            <div class="pagination-nav text-center mt-4">
                                <?php for ($i = 1; $i <= $totalPages; $i++): ?>
                                    <a href="?p_keogram=<?php echo $i; ?>" class="btn-page <?php echo ($page == $i) ? 'active' : ''; ?>">
                                        <?php echo $i; ?>
                                    </a>
                                <?php endfor; ?>
                            </div>
                        <?php endif; ?>
                    </div>

                </div>
            </div>
        </section>

        <section class="live-contact">
            <div class="container text-center">
                <h2>Ingin bekerja sama dengan Panonpoe?</h2>
                <p>Hubungi kami untuk kolaborasi observasi, data falak, dan pengembangan astronomi digital.</p>
                <div class="col-md-6 offset-md-3">
                    <a href="mailto:info@panonpoe.id?subject=Kolaborasi%20Falak%20%26%20Astronomi" class="btn-blue-live">Hubungi Kami</a>
                </div>
            </div>
        </section>

        <a href="https://wa.me/6282333693379" class="whatsapp-float" target="_blank">
            <i class="fa fa-whatsapp my-float"></i>
        </a>

        <div id="videoPopupModal" class="video-popup-overlay">
            <div class="video-popup-container">
                <button class="video-popup-close">&times;</button>
                <div class="video-popup-body">
                    <video id="popupVideoPlayer" controls style="display:none; width:100%;">
                        <source src="" type="video/mp4">
                    </video>
                    <img id="popupImageViewer" src="" alt="Preview" style="display:none; width:100%; height:auto; object-fit:contain;">
                </div>
            </div>
        </div>

        <footer class="footer">
            <div class="container text-center text-white">
                <img src="img/eksternal/logo_1.png" alt="">
                <h2>Hak Cipta © 2026 PT. Panonpoe Digital Creative. Seluruh Hak Dilindungi.</h2>
            </div>
        </footer>

        <script src="js/plugins/jquery-3.3.1.min.js"></script>
        <script src="js/plugins/popper.min.js"></script>
        <script src="js/plugins/bootstrap.min.js"></script>
        <script src="js/plugins/jquery.smoothscroll.min.js"></script>
        <script src="js/plugins/particles.min.js"></script>
        <script src="js/plugins/app.js"></script>
        <script src="js/plugins/wow.min.js"></script>
        <script src="js/plugins/jquery.magnific-popup.min.js"></script>
        <script src="js/plugins/isotope.pkgd.min.js"></script>
        <script src="js/plugins/imagesloaded.pkgd.min.js"></script>
        <script src="js/plugins/jquery.waypoints.min.js"></script>
        <script src="js/plugins/jquery.counterup.min.js"></script>
        <script src="js/main.js"></script>

        <script>
            document.addEventListener("DOMContentLoaded", function () {
                // Logika Perpindahan Tab Menu
                const tabButtons = document.querySelectorAll(".archive-btn");
                const tabContents = document.querySelectorAll(".archive-content");

                tabButtons.forEach(button => {
                    button.addEventListener("click", () => {
                        const targetId = button.getAttribute("data-target");
                        tabButtons.forEach(btn => btn.classList.remove("active"));
                        tabContents.forEach(content => content.classList.remove("active"));
                        button.classList.add("active");
                        document.getElementById(targetId).classList.add("active");
                    });
                });

                // Logika Pop-up Pemutar Video
                const modal = document.getElementById("videoPopupModal");
                const modalVideo = document.getElementById("popupVideoPlayer");
                const closeBtn = document.querySelector(".video-popup-close");
                const videoCards = document.querySelectorAll(".video-item-card");

                videoCards.forEach(card => {
                    card.addEventListener("click", () => {
                        const videoSrc = card.getAttribute("data-video-src");
                        if (videoSrc) {
                            modalVideo.src = videoSrc;
                            modalVideo.load();
                            modal.classList.add("show");
                            modalVideo.play();
                        }
                    });
                });

                function closeModal() {
                    modal.classList.remove("show");
                    modalVideo.pause();
                    modalVideo.src = "";
                }

                closeBtn.addEventListener("click", closeModal);
                modal.addEventListener("click", (e) => {
                    if (e.target === modal) closeModal();
                });
            });
        </script>
    </body>
</html>