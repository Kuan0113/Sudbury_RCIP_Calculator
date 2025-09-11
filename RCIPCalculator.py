import tkinter as tk
from tkinter import ttk

class RCIPCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudbury RCIP Scoring Calculator")
        self.root.geometry("700x900")
        self.root.resizable(False, True)

        # Categories and options
        self.categories = {
            "Job Offer - Section": ["Natural and Applied Sciences", "Health", 
                                    "Education, Social, Community and Government Services", 
                                    "Trades and Transport", "Natural Resources and Agriculture"],
            "Job Offer - Occupation": [
                "12200 – Accounting Technicians and Bookkeepers",
                "13110 – Administrative Assistants",
                "21330 – Mining Engineers",
                "21301 – Mechanical Engineers",
                "21331 – Geological Engineers",
                "22300 – Civil Engineering Technologists and Technicians",
                "22301 – Mechanical Engineering Technologists and Technicians",
                "22310 – Electrical and Electronics Engineering Technologists and Technicians",
                "31202 – Physiotherapists",
                "31301 – Registered Nurses",
                "32101 – Registered Practical Nurses",
                "32109 – Rehabilitation Assistants",
                "33102 – Personal Care Attendants",
                "33100 – Dental Assistants",
                "42201 – Social and Community Service Workers",
                "42202 – Early Childhood Educators and Assistants",
                "44101 – Home Support Workers, Caregivers, and related occupations",
                "72401 – Heavy Duty Equipment Mechanics",
                "72410 – Automotive Service Technicians, Truck and Bus Mechanics, and Mechanical Repairers",
                "72106 – Welders and Related Machine Operators",
                "72400 – Construction Millwrights and Industrial Mechanics",
                "73400 – Heavy Equipment Operators",
                "75110 – Construction Trades Helpers and Labourers",
                "73300 – Truck Drivers",
                "95100 – Labourers in Metal Processing"
            ],
            "Human Capital - Work Experience": ["1 year full-time work experience", "2 years full-time work experience", 
                                               "3 years full-time work experience", "4+ years full-time work experience", 
                                               "International graduate exemption"],
            "Human Capital - Language Proficiency TEER": ["0/1", "2/3", "4/5"],
            "Human Capital - Education": ["Master's/PhD", "Bachelor's (3+ years)", "Post-secondary (1+ year)", "Canadian Secondary School Diploma"],
            "Human Capital - Intent to Reside": ["Submitted genuine statement", "Not submitted"]
        }

        # Points mapping
        self.points_mapping = {
            "Job Offer - Section": [10,15,10,15,15],
            "Job Offer - Occupation": [
                0,0,10,10,10,10,10,10,10,10,8,0,0,0,5,7,0,10,10,10,10,10,5,2,2
            ],
            "Human Capital - Work Experience": [10,15,20,25,10],
            "Human Capital - Education": [25,20,15,10],
            "Human Capital - Intent to Reside": [10,0],
            "LanguageProficiency": {
                "0/1": {"CLB/NCLC 6":10,"CLB/NCLC 7":15,"CLB/NCLC 8":20,"CLB/NCLC 9+":25},
                "2/3": {"CLB/NCLC 5":10,"CLB/NCLC 6":15,"CLB/NCLC 7":20,"CLB/NCLC 8+":25},
                "4/5": {"CLB/NCLC 4":10,"CLB/NCLC 5":15,"CLB/NCLC 6":20,"CLB/NCLC 7+":25}
            },
            "Previous Work/Study in Community": [2,4,6],
            "Close Family in Community": [2],
            "Community Involvement": [2],
            "Property in Community": [2],
            "Spouse/Common-law Experience": [3]
        }

        self.max_scores = {
            "Job Offer - Section": 15,
            "Job Offer - Occupation": 10,
            "Human Capital - Work Experience": 25,
            "LanguageProficiency": 25,
            "Human Capital - Education": 25,
            "Human Capital - Intent to Reside": 10,
            "Previous Work/Study in Community": 6,
            "Close Family in Community": 2,
            "Community Involvement": 2,
            "Property in Community": 2,
            "Spouse/Common-law Experience": 3
        }

        # Selected values dictionary
        self.selected_values = {}
        self.section_scores = {}

        self.create_widgets()

    def create_widgets(self):
        row = 0
        for category, options in self.categories.items():
            tk.Label(self.root, text=category, font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", padx=10, pady=(10,0))
            row += 1

            if category == "Human Capital - Language Proficiency TEER":
                self.selected_values['LanguageProficiency TEER'] = tk.StringVar()
                teer_menu = ttk.Combobox(self.root, textvariable=self.selected_values['LanguageProficiency TEER'], values=options, state="readonly")
                teer_menu.grid(row=row, column=0, sticky="w", padx=20)
                teer_menu.current(0)
                row += 1

                self.selected_values['LanguageProficiency CLB'] = tk.StringVar()
                self.clb_menu = ttk.Combobox(self.root, textvariable=self.selected_values['LanguageProficiency CLB'], state="readonly")
                self.clb_menu.grid(row=row, column=0, sticky="w", padx=20)
                self.clb_menu['values'] = []
                row += 1

                teer_menu.bind("<<ComboboxSelected>>", self.update_clb)
            else:
                var = tk.StringVar()
                dropdown = ttk.Combobox(self.root, textvariable=var, values=options, state="readonly")
                dropdown.grid(row=row, column=0, sticky="w", padx=20)
                dropdown.current(0)
                self.selected_values[category] = var
                row += 1

        # Bonus points
        tk.Label(self.root, text="Bonus Points", font=("Arial", 12, "bold")).grid(row=row, column=0, sticky="w", pady=(20,0), padx=10)
        row += 1

        bonus_questions = {
            "Previous Work/Study in Community": ["None","1 year (combined)","2 years (combined)","3 years or more (combined)"],
            "Close Family in Community": ["No","Yes"],
            "Community Involvement": ["No","Yes"],
            "Property in Community": ["No","Yes"],
            "Spouse/Common-law Experience": ["No","Yes"]
        }

        for key, options in bonus_questions.items():
            tk.Label(self.root, text=key).grid(row=row, column=0, sticky="w", padx=20)
            var = tk.StringVar()
            dropdown = ttk.Combobox(self.root, textvariable=var, values=options, state="readonly")
            dropdown.grid(row=row+1, column=0, sticky="w", padx=20, pady=(0,10))
            dropdown.current(0)
            self.selected_values[key] = var
            row += 2

        # Results
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"), fg="green")
        self.result_label.grid(row=row, column=0, sticky="w", padx=10)
        row += 1

        self.details_label = tk.Label(self.root, text="", justify="left")
        self.details_label.grid(row=row, column=0, sticky="w", padx=10)
        row += 1

        # Buttons
        tk.Button(self.root, text="Calculate Points", command=self.calculate_points, bg="#0366d6", fg="white").grid(row=row, column=0, pady=5, padx=10, sticky="w")
        row += 1
        tk.Button(self.root, text="Show Details", command=lambda:[self.calculate_points(), self.show_details()], bg="#0366d6", fg="white").grid(row=row, column=0, pady=5, padx=10, sticky="w")

    def update_clb(self, event):
        teer = self.selected_values['LanguageProficiency TEER'].get()
        if teer:
            clb_options = list(self.points_mapping['LanguageProficiency'][teer].keys())
            self.clb_menu['values'] = clb_options
            self.clb_menu.current(0)

    def calculate_points(self):
        self.section_scores = {}
        job_offer_total = 0
        human_capital_total = 0

        for category, var in self.selected_values.items():
            score = 0
            val = var.get()
            if category in ['Close Family in Community','Community Involvement','Property in Community','Spouse/Common-law Experience']:
                if val == "Yes":
                    score = self.points_mapping[category][0]
                score = min(score, self.max_scores[category])
            elif category == 'LanguageProficiency TEER':
                teer = self.selected_values['LanguageProficiency TEER'].get()
                clb = self.selected_values['LanguageProficiency CLB'].get()
                if teer and clb:
                    score = self.points_mapping['LanguageProficiency'][teer][clb]
                score = min(score, self.max_scores['LanguageProficiency'])
            elif category == 'Previous Work/Study in Community':
                idx = ["None","1 year (combined)","2 years (combined)","3 years or more (combined)"].index(val)
                score = 0 if idx==0 else self.points_mapping[category][idx-1]
            elif category.startswith("Job Offer") or category.startswith("Human Capital"):
                idx = self.categories[category].index(val)
                score = min(self.points_mapping[category][idx], self.max_scores[category])

            self.section_scores[category] = score
            if category.startswith('Job Offer'):
                job_offer_total += score
            elif category.startswith('Human Capital') or category in ['Previous Work/Study in Community','Close Family in Community','Community Involvement','Property in Community','Spouse/Common-law Experience']:
                human_capital_total += score

        total_job_offer = min(job_offer_total,25)
        total_human = min(human_capital_total,100)
        total_points = total_job_offer + total_human

        self.result_label.config(text=f"Total Points for Job Offer: {total_job_offer} / 25\n"
                                      f"Human Capital Assessment: {total_human} / 100\n"
                                      f"Total Points: {total_points} / 125")
        self.details_label.config(text="")

    def show_details(self):
        text = ""
        bonus_total = 0
        for category, score in self.section_scores.items():
            if category in ['Previous Work/Study in Community','Close Family in Community','Community Involvement','Property in Community','Spouse/Common-law Experience']:
                bonus_total += score
            else:
                max_score = self.max_scores.get(category,"")
                text += f"{category}: {score} / {max_score}\n"
        bonus_total = min(bonus_total,15)
        text += f"Bonus Points: {bonus_total} / 15\n"
        self.details_label.config(text=text)


if __name__ == "__main__":
    root = tk.Tk()
    app = RCIPCalculator(root)
    root.mainloop()
