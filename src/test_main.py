from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_cryptography_text_symmetrical_encrypt_all_and_right_first():
    url = "/cryptography_text_symmetrical/encrypt_text/"
    text = "Привет Мир Hello WORLd 123 fsdjkfh fksdhf !!@4#AZzzsa e2!!@#$%^&*()_+?><"
    key = "000102030405060f000102030405060f"
    iv = "000102030405060f"

    response = client.post(
        url,
        json={
            "method": "grasshopper",
            "text": text,
            "key": key,
            "iv": iv
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Encrypted text":
                                   "cd9e38d9fa04c551007c004fb6b2514646661426c36d98f31850acc46a3b9800df07b78b435849d4e4c"
                                   "07c8b777e995c0de401a6cc81c06a10fbccac029a80d80bc90a778d538447ac83504b5cfd07c63ef6c"
                                   "4e45654f0989ccddb0105965877"}

    key = "000102030405060f"
    response = client.post(
        url,
        json={
            "method": "aes",
            "text": text,
            "key": key,
            "iv": iv
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Encrypted text":
                                   "27fbca99ecd3e9ced8f2c1ef4bbc81973dd6598412ab24f5bdaa1d056077ed030ac8f1ee0e11a043eef"
                                   "7e444f3f66b25750201f8bc5387a9d4275e2e127a8c26cfdb6d1808732420b0dda0b4548f085e3d23488"
                                   "ef3fac6e5d6a04f2bfa307075"}

    key = "3"
    response = client.post(
        url,
        json={
            "method": "caesar",
            "text": text,
            "key": key,
            "iv": iv
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Encrypted text":
                                   "Тулеих Плу Khoor ZRUOg 123 ivgmnik invgki !!@4#DCccvd h2!!@#$%^&*()_+?><"}

def test_cryptography_text_symmetrical_decrypt_all_and_right_first():
    url = "/cryptography_text_symmetrical/decrypt_text/"
    right_text = "Привет Мир Hello WORLd 123 fsdjkfh fksdhf !!@4#AZzzsa e2!!@#$%^&*()_+?><"
    key = "000102030405060f000102030405060f"
    iv = "000102030405060f"

    text = "cd9e38d9fa04c551007c004fb6b2514646661426c36d98f31850acc46a3b9800df07b78b435849d4e4c07c8b777e995c0de401a6cc81c06a10fbccac029a80d80bc90a778d538447ac83504b5cfd07c63ef6c4e45654f0989ccddb0105965877"
    response = client.post(
        url,
        json={
            "method": "grasshopper",
            "text": text,
            "key": key,
            "iv": iv
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Decrypted text":
                                   right_text}

    text = "27fbca99ecd3e9ced8f2c1ef4bbc81973dd6598412ab24f5bdaa1d056077ed030ac8f1ee0e11a043eef7e444f3f66b25750201f8bc5387a9d4275e2e127a8c26cfdb6d1808732420b0dda0b4548f085e3d23488ef3fac6e5d6a04f2bfa307075"
    key = "000102030405060f"
    response = client.post(
        url,
        json={
            "method": "aes",
            "text": text,
            "key": key,
            "iv": iv
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Decrypted text":
                                   right_text}

    text = "Тулеих Плу Khoor ZRUOg 123 ivgmnik invgki !!@4#DCccvd h2!!@#$%^&*()_+?><"
    key = "3"
    response = client.post(
        url,
        json={
            "method": "caesar",
            "text": text,
            "key": key,
            "iv": iv
        },
    )
    assert response.status_code == 200
    assert response.json() == {"Decrypted text":
                                   right_text}


def test_cryptography_text_symmetrical_encrypt_all_and_right_second():
    url = "/cryptography_text_symmetrical/encrypt_text/"
    text = "Привет Мир Hello WORLd 123  kldjslkfj lkjslkdfjlkjdlkfjkjahiu iui2313 ia?><?><?><?>?<?><?>||}}{}{}{ ashdkuhg kh hfkushdfkuh ыагвралорывлоа ловрал рлрывлоарваыв fsdjkfh fksdhf !!@4#AZzzsa e2!!@#$%^&*()_+?><"
    key = "RPkZXTVKjacDK0N2xldPBkgS9CNerDE3"
    iv = "JROH3x6mpQuSYQ6r"

    response = client.post(url, json={"method": "grasshopper","text": text,"key": key,"iv": iv},)
    assert response.status_code == 200
    assert response.json() == {"Encrypted text": "916a2393ee0d2c2ae5c8ffe689d1520058c25a2c7627dc7531c06a0aa7226aeb95241c60fcdb99914c063088842b5239359d8d9faa088604c9b0792311f66e475f6e90d3e41c08981eb4e73449e9cfa470f248bae88a03c45a47884a6f4af8507847ea20422dc58704af7d16d1420b1f6d4fba903439d3b9880446f637ec7b7449d2f115f4448cfe18073997285187bb89a15ab21d51865e4b9624c068163acf11bca0fe03d169c04778054004c10e210a1f507b5c3518bcf58bccd26572cf362f32c4541a36f363a499b950ea08e7c626863ee86c3b006596bdd2c110b78923519cecf6921170fbbc2deff20b673d31e1acd7b3c56c773dfe5f9757825fde3b"}

    key = "RPkZXTVKjacDK0N2"
    response = client.post(url, json={"method": "aes","text": text,"key": key, "iv": iv},)
    assert response.status_code == 200
    assert response.json() == {"Encrypted text": "a123a9a6e7505d8ab126893092c3ec15782171594a6ae906bb120ed64a85fa7804d3bd8e31f3a7291e17c63cb62670e1dbd70fb14bfc176148762f7a02c3c0aac000badee868e6a2dc93f8a8f42555082658f2b5e0d79f342692c0a9ec9d12c52df43899b134e880989ebd1df24991b13458269dff47488252b1e86bc7c91df39bf8143fa904eeff7f99c15c93c8635cb97fd60449594f8fe169d3c22130366cd4eb55ad410f45ebf5402ec8483e4fe4a018d673220323a678f0624a6a264c52254ed2287bba5feea766ae3a49bd4d38d87d4db6ee54f6df875e215724429c993f5728b1b5f70549f0cacca41406779baa8669ef6989622d1d1feb77227ef064"}


    key = "55"
    response = client.post(url, json={"method": "caesar","text": text,"key": key, "iv": iv},)
    assert response.status_code == 200
    assert response.json() == {"Encrypted text": "Деюшыз Бюе Khoor ZRUOg 123  nogmvonim onmvongimonmgonimnmdklx lxl2313 ld?><?><?><?>?<?><?>||}}{}{}{ dvkgnxkj nk kinxvkginxk рцщшецагершагц агшеца еаершагцешцрш ivgmnik invgki !!@4#DCccvd h2!!@#$%^&*()_+?><"}

def test_cryptography_text_symmetrical_decrypt_all_and_right_second():
    url = "/cryptography_text_symmetrical/decrypt_text/"
    right_text = "Привет Мир Hello WORLd 123  kldjslkfj lkjslkdfjlkjdlkfjkjahiu iui2313 ia?><?><?><?>?<?><?>||}}{}{}{ ashdkuhg kh hfkushdfkuh ыагвралорывлоа ловрал рлрывлоарваыв fsdjkfh fksdhf !!@4#AZzzsa e2!!@#$%^&*()_+?><"
    key = "RPkZXTVKjacDK0N2xldPBkgS9CNerDE3"
    iv = "JROH3x6mpQuSYQ6r"

    text = "916a2393ee0d2c2ae5c8ffe689d1520058c25a2c7627dc7531c06a0aa7226aeb95241c60fcdb99914c063088842b5239359d8d9faa088604c9b0792311f66e475f6e90d3e41c08981eb4e73449e9cfa470f248bae88a03c45a47884a6f4af8507847ea20422dc58704af7d16d1420b1f6d4fba903439d3b9880446f637ec7b7449d2f115f4448cfe18073997285187bb89a15ab21d51865e4b9624c068163acf11bca0fe03d169c04778054004c10e210a1f507b5c3518bcf58bccd26572cf362f32c4541a36f363a499b950ea08e7c626863ee86c3b006596bdd2c110b78923519cecf6921170fbbc2deff20b673d31e1acd7b3c56c773dfe5f9757825fde3b"
    response = client.post(url, json={"method": "grasshopper","text": text,"key": key,"iv": iv},)
    assert response.status_code == 200
    assert response.json() == {"Decrypted text": right_text}


    text = "a123a9a6e7505d8ab126893092c3ec15782171594a6ae906bb120ed64a85fa7804d3bd8e31f3a7291e17c63cb62670e1dbd70fb14bfc176148762f7a02c3c0aac000badee868e6a2dc93f8a8f42555082658f2b5e0d79f342692c0a9ec9d12c52df43899b134e880989ebd1df24991b13458269dff47488252b1e86bc7c91df39bf8143fa904eeff7f99c15c93c8635cb97fd60449594f8fe169d3c22130366cd4eb55ad410f45ebf5402ec8483e4fe4a018d673220323a678f0624a6a264c52254ed2287bba5feea766ae3a49bd4d38d87d4db6ee54f6df875e215724429c993f5728b1b5f70549f0cacca41406779baa8669ef6989622d1d1feb77227ef064"
    key = "RPkZXTVKjacDK0N2"
    response = client.post(url, json={"method": "aes","text": text,"key": key,"iv": iv},)
    assert response.status_code == 200
    assert response.json() == {"Decrypted text": right_text}


    text = "Деюшыз Бюе Khoor ZRUOg 123  nogmvonim onmvongimonmgonimnmdklx lxl2313 ld?><?><?><?>?<?><?>||}}{}{}{ dvkgnxkj nk kinxvkginxk рцщшецагершагц агшеца еаершагцешцрш ivgmnik invgki !!@4#DCccvd h2!!@#$%^&*()_+?><"
    key = "55"
    response = client.post(url, json={"method": "caesar","text": text,"key": key,"iv": iv},)
    assert response.status_code == 200
    assert response.json() == {"Decrypted text": right_text}


def test_cryptography_text_symmetrical_encrypt_not_all_and_right_first():
    url = "/cryptography_text_symmetrical/encrypt_text/"
    text = "Привет Мир Hello WORLd 123  kldjslkfj lkjslkdfjlkjdlkfjkjahiu iui2313 ia?><?><?><?>?<?><?>||}}{}{}{ ashdkuhg kh hfkushdfkuh ыагвралорывлоа ловрал рлрывлоарваыв fsdjkfh fksdhf !!@4#AZzzsa e2!!@#$%^&*()_+?><"
    key = "RPkZXTVKjacDK0N2xldPBkgS9CNerDE3"

    response = client.post(url, json={"method": "grasshopper","text": text,"key": key},)
    assert response.status_code == 200
    assert response.json() == {"Encrypted text": "05430cff8ec96aca8e449e678533768d0ea115b6f59f20da00c9e2453f8f13c4e5592c63c6c87c7c6c68865802e38c2df3505f5f5a25185f339f394413c5962e67a9502b9939a3bb9a62fb6856c8961c3103f0105ee25532bb8ba7e0429342b0943271a032d444f6d2acb15298b287364f0e87b024286d8b5554ac2cb628341a8667577483c49b470aedce4794cf552884196b1be9decec9ce3535d0befbdbbd3000f3d19296bbc32c166c189639914712f2779b9acfe644b685f06aab2dbeeb41c9222c9d5606f07019ad624dc14e7019094f74296704015d3122f788b7f8807c334788c12a0bc9d0511d352a41b136b0817c1f43e63efb30fb07e8cc8e2b8b"}

    key = "RPkZXTVKjacDK0N2"
    response = client.post(url, json={"method": "aes","text": text,"key": key},)
    assert response.status_code == 200
    assert response.json() == {"Encrypted text": "4c5c1d21514608e8c4bba08428bd6bd99d5629dc41d2bbf32f6d77ec7346bbd7c8bb7ac8156832d7155611ab89c7079d41913fd7e79aef053199ba0bff7d9ddcf6249ae6e9594f183b8d91e3a4907318da0c6bd51112dbc9c5083b742e32e1e4bda341b40b35d5cd47dd698c5c15c4aecfde75625de6699ae68995ead756a6ffb3519b76fd906aef48ea97fb5a429bb3acf43a372aafd3a9e1acfb2f4132bf61cd63e0b22f6c5c952997f92243127910196e9ea27f822e782631acd20116c6255c1b759ff598d3941213d1be0ee4656aa19db3256863a23302a79f2c6ac9e8b7a235a4f925d230536892da2f97ff92c92e2b85198f431a8a9fc72fc94ec76023"}


    key = "100"
    response = client.post(url, json={"method": "caesar","text": text,"key": key},)
    assert response.status_code == 200
    assert response.json() == {"Encrypted text": "Рсйгжу Нйс Dahhk SKNHz 123  ghzfohgbf hgfohgzbfhgfzhgbfgfwdeq eqe2313 ew?><?><?><?>?<?><?>||}}{}{}{ wodzgqdc gd dbgqodzbgqd ьбдгсбмпсьгмпб мпгсбм смсьгмпбсгбьг bozfgbd bgozdb !!@4#WVvvow a2!!@#$%^&*()_+?><"}

def test_cryptography_text_symmetrical_decrypt_not_all_and_right_first():
    url = "/cryptography_text_symmetrical/decrypt_text/"
    right_text = "Привет Мир Hello WORLd 123  kldjslkfj lkjslkdfjlkjdlkfjkjahiu iui2313 ia?><?><?><?>?<?><?>||}}{}{}{ ashdkuhg kh hfkushdfkuh ыагвралорывлоа ловрал рлрывлоарваыв fsdjkfh fksdhf !!@4#AZzzsa e2!!@#$%^&*()_+?><"
    key = "RPkZXTVKjacDK0N2xldPBkgS9CNerDE3"

    text = "05430cff8ec96aca8e449e678533768d0ea115b6f59f20da00c9e2453f8f13c4e5592c63c6c87c7c6c68865802e38c2df3505f5f5a25185f339f394413c5962e67a9502b9939a3bb9a62fb6856c8961c3103f0105ee25532bb8ba7e0429342b0943271a032d444f6d2acb15298b287364f0e87b024286d8b5554ac2cb628341a8667577483c49b470aedce4794cf552884196b1be9decec9ce3535d0befbdbbd3000f3d19296bbc32c166c189639914712f2779b9acfe644b685f06aab2dbeeb41c9222c9d5606f07019ad624dc14e7019094f74296704015d3122f788b7f8807c334788c12a0bc9d0511d352a41b136b0817c1f43e63efb30fb07e8cc8e2b8b"
    response = client.post(url, json={"method": "grasshopper","text": text,"key": key},)
    assert response.status_code == 200
    assert response.json() == {"Decrypted text": right_text}


    text = "4c5c1d21514608e8c4bba08428bd6bd99d5629dc41d2bbf32f6d77ec7346bbd7c8bb7ac8156832d7155611ab89c7079d41913fd7e79aef053199ba0bff7d9ddcf6249ae6e9594f183b8d91e3a4907318da0c6bd51112dbc9c5083b742e32e1e4bda341b40b35d5cd47dd698c5c15c4aecfde75625de6699ae68995ead756a6ffb3519b76fd906aef48ea97fb5a429bb3acf43a372aafd3a9e1acfb2f4132bf61cd63e0b22f6c5c952997f92243127910196e9ea27f822e782631acd20116c6255c1b759ff598d3941213d1be0ee4656aa19db3256863a23302a79f2c6ac9e8b7a235a4f925d230536892da2f97ff92c92e2b85198f431a8a9fc72fc94ec76023"
    key = "RPkZXTVKjacDK0N2"
    response = client.post(url, json={"method": "aes","text": text,"key": key},)
    assert response.status_code == 200
    assert response.json() == {"Decrypted text": right_text}


    text = "Рсйгжу Нйс Dahhk SKNHz 123  ghzfohgbf hgfohgzbfhgfzhgbfgfwdeq eqe2313 ew?><?><?><?>?<?><?>||}}{}{}{ wodzgqdc gd dbgqodzbgqd ьбдгсбмпсьгмпб мпгсбм смсьгмпбсгбьг bozfgbd bgozdb !!@4#WVvvow a2!!@#$%^&*()_+?><"
    key = "100"
    response = client.post(url, json={"method": "caesar","text": text,"key": key},)
    assert response.status_code == 200
    assert response.json() == {"Decrypted text": right_text}