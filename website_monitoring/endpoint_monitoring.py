import requests
import smtplib
import os
import paramiko
import digitalocean
import time

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
DIGITAL_OCEAN_TOKEN = os.environ.get('DIGITAL_OCEAN_TOKEN')

def send_notification_email(msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f'Subject: The server is down!\n\n{msg}\n\n- Your monitoring tool.'
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
        
def restart_container():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('143.110.212.172', port=22, username='root', key_filename="/Users/ilemo/.ssh/id_rsa")
    stdin, stdout, stderr = ssh.exec_command('docker start f31735041cdd')
    print(stdout.readlines())
    print(stderr.readlines())
    ssh.close()
    print('The server is up and running again!')
    
    

try:
    r = requests.get('http://143.110.212.b172:8080')

    status_code = r.status_code

    if status_code == 200:
        print(f'The server is up and running with status code: {status_code}')
    else: 
        print(f'The server is down, status code: {status_code}')
        # Send an email to the admin
        send_notification_email(f'The server is down, please take a look. We have a status code of: ' + str(status_code) + '')
        
    # SSH into the server and restart the nginx container
    restart_container()
    
except Exception as e:
    print(f"Connection error: {e}")
    status_code = "200:OK"
    # Send an email to the admin for the connection error
    send_notification_email(f"The server is down, please take a look. We have a connection error: ' + {e}.")
    
    # Restart the server using the DigitalOcean API
    manager = digitalocean.Manager(token=DIGITAL_OCEAN_TOKEN)
    droplet_id = '395468824'
    my_droplet = manager.get_droplet(droplet_id)
    print("REBOOTING THE SERVER.............")
    my_droplet.reboot()
    
    #restart_container
    while True:
        actions = my_droplet.get_actions()
        for action in actions:
            action.load()
    #    Once it shows "completed", droplet is up and running
            print(action.status)
            if action.status == "completed":
               restart_container()
               send_notification_email(f"The server is up and running again! We have a status code of: {status_code}")
               break
        
        
    
    
    
      
    