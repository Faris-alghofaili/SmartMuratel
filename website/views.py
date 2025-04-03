from flask import Blueprint, abort,render_template,request,jsonify
from flask_login import login_required,  current_user, LoginManager
from .modules import *

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        data = request.get_json(force=True)
        name = data.get("name")
        translated_version = data.get("translated_version")  # ✅ Get the name from the request
        language = data.get("language")

        # ✅ Retrieve Quran version based on the name
        quran_version = Quranversions.query.filter_by(name=translated_version).first()
        if not quran_version:
            return jsonify({"error": "Quran version not found"}), 400
        
        version_id = quran_version.Version_id  # ✅ Extract version_id from the object

        # ✅ Check if project already exists
        existing_project = Project.query.filter_by(User_id=current_user.User_id, name=name).all()
        if existing_project:
            for project in existing_project:
                if project.quranversions_Version_id == version_id:
                    return jsonify({"error": "Project already exists"}), 400

        # ✅ Save the project with the retrieved version_id
        new_project = Project(
            User_id=current_user.User_id,
            name=name,
            quranversions_Version_id=version_id
        )
        db.session.add(new_project)
        db.session.commit()

        return jsonify({"message": "Project added successfully"}), 201
    
    # ✅ Pass existing projects to frontend
    projects = Project.query.filter_by(User_id=current_user.User_id).all()
    return render_template('home.html', project_data=projects)


# ✅ Route to fetch Quran versions
@views.route('/get_quran_versions', methods=['GET'])
@login_required
def get_quran_versions():
    quran_versions = Quranversions.query.all()

    # ✅ Extract actual values from the object
    versions = [
        {
            "id": version.Version_id, 
            "name": version.name, 
            "language": version.language if version.language else None,
            "created_at": version.created_at.strftime('%Y-%m-%d') if version.created_at else None
        } 
        for version in quran_versions
    ]

    return jsonify(versions)

# ✅ Route to delete a project
@views.route('/delete_project/<int:project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    # ✅ Ensure the project belongs to the current user before deleting
    if project.User_id != current_user.User_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(project)
    db.session.commit()
    
    return jsonify({"message": "Project deleted successfully"}), 200

@views.route('/project/<int:project_id>', methods=['GET'])
@login_required
def project_details(project_id):
    project = Project.query.get(project_id)
    # Verify the project belongs to the current user
    if project.User_id != current_user.User_id:
        abort(403)
    
    voices = Voices.query.all()
    
    return render_template('Main.html', 
                        project=project,
                        voices=voices)

@views.route('/assign_voice/<int:project_id>', methods=['POST'])
@login_required
def assign_voice(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Verify ownership
    if project.User_id != current_user.User_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    voice_id = request.json.get('voice_id')
    
    if not voice_id:
        # Remove voice association if empty selection
        project.voice_id = None
        db.session.commit()
        return jsonify({'message': 'Voice removed', 'voice_name': ''})
    
    voice = Voices.query.get(voice_id)
    if not voice:
        return jsonify({'error': 'Voice not found'}), 404
    
    # Assign the voice
    project.voice_id = voice_id
    db.session.commit()
    
    return jsonify({
        'message': 'Voice assigned successfully',
        'voice_name': voice.name
    })
@views.route('/get_surahs')
@login_required
def get_surahs():
    surahs = Surahs.query.order_by(Surahs.surah_number).all()
    return jsonify([{
        'id': s.sutrah_id,
        'number': s.surah_number,
        'name': s.name,
        'arabic_name': s.arabic_name,
        'ayah_count': s.number_of_ayahs
    } for s in surahs])

@views.route('/get_verses/<int:surah_id>')
@login_required
def get_verses(surah_id):
    verses = Verses.query.filter_by(Surahs_sutrah_id=surah_id)\
                    .order_by(Verses.verse_number)\
                    .all()
    return jsonify([{
        'id': v.verse_id,
        'number': v.verse_number,
        'text': v.text
    } for v in verses])