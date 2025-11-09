import PyPDF2

file_paths = [
    r"C:\Users\Win_11\Downloads\Thomas-Calculus.pdf",
    r"C:\Users\Win_11\Downloads\ANADOLU UNI GENEL MAT.pdf",
    r"C:\Users\Win_11\Downloads\temelmatematik.pdf",
    r"C:\Users\Win_11\Downloads\8.Hafta.pdf",
    r"C:\Users\Win_11\Downloads\2.Hafta.pdf",
    r"C:\Users\Win_11\Downloads\3.Hafta.pdf",
    r"C:\Users\Win_11\Downloads\4.Hafta.pdf",
    r"C:\Users\Win_11\Downloads\5.Hafta.pdf",
    r"C:\Users\Win_11\Downloads\6.Hafta.pdf",
    r"C:\Users\Win_11\Downloads\7.Hafta.pdf",
    r"C:\Users\Win_11\Downloads\1.Hafta.pdf"
]

output_path = "data.txt"

with open(output_path, "a", encoding="utf-8") as output_file:
    for file_path in file_paths:
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                output_file.write(f"\n\n--- {file_path.split('\\')[-1]} ---\n\n")
                output_file.write(text)
                print(f" {file_path} eklendi.")
        except Exception as e:
            print(f" {file_path} okunamadı: {e}")

print("\nTüm PDF'ler başarıyla data.txt dosyasına eklendi.")
