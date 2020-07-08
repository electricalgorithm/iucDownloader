# Bu programın yazım şekli, verdiğim değişken adları,
# karmaşık görüntü vesaire kesinlikle benim stilimi
# yansıtmamaktadır. GitHub'dan diğer projelerime ba-
# kabilirsiniz. Kafamın dolu olduğu bir dönem bu 
# proje ile uğraştığım için bu hale geldi. Bayrak
# sistemi getirmeyi denemiştim, sanırım getopt'u 
# kullanmayı unutmuşum. Katkılarınız öğrenciler için
# faydalı olacaktır.
# ---------------------o------------------------
# Eğer ki bunu okuyan kişi bir yetkili ise bana 
# ulaşabilir ve kaldırmamı talep edebilir, direk
# de kaldırırım zaten. Çok da önemli değil.
# Ben sadece POST metotu ile bölüm doğrulama
# olmadan döküman istendiğini gördüğümde kendimle
# yarışa girmek için bu programı yazmıştım.
# Alengirli bir amacım yoktu.
# --------------------o--------------------------
# Umarım daha güvenli yeni bir sistem ile İÜC kendini 
# geliştirecektir. BTK'nın MERGEN'ine geçmesi ile
# namını yeraltına götürdüğü bir gerçektir.

import requests, os, time, getopt, sys

def academicPrograms():
    res = requests.get("https://ebs.istanbulc.edu.tr/home/getdata/?id=3")
    programs = []
    for i in range(0, 12):
        for j in range (0, 20):
            try: 
                program = {
                    "programAdi": res.json()[i]["nodes"][j]["text"],
                    "programKodu": res.json()[i]["nodes"][j]["id"],
                    "fakulteIsmi": res.json()[i]["text"]
                }
            except IndexError:
                continue
            programs.append(program)
    return programs
def lectureDetails(lecID):
    
    bodyJson = '{"request":{"DersGrupID":"' + str(lecID) + '","Language":"tr"}}'
    head = {
        "Host": "ebs.istanbulc.edu.tr",
        "User-Agent": "iucServerDownloader/v001",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Origin": "https://ebs.istanbulc.edu.tr",
        "Content-Type": "application/json; charset=utf-8",
        "Referer": "https://ebs.istanbulc.edu.tr/",
        "Cookie": "",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Content-Length": "51",
        "X-Requested-With": "XMLHttpRequest"
        }
    res = requests.post("https://ebs.istanbulc.edu.tr/Home/GetPrintData", headers=head, data=bodyJson)
    if not res.status_code == 500:
        if res.json()["IsSuccess"] == 1:
            lectureDetailsAns = {
                "isim": res.json()["Object"]["DersAd"],
                "donem": res.json()["Object"]["DersYariyil"],
                "bolum": res.json()["Object"]["DiplomaProgrami"],
                "fakulte": res.json()["Object"]["Fakulte"],
                "dil": res.json()["Object"]["DersDil"]
            }

            return lectureDetailsAns
    else:
        return None
def documentList(lecID):
    meanData = []
    if not lectureDetails(lecID) == None:
        bolumName = lectureDetails(lecID)["bolum"]
        for i in range(0, len(academicProgramList)):
            if academicProgramList[i]["programAdi"] == bolumName:
                depID = academicProgramList[i]["programKodu"]
                url = "http://obs.istanbulc.edu.tr/Dokuman/Dokuman/DersIzlence"
                bodyJson = '{"oGRDersGrupID":' + str(lecID) + ',"birimID":' + str(depID) + '}'
                head = {
                    "Host": "obs.istanbulc.edu.tr",
                    "User-Agent": "iucServerDownloader/v001",
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Origin": "http://obs.istanbulc.edu.tr",
                    "Content-Type": "application/json;charset=utf-8",
                    "Referer": "http://obs.istanbulc.edu.tr/Dokuman/Dokuman/Index",
                    "Cookie": tempCookieOBS,
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "Content-Length": "39"
                    }
                res = requests.post(url, headers=head, data=bodyJson)
                for index in res.json():
                    if index["DokumanTuru"] != "Link":
                        tempData = {
                            "name": index["FileName"],
                            "FileId": index["FileId"]
                        }
                        meanData.append(tempData)
    return meanData

