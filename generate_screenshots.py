import os
import sys
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    python_exe = os.path.join(base_dir, '.venv', 'Scripts', 'python.exe')
    manage_py = os.path.join(base_dir, 'manage.py')

    print("Starting Django development server on port 8000...")
    server_proc = subprocess.Popen(
        [python_exe, manage_py, 'runserver', '127.0.0.1:8000', '--noreload'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=base_dir
    )
    time.sleep(3)

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1280,900")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_path):
        chrome_options.binary_location = chrome_path

    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Failed to initialize Chrome: {e}")
        from selenium.webdriver.edge.options import Options as EdgeOptions
        edge_options = EdgeOptions()
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--window-size=1280,900")
        edge_options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        driver = webdriver.Edge(options=edge_options)

    try:
        # 1. Take 03-admin-site.png
        print("Navigating to admin login...")
        driver.set_window_size(1280, 900)
        driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
        time.sleep(1)

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("admin")
        password_input.send_keys("adminpassword123")
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(2)

        print("Saving 03-admin-site.png...")
        admin_screenshot_path = os.path.join(base_dir, "03-admin-site.png")
        driver.save_screenshot(admin_screenshot_path)
        print(f"Saved: {admin_screenshot_path}")

        # 2. Take 07-final.png
        print("Logging in as student1...")
        driver.get("http://127.0.0.1:8000/onlinecourse/login/")
        time.sleep(1)

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys("student1")
        password_input.send_keys("studentpassword123")
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

        # Dynamically query latest submission id
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
        django.setup()
        from onlinecourse.models import Submission
        latest_sub = Submission.objects.order_by('-id').first()
        sub_id = latest_sub.id if latest_sub else 1

        print(f"Navigating to exam result page for submission {sub_id}...")
        driver.get(f"http://127.0.0.1:8000/onlinecourse/course/1/submission/{sub_id}/result/")
        time.sleep(2)

        # Set window size to capture FULL page from top to bottom
        total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
        print(f"Full page height: {total_height}")
        driver.set_window_size(1280, max(total_height + 150, 1800))
        time.sleep(1)

        final_screenshot_path = os.path.join(base_dir, "07-final.png")
        driver.save_screenshot(final_screenshot_path)
        print(f"Saved: {final_screenshot_path}")

    finally:
        driver.quit()
        server_proc.terminate()
        server_proc.kill()
        print("Server stopped.")

if __name__ == '__main__':
    main()
