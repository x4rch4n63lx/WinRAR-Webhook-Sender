# ===================================================================================
# Created By     : x_4rch4n63l_x
# Created On     : 6/2/2025 - 4:27PM
# Script Purpose : Send a file along with a preset message to a Discord webhook.
# Description    : 
#                   This script uploads a specified file to a Discord webhook URL,
#                   sends a customized message, and provides a colored terminal
#                   interface with status updates, runtime tracking, and error handling.
#                   It supports Windows console colors via colorama and includes a
#                   spinner animation and countdown timer for user feedback.
#
# Features       : 
#                   - Validates Discord webhook URL before sending
#                   - Sends file and message as webhook payload
#                   - Displays sending progress with spinner and countdown timer
#                   - Color-coded console output for statuses and errors
#                   - Tracks and displays total data sent and runtime duration
#
# Requirements   : 
#                   - Python 3.x
#                   - requests module
#                   - colorama module
#
# Usage Notes    : 
#                   - Set the webhook_url and file_path in the CONFIG section.
#                   - Use raw strings (r"") or double backslashes (\\) for Windows paths.
#                   - Edit the `payload` dictionary to change the bot username, message content,
#                     title, login info, and file password.
#                   - Ensure the file exists and webhook is reachable before running.
# ===================================================================================
import requests
import time
import os
import sys
from colorama import just_fix_windows_console, Fore, Style

# Initialize colorama for Windows terminal color support
just_fix_windows_console()

# --- CONFIG ---
# Set your Discord webhook URL here. Make sure it is valid.
# CHANGE HERE: Replace with your actual Discord webhook.
webhook_url = ""

# Set the full path to the file you want to send.
# Use raw strings (r"...") or double backslashes (\\) for Windows paths.
# CHANGE HERE: Replace with your full .rar file path.
file_path = r"C:\Users\YourName\Downloads\WinRARFileName.rar"

# Webhook payload content setup
# CHANGE HERE: You can customize the message below:
# - username: the bot name shown in Discord
# - content: the message body sent with the file
#   Replace TITLE-HERE, root, PASSWORD, WinRAR password, and USERNAME-HERE as needed.
payload = {
    "username": "File Sender Bot",  # CHANGE HERE: This is the webhook bot's display name
    "content": (
        "**TITLE-HERE**\n"               # CHANGE HERE: Add your custom title
        "🔐 **Login Details:**\n"
        "`Username:` root\n"             # CHANGE HERE: Set your login username
        "`Password:` (default or as provided)\n"  # CHANGE HERE: Set login password
        "📦 **WinRAR Password:** `PUT-PASSWORD-HERE`\n"   # CHANGE HERE: Add your archive password
        "👑 **Creator:** PUT-NAME-HERE"  # CHANGE HERE: Set your name or tag
    )
}

spinner = ['|', '/', '-', '\\']
start_time = time.time()
sent_count = 0
failed_count = 0
total_data_sent = 0

def spinner_animation(message, duration=3):
    total_frames = int(duration / 0.1)
    for i in range(total_frames):
        spin = spinner[i % len(spinner)]
        print(f"\r{Fore.CYAN}{message} {spin}", end="", flush=True)
        time.sleep(0.1)
    print("\r" + " " * 50, end="\r")  # Clear line

def type_text(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def countdown_timer(seconds):
    for remaining in range(seconds, 0, -1):
        spin = spinner[(seconds - remaining) % len(spinner)]
        mins, secs = divmod(remaining, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"\r{Fore.WHITE}⏳ Sending in: {timer} {spin}", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 50, end="\r")  # Clear line after countdown

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def format_runtime(seconds):
    mins, secs = divmod(int(seconds), 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

def format_bytes_to_mb(bytes_size):
    return bytes_size / (1024 * 1024)

def print_status(sent, failed, total_bytes, last_status):
    clear_console()
    print(Fore.CYAN + "=" * 60)
    type_text(Fore.CYAN + "🚀 WinRAR File Sender")
    print(Fore.CYAN + "=" * 60)
    type_text(Fore.CYAN + f"📁 File to send: {file_path}")
    type_text(Fore.CYAN + f"📤 Status: {'Sent' if sent else 'Pending'}")
    type_text(Fore.CYAN + f"✅ Successes: {sent_count}")
    type_text(Fore.CYAN + f"❌ Failures: {failed_count}")
    type_text(Fore.CYAN + f"💾 Total Data Sent: {format_bytes_to_mb(total_bytes):.2f} MB")
    type_text(Fore.CYAN + f"📡 Last Webhook Status: {last_status}")
    elapsed = time.time() - start_time
    type_text(Fore.CYAN + f"⏱️ Runtime: {format_runtime(elapsed)}")
    print(Fore.CYAN + "=" * 60)
    print(Style.RESET_ALL)

def validate_webhook(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception:
        return False

def send_file():
    global sent_count, failed_count, total_data_sent

    print_status(False, failed_count, total_data_sent, "N/A")

    if not os.path.isfile(file_path):
        print(Fore.RED + f"❌ File not found: {file_path}")
        return False

    print(Fore.YELLOW + "[*] Validating webhook URL...")
    if not validate_webhook(webhook_url):
        print(Fore.RED + "❌ Invalid or unreachable webhook URL!")
        return False
    print(Fore.GREEN + "[+] Webhook URL is valid.")

    countdown_timer(3)

    print(Fore.YELLOW + "[*] Sending file and message to webhook...")
    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(webhook_url, data=payload, files=files)

        if response.status_code in (200, 204):
            sent_count += 1
            total_data_sent += os.path.getsize(file_path)
            print(Fore.GREEN + "✅ File and message sent successfully!")
            print_status(True, failed_count, total_data_sent, response.status_code)
            return True
        else:
            failed_count += 1
            print(Fore.RED + f"❌ Failed to send. Status: {response.status_code}")
            print(Fore.YELLOW + f"Response: {response.text}")
            print_status(False, failed_count, total_data_sent, response.status_code)
            return False
    except Exception as e:
        failed_count += 1
        print(Fore.RED + f"❌ Exception occurred: {str(e)}")
        print_status(False, failed_count, total_data_sent, "Exception")
        return False

if __name__ == "__main__":
    clear_console()
    type_text(Fore.CYAN + "🚀 Starting WinRAR File Sender...\n", 0.03)
    send_file()
    print(Fore.CYAN + "=" * 60)
    input("Press Enter to exit...")
