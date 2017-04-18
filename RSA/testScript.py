from Crypto.PublicKey import RSA
import RSATool
import os

keys =[]

def loadBostonKeyPartyPEMs():
    for i in range(7):
        key = RSA.importKey(open('testKeys/key-%s.pem' % i).read())
        keys.append(key)

def main():
    loadBostonKeyPartyPEMs()

    print("[#] Checking factorModulii with Boston Key Party keys")
    # CHECK FOR ERRORS:
    # key-0, key-6 is GCD
    # key-1 is Fermat Attack
    # key-2 is Factordb
    # key-3 is Wiener Attack
    # key-4 is KEY NOT FOUND
    # key-5 is P-1 attack
    tool.factorModulii(keys,'/tmp/privkey-%s.pem')
    print("[*] Boston Key Party Checks completed")

    print("[#] Checking Sieved Fermat Attack")
    checkSievedFermatAttack()
    print("[#] Checking broken pub exp attack")
    checkBrokenPublicExponent()
    print("[#] Checking Half D Partial Key Recovery")
    checkHalfdPartialKeyRecoveryAttack()

def checkSievedFermatAttack():
    # primes taken from https://en.wikipedia.org/wiki/Prime_gap
    # Any primes would work, just these were easily accesible and spaced far apart
    p = int("1,294,268,491".replace(',',''))
    q = int("2,300,942,549".replace(',',''))
    tool.sieveFermatAttack(p*q,limit=100000000)
    if(tool.q == q or tool.q == p):
        print("[*] Sieved Fermat Factorization Check Passed")
    else:
        print("[x] q = %s" % tool.q)
        print("[x] p = %s" % tool.p)
        print("[x] Sieved Fermat Factorization Check FAILED")

def checkBrokenPublicExponent():
    #Using EasyCTF RSA 4 values
    p= 13013195056445077675245767987987229724588379930923318266833492046660374216223334270611792324721132438307229159984813414250922197169316235737830919431103659
    q= 12930920340230371085700418586571062330546634389230084495106445639925420450591673769061692508272948388121114376587634872733055494744188467315949429674451947
    e= 100
    C= 2536072596735405513004321180336671392201446145691544525658443473848104743281278364580324721238865873217702884067306856569406059869172045956521348858084998514527555980415205217073019437355422966248344183944699168548887273804385919216488597207667402462509907219285121314528666853710860436030055903562805252516

    RSASolver = RSATool.RSATool()
    RSASolver.invalidPubExponent(C,p,q,e)
    plaintext = str(bytearray.fromhex(hex(RSASolver.invalidPubExponent(C,p,q,e))[2:]))

    if('easyctf' in plaintext.lower()):
        print("Broken Public Exponent Check Passed")
    else:
        print("Broken Public Exponent Check FAILED")

