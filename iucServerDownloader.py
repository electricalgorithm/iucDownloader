import requests, os, time

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

tempCookieOBS = "_ga=GA1.3.382159817.1566239795; _gid=GA1.3.624255600.1593989698; admin_leftbar_collapse=collapse-leftbar; ASP.NET_SessionId=rzt0g0nueow0e0am05oo0xc1; _gat_gtag_UA_123642408_2=1; .OGRISFormAuth=1CDE165BC19E39C1FFD34E83D2F5271B43BC72ECEE021BEBA21A1568006A9FBC06EEAD933718091331246BE9B442E0E103583C9E42FD210FD24E03F37CE440EBEA315CF95110B625B08DD781DBD4812D2DDAAEF07B302FF9AE351762298BB19A1B28F9014DCB4A60ABB047AA12117F8D2A428477A36DD1300761FB49053BB66D5A412FEC14612D14345DB7488673B3DAE72E2C8380ED0591D692E442E69C5231207302C9494393BE3D1EA26E784CF665A2B104900A8B8C7B45F8EAB3B6B8415B6E5BF4E4; _gat_gtag_UA_123642408_3=1"
academicProgramList = academicPrograms()

path = os.getcwd()
for index in range(600000, 700000, 1):
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