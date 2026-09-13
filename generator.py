import pandas as pd
import random
from datetime import datetime, timedelta

# Configuration
NUM_RESPONSES = 12647
OUTPUT_FILE = "DICT_CoursesEvaluationSurvey_MockDataset.xlsx"

# Synthetic Data Pools
first_names = ["Dexter", "John Ford", "Shela Mae", "John Paul Emil", "Jhara Mae", "Sarah Jean", "Dan Lloyd", "Michaela Faye", "Ederlyn", "Danilo", "Juan", "Maria", "Mark", "Grace", "Paul"]
last_names = ["Ocado", "Agana", "Deloviar", "Faller", "Javal", "Morada", "Otico", "Palines", "Raflores", "Solana", "Cruz", "Santos", "Reyes", "Bautista", "Mendoza"]
middle_initials = ["A.", "B.", "C.", "D.", "E.", "M.", "P.", "S.", "V."]

# 1. SECTOR SKEW (Gov & Students dominate)
employment_statuses = [
    "Government Employee", "Student", "Private Sector Employee", 
    "Unemployed", "Freelancer / Self-Employed", "OJT / Student Intern", 
    "Academe / Educator", "Business Owner", "NGO Worker"
]
sector_weights = [0.35, 0.25, 0.15, 0.10, 0.05, 0.05, 0.03, 0.01, 0.01]

# 2. GEOGRAPHIC SKEW (NCR, IV-A, III dominate based on PH population/tech penetration)
all_regions = [
    "NCR (National Capital Region)", "Region IV-A (CALABARZON)", "Region III (Central Luzon)", 
    "Region VII (Central Visayas)", "Region XI (Davao Region)", "Region VI (Western Visayas)", 
    "Region X (Northern Mindanao)", "Region I (Ilocos Region)", "Region V (Bicol Region)",
    "Region VIII (Eastern Visayas)", "Region II (Cagayan Valley)", "Region XII (SOCCSKSARGEN)",
    "Region IX (Zamboanga Peninsula)", "Region XIII (Caraga)", "Region IV-B (MIMAROPA)", 
    "CAR (Cordillera Administrative Region)", "BARMM (Bangsamoro)"
]
region_weights = [0.25, 0.18, 0.12, 0.08, 0.06, 0.06, 0.05, 0.04, 0.04, 0.03, 0.02, 0.02, 0.015, 0.015, 0.01, 0.005, 0.005]

# 3. COURSE POPULARITY SKEW
courses = [
    "Digital Productivity Essentials",
    "Google Workspace Essentials: Tools for Modern Teamwork",
    "AI for Operations and Finance Workshop"
]
course_weights = [0.50, 0.35, 0.15] # Broadest to most niche

likert_scale = ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]
hours_spent = ["Under 10 hours", "10-20 hours", "21-30 hours", "31-40 hours", "Over 40 hours"]
hour_weights = [0.10, 0.40, 0.30, 0.15, 0.05] # Most finish in 10-30 hours

# Generic self-paced comments
generic_best_practices = [
    "Setting aside 1 hour every night before bed to focus.",
    "Using the mobile app to listen to lectures during my daily commute.",
    "Taking handwritten notes to retain information better.",
    "Treating the self-paced course like a mandatory college class.",
    "Downloading modules for offline viewing to avoid internet lag.",
    "Joining online study groups with friends taking the same course.",
    "Watching the videos at 1.25x speed to save time.",
    "Completing all the quizzes on weekends when I have no work.",
    "Breaking down the modules into 30-minute chunks to avoid burnout.",
    "Setting personal calendar reminders since there are no hard deadlines."
]

generic_challenges = [
    "Procrastination is a huge factor since there are no hard deadlines.",
    "Sometimes I get stuck on a topic and there is no live instructor to ask.",
    "Balancing the modules with my full-time job and family responsibilities.",
    "Internet buffering during the high-definition video lectures.",
    "Feeling isolated without peer interaction or discussion.",
    "Losing motivation midway through the lengthy modules.",
    "Reading the text-heavy slides on a small smartphone screen.",
    "Finding a quiet place to concentrate at home.",
    "Forgetting what I learned in the previous module because of long breaks.",
    "Self-discipline was definitely the hardest part of the asynchronous setup."
]

generic_suggestions = [
    "Include a discussion board where learners can ask questions.",
    "Provide downloadable PDF summaries of the video lectures.",
    "Add more interactive quizzes to break up the long videos.",
    "Implement a progress tracker that sends weekly email reminders.",
    "Add English subtitles/captions to all video lectures.",
    "Make the UI more mobile-friendly for smartphone users.",
    "Offer a live Q&A session at least once a month.",
    "Gamify the platform with badges to keep learners motivated.",
    "Allow background audio playback on the mobile app.",
    "Shorter, more focused videos rather than 45-minute lectures."
]

# Course-Specific Dictionaries
specific_best_practices = {
    "Digital Productivity Essentials": ["Immediately setting up my inbox zero system while watching the module.", "Applying the Pomodoro technique directly to the course study time itself."],
    "Google Workspace Essentials: Tools for Modern Teamwork": ["Testing the collaboration features live with my co-workers on a shared Google Doc.", "Practicing the keyboard shortcuts on a dummy spreadsheet."],
    "AI for Operations and Finance Workshop": ["Testing the AI prompts on our actual sanitized financial datasets to see immediate results.", "Building a personal prompt library in a notepad as the videos played."]
}

