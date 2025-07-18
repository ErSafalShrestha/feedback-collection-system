from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os
import io
import base64
import csv
from datetime import datetime
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here_change_in_production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class StudentFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    student_class = db.Column(db.String(50), nullable=False)
    student_email = db.Column(db.String(120), nullable=False)
    student_phone = db.Column(db.String(20), nullable=False)
    
    # Closed-ended questions
    q1 = db.Column(db.String(50), nullable=False)  # satisfaction
    q2 = db.Column(db.String(10), nullable=False)  # internet access
    q3 = db.Column(db.String(50), nullable=False)  # technical issues
    q4 = db.Column(db.String(10), nullable=False)  # interactive
    q5 = db.Column(db.String(10), nullable=False)  # comfortable asking
    q6 = db.Column(db.String(50), nullable=False)  # teaching materials
    q7 = db.Column(db.String(10), nullable=False)  # assignments manageable
    q8 = db.Column(db.String(50), nullable=False)  # preference
    q9 = db.Column(db.String(50), nullable=False)  # timely feedback
    q10 = db.Column(db.String(10), nullable=False) # recommend
    
    # Open-ended questions
    open_q1 = db.Column(db.Text, nullable=False)
    open_q2 = db.Column(db.Text, nullable=False)
    open_q3 = db.Column(db.Text, nullable=False)
    open_q4 = db.Column(db.Text, nullable=False)
    open_q5 = db.Column(db.Text, nullable=False)
    open_q6 = db.Column(db.Text, nullable=False)
    open_q7 = db.Column(db.Text, nullable=False)
    open_q8 = db.Column(db.Text, nullable=False)
    open_q9 = db.Column(db.Text, nullable=False)
    open_q10 = db.Column(db.Text, nullable=False)
    
    # Sentiment analysis results
    sentiment_polarity = db.Column(db.Float, nullable=True)
    sentiment_subjectivity = db.Column(db.Float, nullable=True)
    sentiment_label = db.Column(db.String(20), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TeacherFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(100), nullable=False)
    teacher_subject = db.Column(db.String(50), nullable=False)
    teacher_email = db.Column(db.String(120), nullable=False)
    teacher_phone = db.Column(db.String(20), nullable=False)
    
    # Closed-ended questions
    q1 = db.Column(db.String(50), nullable=False)  # effectiveness
    q2 = db.Column(db.String(10), nullable=False)  # resources access
    q3 = db.Column(db.String(50), nullable=False)  # technical issues
    q4 = db.Column(db.String(10), nullable=False)  # student engagement
    q5 = db.Column(db.String(10), nullable=False)  # comfortable with tools
    q6 = db.Column(db.String(50), nullable=False)  # student participation
    q7 = db.Column(db.String(10), nullable=False)  # assessments manageable
    q8 = db.Column(db.String(50), nullable=False)  # preference
    q9 = db.Column(db.String(50), nullable=False)  # provide feedback
    q10 = db.Column(db.String(10), nullable=False) # recommend
    
    # Open-ended questions
    open_q1 = db.Column(db.Text, nullable=False)
    open_q2 = db.Column(db.Text, nullable=False)
    open_q3 = db.Column(db.Text, nullable=False)
    open_q4 = db.Column(db.Text, nullable=False)
    open_q5 = db.Column(db.Text, nullable=False)
    open_q6 = db.Column(db.Text, nullable=False)
    open_q7 = db.Column(db.Text, nullable=False)
    open_q8 = db.Column(db.Text, nullable=False)
    open_q9 = db.Column(db.Text, nullable=False)
    open_q10 = db.Column(db.Text, nullable=False)
    
    # Sentiment analysis results
    sentiment_polarity = db.Column(db.Float, nullable=True)
    sentiment_subjectivity = db.Column(db.Float, nullable=True)
    sentiment_label = db.Column(db.String(20), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper function to sanitize input
def sanitize_input(text):
    if not text:
        return ""
    # Remove HTML tags and dangerous characters
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[<>"\';]', '', text)
    return text.strip()

# Helper function to perform sentiment analysis
def analyze_sentiment(open_responses):
    combined_text = " ".join([response for response in open_responses if response])
    combined_text = sanitize_input(combined_text)
    
    if not combined_text:
        return 0.0, 0.0, "neutral"
    
    blob = TextBlob(combined_text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"
    
    return polarity, subjectivity, label

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student_feedback', methods=['GET', 'POST'])
def student_feedback():
    if request.method == 'POST':
        try:
            # Get form data and sanitize
            name = sanitize_input(request.form.get('student_name'))
            class_name = sanitize_input(request.form.get('student_class'))
            email = sanitize_input(request.form.get('student_email'))
            phone = sanitize_input(request.form.get('student_phone'))
            
            # Validate required fields
            if not all([name, class_name, email, phone]):
                flash('All fields are required!', 'error')
                return render_template('student_feedback.html')
            
            # Get closed-ended responses
            q_responses = []
            for i in range(1, 11):
                q_responses.append(sanitize_input(request.form.get(f'q{i}')))
            
            # Get open-ended responses
            open_responses = []
            for i in range(1, 11):
                open_responses.append(sanitize_input(request.form.get(f'open_q{i}')))
            
            # Perform sentiment analysis
            polarity, subjectivity, sentiment_label = analyze_sentiment(open_responses)
            
            # Create new student feedback record
            feedback = StudentFeedback(
                student_name=name,
                student_class=class_name,
                student_email=email,
                student_phone=phone,
                q1=q_responses[0], q2=q_responses[1], q3=q_responses[2], q4=q_responses[3], q5=q_responses[4],
                q6=q_responses[5], q7=q_responses[6], q8=q_responses[7], q9=q_responses[8], q10=q_responses[9],
                open_q1=open_responses[0], open_q2=open_responses[1], open_q3=open_responses[2], 
                open_q4=open_responses[3], open_q5=open_responses[4], open_q6=open_responses[5],
                open_q7=open_responses[6], open_q8=open_responses[7], open_q9=open_responses[8], open_q10=open_responses[9],
                sentiment_polarity=polarity,
                sentiment_subjectivity=subjectivity,
                sentiment_label=sentiment_label
            )
            
            db.session.add(feedback)
            db.session.commit()
            
            return redirect(url_for('thankyou_student', name=name))
        
        except Exception as e:
            flash('An error occurred while submitting your feedback. Please try again.', 'error')
            return render_template('student_feedback.html')
    
    return render_template('student_feedback.html')

@app.route('/teacher_feedback', methods=['GET', 'POST'])
def teacher_feedback():
    if request.method == 'POST':
        try:
            # Get form data and sanitize
            name = sanitize_input(request.form.get('teacher_name'))
            subject = sanitize_input(request.form.get('teacher_subject'))
            email = sanitize_input(request.form.get('teacher_email'))
            phone = sanitize_input(request.form.get('teacher_phone'))
            
            # Validate required fields
            if not all([name, subject, email, phone]):
                flash('All fields are required!', 'error')
                return render_template('teacher_feedback.html')
            
            # Get closed-ended responses
            q_responses = []
            for i in range(1, 11):
                q_responses.append(sanitize_input(request.form.get(f'q{i}')))
            
            # Get open-ended responses
            open_responses = []
            for i in range(1, 11):
                open_responses.append(sanitize_input(request.form.get(f'open_q{i}')))
            
            # Perform sentiment analysis
            polarity, subjectivity, sentiment_label = analyze_sentiment(open_responses)
            
            # Create new teacher feedback record
            feedback = TeacherFeedback(
                teacher_name=name,
                teacher_subject=subject,
                teacher_email=email,
                teacher_phone=phone,
                q1=q_responses[0], q2=q_responses[1], q3=q_responses[2], q4=q_responses[3], q5=q_responses[4],
                q6=q_responses[5], q7=q_responses[6], q8=q_responses[7], q9=q_responses[8], q10=q_responses[9],
                open_q1=open_responses[0], open_q2=open_responses[1], open_q3=open_responses[2], 
                open_q4=open_responses[3], open_q5=open_responses[4], open_q6=open_responses[5],
                open_q7=open_responses[6], open_q8=open_responses[7], open_q9=open_responses[8], open_q10=open_responses[9],
                sentiment_polarity=polarity,
                sentiment_subjectivity=subjectivity,
                sentiment_label=sentiment_label
            )
            
            db.session.add(feedback)
            db.session.commit()
            
            return redirect(url_for('thankyou_teacher', name=name))
        
        except Exception as e:
            flash('An error occurred while submitting your feedback. Please try again.', 'error')
            return render_template('teacher_feedback.html')
    
    return render_template('teacher_feedback.html')

@app.route('/thankyou_student/<name>')
def thankyou_student(name):
    return render_template('thankyou_student.html', name=name)

@app.route('/thankyou_teacher/<name>')
def thankyou_teacher(name):
    return render_template('thankyou_teacher.html', name=name)

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('admin_password')
        if password == 'admin123':  # Simple hardcoded password for prototype
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', 
                                 error='Invalid password')
    
    # Show login form
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    # Get statistics
    student_count = StudentFeedback.query.count()
    teacher_count = TeacherFeedback.query.count()
    
    # Generate charts
    charts = generate_charts()
    
    return render_template('admin_analytics.html', 
                         student_count=student_count,
                         teacher_count=teacher_count,
                         charts=charts)

def generate_charts():
    charts = {}
    
    # Sentiment distribution chart
    student_sentiments = db.session.query(StudentFeedback.sentiment_label).all()
    teacher_sentiments = db.session.query(TeacherFeedback.sentiment_label).all()
    
    sentiment_data = {}
    for sentiment in [s[0] for s in student_sentiments + teacher_sentiments]:
        sentiment_data[sentiment] = sentiment_data.get(sentiment, 0) + 1
    
    if sentiment_data:
        plt.figure(figsize=(8, 6))
        plt.bar(list(sentiment_data.keys()), list(sentiment_data.values()), color=['#28a745', '#ffc107', '#dc3545'])
        plt.title('Overall Sentiment Distribution')
        plt.ylabel('Count')
        plt.xlabel('Sentiment')
        
        # Save chart as base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        charts['sentiment'] = base64.b64encode(img.getvalue()).decode()
        plt.close()
    
    # Satisfaction levels
    student_satisfaction = db.session.query(StudentFeedback.q1).all()
    satisfaction_data = {}
    for sat in [s[0] for s in student_satisfaction]:
        satisfaction_data[sat] = satisfaction_data.get(sat, 0) + 1
    
    if satisfaction_data:
        plt.figure(figsize=(10, 6))
        plt.bar(list(satisfaction_data.keys()), list(satisfaction_data.values()), color='#007bff')
        plt.title('Student Satisfaction Levels')
        plt.ylabel('Count')
        plt.xlabel('Satisfaction Level')
        plt.xticks(rotation=45)
        
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        charts['satisfaction'] = base64.b64encode(img.getvalue()).decode()
        plt.close()
    
    return charts

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# Download routes
@app.route('/admin/download/students/csv')
def download_students_csv():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    students = StudentFeedback.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    header = [
        'ID', 'Name', 'Class', 'Email', 'Phone',
        'Satisfaction', 'Internet Access', 'Technical Issues', 'Interactive', 'Comfortable Asking',
        'Teaching Materials', 'Assignments Manageable', 'Preference', 'Timely Feedback', 'Recommend',
        'Challenge 1', 'Challenge 2', 'Improvement 1', 'Improvement 2', 'Benefit 1',
        'Benefit 2', 'Experience', 'Support', 'Additional Comments', 'Future Suggestions',
        'Sentiment Polarity', 'Sentiment Subjectivity', 'Sentiment Label', 'Created At'
    ]
    writer.writerow(header)
    
    # Write data
    for student in students:
        row = [
            student.id, student.student_name, student.student_class, student.student_email, student.student_phone,
            student.q1, student.q2, student.q3, student.q4, student.q5,
            student.q6, student.q7, student.q8, student.q9, student.q10,
            student.open_q1, student.open_q2, student.open_q3, student.open_q4, student.open_q5,
            student.open_q6, student.open_q7, student.open_q8, student.open_q9, student.open_q10,
            student.sentiment_polarity, student.sentiment_subjectivity, student.sentiment_label,
            student.created_at.strftime('%Y-%m-%d %H:%M:%S') if student.created_at else ''
        ]
        writer.writerow(row)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=student_feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response

@app.route('/admin/download/teachers/csv')
def download_teachers_csv():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    teachers = TeacherFeedback.query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    header = [
        'ID', 'Name', 'Subject', 'Email', 'Phone',
        'Effectiveness', 'Resources Access', 'Technical Issues', 'Student Engagement', 'Comfortable with Tools',
        'Student Participation', 'Assessments Manageable', 'Preference', 'Provide Feedback', 'Recommend',
        'Challenge 1', 'Challenge 2', 'Improvement 1', 'Improvement 2', 'Benefit 1',
        'Benefit 2', 'Experience', 'Support', 'Additional Comments', 'Future Suggestions',
        'Sentiment Polarity', 'Sentiment Subjectivity', 'Sentiment Label', 'Created At'
    ]
    writer.writerow(header)
    
    # Write data
    for teacher in teachers:
        row = [
            teacher.id, teacher.teacher_name, teacher.teacher_subject, teacher.teacher_email, teacher.teacher_phone,
            teacher.q1, teacher.q2, teacher.q3, teacher.q4, teacher.q5,
            teacher.q6, teacher.q7, teacher.q8, teacher.q9, teacher.q10,
            teacher.open_q1, teacher.open_q2, teacher.open_q3, teacher.open_q4, teacher.open_q5,
            teacher.open_q6, teacher.open_q7, teacher.open_q8, teacher.open_q9, teacher.open_q10,
            teacher.sentiment_polarity, teacher.sentiment_subjectivity, teacher.sentiment_label,
            teacher.created_at.strftime('%Y-%m-%d %H:%M:%S') if teacher.created_at else ''
        ]
        writer.writerow(row)
    
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=teacher_feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response

@app.route('/admin/download/students/json')
def download_students_json():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    students = StudentFeedback.query.all()
    data = []
    
    for student in students:
        student_data = {
            'id': student.id,
            'personal_info': {
                'name': student.student_name,
                'class': student.student_class,
                'email': student.student_email,
                'phone': student.student_phone
            },
            'closed_questions': {
                'satisfaction': student.q1,
                'internet_access': student.q2,
                'technical_issues': student.q3,
                'interactive': student.q4,
                'comfortable_asking': student.q5,
                'teaching_materials': student.q6,
                'assignments_manageable': student.q7,
                'preference': student.q8,
                'timely_feedback': student.q9,
                'recommend': student.q10
            },
            'open_questions': {
                'challenge_1': student.open_q1,
                'challenge_2': student.open_q2,
                'improvement_1': student.open_q3,
                'improvement_2': student.open_q4,
                'benefit_1': student.open_q5,
                'benefit_2': student.open_q6,
                'experience': student.open_q7,
                'support': student.open_q8,
                'additional_comments': student.open_q9,
                'future_suggestions': student.open_q10
            },
            'sentiment_analysis': {
                'polarity': student.sentiment_polarity,
                'subjectivity': student.sentiment_subjectivity,
                'label': student.sentiment_label
            },
            'created_at': student.created_at.isoformat() if student.created_at else None
        }
        data.append(student_data)
    
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = f'attachment; filename=student_feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    return response

@app.route('/admin/download/teachers/json')
def download_teachers_json():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    teachers = TeacherFeedback.query.all()
    data = []
    
    for teacher in teachers:
        teacher_data = {
            'id': teacher.id,
            'personal_info': {
                'name': teacher.teacher_name,
                'subject': teacher.teacher_subject,
                'email': teacher.teacher_email,
                'phone': teacher.teacher_phone
            },
            'closed_questions': {
                'effectiveness': teacher.q1,
                'resources_access': teacher.q2,
                'technical_issues': teacher.q3,
                'student_engagement': teacher.q4,
                'comfortable_with_tools': teacher.q5,
                'student_participation': teacher.q6,
                'assessments_manageable': teacher.q7,
                'preference': teacher.q8,
                'provide_feedback': teacher.q9,
                'recommend': teacher.q10
            },
            'open_questions': {
                'challenge_1': teacher.open_q1,
                'challenge_2': teacher.open_q2,
                'improvement_1': teacher.open_q3,
                'improvement_2': teacher.open_q4,
                'benefit_1': teacher.open_q5,
                'benefit_2': teacher.open_q6,
                'experience': teacher.open_q7,
                'support': teacher.open_q8,
                'additional_comments': teacher.open_q9,
                'future_suggestions': teacher.open_q10
            },
            'sentiment_analysis': {
                'polarity': teacher.sentiment_polarity,
                'subjectivity': teacher.sentiment_subjectivity,
                'label': teacher.sentiment_label
            },
            'created_at': teacher.created_at.isoformat() if teacher.created_at else None
        }
        data.append(teacher_data)
    
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = f'attachment; filename=teacher_feedback_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Get port from environment variable for deployment or use 5000 for local
    import os
    port = int(os.environ.get('PORT', 5000))
    
    # Use debug=False for production deployment
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port) 