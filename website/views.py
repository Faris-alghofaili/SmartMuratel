from flask import Blueprint, abort,render_template,request,jsonify
from flask_login import login_required,  current_user, LoginManager
from .modules import *
import requests
from datetime import datetime

views = Blueprint('views',__name__)

quran_versions = [
        { "name": "english_rwwad", "language": "English"},
        ]
surah_names = ["Al-Fatiha", "Al-Baqarah", "Ali 'Imran", "An-Nisa", "Al-Ma'idah", "Al-An'am", "Al-A'raf", "Al-Anfal", 
"At-Tawbah", "Yunus", "Hud", "Yusuf", "Ar-Ra'd", "Ibrahim", "Al-Hijr", "An-Nahl", "Al-Isra", "Al-Kahf", "Maryam", 
"Ta-Ha", "Al-Anbiya", "Al-Hajj", "Al-Mu'minun", "An-Nur", "Al-Furqan", "Ash-Shu'ara", "An-Naml", "Al-Qasas", 
"Al-Ankabut", "Ar-Rum", "Luqman", "As-Sajdah", "Al-Ahzab", "Saba", "Fatir", "Ya-Sin", "As-Saffat", "Sad", 
"Az-Zumar", "Ghafir", "Fussilat", "Ash-Shura", "Az-Zukhruf", "Ad-Dukhan", "Al-Jathiyah", "Al-Ahqaf", "Muhammad", 
"Al-Fath", "Al-Hujurat", "Qaf", "Adh-Dhariyat", "At-Tur", "An-Najm", "Al-Qamar", "Ar-Rahman", "Al-Waqi'ah", 
"Al-Hadid", "Al-Mujadila", "Al-Hashr", "Al-Mumtahanah", "As-Saff", "Al-Jumu'ah", "Al-Munafiqun", "At-Taghabun", 
"At-Talaq", "At-Tahrim", "Al-Mulk", "Al-Qalam", "Al-Haqqah", "Al-Ma'arij", "Nuh", "Al-Jinn", "Al-Muzzammil", 
"Al-Muddaththir", "Al-Qiyamah", "Al-Insan", "Al-Mursalat", "An-Naba", "An-Nazi'at", "'Abasa", "At-Takwir", 
"Al-Infitar", "Al-Mutaffifin", "Al-Inshiqaq", "Al-Buruj", "At-Tariq", "Al-A'la", "Al-Ghashiyah", "Al-Fajr", 
"Al-Balad", "Ash-Shams", "Al-Layl", "Ad-Duha", "Ash-Sharh", "At-Tin", "Al-'Alaq", "Al-Qadr", "Al-Bayyinah", 
"Az-Zalzalah", "Al-'Adiyat", "Al-Qari'ah", "At-Takathur", "Al-'Asr", "Al-Humazah", "Al-Fil", "Quraysh", 
"Al-Ma'un", "Al-Kawthar", "Al-Kafirun", "An-Nasr", "Al-Masad", "Al-Ikhlas", "Al-Falaq", "An-Nas"]

@views.route('/how-it-works')
def how_it_works():
    return render_template('How_it_works.html')

@views.route('/about-us')
def about_us():
    return render_template('About_us.html')




@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        data = request.get_json(force=True)
        name = data.get("name")
        translated_version = data.get("translated_version")
        language = data.get("language")

        # Check against hardcoded list
        allowed_version = next(
            (v for v in quran_versions if v["name"] == translated_version and v["language"] == language), None
        )
        if not allowed_version:
            return jsonify({"error": "Invalid Quran version selected"}), 400

        # Check for existing project
        existing_project = Project.query.filter_by(User_id=current_user.User_id, name=name).first()
        if existing_project:
            return jsonify({"error": "Project already exists"}), 400
        
        # Create new Quran version
        new_version = Quranversions(
            name=translated_version,
            language=language,
            created_at=datetime.utcnow()
        )
        db.session.add(new_version)
        db.session.commit()

        # Create new project
        new_project = Project(
            User_id=current_user.User_id,
            name=name,
            quranversions_Version_id=new_version.Version_id
        )
        db.session.add(new_project)
        db.session.commit()

        return jsonify({"message": "Project added successfully"}), 201
    # ✅ Pass existing projects to frontend
    projects = Project.query.filter_by(User_id=current_user.User_id).all()
    return render_template('home.html', project_data=projects)


# ✅ Route to fetch Quran versions (hardcoded)
@views.route('/get_quran_versions', methods=['GET'])
@login_required
def get_quran_versions():
    return jsonify(quran_versions)

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
    project = Project.query.get_or_404(project_id)
    # Verify the project belongs to the current user
    if project.User_id != current_user.User_id:
        abort(403)
    
    # Get the fixed version for this project
    version = Quranversions.query.get(project.quranversions_Version_id)
    if not version:
        abort(404)
    
    voices = Voices.query.all()
    
    return render_template('Main.html', 
                        project=project,
                        version=version, 
                        voices=voices,
                        surah_names=surah_names)

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


@views.route('/load_surah', methods=['POST'])
@login_required
def load_surah():
    project_id = request.json.get('project_id')
    surah_number = request.json.get('surah_number')
    
    if not project_id or not surah_number:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        surah_number = int(surah_number)  # Convert to integer
        if surah_number < 1 or surah_number > 114:
            return jsonify({'error': 'Invalid surah number'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid surah number format'}), 400
    
    # Get the project and verify ownership
    project = Project.query.get(project_id)
    if not project or project.User_id != current_user.User_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get the Quran version for this project
    version = Quranversions.query.get(project.quranversions_Version_id)
    if not version:
        return jsonify({'error': 'Quran version not found'}), 404
    
    # Check if the surah exists in our database for this version
    surah = Surahs.query.filter_by(
        surah_number=surah_number,
        QuranVersions_Version_id=version.Version_id
    ).first()
    
    if not surah:
        # Fetch from API and store in database
        api_url = f"https://quranenc.com/api/v1/translation/sura/{version.name}/{surah_number}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            
            if not data or 'result' not in data:
                return jsonify({'error': 'Invalid API response'}), 500
                
            # Create the surah record - using your surah_names list
            surah_name = surah_names[surah_number-1]  # Convert to 0-based index
            first_verse = data['result'][0]
            surah = Surahs(
                surah_number=surah_number,
                name=surah_name,
                arabic_name=first_verse.get('sura_name_ar', ''),
                number_of_ayahs=len(data['result']),
                QuranVersions_Version_id=version.Version_id
            )
            db.session.add(surah)
            db.session.commit()
            
            # Add all verses
            for verse_data in data['result']:
                verse = Verses(
                    verse_number=int(verse_data['aya']),
                    text=verse_data['translation'],
                    Surahs_sutrah_id=surah.sutrah_id
                )
                db.session.add(verse)
            db.session.commit()
            
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Failed to fetch surah from API: {str(e)}'}), 500
        except Exception as e:
            return jsonify({'error': f'Error processing surah: {str(e)}'}), 500
    
    # Get all verses for this surah
    verses = Verses.query.filter_by(Surahs_sutrah_id=surah.sutrah_id)\
                        .order_by(Verses.verse_number)\
                        .all()
    
    # Prepare response
    verses_data = [{
        'number': verse.verse_number,
        'text': verse.text
    } for verse in verses]
    
    return jsonify({
        'surah': {
            'number': surah.surah_number,
            'name': surah.name,
            'arabic_name': surah.arabic_name,
            'verse_count': surah.number_of_ayahs
        },
        'verses': verses_data
    })