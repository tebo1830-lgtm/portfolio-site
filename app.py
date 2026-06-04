from flask import Flask, render_template, send_file, abort, request
from pathlib import Path
import os

app = Flask(__name__)

# -------- HELPER FUNCTIONS --------
def is_local_access():
    """Check if the request is from a local network or localhost"""
    remote_addr = request.remote_addr
    # Localhost
    if remote_addr in ('127.0.0.1', '::1', 'localhost'):
        return True
    # Private IP ranges
    if remote_addr.startswith('192.168.') or remote_addr.startswith('10.') or remote_addr.startswith('172.'):
        return True
    return False

# -------- COURSE MATERIALS PATHS --------
ONEDRIVE_BASE_PATH = r"C:\Users\User\OneDrive - BYU-Pathway Worldwide\BYU"

# -------- COURSE INFORMATION --------
COURSES = {
    "pc-hardware": {
        "title": "PC Hardware Technician",
        "certificate": "Technical Support Engineer",
        "description": "Learn the fundamentals of PC hardware, including components, assembly, troubleshooting, and maintenance.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT102 PC Hardware Technician",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBJ4I2SAS8mTKvJkgPxsLSxAWQIt5Dcvj7yeDLKbM806jw?e=BxTziD"
    },
    "networking-fundamentals": {
        "title": "Networking Fundamentals",
        "certificate": "Technical Support Engineer",
        "description": "Introduction to networking concepts, protocols, and network infrastructure basics.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT255 Networking Fundamentals",
        "onedrive_link": ""  # Add your OneDrive share link here
    },
    "cloud-server": {
        "title": "Cloud Server Administration",
        "certificate": "Technical Support Engineer",
        "description": "Learn to administer cloud-based servers and cloud infrastructure platforms.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT235 - Cloud server administration",
        "onedrive_link": ""  # Add your OneDrive share link here
    },
    "intro-it": {
        "title": "Introduction to Information Technology",
        "certificate": "Technical Support Engineer",
        "description": "Foundational concepts in Information Technology and the IT industry.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT125 Intro to Information Technology",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBvS-sSsknIT7HYo82_wUM3AWQeBr-IgWkN6aFSLJvAgnQ?e=HQBiMx"
    },
    "applied-programming": {
        "title": "Foundations of Applied Programming",
        "certificate": "Technical Support Engineer",
        "description": "Introduction to programming fundamentals and software development principles.",
        "url": "https://www.byupathway.edu",
        "local_folder": "CS104 Foundations of Applied Programming",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgCKPC7nHTdzR7HjE7DKILvjAaqeCiO75vZojPBQkm2qTUI?e=kuNrwn"
    },
    "database-design": {
        "title": "Database Design and Analysis",
        "certificate": "IT Professional",
        "description": "Learn database design principles, SQL, and data management.",
        "url": "https://www.byupathway.edu"
    },
    "linux-fundamentals": {
        "title": "Linux Fundamentals",
        "certificate": "IT Professional",
        "description": "Master Linux operating system basics, commands, and system administration.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT210 Linux Fundamentals",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgDO7_2OGwHdT4AE1LKJwsZKAXfPNe7Iia1X1O6aF3LaWK8?e=LaidyB"
    },
    "cloud-computing": {
        "title": "Cloud Computing Essentials",
        "certificate": "IT Professional",
        "description": "Core concepts of cloud computing, deployment models, and cloud services.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 160 Cloud Computing Essentials",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBdYk-rqyVWRoxBxn3QkSe8ASeqIPGKTn7aunzxw6IRobw?e=dRUJtm"
    },
    "network-config": {
        "title": "Network Configuration & Design",
        "certificate": "IT Professional",
        "description": "Network design, configuration, and best practices for enterprise networks.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 350 Network Configuration & Design",
        "onedrive_link": ""  # Add your OneDrive share link here
    },
    "cybersecurity-foundations": {
        "title": "Cybersecurity Foundations",
        "certificate": "IT Professional",
        "description": "Introduction to cybersecurity principles, threats, and defense mechanisms.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 312 Cybersecurity",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgDuJxwBOzdVQLmc7F2ik_8qAWfFsr_rPVC-jzyRsPTMBQc?e=DcBF87"
    },
    "business-intelligence": {
        "title": "Business Intelligence Systems",
        "certificate": "System Administration",
        "description": "Learn to work with BI tools, data analytics, and business intelligence platforms.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 340 Business Intelligence Systems",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBx73_z5374T4NCwCjIfDUbAV1AqkiURxqSgcuv2UVjkos?e=1i0DKB"
    },
    "advanced-linux": {
        "title": "Advanced Linux",
        "certificate": "System Administration",
        "description": "Advanced Linux system administration, scripting, and performance tuning.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 370 Advanced Linux",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBbUVpk1e3tRYhHHvJlM3C1AUYMZLzHptx1ATb5wmqtqeY?e=SxJZ7a"
    },
    "scripting-security": {
        "title": "Scripting for Security Operations",
        "certificate": "System Administration",
        "description": "Learn scripting languages for security automation and operations.",
        "url": "https://www.byupathway.edu"
    },
    "azure-tech": {
        "title": "Azure Technologies",
        "certificate": "System Administration",
        "description": "Microsoft Azure cloud platform services and administration.",
        "url": "https://www.byupathway.edu"
    },
    "aws-practitioner": {
        "title": "AWS Cloud Practitioner",
        "certificate": "System Administration",
        "description": "Amazon Web Services fundamentals and cloud best practices.",
        "url": "https://www.byupathway.edu"
    }
}

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------- STATIC PAGES ----------------
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cv')
def cv():
    return render_template('cv.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/byu')
