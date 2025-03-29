from datetime import datetime
from models import db

class APILog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    endpoint = db.Column(db.String(200))
    method = db.Column(db.String(10))
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    response_code = db.Column(db.Integer)
    request_data = db.Column(db.Text)

def log_api_call(endpoint, method, ip, user_agent, response_code, request_data):
    log = APILog(
        endpoint=endpoint,
        method=method,
        ip_address=ip,
        user_agent=user_agent,
        response_code=response_code,
        request_data=str(request_data)
    )
    db.session.add(log)
    db.session.commit() 