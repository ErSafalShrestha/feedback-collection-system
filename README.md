# 🎓 Feedback Collection and Analysis System for Online Learning Platforms

## Project Overview

This is a full-stack web application developed as part of an MSc dissertation project at the University of the West of Scotland. The system collects valuable feedback from students and teachers to improve the quality of online learning in Nepalese secondary schools.

## 🚀 Technologies Used

- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Backend**: Python Flask
- **Database**: SQLite
- **NLP Library**: TextBlob (for sentiment analysis)
- **Visualization**: Matplotlib
- **Additional**: Flask-SQLAlchemy, Flask-WTF

## 📁 Project Structure

```
ABC/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── forms.py              # Form classes (placeholder)
├── db.sqlite3            # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── student_feedback.html
│   ├── teacher_feedback.html
│   ├── thankyou_student.html
│   ├── thankyou_teacher.html
│   └── admin_dashboard.html
├── static/              # CSS and static files
│   └── style.css
└── README.md           # This file
```

## 🔧 Setup Instructions

### 1. Install Dependencies

Make sure you have Python 3.7+ installed, then run:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Set Flask app
export FLASK_APP=app.py

# Run in development mode
flask run
```

Or simply:

```bash
python app.py
```

### 3. Access the Application

Open your browser and go to: `http://127.0.0.1:5000`

## 🖥️ Features

### Landing Page
- Clean, academic design with soft blue/green color scheme
- Two call-to-action buttons for student and teacher feedback
- Responsive Bootstrap layout

### Student Feedback Form
- Personal information: Name, Class, Email, Phone
- 10 closed-ended questions (satisfaction, technical issues, preferences)
- 10 open-ended questions about online learning experience
- Form validation and error handling

### Teacher Feedback Form
- Personal information: Name, Subject, Email, Phone
- 10 closed-ended questions (teaching effectiveness, resources, engagement)
- 10 open-ended questions about online teaching experience
- Form validation and error handling

### Admin Dashboard
- Password protected (Password: `admin123`)
- Statistics: Total student and teacher responses
- Sentiment analysis charts using TextBlob
- Student satisfaction level charts
- Responsive dashboard with Bootstrap cards

### Backend Features
- **Data Storage**: All responses stored in SQLite database
- **Input Sanitization**: Protection against malicious input
- **Sentiment Analysis**: TextBlob analyzes open-ended responses
- **Security**: Session management and basic authentication

## 📊 Database Schema

### StudentFeedback Table
- Personal info: student_name, student_class, student_email, student_phone
- Closed questions: q1-q10 (satisfaction, preferences, issues)
- Open questions: open_q1-open_q10 (detailed feedback)
- Sentiment data: sentiment_polarity, sentiment_subjectivity, sentiment_label

### TeacherFeedback Table
- Personal info: teacher_name, teacher_subject, teacher_email, teacher_phone
- Closed questions: q1-q10 (effectiveness, engagement, tools)
- Open questions: open_q1-open_q10 (teaching experience)
- Sentiment data: sentiment_polarity, sentiment_subjectivity, sentiment_label

## 🔒 Security Features

- Input sanitization to prevent XSS attacks
- Session-based authentication for admin
- HTML tag removal and dangerous character filtering
- Email validation

## 📈 Analytics & Insights

The admin dashboard provides:
- **Sentiment Analysis**: Positive/Negative/Neutral distribution
- **Satisfaction Metrics**: Student satisfaction levels
- **Response Counts**: Total submissions from students and teachers
- **Visual Charts**: Generated using Matplotlib

## 🎨 Design Philosophy

- **Academic Focus**: Clean, professional design suitable for educational research
- **Accessibility**: Mobile-responsive layout with Bootstrap
- **User Experience**: Simple navigation, clear forms, helpful error messages
- **Color Scheme**: Soft blues and greens for a calming, trustworthy feel

## 🚀 Deployment

For production deployment:

1. Change the secret key in `app.py`
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure environment variables
4. Use a production database (PostgreSQL/MySQL)
5. Enable HTTPS

## 🔧 Customization

### Adding New Questions
1. Update the HTML forms in `templates/`
2. Add new database columns in `app.py`
3. Update form processing logic

### Changing Admin Password
Edit line in `app.py`:
```python
if password == 'your_new_password':
```

### Styling Changes
Edit `static/style.css` or update Bootstrap classes in templates.

## 📝 License

This project is created for academic purposes as part of an MSc dissertation.

## 👨‍💻 Author

Developed for MSc dissertation research at the University of the West of Scotland.

---

**Note**: This is a prototype system designed for academic research. For production use, implement additional security measures and testing. 

Perfect! Your Flask server is now running successfully! 🎉

## 🌐 How to Access Your Website:

**Open your web browser** (Chrome, Safari, Firefox, etc.) and go to:

```
http://localhost:5000
```

## 📱 What You'll See:

1. **Landing Page** - Beautiful homepage with two buttons
2. **Student Feedback Form** - Click "Student Feedback Form" button
3. **Teacher Feedback Form** - Click "Teacher Feedback Form" button
4. **Admin Dashboard** - Go to `http://127.0.0.1:5000/admin` (Password: `admin123`)

## 🔗 Direct Links:

- **Home**: http://127.0.0.1:5000
- **Student Form**: http://127.0.0.1:5000/student_feedback
- **Teacher Form**: http://127.0.0.1:5000/teacher_feedback
- **Admin Dashboard**: http://127.0.0.1:5000/admin

## ✅ Server Status:
Your server is running perfectly on **port 5000**. The message shows:
- ✅ Matplotlib font cache built successfully
- ✅ Flask app running in debug mode
- ✅ Server accessible at http://127.0.0.1:5000

Just **copy and paste** `http://127.0.0.1:5000` into your browser address bar and press Enter! 🚀 