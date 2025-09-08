from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, g
import os
import time

bp_submit = Blueprint("main_submit", __name__, url_prefix="/submit")

ALLOWED_MANUSCRIPT_EXT = {"pdf", "doc", "docx"}
ALLOWED_COVER_EXT = {"jpg", "jpeg", "png", "webp", "pdf"}

def _allowed(filename, allowed_set):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_set

@bp_submit.route("/", methods=["GET"])
def submit_form():
    return "halo ini submit"
    # return render_template("submit.html")

@bp_submit.route("/submit", methods=["POST"])
def submit_post():
    title = request.form.get("title", "").strip()
    author_name = request.form.get("author_name", "").strip()
    author_email = request.form.get("author_email", "").strip()
    synopsis = request.form.get("synopsis", "").strip()
    file = request.files.get("manuscript")

    if not title or not author_name:
        flash("Judul dan Nama Penulis wajib diisi.", "danger")
        return redirect(url_for("main_submit.submit_form"))

    saved_path = None
    if file and file.filename:
        if not _allowed(file.filename, ALLOWED_MANUSCRIPT_EXT):
            flash("Format naskah harus pdf/doc/docx.", "danger")
            return redirect(url_for("main_submit.submit_form"))
        fname = f"{int(time.time())}_{file.filename.replace(' ', '_')}"
        file.save(os.path.join(current_app.config["UPLOAD_MANUSCRIPTS"], fname))
        saved_path = fname

    mid = g.db.add_manuscript(title, author_name, author_email, synopsis, saved_path)
    flash("Naskah berhasil diajukan. Terima kasih!", "success")
    return redirect(url_for("main_submit.view_manuscript", manuscript_id=mid))

@bp_submit.route("/admin", methods=["GET"])
def admin_list():
    rows = g.db.list_manuscripts()
    return render_template("admin.html", rows=rows)

@bp_submit.route("/view/<int:manuscript_id>", methods=["GET"])
def view_manuscript(manuscript_id):
    row = g.db.get_manuscript(manuscript_id)
    if not row:
        return "Data tidak ditemukan", 404
    return render_template("view.html", m=row)

@bp_submit.route("/admin/<int:manuscript_id>/status", methods=["POST"])
def admin_update_status(manuscript_id):
    new_status = request.form.get("status")
    if new_status not in ("DIAJUKAN", "DIEDIT", "SELESAI"):
        flash("Status tidak valid.", "danger")
        return redirect(url_for("main_submit.admin_list"))
    g.db.update_status(manuscript_id, new_status)
    flash("Status diperbarui.", "success")
    return redirect(url_for("main_submit.view_manuscript", manuscript_id=manuscript_id))

@bp_submit.route("/admin/<int:manuscript_id>/upload-cover", methods=["POST"])
def admin_upload_cover(manuscript_id):
    file = request.files.get("cover")
    if not file or not file.filename:
        flash("File cover belum dipilih.", "danger")
        return redirect(url_for("main_submit.view_manuscript", manuscript_id=manuscript_id))
    if not _allowed(file.filename, ALLOWED_COVER_EXT):
        flash("Format cover harus jpg/jpeg/png/webp/pdf.", "danger")
        return redirect(url_for("main_submit.view_manuscript", manuscript_id=manuscript_id))

    fname = f"cover_{manuscript_id}_{int(time.time())}_{file.filename.replace(' ', '_')}"
    file.save(os.path.join(current_app.config["UPLOAD_COVERS"], fname))

    g.db.update_cover(manuscript_id, fname)
    flash("Cover berhasil diupload.", "success")
    return redirect(url_for("main_submit.view_manuscript", manuscript_id=manuscript_id))

@bp_submit.route("/files/manuscripts/<path:filename>")
def files_manuscripts(filename):
    return send_from_directory(current_app.config["UPLOAD_MANUSCRIPTS"], filename, as_attachment=False)

@bp_submit.route("/files/covers/<path:filename>")
def files_covers(filename):
    return send_from_directory(current_app.config["UPLOAD_COVERS"], filename, as_attachment=False)