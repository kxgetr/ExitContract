# ExitContract

İki CLI sürümünün çıkış kodunu, stdout ve stderr baytlarını vaka bazında karşılaştırır.

## Kullanım

Python 3.11 veya üzeri.

```sh
python exitcontract.py /path/to/old /path/to/new --cases cases.json
```

cases.json biçimi: [{"name":"help","args":["--help"],"stdin":""}]. Her çalıştırma boş geçici dizinde başlar. 0 eşit, 1 fark, 2 yürütme hatası.

## Doğrulama

```sh
python verify.py
```

MIT lisansı.
