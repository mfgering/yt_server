from app import app
import datetime
app.start_time = datetime.datetime.utcnow()
if __name__ == "__main__":
    app.run()