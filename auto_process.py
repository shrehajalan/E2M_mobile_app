from celery import Celery
from celery.schedules import crontab
from datetime import datetime, timedelta
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import models
from models import EmployeeJobDetailsModel,EmployeeAttendanceModel

#celery -A auto_process worker --loglevel=info --concurrency=2
#celery -A auto_process beat --loglevel=info

# Initialize Celery
celery_app = Celery('tasks', broker='redis://localhost:6379/0')
celery_app.conf.timezone = 'Asia/Kolkata'

# Global MySQL Connection (for fetching databases)
DB_URL = "mysql+pymysql://root:password123@localhost:3306/mysql"
mysql_engine = create_engine(DB_URL)  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

def get_resource_databases():
    inspector = inspect(mysql_engine)#Creates an inspector object to retrieve metadata about the database
    all_databases = inspector.get_schema_names()
    resource_databases = [db for db in all_databases if db.startswith("resource_db_")]
    return resource_databases

@celery_app.task
def process_carry_forward_leaves():
    today = datetime.today()
    tomorrow = today + timedelta(days = 1)

    if tomorrow.month != today.month :
        resource_dbs = get_resource_databases()
        for db_name in resource_dbs:
    
            individual_db_url = f"mysql+pymysql://root:password123@localhost:3306/{db_name}"
            db_engine = create_engine(individual_db_url)
            Session = sessionmaker(bind=db_engine)
            db = Session()
            last_execution = db.query(models.SystemLogs).filter_by(task_name="process_carry_forward_leaves").first()

            try:
                employees = db.query(EmployeeJobDetailsModel).all()
                for employee in employees:
                    attendance_count  = db.query(EmployeeAttendanceModel).filter(EmployeeAttendanceModel.employeeId == employee.employeeId,
                                    EmployeeAttendanceModel.attendanceDate.between(
                                    datetime.today().replace(day=1), datetime.today())).count()

                    total_days = datetime.today().day  # Days completed in the month
                    days_absent = total_days - attendance_count

                    if days_absent >= (employee.leavesPerMonth + employee.leavesCarriedForward):
                        employee.leavesCarriedForward = 0
                    else:
                        employee.leavesCarriedForward = (employee.leavesPerMonth + employee.leavesCarriedForward) - days_absent
                    db.commit()

            except Exception as e:
                print(f"Error in processing {db_name}: {e}")
            
            finally:
                db.close()

# Celery Beat Scheduler (Runs at 12:00 AM on the last day of the month)
celery_app.conf.beat_schedule = {
    'carry-forward-leaves': {
        'task': 'tasks.process_carry_forward_leaves',
        'schedule': crontab(hour=0, minute=0, day_of_month='last'),  # Runs on last day of the month
    },
}
