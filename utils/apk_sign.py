import os
from subprocess import Popen,PIPE

def make_sign(rsa_name,password,name,commpany,organization,city,province,country):
    s = Popen("keytool -genkeypair -alias {} -keyalg RSA -validity 2000 -keystore ./media/sign/{}.jks".format(rsa_name,rsa_name), stdout=PIPE, stdin=PIPE,shell=True)
    s.stdin.write((password + '\n').encode())
    s.stdin.write((password + '\n').encode())
    s.stdin.write((name + '\n').encode())
    s.stdin.write((commpany + '\n').encode())
    s.stdin.write((organization + '\n').encode())
    s.stdin.write((city + '\n').encode())
    s.stdin.write((province + '\n').encode())
    s.stdin.write((country + '\n').encode())
    s.stdin.write(('y' + '\n').encode())
    s.stdin.write((password + '\n').encode())
    s.stdin.write((password + '\n').encode())
    s.stdin.close()

def commpress_apk(apk_path):
    # Popen("/Users/abc/Desktop/build-tools/29.0.0/zipalign -v -p 4 '{}'  ./media/commpress/out.apk".format(apk_path),shell=True)
    Popen("zipalign -v -p 4 '{}'  ./media/commpress/out.apk".format(apk_path),shell=True)
def apk_sign(sign_path,apk_name):
    # print(os.path.exists(sign_path))
    while True:
        if os.path.exists('./media/commpress/out.apk') and os.path.exists(sign_path):
            # print("apksigner sign --ks '{}' --ks-pass pass:123456 --out ./media/out/{}.apk './media/commpress/out.apk'".format(sign_path,apk_name))
            os.system("apksigner sign --ks '{}' --ks-pass pass:123456 --out ./media/out/{}.apk './media/commpress/out.apk'".format(sign_path,apk_name))
            os.system('rm ./media/commpress/out.apk')
            break
