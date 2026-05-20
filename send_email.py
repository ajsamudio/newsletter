import json, subprocess, sys
from datetime import date
from pathlib import Path

today = date.today().isoformat()
html_path = Path(f"archive/{today}.html")
if not html_path.exists():
    print(f"ERROR: {html_path} not found")
    sys.exit(1)

payload = json.dumps({
    "from": "AJ's Brief <onboarding@resend.dev>",
    "to": "antsamudio99@gmail.com",
    "subject": f"AJ's Brief — {today}",
    "html": html_path.read_text(encoding="utf-8")
})

r = subprocess.run(
    ["curl", "-s", "-X", "POST", "https://api.resend.com/emails",
     "-H", "Authorization: Bearer re_AbZCHCCA_GagtaezLQjjrv3ZprHivM5XM",
     "-H", "Content-Type: application/json",
     "-d", payload],
    capture_output=True, text=True
)
print(r.stdout)
if '"id"' in r.stdout:
    print(f"Email sent to antsamudio99@gmail.com")
else:
    print("Send may have failed - check response above")
