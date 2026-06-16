import os
import smtplib
import re
import mimetypes
from email.message import EmailMessage
from email.utils import make_msgid
import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flash_messages'

@app.route('/preview')
def preview():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'email_template.html')

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        smtp_host = request.form.get('smtp_host')
        smtp_port = int(request.form.get('smtp_port', 587))
        smtp_user = request.form.get('smtp_user')
        smtp_pass = request.form.get('smtp_pass')
        email_subject = request.form.get('email_subject')
        html_template = request.form.get('html_template')
        
        file = request.files.get('csv_file')
        
        if not file or file.filename == '':
            flash('No file uploaded', 'error')
            return redirect(url_for('index'))
            
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        except Exception as e:
            flash(f'Error reading file: {str(e)}', 'error')
            return redirect(url_for('index'))
            
        df = df.fillna('')
        
        success_count = 0
        error_count = 0
        
        local_images = []
        def replace_img_src(match):
            src = match.group(1)
            if not src.startswith(('http://', 'https://', 'data:')) and os.path.isfile(src):
                cid = make_msgid()
                local_images.append((src, cid))
                return f'src="cid:{cid[1:-1]}"'
            return match.group(0)
            
        html_template_modified = re.sub(r'src="([^"]+)"', replace_img_src, html_template)
        
        try:
            # Connect to SMTP
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            
            for idx, row in df.iterrows():
                # Flexible column names (case-insensitive search)
                cols = {c.lower(): c for c in df.columns}
                
                email_col = next((c for c in cols if 'email' in c), None)
                if not email_col:
                    continue
                    
                to_email = str(row[cols[email_col]]).strip()
                if not to_email:
                    continue
                
                # Render template
                rendered_html = html_template_modified
                
                # Replace $User with First Name if available
                first_name_col = next((c for c in cols if 'first' in c or 'name' in c), None)
                if first_name_col:
                    first_name = str(row[cols[first_name_col]]).strip()
                    rendered_html = rendered_html.replace('$User', first_name)
                else:
                    rendered_html = rendered_html.replace('$User', 'there')
                    
                # [PHONE NUMBER] is the fixed company number — already set in the template
                
                # Replace other potential merge tags from columns like {{Column Name}}
                for col in df.columns:
                    val = str(row[col])
                    rendered_html = rendered_html.replace(f"{{{{{col}}}}}", val)
                
                msg = EmailMessage()
                msg['Subject'] = email_subject
                msg['From'] = smtp_user
                msg['To'] = to_email
                msg.set_content("Please view this email in an HTML compatible client.")
                msg.add_alternative(rendered_html, subtype='html')
                
                if local_images:
                    html_part = msg.get_payload()[1]
                    for img_path, cid in local_images:
                        with open(img_path, 'rb') as img:
                            img_data = img.read()
                            mime_guess = mimetypes.guess_type(img_path)[0]
                            if mime_guess:
                                maintype, subtype = mime_guess.split('/')
                            else:
                                maintype, subtype = 'image', 'jpeg'
                            html_part.add_related(img_data, maintype=maintype, subtype=subtype, cid=cid)
                
                try:
                    server.send_message(msg)
                    success_count += 1
                except Exception as e:
                    print(f"Failed to send to {to_email}: {e}")
                    error_count += 1
                    
            server.quit()
            
            flash(f'Campaign sent successfully! {success_count} emails sent. {error_count} failed.', 'success')
            
        except Exception as e:
            flash(f'SMTP Error: {str(e)}', 'error')
            
        return redirect(url_for('index'))
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