specific_challenges = {
    "Digital Productivity Essentials": ["Felt overwhelmed by the sheer number of productivity frameworks introduced.", "Struggled to integrate the suggested task managers with my agency's outdated legacy systems."],
    "Google Workspace Essentials: Tools for Modern Teamwork": ["Some of the Google Workspace features shown in the video look different from the current version of my browser.", "Hard to practice collaboration tools asynchronously when I'm studying alone."],
    "AI for Operations and Finance Workshop": ["The AI prompt engineering exercises were a bit difficult to understand without a live instructor to guide us.", "My agency network actually blocks some of the AI tools mentioned in the course."]
}

specific_suggestions = {
    "Digital Productivity Essentials": ["Include more templates for Notion or Trello.", "Provide a breakdown of free vs. paid productivity software alternatives."],
    "Google Workspace Essentials: Tools for Modern Teamwork": ["Include a deeper dive into Google Sheets advanced formulas and AppSheet.", "Add a troubleshooting guide for common file-sharing permission errors."],
    "AI for Operations and Finance Workshop": ["Offer a follow-up workshop focused purely on AI automation for financial spreadsheets.", "Include a cheat sheet of the most effective prompt structures for data analysis."]
}

rows = []
start_date = datetime(2026, 1, 1, 8, 0)

for i in range(NUM_RESPONSES):
    f_name = random.choice(first_names)
    l_name = random.choice(last_names)
    mi = random.choice(middle_initials)
    
    full_name = f"{f_name} {mi} {l_name}"
    short_name = f"{f_name} {l_name}"
        
    email = f"{f_name.split(' ')[0].lower()}.{l_name.lower().replace(' ', '')}@gmail.com"
    sex = random.choices(["Male", "Female"], weights=[0.48, 0.52])[0]
    
    sector = random.choices(employment_statuses, weights=sector_weights)[0]
    region = random.choices(all_regions, weights=region_weights)[0]
    selected_course = random.choices(courses, weights=course_weights)[0]
    
    # Conditional Device Skew
    if sector in ["Student", "Unemployed", "OJT / Student Intern"]:
        device = random.choices(["Smartphone", "Laptop", "Desktop PC", "Tablet"], weights=[0.60, 0.30, 0.05, 0.05])[0]
    elif sector in ["Government Employee", "Private Sector Employee"]:
        device = random.choices(["Laptop", "Desktop PC", "Smartphone", "Tablet"], weights=[0.55, 0.35, 0.08, 0.02])[0]
    else:
        device = random.choices(["Laptop", "Smartphone", "Desktop PC", "Tablet"], weights=[0.40, 0.40, 0.10, 0.10])[0]
    
    # Feedback injection
    if random.random() < 0.3:
        best_practice = random.choice(specific_best_practices[selected_course])
        challenge = random.choice(specific_challenges[selected_course])
        suggestion = random.choice(specific_suggestions[selected_course])
    else:
        best_practice = random.choice(generic_best_practices)
        challenge = random.choice(generic_challenges)
        suggestion = random.choice(generic_suggestions)
    
    if device == "Smartphone":
        likert_weights = [0.35, 0.35, 0.20, 0.08, 0.02]
    else:
        likert_weights = [0.45, 0.40, 0.10, 0.04, 0.01]
    
    # Simulate realistic H1 rollout curve (peak completions around April/May)
    # random.triangular(low, high, mode) -> mode=110 sets the peak around April
    random_day = int(random.triangular(0, 180, 110))
    random_minute = random.randint(0, 1440)
    completion_timestamp = start_date + timedelta(days=random_day, minutes=random_minute)
    
    row = [
        i + 1,
        completion_timestamp.strftime("%m/%d/%y %H:%M"),
        email,
        short_name,
        full_name,
        sex,
        sector,
        region,
        selected_course,
        device,
        random.choices(likert_scale, weights=likert_weights)[0], 
        random.choices(likert_scale, weights=likert_weights)[0], 
        random.choices(likert_scale, weights=likert_weights)[0], 
        random.choices(["Yes", "No", "Sometimes"], weights=[0.15, 0.65, 0.20])[0], 
        random.choices(likert_scale, weights=likert_weights)[0], 
        random.choices(hours_spent, weights=hour_weights)[0],
        random.choices(["Yes, very manageable.", "Pacing was a bit too fast.", "Required too much time."], weights=[0.7, 0.2, 0.1])[0], 
        best_practice,
        challenge,
        suggestion
    ]
    rows.append(row)

# Export configuration
headers = [
    "Respondent_ID", "Completion_Timestamp", "Email", "Name", "Full_Name", "Sex", "Employment_Sector", "Region", 
    "Course_Track", "Primary_Learning_Device", "Rating_Platform_Usability", "Rating_Content_Relevance", "Rating_Video_Clarity", 
    "Encountered_Tech_Issues", "Rating_Overall_Satisfaction", "Estimated_Hours_Spent", 
    "Pacing_Manageability", "Qual_Best_Practices", "Qual_Challenges", "Qual_Suggestions"
]

df = pd.DataFrame(rows, columns=headers)
df['Completion_Timestamp'] = pd.to_datetime(df['Completion_Timestamp'], format='%m/%d/%y %H:%M')

writer = pd.ExcelWriter(OUTPUT_FILE, engine='xlsxwriter')
df.to_excel(writer, sheet_name='Survey_Data', index=False)
worksheet = writer.sheets['Survey_Data']
(max_row, max_col) = df.shape
worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': [{'header': c} for c in df.columns], 'style': 'Table Style Medium 2', 'name': 'DICT_Survey_Table'})
worksheet.set_column(0, max_col - 1, 22)
writer.close()

print(f"Generated {NUM_RESPONSES} rows of H1 2026 data (Jan-Jun) with realistic rollout curves in {OUTPUT_FILE}.")