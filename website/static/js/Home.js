from flask import Blueprint,render_template,request,jsonify
from flask_login import login_required,  current_user, LoginManager
from .modules import db, Project, Quranversions

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


    
    

