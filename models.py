from flask_login import UserMixin
from supabase import create_client, Client
from datetime import datetime
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Load environment variables
load_dotenv()

# Initialize Supabase client
try:
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("Missing Supabase credentials in environment variables")
        
    supabase: Client = create_client(
        supabase_url=supabase_url,
        supabase_key=supabase_key
    )
except Exception as e:
    print(f"Error initializing Supabase client: {e}")
    raise

class User(UserMixin):
    def __init__(self, id, email, password_hash=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    def get_id(self):
        return str(self.email)  # Flask-Login requires this method

class Project:
    def __init__(self, id, title, description, image_url, github_url, live_url, technologies, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.image_url = image_url
        self.github_url = github_url
        self.live_url = live_url
        self.technologies = technologies
        self.created_at = created_at

class Message:
    def __init__(self, id, name, email, message, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.message = message
        # Convert string to datetime if it's a string
        if isinstance(created_at, str):
            self.created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        else:
            self.created_at = created_at

class Profile:
    def __init__(self, id, about_text, image_url, resume_url=None, created_at=None, updated_at=None):
        self.id = id
        self.about_text = about_text
        self.image_url = image_url
        self.resume_url = resume_url
        self.created_at = created_at
        self.updated_at = updated_at

# Database operations
def get_user_by_email(email):
    response = supabase.table('users').select('*').eq('email', email).execute()
    if response.data:
        user_data = response.data[0]
        return User(user_data['id'], user_data['email'], user_data['password_hash'])
    return None

def get_all_projects():
    response = supabase.table('projects').select('*').execute()
    return [Project(**project) for project in response.data]

def get_project_by_id(project_id):
    response = supabase.table('projects').select('*').eq('id', project_id).execute()
    if response.data:
        return Project(**response.data[0])
    return None

def add_project(project_data):
    response = supabase.table('projects').insert(project_data).execute()
    return Project(**response.data[0])

def update_project(project_id, project_data):
    response = supabase.table('projects').update(project_data).eq('id', project_id).execute()
    return Project(**response.data[0])

def delete_project(project_id):
    supabase.table('projects').delete().eq('id', project_id).execute()

def get_all_messages():
    response = supabase.table('messages').select('*').order('created_at', desc=True).execute()
    return [Message(**message) for message in response.data]

def create_message(message_data):
    response = supabase.table('messages').insert(message_data).execute()
    return Message(**response.data[0])

def delete_message(message_id):
    supabase.table('messages').delete().eq('id', message_id).execute()

def get_profile():
    response = supabase.table('profile').select('*').limit(1).execute()
    if response.data:
        return Profile(**response.data[0])
    return None

def update_profile(profile_data):
    try:
        # Get current profile
        current_profile = get_profile()
        if not current_profile:
            return None
            
        # Update only provided fields
        update_data = {}
        for key, value in profile_data.items():
            if value is not None:
                update_data[key] = value
                
        # Always update the updated_at timestamp
        update_data['updated_at'] = datetime.utcnow().isoformat()
        
        # Update profile in database
        response = supabase.table('profile').update(update_data).eq('id', current_profile.id).execute()
        if response.data:
            return Profile(**response.data[0])
        return None
    except Exception as e:
        print(f"Error updating profile: {e}")
        return None

def create_profile(profile_data):
    try:
        # Set timestamps
        now = datetime.utcnow().isoformat()
        profile_data['created_at'] = now
        profile_data['updated_at'] = now
        
        # Insert new profile
        response = supabase.table('profile').insert(profile_data).execute()
        if response.data:
            return Profile(**response.data[0])
        return None
    except Exception as e:
        print(f"Error creating profile: {e}")
        return None

def create_user(email, password):
    password_hash = generate_password_hash(password)
    user_data = {
        'email': email,
        'password_hash': password_hash
    }
    response = supabase.table('users').insert(user_data).execute()
    if response.data:
        return User(response.data[0]['id'], response.data[0]['email'], response.data[0]['password_hash'])
    return None 