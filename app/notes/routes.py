from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models import Note

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/')
@login_required
def index():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('notes.html', notes=notes)

@notes_bp.route('/note/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_note = Note(title=title, content=content, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note created successfully!', 'success')
        return redirect(url_for('notes.index'))
    return render_template('note_form.html', note=None)

@notes_bp.route('/note/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        flash('You are not authorized to edit this note.', 'danger')
        return redirect(url_for('notes.index'))

    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        flash('Note updated successfully!', 'success')
        return redirect(url_for('notes.index'))
    
    return render_template('note_form.html', note=note)

@notes_bp.route('/note/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    note = Note.query.get_or_404(id)
    if note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Note deleted successfully!', 'success')
    else:
        flash('You are not authorized to delete this note.', 'danger')
    return redirect(url_for('notes.index'))