def checkHalfdPartialKeyRecoveryAttack():
    # Using EasyCTF PremiumRSA Values
    n = int('0x6c451672f63e8ece9c3bde03f4483ed3d0e286c908a55b78e2d235021d95f4ba403e6cbaf14d15928867bb14ac855d7fbdc6ebbf99f151ab49832e70fdd19e8d29dfc4c4ca7329564a1d4182c1b02ef040d7e347e13db768203319357abe07b1ecaf5d099d3326d2639e0a5991ded8cb46b825709e0942e67f770520c26306e5f44c8ca72313106ff0dd9a90294edaa7e0097997ff2425c266e1d52c6935799a8cf7ebf12f88edd1dc683ffd252facf7fb3e9bca0467ebbb1dbe731e7ff9b245a78ca50e8f810202eef4e44ea0c01443584baf727b13aa2ba8978445345981a264fb15709f7b71b9611e0ef3f0b69c6a3ba9f12ea703bf742b3aa3fc1522d8d20466223bdfe5c2cc726d66a1416bcb26cab2976a915e6646143500e012896f355dea77e10a7ec36aacd547f66bf543a7d7841acbcd4f54ec267ad185984ef74a995ad7c141fa34f46956bb3d66db54c5f8f84252800d968cb1bd47b30030f3c54c8d45b2ed9e1809ae7aad3367a7d3b11c80539282b3deaa8e23bda567e09b87f33a60666e9247cc38c0d09666346d54e18fcd58e987fcfc1796ad4bc0cb498d5e100d640abdbdfcb45039464fe023679ad70fce916a5adffcb58520a22bbf1870cfe5fcbf651a30ace03a716b2a283bfaa076330abd502e1460f2182e64b565c3c1b3a77312fe98e77dd1b8eca1f80fe11d6f2675f9ea90cc533abd507dc285',0)
    e = int('0x10001',0)
    d0 = int('0xa5cb79ef8059485d8ee47a9da0ed128ea83febf509c009aafcada53d35b28a7b020f7308078257aae306052f2086fa89ad9c810a4fd9afe498825bdc16b3050e6e26c2ebcc49de22ab34c09e53a699f29252adc01c1a3c036f192105154d94858bbaf42bf1dfadc0cdf7338c5c9e9fdf9c508bdc9d260df831b781e5ce33b874999ebb0f07d72bbe6d0971a2164b660e1d3df4cb265e8edbc63ec56c2b05ce2eb32cf9808931a3968f1045c38ea022bfd750c3925073d1c5befec2268efe0bd047f2411f081aee2b71c443c5fd26fed6a75c9e31b89dfd93180215eaa51117bcf4be54f140fc39322c5deb32ae1ec164f4ae451a1391d7b612645c06cdf83541',0)
    c =  int('0x36e7437512d71ca2a412fa411f7d376feaf02db7a6c301284ed9dc7dcffa8a658c24d199aa14d008ed72a88e36e2c5520caf95c88e5deb0d311d4fe2641732455bde7bc1c64a7274bcbe3825cd59b66727354fbbd01ab4ea39dbddd765395fa9c653556987f2f7efbdf86e741573338699e7fb7ad8405eeb02bc8fbca39a55870255328fcd44998bb5339805298575c0aef9bcfe791e8330bac92cd11620ad837ac2f7e9fcc4bf61da3c09cb8455e6d46890d5beb0b1af0bf989c10c6d83604de862bbb82fc697c2513488a9e3321d2590e9f5c0eb4a1882aa26c455da6e45f1fff42e233208ebd494365e89fb8e1ae89ea5b2f800e07b9e6b362bf4caaec11e81a8fc04377a7820f1392057f44bcbac03e9846b29989106e0dcf98559af1d5221aea01dd0d64667eb6615f7cce13e004249f2a0ccf065044450c1bd6661a986a53c983bf810d961f5c0a551fa66a08cf6cabf4e08291f1a08c7ee73c3b7c51a6d1620c9005530b8c1ce883eae095b1949eb4df159a35c7ce654cfc18527f08c8483d3630803bd688040a4b4bae86766f5535421bb8ec9c6e071b280f9e0db26c1cc90b56dba1cd09adeb520a996d6fd6ce135edb9e496986770cff49abc68473edc51ce0c79db915aae4ce1bb6fd42adb62b6b350cb84d37c52f30fe1e4943babf868bed50fa912ca431500ecb18643bb3df560450f673769818fdc48cdcdf6',0)
    bitLenD0 = 2048

    privkey = tool.halfdPartialKeyRecoveryAttack(d0,2048,n=n,e=e)
    c = pow(c,tool.modinv(e, (tool.p-1)*(tool.q-1)) ,n)
    plaintext = str(bytearray.fromhex(hex(c)[2:]))
    if('easyctf' in plaintext.lower()):
        print("Half D Partial Key Recovery Check Passed")
    else:
        print("Half D Partial Key Recovery Check FAILED")

tool = RSATool.RSATool()
main()
