from prefect import flow, task
import subprocess
import runpy
import os
from datetime import timedelta
from prefect.client.schemas.schedules import CronSchedule
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", "config/.env"), override=True)
print("✅ Loaded CLIENT_ID:", os.getenv("KROGER_CLIENT_ID"))
print("✅ Loaded CLIENT_SECRET:", os.getenv("KROGER_CLIENT_SECRET"))




@task
def run_command(command: str):
    """
    Runs a shell command and waits for it to finish.
    Raises an error if the command fails.
    """
    print(f"Running command: {command}")
    env = os.environ.copy()
    result = subprocess.run(command, shell=True, capture_output=True, text=True, env=env)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Command failed: {command}")

@task
def run_python_file(file_path: str):
    """
    Runs a Python file directly, as if imported and executed.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    print(f"🔹 Running Python file directly: {file_path}")
    runpy.run_path(file_path, run_name="__main__")
    print("✅ Python file executed successfully.")

@flow
def orchestrate_command():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    ingestion_path = os.path.join(project_root, "ingestion", "latest_file.py")
    load_path = os.path.join(project_root, "load", "load.py")

    run_command(f"python '{ingestion_path}' milk eggs orange")
    run_python_file(load_path)

if __name__ == "__main__":
    orchestrate_command()  # Immediate run
    # ✅ Create and register a Prefect deployment
    orchestrate_command.serve(
        name="daily-orchestration",
        schedule=CronSchedule(cron="0 8 * * *", timezone="America/Los_Angeles"),
        description="Daily orchestration of ingestion + load pipeline",
        tags=["daily", "pipeline"],
    )
