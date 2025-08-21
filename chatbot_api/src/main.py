from chatbot_api.main_app import run_app
import uvicorn

app = run_app()

if __name__ == "__main__":
    print("API server is loaded.")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
