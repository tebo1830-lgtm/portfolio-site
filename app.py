from flask import Flask, render_template, send_file, abort, request
from pathlib import Path
import os
from messaging import get_messaging_service

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
        "description": "This is a 3-credit course exploring the fundamental components and concepts around the personal computer (PC), including hardware components, networking devices, memory, bootup issues, operating system components, storage, wireless connectivity, security and troubleshooting exercises. As a final exam, students will take the TestOut PC Pro Certification exam to receive an important industry certification.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT102 PC Hardware Technician",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBJ4I2SAS8mTKvJkgPxsLSxAWQIt5Dcvj7yeDLKbM806jw?e=BxTziD"
    },
    "networking-fundamentals": {
        "title": "Networking Fundamentals",
        "certificate": "Technical Support Engineer",
        "description": "This is a 3-credit course that explores different hardware technology required to create a simple network including cabling, routers and switches. It explores the different layers of the OSI model using packet capture technology to read and analyze network traffic. Using several hands-on projects, the course focuses on subnetting and how to identify network IDs, broadcast addresses, as well as how to troubleshoot basic networking problems.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT255 Networking Fundamentals",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgCcpZTs2DfEQq-U3GqvZQghAReSYi_TGOtGwIr-AzdsKSI?e=y8NghJ"
    },
    "cloud-server": {
        "title": "Cloud Server Administration",
        "certificate": "Technical Support Engineer",
        "description": "This is a 3-credit course introducing critical concepts of server technology, including installation, configuration, maintenance, and troubleshooting. Successful completion of this course will prepare students to take the MS AZ-800 certification exam.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT235 - Cloud server administration",
        "onedrive_link": ""  # Add your OneDrive share link here
    },
    "intro-it": {
        "title": "Introduction to Information Technology",
        "certificate": "Technical Support Engineer",
        "description": "This is a 3-credit course focused on installing, configuring and administering Windows Desktop systems across peer-to-peer configurations as well as client-server domain environments. It develops the skills required to be a consultant, full-time desktop support technician, or IT generalist who administers Windows-based computers and devices as part of broader technical responsibilities.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT125 Intro to Information Technology",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBvS-sSsknIT7HYo82_wUM3AWQeBr-IgWkN6aFSLJvAgnQ?e=HQBiMx"
    },
    "applied-programming": {
        "title": "Foundations of Applied Programming",
        "certificate": "Technical Support Engineer",
        "description": "This is a 3-credit introductory course in programming using the Python programming language. Students learn programming from the perspective of a Junior Developer, covering scripting concepts such as variables, operators, input/output, conditional logic, loops, functions, strings, arrays, and files. The course develops problem-solving techniques and computational thinking skills to solve basic operations problems, including creating functions as part of an API, calling APIs, and interacting with databases. Students will also program a Raspberry Pi (virtual or physical) with sensors.",
        "url": "https://www.byupathway.edu",
        "local_folder": "CS104 Foundations of Applied Programming",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgCKPC7nHTdzR7HjE7DKILvjAaqeCiO75vZojPBQkm2qTUI?e=kuNrwn"
    },
    "database-design": {
        "title": "Database Design and Analysis",
        "certificate": "IT Professional",
        "description": "This is a 3-credit course where students use Structured Query Language (SQL) to analyze, design, and build database objects and structures for efficient data retrieval. These technical skills are enhanced with soft skills needed to identify project requirements, communicate roadblocks, and present professional summaries that provide timely solutions for stakeholders.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 143 Database Design and Analysis",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgCswwNvuCkzTKtS9dd3at0eAbvqlJxYWSsV0gXTPo37jLw?e=dBBULa"
    },
    "linux-fundamentals": {
        "title": "Linux Fundamentals",
        "certificate": "IT Professional",
        "description": "This is a 3-credit course introducing critical concepts of Linux administration, including installation, configuration, management, maintenance, monitoring, security, and troubleshooting. Successful completion prepares students to take the CompTIA Linux+ Certification Exam. It is highly recommended that students have some IT background or have completed IT 125 before taking this course.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT210 Linux Fundamentals",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgDO7_2OGwHdT4AE1LKJwsZKAXfPNe7Iia1X1O6aF3LaWK8?e=LaidyB"
    },
    "cloud-computing": {
        "title": "Cloud Computing Essentials",
        "certificate": "IT Professional",
        "description": "This is a 3-credit course immersing students in what cloud computing is and how cloud services differ from hosted services. Students identify cloud service models using aaS terminology and explain how they relate to one another. The course covers business drivers for cloud computing, such as reduced costs and increased efficiency, and explores cloud infrastructure planning, adoption strategies, and cloud security models using NIST standards and common risk mitigation.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 160 Cloud Computing Essentials",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBdYk-rqyVWRoxBxn3QkSe8ASeqIPGKTn7aunzxw6IRobw?e=dRUJtm"
    },
    "network-config": {
        "title": "Network Configuration & Design",
        "certificate": "IT Professional",
        "description": "This is a 3-credit course exploring the infrastructure of a large network, including hardware and design strategies. Using virtual and simulation technologies, students configure routers, switches, and learn how to design and secure networks.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 350 Network Configuration & Design",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgDe-H6FSybYRY7ZSASunPGnAV-HzZ1AA2RfXrN83thrJcg?e=yg1Fe5"
    },
    "cybersecurity-foundations": {
        "title": "Cybersecurity Foundations",
        "certificate": "IT Professional",
        "description": "This is a 3-credit hands-on course exploring basic cybersecurity concepts including access control management in both Windows AD and Linux environments. It covers security policies, perimeter, network, host, and application defenses, and includes labs with Kali Linux and IDS systems.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 312 Cybersecurity",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgDuJxwBOzdVQLmc7F2ik_8qAWfFsr_rPVC-jzyRsPTMBQc?e=DcBF87"
    },
    "business-intelligence": {
        "title": "Business Intelligence Systems",
        "certificate": "System Administration",
        "description": "This is a 3-credit course focused on extracting business intelligence from data sets for reporting and visual analytics across domains such as web analytics and business analytics. It provides hands-on experience with BI software for reporting, visualization, and dashboards to support decision-making.",
        "url": "https://www.byupathway.edu",
        "local_folder": "IT 340 Business Intelligence Systems",
        "onedrive_link": "https://byupathwayworldwideprod-my.sharepoint.com/:f:/g/personal/smokhele_byupathway_edu/IgBx73_z5374T4NCwCjIfDUbAV1AqkiURxqSgcuv2UVjkos?e=1i0DKB"
    },
    "advanced-linux": {
        "title": "Advanced Linux",
        "certificate": "System Administration",
        "description": "This is a 3-credit course in which students enhance their foundational Linux skills through experiential projects, interact with advanced Linux command stacks, build and integrate server configurations, and implement business infrastructure plans for secure environments. Students also engage in team collaboration and student-led teaching to experience the life of a Linux administrator.",
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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    sent = False
    confirmation = None
    chat_message = None
    error = None

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        channel = request.form.get('channel', 'WhatsApp')

        if message:
            chat_message = {
                'name': name or 'Guest',
                'email': email or 'tebza27@gmail.com',
                'message': message,
                'channel': channel
            }

            # Attempt to send via selected channel
            messaging = get_messaging_service()
            result = None

            if channel == 'WhatsApp':
                result = messaging.send_whatsapp(chat_message['name'], chat_message['email'], message)
            elif channel == 'Google Hangouts':
                result = messaging.send_google_chat(chat_message['name'], chat_message['email'], message)
            elif channel == 'Email':
                result = messaging.send_email(chat_message['name'], chat_message['email'], message)

            if result and result.get('success'):
                sent = True
                confirmation = f"✓ Message sent via {channel}! You'll receive a response shortly."
            else:
                error = result.get('error', 'Failed to send message.') if result else 'Unknown error.'
                confirmation = f"Message saved locally. {error}"
        else:
            error = 'Please enter a message before sending.'
            confirmation = error

    return render_template('contact.html', sent=sent, confirmation=confirmation, chat_message=chat_message, error=error)


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

    courses_by_name = {}
    source_roots = [
        ONEDRIVE_BASE_PATH,
        os.path.join(app.root_path, 'static', 'projects')
    ]

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

    for root_path in source_roots:
        if not os.path.exists(root_path):
            continue

        for course_name in sorted(os.listdir(root_path)):
            course_path = os.path.join(root_path, course_name)
            if not os.path.isdir(course_path):
                continue

            weeks = collect_weeks(course_path)
            if not weeks:
                continue

            if course_name not in courses_by_name:
                courses_by_name[course_name] = {
                    "course": course_name,
                    "weeks": weeks
                }
            else:
                existing_weeks = courses_by_name[course_name]["weeks"]
                existing_week_names = {week["week"] for week in existing_weeks}
                for week in weeks:
                    if week["week"] not in existing_week_names:
                        existing_weeks.append(week)

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

    project_links = []
    for course in COURSES.values():
        if course.get('onedrive_link'):
            project_links.append({
                "title": course['title'],
                "display": course.get('local_folder', course['title']),
                "url": course['onedrive_link'],
                "description": course.get('description', ''),
                "certificate": course.get('certificate', '')
            })

    no_files = len(courses_by_name) == 0
    return render_template(
        "projects.html",
        courses=list(courses_by_name.values()),
        recordings_by_course=recordings_by_course,
        project_links=project_links,
        no_files=no_files
    )


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)


