from TitleShare import create_app
from TitleShare.scheduler import scheduler
app = create_app()

if __name__ == "__main__":
    app.run(debug=False)