import requests
import os
from datetime import datetime


class Mimosa:
    def __init__(self, ips):
        self.ips = ips
        self.dirName = "BackupMimosa"
        self.nameArqLog = "logoBackupMimosa.log"
        self.data  = {"username": "configure", "password":"rs%$p33d"}
        self.file = open(self.nameArqLog, 'a')
        self.s = requests.Session()

    def login(self, ip):
        urlLogin = "http://{}/?q=index.login&mimosa_ajax=1".format(ip)
        r = self.s.post(urlLogin, data=self.data)
        return r.status_code

    def Download(self):
        for ip in self.ips:
            day = datetime.now()
            try:
                #print("Realizando Backup da Mimosa do ip:{}".format(ip[1]))
                self.file.write("\n ========= {} ===========\n".format(day))
                self.file.write("Realizando Backup da Mimosa do ip: {}\n".format(ip[1]))
                if self.login(ip[1]) != 200:
                    #print("Ops! Erro ao logar")
                    self.file.write("Ops! Erro ao logar\n")
                if os.path.isdir(self.dirName) == False:
                    self.file.write("Criando Diretorio de BKP\n")
                    os.mkdir(self.dirName)
                urlDowload = "http://{}/?q=preferences.configure&mimosa_action=download".format(ip[1])
                r= self.s.get(urlDowload, allow_redirects=True)
                
                #2021-12-13 20:12:46.527819
                #2021-12-13_172.16.16.16_nome.conf
                path = "{}/{}_{}_{}.conf".format(self.dirName,str(day).split(" ")[0], ip[1], ip[0])
                open(path, 'wb').write(r.content)
                self.file.write("Salvando Arquivo em {}\n".format(path))
            except:
                #print("ops!")
                self.file.write("Erro ao Processar!\n")
                continue
        self.file.write("=======================\n")
        self.file.close


def main():
    ips = [
        ["CRI-PTP-FRAN", "172.17.8.8"],
        ["FRAN-PTP-CRI", "172.17.8.9"]
    ]
    m = Mimosa(ips)
    m.Download()

if __name__ == "__main__":
    main()