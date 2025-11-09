from bs4 import BeautifulSoup
import requests
import time
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}




output_file = "data.txt"


urls = [
    "https://tr.wikipedia.org/wiki/Aritmeti%C4%9Fin_temel_teoremi",
    "https://tr.wikipedia.org/wiki/Cebirin_temel_teoremi",
    "https://tr.wikipedia.org/wiki/Kalk%C3%BCl%C3%BCs%C3%BCn_temel_teoremi",
    "https://tr.wikipedia.org/wiki/Riemann_hipotezi",
    "https://tr.wikipedia.org/wiki/Olas%C4%B1l%C4%B1k_teorisi",
    "https://tr.wikipedia.org/wiki/Matematiksel_g%C3%B6sterim",
    "https://tr.wikipedia.org/wiki/Temel_cebir",
    "https://tr.wikipedia.org/wiki/Karma%C5%9F%C4%B1k_analiz",
    "https://tr.wikipedia.org/wiki/Ger%C3%A7el_analiz",
    "https://tr.wikipedia.org/wiki/Belirsiz_integral",
    "https://tr.wikipedia.org/wiki/Adi_logaritma",
    "https://tr.wikipedia.org/wiki/Karma%C5%9F%C4%B1k_say%C4%B1",
    "https://tr.wikipedia.org/wiki/Mutlak_de%C4%9Fer",
    "https://tr.wikipedia.org/wiki/Limit#%CE%B5-%CE%B4_limit_tan%C4%B1m%C4%B1",
    "https://tr.wikipedia.org/wiki/De%C4%9Fi%C5%9Fken_(matematik)",
    "https://tr.wikipedia.org/wiki/Türev",
    "https://tr.wikipedia.org/wiki/Integral",
    "https://tr.wikipedia.org/wiki/Matris",
    "https://tr.wikipedia.org/wiki/Fonksiyon",
    "https://tr.wikipedia.org/wiki/Matematik",
    "https://tr.wikipedia.org/wiki/Matematiksel_ispat",
    "https://tr.wikipedia.org/wiki/Geometri",
    "https://tr.wikipedia.org/wiki/Aritmetik",
    "https://tr.wikipedia.org/wiki/Cebir",
    "https://tr.wikipedia.org/wiki/Kalk%C3%BCl%C3%BCs",
    "https://tr.wikipedia.org/wiki/Say%C4%B1",
    "https://tr.wikipedia.org/wiki/Do%C4%9Fal_say%C4%B1",
    "https://tr.wikipedia.org/wiki/Tam_say%C4%B1",
    "https://tr.wikipedia.org/wiki/Rasyonel_say%C4%B1",
    "https://tr.wikipedia.org/wiki/%C4%B0rrasyonel_say%C4%B1",
    "https://tr.wikipedia.org/wiki/Reel_say%C4%B1",
    "https://tr.wikipedia.org/wiki/Ard%C4%B1%C5%9F%C4%B1k_say%C4%B1lar",
    "https://tr.wikipedia.org/wiki/Analiz_(matematik)",
    "https://tr.wikipedia.org/wiki/Trigonometrik_fonksiyonlar",
    "https://tr.wikipedia.org/wiki/%C3%96nerme",
    "https://tr.wikipedia.org/wiki/%C3%96klid%27in_Elementleri",
    "https://tr.wikipedia.org/wiki/Limit",
    "https://tr.wikipedia.org/wiki/S%C3%BCreklilik",
    "https://tr.wikipedia.org/wiki/Kesir",
    "https://tr.wikipedia.org/wiki/Polinom",
    "https://tr.wikipedia.org/wiki/Perm%C3%BCtasyon",
    "https://tr.wikipedia.org/wiki/Kombinasyon",
    "https://tr.wikipedia.org/wiki/Logaritma",
    "https://tr.wikipedia.org/wiki/%C3%9Cstel_fonksiyon",
    "https://tr.wikipedia.org/wiki/Dizi",
    "https://tr.wikipedia.org/wiki/Seri",
    "https://tr.wikipedia.org/wiki/Say%C4%B1lar_teorisi",
    "https://tr.wikipedia.org/wiki/Diferansiyel_denklem",
    "https://tr.wikipedia.org/wiki/Fermat%27n%C4%B1n_son_teoremi",
    "https://tr.wikipedia.org/wiki/Riemann_hipotezi",
    "https://tr.wikipedia.org/wiki/S%C3%BCreklilik_hipotezi",
    "https://tr.wikipedia.org/wiki/Kalk%C3%BCl%C3%BCs%C3%BCn_temel_teoremi",
    "https://tr.wikipedia.org/wiki/Cebirin_temel_teoremi",
    "https://tr.wikipedia.org/wiki/Say%C4%B1sal_analiz",
    "https://tr.wikipedia.org/wiki/Olas%C4%B1l%C4%B1k",
    "https://tr.wikipedia.org/wiki/Saf_k%C3%BCme",
    "https://tr.wikipedia.org/wiki/%C4%B0%C5%9Flem",
    "https://tr.wikipedia.org/wiki/K%C3%BCme",
    "https://tr.wikipedia.org/wiki/Kartezyen_%C3%A7arp%C4%B1m%C4%B1",
    "https://tr.wikipedia.org/wiki/Tan%C4%B1m_k%C3%BCmesi",
    "https://tr.wikipedia.org/wiki/G%C3%B6r%C3%BCnt%C3%BC_k%C3%BCmesi",
    "https://tr.wikipedia.org/wiki/Bo%C5%9F_k%C3%BCme",
    "https://tr.wikipedia.org/wiki/Bo%C5%9F_fonksiyon",
    "https://tr.wikipedia.org/wiki/Karek%C3%B6k",
    "https://tr.wikipedia.org/wiki/Negatif_say%C4%B1",
    "https://tr.wikipedia.org/wiki/Sabit_fonksiyon",
]

for url in urls:
    try:
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        
        paragraphs = soup.find_all("p")
        
        with open(output_file, "a", encoding="utf-8") as f:  
            for p in paragraphs:
                text = ''.join(p.strings).strip() 
                if text:  
                    f.write(text + "\n\n")  
        
        print(f"{url} sayfası başarıyla kaydedildi.")
        time.sleep(2)  

    except Exception as e:
        print(f"Hata oluştu {url} için:", e)