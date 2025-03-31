from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from models import *
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Check for required environment variables
required_env_vars = ['SUPABASE_URL', 'SUPABASE_KEY', 'SECRET_KEY']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching for uploaded files
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Session lifetime

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/resume', exist_ok=True)  # Ensure resume directory exists

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        user = get_user_by_email(user_id)
        return user
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message='Page Not Found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500,
                         error_message='Internal Server Error'), 500

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = get_user_by_email(email)
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        
        flash('Invalid email or password', 'danger')
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    projects = get_all_projects()
    messages = get_all_messages()
    return render_template('admin/dashboard.html', projects=projects, messages=messages)

@app.route('/admin/projects')
@login_required
def admin_projects():
    projects = get_all_projects()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/projects', methods=['POST'])
@login_required
def create_project():
    try:
        # Get form data
        project_data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'technologies': [tech.strip() for tech in request.form.get('technologies').split(',')],
            'github_url': request.form.get('github_url'),
            'live_url': request.form.get('live_url')
        }
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                project_data['image_url'] = f'/static/uploads/{filename}'
        
        # Create project in database
        project = add_project(project_data)
        if project:
            return jsonify({'success': True, 'message': 'Project created successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to create project'})
    except Exception as e:
        print(f"Error creating project: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/projects/<uuid:project_id>', methods=['GET'])
@login_required
def get_project(project_id):
    project = get_project_by_id(str(project_id))
    if project:
        return jsonify({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'technologies': project.technologies,
            'github_url': project.github_url,
            'live_url': project.live_url,
            'image_url': project.image_url
        })
    return jsonify({'error': 'Project not found'}), 404

@app.route('/admin/projects/<uuid:project_id>', methods=['PUT'])
@login_required
def update_project(project_id):
    try:
        # Get form data
        project_data = {
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'technologies': [tech.strip() for tech in request.form.get('technologies').split(',')],
            'github_url': request.form.get('github_url'),
            'live_url': request.form.get('live_url')
        }
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                project_data['image_url'] = f'/static/uploads/{filename}'
        
        # Update project in database
        project = update_project(str(project_id), project_data)
        if project:
            return jsonify({'success': True, 'message': 'Project updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to update project'})
    except Exception as e:
        print(f"Error updating project: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/projects/<uuid:project_id>', methods=['DELETE'])
@login_required
def delete_project_route(project_id):
    try:
        # Get project details before deletion to get the image path
        project = get_project_by_id(str(project_id))
        if project and project.image_url:
            # Extract filename from image_url
            filename = project.image_url.split('/')[-1]
            # Delete the file from uploads folder
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete project from database
        delete_project(str(project_id))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/messages')
@login_required
def admin_messages():
    messages = get_all_messages()
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/messages/<uuid:message_id>', methods=['DELETE'])
@login_required
def delete_message_route(message_id):
    try:
        delete_message(str(message_id))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    if request.method == 'POST':
        try:
            # Get form data
            profile_data = {
                'about_text': request.form.get('about_text')
            }
            
            # Handle profile image upload
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file and file.filename:
                    try:
                        # Get current profile to delete old image
                        current_profile = get_profile()
                        if current_profile and current_profile.image_url:
                            # Extract filename from the full URL path
                            old_filename = current_profile.image_url.split('/')[-1]
                            old_file_path = os.path.join('static/uploads', old_filename)
                            if os.path.exists(old_file_path):
                                os.remove(old_file_path)
                        
                        filename = secure_filename(file.filename)
                        # Add timestamp to filename to prevent caching
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{timestamp}_{filename}"
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        profile_data['image_url'] = f'/static/uploads/{filename}'
                    except Exception as e:
                        print(f"Error saving image: {e}")
                        flash('Error saving profile image', 'danger')
                        return redirect(url_for('admin_profile'))
            
            # Handle resume upload
            if 'resume' in request.files:
                file = request.files['resume']
                if file and file.filename:
                    try:
                        # Get current profile to delete old resume
                        current_profile = get_profile()
                        if current_profile and current_profile.resume_url:
                            old_filename = current_profile.resume_url.split('/')[-1]
                            old_file_path = os.path.join('static/resume', old_filename)
                            if os.path.exists(old_file_path):
                                os.remove(old_file_path)
                        
                        # Ensure the file is a PDF
                        if not file.filename.lower().endswith('.pdf'):
                            flash('Resume must be a PDF file', 'danger')
                            return redirect(url_for('admin_profile'))
                        
                        filename = secure_filename(file.filename)
                        # Add timestamp to filename to prevent caching
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{timestamp}_{filename}"
                        file_path = os.path.join('static/resume', filename)
                        file.save(file_path)
                        profile_data['resume_url'] = f'/static/resume/{filename}'
                    except Exception as e:
                        print(f"Error saving resume: {e}")
                        flash('Error saving resume', 'danger')
                        return redirect(url_for('admin_profile'))
            
            # Check if profile exists
            current_profile = get_profile()
            if current_profile:
                # Update existing profile
                profile = update_profile(profile_data)
                if profile:
                    flash('Profile updated successfully', 'success')
                else:
                    flash('Failed to update profile', 'danger')
            else:
                # Create new profile
                profile = create_profile(profile_data)
                if profile:
                    flash('Profile created successfully', 'success')
                else:
                    flash('Failed to create profile', 'danger')
            
            return redirect(url_for('admin_profile'))
        except Exception as e:
            print(f"Error updating profile: {e}")
            flash('Error updating profile', 'danger')
            return redirect(url_for('admin_profile'))
    
    profile = get_profile()
    return render_template('admin/profile.html', profile=profile)


# @app.route('/admin/setup', methods=['GET', 'POST'])
# def setup_admin():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
        
#         # Check if user already exists
#         existing_user = get_user_by_email(email)
#         if existing_user:
#             flash('Admin user already exists', 'warning')
#             return redirect(url_for('login'))
        
#         # Create new admin user
#         user = create_user(email, password)
#         if user:
#             flash('Admin user created successfully', 'success')
#             return redirect(url_for('login'))
#         else:
#             flash('Failed to create admin user', 'danger')
    
#     return render_template('admin/setup.html')

# Main routes
@app.route('/')
def home():
    projects = get_all_projects()
    profile = get_profile()
    return render_template('index.html', projects=projects, profile=profile)

@app.route('/contact', methods=['POST'])
def contact():
    try:
        message_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'message': request.form.get('message')
        }
        create_message(message_data)
        flash('Message sent successfully!', 'success')
    except Exception as e:
        flash('Error sending message. Please try again.', 'danger')
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Use environment variable to determine if we're in production
    is_production = os.getenv('FLASK_ENV') == 'production'
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=not is_production)