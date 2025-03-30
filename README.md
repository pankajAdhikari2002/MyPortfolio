# Portfolio Website

A modern, responsive portfolio website built with Flask and Supabase. This website allows you to showcase your projects, manage your profile, and handle contact messages through an admin dashboard.

## Features

- 🎨 Modern and responsive design
- 📱 Mobile-friendly interface
- 🔒 Secure admin dashboard
- 📝 Project management system
- 👤 Profile management
- 📄 Resume upload functionality
- 📧 Contact form with message management
- 🖼️ Image upload for projects and profile
- 🔍 SEO optimized

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: Supabase
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **CSS Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Deployment**: Gunicorn

## Prerequisites

- Python 3.8 or higher
- Supabase account
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pankajAdhikari2002/MyPortfolio.git
cd MyPortfolio
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

5. Set up the database:
   - Create a new project in Supabase
   - Create the following tables:
     - users
     - projects
     - messages
     - profile

## Directory Structure

```
portfolio-website/
├── static/
│   ├── css/
│   ├── js/
│   ├── uploads/
│   └── resume/
├── templates/
│   ├── admin/
│   └── index.html
├── app.py
├── models.py
├── requirements.txt
└── .env
```

## Usage

1. Run the development server:
```bash
python app.py
```

2. Access the website at `http://localhost:5000`

3. Set up the admin account:
   - Visit `http://localhost:5000/admin/setup`
   - Create your admin account
   - Log in to the admin dashboard

## Admin Dashboard Features

- Project Management
  - Add, edit, and delete projects
  - Upload project images
  - Manage project details and links

- Profile Management
  - Update about text
  - Change profile picture
  - Upload/update resume

- Message Management
  - View contact form submissions
  - Delete messages

## Production Deployment

1. Set environment variables for production:
```env
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
PORT=5000
```

2. Run with Gunicorn:
```bash
gunicorn app:app
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Pankaj Adhikari - pankajadhikari75@gmail.com
Project Link: https://github.com/pankajAdhikari2002/MyPortfolio 