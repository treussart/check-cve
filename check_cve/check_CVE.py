import sqlite3
import argparse
import smtplib
from email.mime.text import MIMEText
from CVESearch import CVESearch
from CheckVersions import CheckVersions
import os


def check_white_list(cve_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/whitelist-CVE.db")
    c = conn.cursor()
    for row in c.execute("SELECT * FROM CVE"):
        if row[1] == cve_name:
            return True
    return False


def send_email(from_address, to_address, cve_new, nbr):
    msg = MIMEText(
        "<html><head></head><body>" + str(cve_new) + "</body></html>", "html"
    )
    msg["Subject"] = "%s new CVE for services" % nbr
    msg["From"] = from_address
    msg["To"] = to_address
    # Send the message via our own SMTP server.
    s = smtplib.SMTP("localhost")
    s.send_message(msg)
    s.quit()


def check_cve():
    """Main function."""
    current_path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--username", help="the username of the SSH connection", default="matthieu"
    )
    parser.add_argument(
        "--private_key",
        help="the private key of the SSH connection",
        default="matthieu@treussart.com_rsa",
    )
    parser.add_argument(
        "--from_address",
        help="The address who send the email",
        default="cve@treussart.com",
    )
    parser.add_argument(
        "--to_address",
        help="The address who receive the email",
        default="matthieu@treussart.com",
    )
    args = parser.parse_args()
    username = args.username
    private_key = f"{current_path}/../.ssh/{args.private_key}"
    from_address = args.from_address
    to_address = args.to_address
    list_new_cve = ""
    nbr = 0
    cv = CheckVersions()
    cpe_list = cv.check_versions(username=username, private_key=private_key)
    for cpe in cpe_list:
        new = False
        list_new_cve_rows = ""
        cve = CVESearch()
        cves_json = cve.cvefor(cpe)
        for i, val in enumerate(cves_json):
            if not check_white_list(cves_json[i]["id"]):
                # print(cves_json[i]['id'])
                new = True
                nbr += 1
                list_new_cve_rows = f"{list_new_cve_rows}<h4>{cves_json[i]['id']} :</h4>{cves_json[i]['summary']}<br/>"
        if new:
            # print(cpe)
            list_new_cve += f"<h2>{cpe}</h2><br/>{list_new_cve_rows}"
    if list_new_cve:
        print("send email")
        send_email(from_address, to_address, list_new_cve, nbr)


if __name__ == "__main__":
    check_cve()
