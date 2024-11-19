from datetime import timedelta
from flask import current_app as app
from flask import render_template
from sqlalchemy import or_
from tools.workers import celery
from models import *
from celery.schedules import crontab
from tools.mailer import send_email
import io, os, csv


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=18, minute=00), send_daily_mail.s(), name="Daily reminder")
    sender.add_periodic_task(40, monthly_report.s(), name="Monthly reminder")
    # sender.add_periodic_task(crontab(day_of_month=1), monthly_report.s(), name="Sending monthly report")
    # crontab: daily: hour&minute, weekly: day_of_week = which day(1/2/...), monthly: day_of_month: which date in a month(1/2/..)
    #for every ten seconds: seconds='*/10'


#Daily reminders to the ones who have not logged in last 24 hours
@celery.task
def send_daily_mail():
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    
    users = User.query.outerjoin(ServiceRequest, ServiceRequest.professional_id == User.id
        ).filter(User.role == 'professional', or_( User.lastLoggedIn < twenty_four_hours_ago,  
                                            ServiceRequest.service_status == 'requested')).all()
    message = "You are getting this email because: Either you have not logged in for the last 24 hours or having pending service requests."
    count=0
    for user in users:
        service_requests = ServiceRequest.query.filter_by(professional_id=user.id, 
                                                          service_status='requested').all()
        html = render_template("daily_email.html", user=user, message=message, service_requests=service_requests)
        send_email(user.email, "Daily reminder from A-Z", html)
        count +=1
    return f"Reminder sent to {count} professionals"
    
@celery.task
def monthly_report():
    users= User.query.filter_by(role="customer").all()
    one_month_ago = datetime.now() - timedelta(days=10)
    
    for user in users:
        user_services = ServiceRequest.query.filter_by(customer_id=user.id
                        ).filter(ServiceRequest.date_of_request < one_month_ago
                                 ).filter(ServiceRequest.service_status != "rejected" ).all()
        service_details = []
        
        for service in user_services:
            service_details.append({
                "service_name": service.service.name,
                "category": service.service.category.name,
                "date_of_request": service.date_of_request,
                "status": service.service_status,
                "id": service.id
            })
            
        html = render_template("monthly_report.html", user=user, services=service_details)
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