print('''
Programın çalışabilmesi için OBS.istanbulc.edu.tr adresinden cookielerinizi almalısınız. 
Bunun için F12'ye basarak geliştirici seçeneklerini açabilir ve network/ağ panelinden
herhangi bir GET/POST olayına tıklayarak "cookie" kısmını direk kopyalayabilirsiniz.
Unutmayınız ki bir cookie'nin geçerlilik süresi 20 dakika kadardır.
Örnek cookie:

_ga=GA1.3.382159817.1566239795; admin_leftbar_collapse=collapse-leftbar; _gid=GA1.3.1439038013.1594151929; .OGRISFormAuth=043CC990CE8FDB35FFDD446A68629CC3829FC301973421160DAA7500EEF2FAD90876FE0FF9741267772A123EF17A4E387E638018CE6A20400CF9FA990643096FC108A81D536428DB545CB35A6FCC471CDF3FC3D2AE1109C82A97151B74836DD6F15A2F75BD6C493E94DB818A91A2C77A64A9C1977EA3F16A461D143A6927DD9EB398FAC38B47832B3A795FC6FC0DE26BF33C4B9352B69606CD7757B1ECE8F195668A60CEBA4AAE6C574A48D2A8A48F64458ED5A534DDEC83EBC3AB80944A02DE8FA8F7A4; _gat_gtag_UA_123642408_2=1; ASP.NET_SessionId=hnyfshv4mnea0hp3uk1er0uw; _gat_gtag_UA_123642408_3=1

''')

tempCookieOBS = input("Cookie'yi buraya kopyalayın (CTRL+SHIFT+V): ")
academicProgramList = academicPrograms()
path = os.getcwd()

print("""
### İÜC Döküman İndirme/Bulma ###
1) EBS'deki kod ile ders dökümanlarını indirme
2) Seçilen aralıkta bulunan ders kodlarının 
tüm dökümanlarını indirme

Çıkış için CTRL+Z

Not: Dökümanlar bir HTML sayfasına kaydedilir.
Programın bulunduğu klasörde bu sayfayı görebilirsiniz.
""")

choose = input("Yapmak istediğiniz işlemin numarasını giriniz: ")
if choose == "1":
    lessonWanted = int(input("Ders Kodunu giriniz (EBS.istanbulc.edu.tr): "))
    if lessonWanted >= 100000:
        lectureDetails_ = lectureDetails(lessonWanted)
        lectureName = lectureDetails_["isim"]
        lectureDepart = lectureDetails_["bolum"]
        lectureFaculty = lectureDetails_["fakulte"]
        documentListe = documentList(lessonWanted)
        print("--- " + lectureName)
        if not os.path.isfile(os.path.join(path, lectureDepart) + ".html"):
            with open(os.path.join(path, lectureDepart) + ".html", "w") as html:
                veriler = ""
                for dokuman in documentListe:
                    veriler += f"<tr><td>{dokuman['name']}</td><td><a href='http://obs.istanbulc.edu.tr/Dokuman/Dokuman/DokumanIndir?FileId={dokuman['FileId']}'>İndir</a></td></tr>"
                htmlSkeleton = f"""
                <!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{lectureDepart} IUC</title></head>
                <body><h1 style="text-align: center;">{lectureDepart}</h1><br><br><b>{lectureName}</b>
                <table style="border: 0.5px solid black;"><tr><th>Döküman Adı</th><th>İndirme Bağlantısı</th></tr>{veriler}</table></body></html>
                """
                html.write(htmlSkeleton)
                print("Hazır. Kaydedilen yol:", path)
        else:
                with open(os.path.join(path, lectureDepart) + ".html", "a") as html:
                    veriler = ""
                    for dokuman in documentListe:
                        veriler += f"<tr><td>{dokuman['name']}</td><td><a href='http://obs.istanbulc.edu.tr/Dokuman/Dokuman/DokumanIndir?FileId={dokuman['FileId']}'>İndir</a></td></tr>"
                    htmlSkeleton = f"""<br><b>{lectureName}</b>
                    <table style="border: 0.5px solid black;"><tr><th>Döküman Adı</th><th>İndirme Bağlantısı</th></tr>{veriler}</table></body></html>
                    """
                    html.write(htmlSkeleton)
                    print("Hazır. Kaydedilen yol:", path)
    else:
        print("Ders kodunda bir sorun var gibi görülüyor.")