def byu():
    return render_template('byu.html')

@app.route('/cloud')
def cloud():
    return render_template('cloud.html')

@app.route('/cybersecurity')
def cybersecurity():
    return render_template('cybersecurity.html')

@app.route('/certifications')
def certifications():
    return render_template('certifications.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# ---------------- COURSE DETAILS ----------------
@app.route('/course/<course_id>')
def course_detail(course_id):
    course = COURSES.get(course_id)
    if not course:
        return "Course not found", 404
    
    # Check access type and get course materials info
    is_local = is_local_access()
    course_materials = None
    
    if 'local_folder' in course or 'onedrive_link' in course:
        if is_local and 'local_folder' in course:
            # Local access - show file path from OneDrive
            course_folder = course.get('local_folder')
            local_path = os.path.join(ONEDRIVE_BASE_PATH, course_folder)
            if os.path.exists(local_path):
                course_materials = {
                    'type': 'local',
                    'path': local_path,
                    'display': course_folder
                }
        elif 'onedrive_link' in course and course.get('onedrive_link'):
            # Remote access - show OneDrive link
            course_materials = {
                'type': 'cloud',
                'url': course.get('onedrive_link'),
                'display': course.get('local_folder', course.get('title'))
            }
    
    return render_template('course_detail.html', course_id=course_id, course=course, course_materials=course_materials)

# ---------------- PROJECTS (DYNAMIC) ----------------
@app.route('/projects')
def projects():

    courses = []
    source_roots = [
        r"F:\\BYU",
        r"C:\\Users\\User\\OneDrive - BYU-Pathway Worldwide\\Documents"
    ]
    one_drive_course_names = [
        "CS104 Foundations of Applied Programming",
        "IT102 PC Hardware Technician",
        "IT125 Intro to Information Technology",
        "IT210 Linux Fundamentals",
        "IT235 - Cloud server administration",
        "IT255 Networking Fundamentals"
    ]

    def collect_course_path(course_name, root_path):
        course_path = os.path.join(root_path, course_name)
        if os.path.isdir(course_path):
            return course_path
        return None

    def collect_files_from_folder(folder_path):
        files = []
        for file in sorted(os.listdir(folder_path)):
            if file.startswith('.'):
                continue
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                file_type = file.split('.')[-1].lower() if '.' in file else "other"
                files.append({
                    "name": file,
                    "type": file_type,
                    "path": file_path
                
                })
        return files

    def collect_weeks(course_path):
        weeks = []
        root_files = []
        for entry in sorted(os.listdir(course_path)):
            entry_path = os.path.join(course_path, entry)
            if entry.startswith('.'):
                continue
            if os.path.isdir(entry_path):
                week_files = collect_files_from_folder(entry_path)
                weeks.append({
                    "week": entry,
                    "files": week_files
                })
            elif os.path.isfile(entry_path):
                root_files.append({
                    "name": entry,
                    "type": entry.split('.')[-1].lower() if '.' in entry else "other"
                })

        if root_files:
            weeks.insert(0, {
                "week": "Course Files",
                "files": root_files
            })

        return weeks

    # First try the BYU shared folder, then the identified OneDrive course folders.
    for root_path in source_roots:
        if not os.path.exists(root_path):
            continue

        if root_path.endswith("Documents"):
            for course_name in one_drive_course_names:
                course_path = collect_course_path(course_name, root_path)
                if course_path:
                    weeks = collect_weeks(course_path)
                    if weeks:
                        courses.append({
                            "course": course_name,
                            "weeks": weeks
                        })
        else:
            for course_name in sorted(os.listdir(root_path)):
                course_path = os.path.join(root_path, course_name)
                if os.path.isdir(course_path):
                    weeks = collect_weeks(course_path)
                    courses.append({
                        "course": course_name,
                        "weeks": weeks
                    })

    recordings_root = r"C:\Users\User\OneDrive - BYU-Pathway Worldwide\Recordings"
    recordings_by_course = {}
    
    if os.path.exists(recordings_root) and os.path.isdir(recordings_root):
        for file in sorted(os.listdir(recordings_root)):
            if file.startswith('.'):
                continue
            file_path = os.path.join(recordings_root, file)
            if os.path.isfile(file_path):
                course_name = "Other Projects"
                
                file_lower = file.lower()
                if 'it160' in file_lower or 'csp_it160' in file_lower or 'cloud' in file_lower:
                    course_name = "IT160 - Cloud Solution Proposal"
                elif 'it255' in file_lower or 'network' in file_lower:
                    course_name = "IT255 Networking Fundamentals"
                elif 'it210' in file_lower or 'linux' in file_lower:
                    course_name = "IT210 Linux Fundamentals"
                elif 'it235' in file_lower or 'cloud server' in file_lower:
                    course_name = "IT235 - Cloud server administration"
                elif 'it125' in file_lower or 'intro' in file_lower or 'information technology' in file_lower:
                    course_name = "IT125 Intro to Information Technology"
                elif 'it102' in file_lower or 'hardware' in file_lower:
                    course_name = "IT102 PC Hardware Technician"
                elif 'cs104' in file_lower or 'applied programming' in file_lower:
                    course_name = "CS104 Foundations of Applied Programming"
                elif 'function' in file_lower or 'trigger' in file_lower:
                    course_name = "Database - Functions and Triggers"
                
                if course_name not in recordings_by_course:
                    recordings_by_course[course_name] = []
                
                recordings_by_course[course_name].append({
                    "name": file,
                    "url": Path(file_path).as_uri(),
                    "type": file.split('.')[-1].lower() if '.' in file else "other"
                })

    return render_template("projects.html", courses=courses, recordings_by_course=recordings_by_course)


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)


