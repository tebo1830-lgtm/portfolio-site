from flask import Flask, render_template, send_file, abort, request, jsonify, url_for
from pathlib import Path
import os
import json
import base64
import mimetypes
import subprocess
import sys
import shlex

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

def is_safe_path(file_path, allowed_base_paths):
    """Verify that file_path is within allowed directories (prevent directory traversal)"""
    try:
        real_path = os.path.realpath(file_path)
        for allowed_base in allowed_base_paths:
            allowed_real = os.path.realpath(allowed_base)
            if real_path.startswith(allowed_real):
                return True
        return False
    except:
        return False

# -------- COURSE MATERIALS PATHS --------
ONEDRIVE_BASE_PATH = r"C:\Users\User\OneDrive - BYU-Pathway Worldwide\BYU"

# Allowed paths for file viewing (security)
ALLOWED_PATHS = [
    r"F:\BYU",
    r"C:\Users\User\OneDrive - BYU-Pathway Worldwide\Documents",
    r"C:\Users\User\OneDrive - BYU-Pathway Worldwide\Recordings"
]

# OneDrive recordings folder (shared recordings link)
RECORDINGS_ONEDRIVE_LINK = "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgAAXsavR2q1RL4dYvxeoZNaAawbscjq6BRRRRoVZIk2Ewo?e=mQKQon"
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
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 143 Database Design and Analysis",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgCswwNvuCkzTKtS9dd3at0eAbvqlJxYWSsV0gXTPo37jLw?e=Q9sT0j"
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
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBdYk-rqyVWRoxBxn3QkSe8ASeqIPGKTn7aunzxw6IRobw?e=yvaLHw"
    },
    "network-config": {
        "title": "Network Configuration & Design",
        "certificate": "IT Professional",
        "description": "Network design, configuration, and best practices for enterprise networks.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 350 Network Configuration & Design",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgDe-H6FSybYRY7ZSASunPGnAV-HzZ1AA2RfXrN83thrJcg?e=hPZbw7"
    },
    "cybersecurity-foundations": {
        "title": "Cybersecurity Foundations",
        "certificate": "IT Professional",
        "description": "Introduction to cybersecurity principles, threats, and defense mechanisms.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 312 Cybersecurity",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgDuJxwBOzdVQLmc7F2ik_8qAWfFsr_rPVC-jzyRsPTMBQc?e=OsI0Ff"
    },
    "business-intelligence": {
        "title": "Business Intelligence Systems",
        "certificate": "System Administration",
        "description": "Learn to work with BI tools, data analytics, and business intelligence platforms.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 340 Business Intelligence Systems",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBx73_z5374T4NCwCjIfDUbAV1AqkiURxqSgcuv2UVjkos?e=xmr6me"
    },
    "advanced-linux": {
        "title": "Advanced Linux",
        "certificate": "System Administration",
        "description": "Advanced Linux system administration, scripting, and performance tuning.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 370 Advanced Linux",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBbUVpk1e3tRYhHHvJlM3C1AUYMZLzHptx1ATb5wmqtqeY?e=3IB9pF"
    },
    "networking-fundamentals": {
        "title": "IT 255 Networking Fundamentals",
        "certificate": "Information Technology",
        "description": "Networking fundamentals, protocols, and infrastructure design.",
        "url": "https://www.byupathway.edu",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgCcpZTs2DfEQq-U3GqvZQghAReSYi_TGOtGwIr-AzdsKSI?e=7xvZ6Z"
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

CERTIFICATE_TRACKS = [
    {
        "id": "technical-support-engineer",
        "title": "Technical Support Engineer",
        "summary": "Practical IT support skills for hardware, networking, desktop support, and programming fundamentals.",
        "status": "Completed",
        "detail": "All 5 courses completed",
        "courses": [
            {"id": "pc-hardware", "note": "Completed"},
            {"id": "networking-fundamentals", "note": "Completed"},
            {"id": "cloud-server", "note": "Completed"},
            {"id": "intro-it", "note": "Completed"},
            {"id": "applied-programming", "note": "Completed"}
        ]
    },
    {
        "id": "it-professional",
        "title": "IT Professional",
        "summary": "Advanced IT skills in databases, Linux, cloud, networking, and cybersecurity.",
        "status": "In Progress",
        "detail": "4 of 5 courses complete",
        "courses": [
            {"id": "database-design", "note": "Completed"},
            {"id": "linux-fundamentals", "note": "Completed"},
            {"id": "cloud-computing", "note": "Completed"},
            {"id": "network-config", "note": "Completed"},
            {"id": "cybersecurity-foundations", "note": "In Progress"}
        ]
    },
    {
        "id": "system-administration",
        "title": "System Administration",
        "summary": "Foundational server and network administration training for entry-level sysadmin roles.",
        "status": "In Progress",
        "detail": "2 of 5 courses in progress",
        "courses": [
            {"id": "business-intelligence", "note": "In Progress"},
            {"id": "advanced-linux", "note": "In Progress"},
            {"id": "scripting-security", "note": "Planned"},
            {"id": "azure-tech", "note": "Planned"},
            {"id": "aws-practitioner", "note": "Planned"}
        ]
    }
]

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
    certificates = []
    for cert in CERTIFICATE_TRACKS:
        courses = []
        completed = 0
        for item in cert['courses']:
            course = COURSES.get(item['id'], {})
            title = course.get('title', item['id'].replace('-', ' ').title())
            url = url_for('course_detail', course_id=item['id']) if item['id'] in COURSES else None
            note = item['note']
            if note == 'Completed':
                completed += 1
            courses.append({
                'id': item['id'],
                'title': title,
                'url': url,
                'note': note
            })

        certificates.append({
            'id': cert['id'],
            'title': cert['title'],
            'summary': cert['summary'],
            'status': cert['status'],
            'detail': cert['detail'],
            'courses': courses,
            'completed': completed,
            'total': len(courses)
        })

    return render_template('certifications.html', certificates=certificates)

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# -------- FILE VIEWING API (VIEW-ONLY) --------
@app.route('/api/file-content', methods=['POST'])
def get_file_content():
    """Serve file content for viewing (view-only, no edit/delete)"""
    try:
        file_path = request.json.get('path')
        
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400
        
        # Security check: verify path is within allowed directories
        if not is_safe_path(file_path, ALLOWED_PATHS):
            return jsonify({'error': 'Access denied to this file'}), 403
        
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Get file size to decide how to handle it
        file_size = os.path.getsize(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # For text files, return content
        text_extensions = {'.txt', '.py', '.sh', '.sql', '.js', '.html', '.css', '.json', '.csv', '.xml', '.md'}
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in text_extensions or (mime_type and mime_type.startswith('text/')):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    return jsonify({
                        'success': True,
                        'content': content,
                        'filename': os.path.basename(file_path),
                        'type': 'text',
                        'file_ext': file_ext
                    })
            except Exception as e:
                return jsonify({'error': f'Could not read file: {str(e)}'}), 500
        
        # For binary files, return file info and download link
        else:
            return jsonify({
                'success': True,
                'filename': os.path.basename(file_path),
                'type': 'binary',
                'file_ext': file_ext,
                'size': file_size,
                'mime_type': mime_type or 'application/octet-stream',
                'message': f'This is a binary file. Click the download button to view/save it.'
            })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# -------- FILE DOWNLOAD API (VIEW-ONLY) --------
@app.route('/api/file-download', methods=['POST'])
def download_file():
    """Download file for viewing (view-only)"""
    try:
        file_path = request.json.get('path')
        
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400
        
        # Security check
        if not is_safe_path(file_path, ALLOWED_PATHS):
            return jsonify({'error': 'Access denied to this file'}), 403
        
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True, download_name=os.path.basename(file_path))
    
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

# -------- COURSE DETAILS --------
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

    # Generate project links from COURSES with onedrive_link
    project_links = []
    for course_id, course in COURSES.items():
        if course.get('onedrive_link'):
            project_links.append({
                "title": course.get('title'),
                "certificate": course.get('certificate'),
                "description": course.get('description'),
                "url": course.get('onedrive_link'),
                "display": course.get('local_folder', course.get('title'))
            })

    # Add OneDrive recordings link as a top-level recordings entry
    if RECORDINGS_ONEDRIVE_LINK:
        recordings_by_course.setdefault('Project Recordings', [])
        # only add once
        if not any(r.get('url') == RECORDINGS_ONEDRIVE_LINK for r in recordings_by_course['Project Recordings']):
            recordings_by_course['Project Recordings'].insert(0, {
                'name': 'All Recordings (OneDrive)',
                'url': RECORDINGS_ONEDRIVE_LINK,
                'type': 'folder'
            })

        # Also map the recordings link under each course title for discoverability
        for course_id, course in COURSES.items():
            course_title = course.get('title')
            if not course_title:
                continue
            recordings = recordings_by_course.get(course_title, [])
            if not any(r.get('url') == RECORDINGS_ONEDRIVE_LINK for r in recordings):
                recordings.append({
                    'name': 'Recordings (OneDrive)',
                    'url': RECORDINGS_ONEDRIVE_LINK,
                    'type': 'folder'
                })
                recordings_by_course[course_title] = recordings

    return render_template("projects.html", courses=courses, recordings_by_course=recordings_by_course, project_links=project_links)


# ---------------- PYTHON PROJECTS (LOCAL + OneDrive links) ----------------
@app.route('/python-projects')
def python_projects():
    # local folder inside the repo where the user will place CS104 files
    repo_root = os.path.dirname(os.path.abspath(__file__))
    local_folder = os.path.join(repo_root, 'python_programs')
    metadata_path = os.path.join(local_folder, 'metadata.json')

    metadata = {}
    if os.path.exists(metadata_path) and os.path.isfile(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as meta_file:
                metadata = json.load(meta_file)
        except Exception:
            metadata = {}

    files = []
    if os.path.exists(local_folder) and os.path.isdir(local_folder):
        for fname in sorted(os.listdir(local_folder)):
            if fname.startswith('.'):
                continue
            fpath = os.path.join(local_folder, fname)
            if os.path.isfile(fpath) and fname.lower().endswith('.py'):
                clean_name = os.path.splitext(fname)[0]
                clean_display = clean_name.replace('_', ' ').replace('-', ' ').title()
                files.append({
                    'name': fname,
                    'display_name': clean_display,
                    'description': metadata.get(fname, ''),
                    'path': fpath
                })

    # OneDrive links provided (hybrid approach) - user-supplied folders
    onedrive_links = [
        { 'title': '1-4 Integrated Development Environments', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '2-4 First Programs', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '2-5 Putting Python to Work', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '2-7 Flow of Information', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '3-4 Tilling Soil', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '3-5 Limiting Access', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '4-4 The Nature of Numbers', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '4-6 Iterating Through a JSON Object', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '4-7 Raspberry Pi Python Execution', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '5-3 Tracking Finances', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '5-4 Career Connections', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '5-7 Security Device Monitoring', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '6-4 Creating and Filling a Database', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '6-8 Connecting with the WhatsApp API', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '7-2 Flask Routing Quiz', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'},
        { 'title': '7-3 Reading and Revising an API', 'url': 'https://byupathwayworldwideprod-my.sharepoint.com/personal/smokhele_byupathway_edu/Documents/'}
    ]

    return render_template('python_projects.html', files=files, onedrive_links=onedrive_links)


@app.route('/api/python-projects/files', methods=['GET'])
def python_projects_files():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    local_folder = os.path.join(repo_root, 'python_programs')
    metadata_path = os.path.join(local_folder, 'metadata.json')

    metadata = {}
    if os.path.exists(metadata_path) and os.path.isfile(metadata_path):
        try:
            with open(metadata_path, 'r', encoding='utf-8') as meta_file:
                metadata = json.load(meta_file)
        except Exception:
            metadata = {}

    files = []
    if os.path.exists(local_folder) and os.path.isdir(local_folder):
        for fname in sorted(os.listdir(local_folder)):
            if fname.startswith('.'):
                continue
            fpath = os.path.join(local_folder, fname)
            if os.path.isfile(fpath) and fname.lower().endswith('.py'):
                clean_name = os.path.splitext(fname)[0]
                clean_display = clean_name.replace('_', ' ').replace('-', ' ').title()
                files.append({
                    'name': fname,
                    'display_name': clean_display,
                    'description': metadata.get(fname, ''),
                })

    return jsonify({'files': files})


@app.route('/api/run-python', methods=['POST'])
def run_python():
    data = request.json or {}
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    repo_root = os.path.dirname(os.path.abspath(__file__))
    local_folder = os.path.join(repo_root, 'python_programs')
    target_path = os.path.join(local_folder, os.path.basename(filename))

    # Security: ensure the path is inside local_folder
    if not is_safe_path(target_path, [local_folder]):
        return jsonify({'error': 'Access denied'}), 403

    if not os.path.exists(target_path) or not os.path.isfile(target_path):
        return jsonify({'error': 'File not found'}), 404

    # Run with the same Python interpreter used by the server
    cmd = [sys.executable, target_path]

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=8, cwd=local_folder, text=True)
        stdout = proc.stdout[:10000]
        stderr = proc.stderr[:10000]
        return jsonify({'success': True, 'stdout': stdout, 'stderr': stderr, 'returncode': proc.returncode})
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Execution timed out'}), 504
    except Exception as e:
        return jsonify({'error': f'Execution error: {str(e)}'}), 500


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)


