# Portfolio Website

A modern, responsive portfolio website built with Flask and Bootstrap 5. Features a clean design, smooth animations, and a comprehensive admin dashboard.

## Features

### Main Website
- Modern and responsive design
- Smooth scroll animations
- Dynamic navigation with scroll spy
- Beautiful hover effects
- Mobile-friendly layout
- Sections for:
  - Hero/Introduction
  - About Me
  - Skills
  - Projects
  - Contact
- Custom favicon support
- Error page handling

### Admin Dashboard
- Secure login system
- Project management
- Skills management
- About section management
- Responsive sidebar navigation
- Clean and intuitive interface

## Recent Updates

### Navigation Improvements
- Added scroll spy functionality to highlight active sections
- Enhanced navbar title with hover effects and animations
- Improved spacing between navigation items
- Added smooth transitions for hover and active states

### Visual Enhancements
- Added custom favicon support
- Improved error page layout and styling
- Enhanced setup page design with gradient background
- Better form styling and input focus states
- Consistent spacing and alignment throughout

### Admin Dashboard Updates
- Improved sidebar navigation
- Better card and table layouts
- Enhanced form styling
- Responsive design improvements
- Better visual hierarchy

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/portfolio-website.git
cd portfolio-website
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

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
flask db upgrade
```

6. Run the development server:
```bash
flask run
```

## Project Structure

```
portfolio-website/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── scroll-spy.js
│   └── favicon/
│       ├── favicon-16x16.png
│       ├── favicon-32x32.png
│       ├── apple-touch-icon.png
│       ├── android-chrome-192x192.png
│       ├── android-chrome-512x512.png
│       └── site.webmanifest
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── error.html
│   └── admin/
│       ├── base.html
│       ├── login.html
│       ├── setup.html
│       ├── dashboard.html
│       ├── projects.html
│       └── skills.html
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── admin/
│       ├── __init__.py
│       └── routes.py
├── migrations/
├── .env
├── .env.example
├── config.py
├── requirements.txt
└── run.py
```

## Technologies Used

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Login
- Flask-Migrate
- Bootstrap 5
- Font Awesome
- Google Fonts

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/portfolio-website](https://github.com/yourusername/portfolio-website) 