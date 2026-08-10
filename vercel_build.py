"""
Vercel Build Script for Django
This runs during deployment
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"▶ {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed!")
        print(f"Exit code: {e.returncode}")
        print(f"Output: {e.output}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Main build process"""
    print("\n" + "="*50)
    print("🚀 Starting Vercel Build Process")
    print("="*50)
    
    # Step 1: Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing dependencies"
    ):
        sys.exit(1)
    
    # Step 2: Collect static files
    if not run_command(
        "python manage.py collectstatic --noinput --clear",
        "Collecting static files"
    ):
        print("⚠️ Warning: Static files collection failed (may be okay)")
    
    # Step 3: Run migrations
    if not run_command(
        "python manage.py migrate --noinput",
        "Running database migrations"
    ):
        print("⚠️ Warning: Migrations failed (may be okay for first deploy)")
    
    print("\n" + "="*50)
    print("✅ Build Process Complete!")
    print("="*50)

if __name__ == "__main__":
    main()
