import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase özel anahtar dosyanı yükle
cred = credentials.Certificate("C:/Users/user/Downloads/coursecheckerdb-firebase-adminsdk-fbsvc-283474d885.json")
firebase_admin.initialize_app(cred)

# Firestore bağlantısı
db = firestore.client()

excel_path = r"C:\Users\user\OneDrive\Masaüstü\coursecheckerPY\dersler.xlsx"

df = pd.read_excel(excel_path)

# Departman adlarını belirleyelim
departments = ["CENG", "EE", "ECE", "IE", "CE", "ME", "MSE", "MECE", "SENG"]

# Verileri Firebase'e kaydetme
def save_to_firestore(df):
    # Her bir satırı döngüye al
    for index, row in df.iterrows():
        course_data = {
            "course_code": row['DERS'],
            "course_name": row['CREDIT'],  # Dersin adı genellikle 'CREDIT' değil, 'DERS' sütununda
            "credit": row['CREDIT'],
            "ects": row['ECTS'],
            "name": row ['NAME'],
            "departments": []  # Uygun departmanları buraya ekleyeceğiz
        }
        
        # Her bir departman için uygun olup olmadığını kontrol et
        for department in departments:
            if pd.notna(row[department]) and row[department] == 'X':  # Eğer 'X' işareti varsa
                course_data["departments"].append(department)
        
        # Veriyi Firebase'e kaydet
        for department in course_data["departments"]:
            collection_ref = db.collection(f"{department}_ELECTIVE_SOCIAL")  # Örnek: CENG_ELECTIVE_SOCIAL
            collection_ref.add(course_data)
            print(f"Course {row['DERS']} added to {department}_ELECTIVE_SOCIAL")

# Verileri kaydedelim
save_to_firestore(df)