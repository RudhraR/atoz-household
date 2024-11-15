from datetime import timedelta
from flask import current_app as app
from flask import render_template
from tools.workers import celery
from models import *
from celery.schedules import crontab
from tools.mailer import send_email
import io, os, csv


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(crontab(hour=10, minute=00), send_daily_mail.s(), name="Send email every 30 secs")
    sender.add_periodic_task(30, monthly_report.s(), name="Send monthly report")
    # crontab: daily: hour&minute, weekly: day_of_week = which day(1/2/...), monthly: day_of_month: which date in a month(1/2/..)
    #for every ten seconds: seconds='*/10'

@celery.task
def add(x,y):
    return (x+y)  

@celery.task
def sendHello(userId):
    user = User.query.filter_by(id=userId).first()
    return "Hi " + user.username

@celery.task
def sendMail():
    users = User.query.all()
    for user in users:
        print(f"Sending email to user {user.username}")
    return "Email sent successfully"

#Daily reminders to the ones who have not logged in last 24 hours
@celery.task
def send_daily_mail():
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    users = User.query.filter(User.lastLoggedIn < twenty_four_hours_ago).filter(User.role == 'professional').all()
    message = "Hey.. You are getting this email because you have not logged in last 24 hours"
    count=0
    for user in users:
        html = render_template("daily_email.html", user=user, message=message)
        send_email(user.email, "Daily Reminder: Inactive user", html)
        count +=1
    return f"Reminder sent to {count} inactive users"
    
@celery.task
def monthly_report():
    users= User.query.filter_by(role="customer").all()
    one_month_ago = datetime.now() - timedelta(days=10)
    
    for user in users:
        user_services = ServiceRequest.query.filter_by(customer_id=user.id
                        ).filter(ServiceRequest.date_of_request < one_month_ago
                                 ).filter(ServiceRequest.service_status == "completed").all()
        service_details = []
        total_amount_spent = 0
        
        for service in user_services:
            service_details.append({
                "service_name": service.service.name,
                "price": service.service.price,
                "date_of_request": service.date_of_request
            })
            total_amount_spent += service.service.price
            
        html = render_template("monthly_report.html", user=user, services=service_details, total_amount_spent=total_amount_spent)
        send_email(user.email, "Monthly Report", html)
        
    return f"Monthly report sent to {len(users)} users" 

#Send monthly report csv file
@celery.task
def generate_csv_report():
    service_requests = ServiceRequest.query.all()
    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['ID', 'Service Name', 'Category', 'Status', 'Date Booked', 'Date Closed', 'Assigned Professional', 'Customer Name'])  # Header row
    for request in service_requests:
        csv_writer.writerow([request.id, request.service.name, request.service.category.name, 
                             request.service_status, request.date_of_request.strftime('%Y-%m-%d'), 
                             request.date_of_completion.strftime('%Y-%m-%d'), 
                             request.professional.username, request.customer.username])
    
     # Save CSV to file system
    output_path = os.path.join(app.config['CSV_REPORT_EXPORT_FOLDER'], f'service_requests_{datetime.now().strftime("%Y-%m-%d")}.csv') 
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        file.write(csv_buffer.getvalue())

    return output_path  