elif choose == "2":
    startPoint = int(input("Taramanın yapılacağı başlangıç ders numarası: "))
    endPoint = int(input("Taramanın yapılacağı bitiş ders numarası: "))
    if startPoint > 0 and startPoint < 999999 and endPoint < 999999 and endPoint > startPoint:
        for index in range(startPoint, endPoint, 1):
            print(index)
            while True:
                try:
                    if len(documentList(index)) != 0:
                        print("--- FOUND ---")
                        lectureDetails_ = lectureDetails(index)
                        lectureName = lectureDetails_["isim"]
                        lectureDepart = lectureDetails_["bolum"]
                        lectureFaculty = lectureDetails_["fakulte"]
                        documentListe = documentList(index)
                        print("--- " +lectureDepart)
                        try:
                            os.makedirs(os.path.join(path, "iucDokumanlar", lectureFaculty))
                            try:
                                with open(os.path.join(os.path.join(path, "iucDokumanlar", lectureFaculty), lectureDepart) + ".html", "w") as html:
                                    veriler = ""
                                    for dokuman in documentListe:
                                        veriler += f"<tr><td>{dokuman['name']}</td><td><a href='http://obs.istanbulc.edu.tr/Dokuman/Dokuman/DokumanIndir?FileId={dokuman['FileId']}'>İndir</a></td></tr>"
                                    htmlSkeleton = f"""
                                    <!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{lectureDepart} IUC</title></head>
                                    <body><h1 style="text-align: center;">{lectureDepart}</h1><br><br><b>{lectureName}</b>
                                    <table style="border: 0.5px solid black;"><tr><th>Döküman Adı</th><th>İndirme Bağlantısı</th></tr>{veriler}</table></body></html>
                                    """
                                    html.write(htmlSkeleton)
                            except:
                                with open(os.path.join(os.path.join(path, "iucDokumanlar", lectureFaculty), lectureDepart) + ".html", "a") as html:
                                    veriler = ""
                                    for dokuman in documentListe:
                                        veriler += f"<tr><td>{dokuman['name']}</td><td><a href='http://obs.istanbulc.edu.tr/Dokuman/Dokuman/DokumanIndir?FileId={dokuman['FileId']}'>İndir</a></td></tr>"
                                    print(veriler)
                                    html.write(f"<br><b>{lectureName}</b><table style='border: 0.5px solid black;'><tr><th>Döküman Adı</th><th>İndirme Bağlantısı</th></tr>{veriler}</table>")
                        except OSError:
                            if not os.path.isfile(os.path.join(path, "iucDokumanlar", lectureFaculty, lectureDepart) + ".html"):
                                with open(os.path.join(path, "iucDokumanlar", lectureFaculty, lectureDepart) + ".html", "w") as html:
                                    veriler = ""
                                    for dokuman in documentListe:
                                        veriler += f"<tr><td>{dokuman['name']}</td><td><a href='http://obs.istanbulc.edu.tr/Dokuman/Dokuman/DokumanIndir?FileId={dokuman['FileId']}'>İndir</a></td></tr>"
                                    htmlSkeleton = f"""
                                    <!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{lectureDepart} IUC</title></head>
                                    <body><h1 style="text-align: center;">{lectureDepart}</h1><br><br><b>{lectureName}</b>
                                    <table style="border: 0.5px solid black;"><tr><th>Döküman Adı</th><th>İndirme Bağlantısı</th></tr>{veriler}</table></body></html>
                                    """
                                    html.write(htmlSkeleton)
                            else:
                                with open(os.path.join(os.path.join(path, "iucDokumanlar", lectureFaculty), lectureDepart) + ".html", "a") as html:
                                    veriler = ""
                                    for dokuman in documentListe:
                                        veriler += f"<tr><td>{dokuman['name']}</td><td><a href='http://obs.istanbulc.edu.tr/Dokuman/Dokuman/DokumanIndir?FileId={dokuman['FileId']}'>İndir</a></td></tr>"
                                    html.write(f"<br><b>{lectureName}</b><table style='border: 0.5px solid black;'><tr><th>Döküman Adı</th><th>İndirme Bağlantısı</th></tr>{veriler}</table>")
                except requests.exceptions.ConnectionError:
                    print("Sleep time! Zzzzzz....")
                    time.sleep(15)
                    continue
                break
    else: 
        print("Girdiğiniz değerleri kontrol ediniz.")
else: 
    print("Girdiğiniz seçim hatalı.")
