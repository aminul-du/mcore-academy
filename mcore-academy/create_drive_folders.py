#!/usr/bin/env python3
# create_drive_folders.py – MCore Academy Google Drive Folder Creator
# Owner: MCORE-FDR-AIS-001 | Date: 22 July 2026
# CONFIG PATH: E:\ME@DevAI\.config\google-drive-mcp\ (Windows raw string)

import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# -------- PERMANENT E: DRIVE PATH (WINDOWS RAW STRING) --------
CONFIG_DIR = r'E:\ME@DevAI\.config\google-drive-mcp'
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, 'gcp-oauth.keys.json')
TOKEN_FILE = os.path.join(CONFIG_DIR, 'token.json')
# --------------------------------------------------------------

# Verify the file exists before proceeding
if not os.path.exists(CREDENTIALS_FILE):
    print(f"❌ ERROR: Credentials file not found at {CREDENTIALS_FILE}")
    print("Please ensure the file exists or adjust the path.")
    exit(1)

FOLDERS = [
    "00-MASTER-CONTROL",
    "01-KNOWLEDGE-INDEX",
    "02-DIGITAL-BOOKS",
    "03-RESEARCH-PAPERS",
    "04-TECHNICAL-DOCUMENTATION",
    "05-NETWORKING",
    "06-CYBERSECURITY",
    "07-TELECOMMUNICATION",
    "08-CLOUD-COMPUTING",
    "09-AI-AGI",
    "10-DEVSECOPS",
    "11-AUTOMATION",
    "12-SYSTEM-DESIGN",
    "13-LABS",
    "14-PROJECTS",
    "15-COURSES",
    "16-STANDARDS",
    "17-BUSINESS",
    "18-LEGAL",
    "19-MULTIMEDIA",
    "20-DRAFTS",
    "21-TEMPLATES",
    "22-KNOWLEDGE-GRAPH",
    "23-MASTER-PROMPTS",
    "24-AI-AGENTS",
    "25-WORKFLOW",
    "90-BACKUP",
    "99-ARCHIVE"
]

SUBFOLDERS = {
    "02-DIGITAL-BOOKS": ["BK-0001-Introduction-to-Networking", "BK-0002-Cybersecurity-Architecture", "BK-0003-AI-Infrastructure", "BK-0004-BGP-Deep-Dive", "BK-0005-MPLS-Fundamentals"],
    "03-RESEARCH-PAPERS": ["RS-0001-BGP-Research", "RS-0002-Cloud-Research", "RS-0003-AI-Governance", "RS-0004-Network-Automation", "RS-0005-Post-Quantum-Crypto", "RS-0006-eBPF-Telemetry"],
    "04-TECHNICAL-DOCUMENTATION": ["TD-0001-MCore-Architecture", "TD-0002-MEP-Platform", "TD-0003-OSI-Model", "TD-0004-9-Layer-AI-Stack"],
    "05-NETWORKING": ["BGP", "MPLS", "SRv6", "OSPF", "ISIS", "EVPN-VXLAN"],
    "06-CYBERSECURITY": ["Zero_Trust", "DDoS_Mitigation", "SOC_Operations", "Digital_Forensics", "GRC_Automation", "Incident_Response"],
    "09-AI-AGI": ["Agentic_AI", "LLM_Architecture", "RAG_Systems", "Vector_Databases", "eBPF_Telemetry"],
    "10-DEVSECOPS": ["CI_CD_Pipelines", "GitOps", "Infrastructure_as_Code", "Security_Scanning"],
    "14-PROJECTS": ["PJ-0001-MCore-Cloud", "PJ-0002-MCore-Wifi", "PJ-0003-MCore-XDR", "PJ-0004-MCore-SensyAI", "PJ-0005-WhatsApp-Analyzer", "PJ-0006-NCG-Prototype"],
    "15-COURSES": ["CS-0001-BGP-Advanced", "CS-0002-MPLS-Architecture", "CS-0003-SRv6-Deployment", "CS-0004-AI-for-Networks", "CS-0005-Zero-Trust-Security"],
    "16-STANDARDS": ["STD-0001-RFC-Documentation", "STD-0002-NIST-800-53", "STD-0003-ISO-27001", "STD-0004-BTRC-Regulations"],
    "21-TEMPLATES": ["SOP_Template.md", "ADR_Template.md", "Project_Plan_Template.md", "Report_Template.md", "Pitch_Deck_Template.md"],
    "23-MASTER-PROMPTS": ["LLM_Prompts", "Agentic_Workflows", "System_Prompts", "Persona_Definitions"],
    "24-AI-AGENTS": ["Agent_Configurations", "Agent_Logs", "Agent_Outputs"]
}

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def create_folder(service, folder_name, parent_id=None):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
    try:
        file = service.files().create(body=file_metadata, fields='id').execute()
        print(f"  ✅ Created: {folder_name}")
        return file.get('id')
    except HttpError as error:
        print(f"  ❌ Failed: {folder_name} - {error}")
        return None

def main():
    print("📁 Connecting to Google Drive API using E: drive config...")
    service = get_authenticated_service()
    root_name = "MCore Academy"
    root_id = None
    try:
        response = service.files().list(
            q=f"name='{root_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields='files(id)'
        ).execute()
        if response.get('files'):
            root_id = response['files'][0]['id']
            print(f"  📁 Found existing root: {root_name}")
        else:
            root_id = create_folder(service, root_name)
    except HttpError:
        root_id = create_folder(service, root_name)
    if not root_id:
        print("❌ Failed to create root folder")
        return
    path_map = {'root': root_id}
    for folder in FOLDERS:
        folder_id = create_folder(service, folder, root_id)
        if folder_id:
            path_map[folder] = folder_id
    print("\n📁 Creating subfolders...")
    for parent, children in SUBFOLDERS.items():
        parent_id = path_map.get(parent)
        if not parent_id:
            print(f"  ⚠️ Parent not found: {parent}")
            continue
        for child in children:
            create_folder(service, child, parent_id)
    print("\n✅ MCore Academy Google Drive structure created successfully!")
    print(f"📊 Total folders: {len(FOLDERS) + sum(len(v) for v in SUBFOLDERS.values())}")
    print("🔗 Verify at: https://drive.google.com")

if __name__ == '__main__':
    main()
