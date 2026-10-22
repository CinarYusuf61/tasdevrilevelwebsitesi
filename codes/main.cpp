#include <iostream>
#include <string>

using namespace std;

int main() {
    double sonuc = 0;
    string giris;

    cout << "=== Kesintisiz C++ Hesap Makinesi ===" << endl;
    cout << "Ilk sayiyi girin: ";
    
    while (true) {
        cin >> giris;
        try {
            sonuc = stod(giris);
            break;
        } catch (...) {
            cout << "Gecersiz giris! Tekrar ilk sayiyi girin: ";
        }
    }

    while (true) {
        cout << "Islem ve yeni sayi girin (Orn: + 5, * 2) [Cikis icin 'q']: ";
        char islem;
        cin >> islem;

        if (islem == 'q' || islem == 'Q') {
            break;
        }

        string sayiStr;
        cin >> sayiStr;
        
        double sayi = 0;
        try {
            sayi = stod(sayiStr);
        } catch (...) {
            cout << "Gecersiz sayi! Tekrar deneyin." << endl;
            continue;
        }

        switch (islem) {
            case '+':
                sonuc += sayi;
                break;
            case '-':
                sonuc -= sayi;
                break;
            case '*':
                sonuc *= sayi;
                break;
            case '/':
                if (sayi != 0) {
                    sonuc /= sayi;
                } else {
                    cout << "Hata: Bir sayi sifira bolunemez!" << endl;
                }
                break;
            default:
                cout << "Gecersiz operator! (+, -, *, / kullanin)" << endl;
                continue;
        }

        cout << "Guncel Sonuc: " << sonuc << endl;
        cout << "-----------------------------------" << endl;
    }

    cout << "Hesaplama bitti. Toplam Sonuc: " << sonuc << endl;
    cout << "Iyi gunler dileriz!" << endl;
    
    return 0;
}