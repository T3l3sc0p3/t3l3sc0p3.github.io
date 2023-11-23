---
layout: post
title: Hutech CTF Newbie 2023 Writeup
tags: [writeup, web, crypto, reverse]
date: 2023-11-22 00:00 +0700
img_path: '/assets/img/writeups/hutech-ctf-newbie-2023/'
image:
  path: banner.jpg
---

Hi, vừa rồi CLB ATTT của trường HUTECH vừa tổ chức giải CTF dành cho tân sinh viên và mình cũng giải được vài challenges trong đó. Dưới đây là writeup về những bài mình đã giải được

# WELCOME

## WELCOME

![welcome](https://i.imgur.com/OQQNvL4.png)

Bài này như là Sanity Check với nhắc cho mọi người về format của flag thôi

`Flag: HUTECH_CTF{Some_Thing}`

# Web

## P1NG

![p1ng](https://i.imgur.com/EBikeGi.png)

Truy cập thì mình thấy giao diện của "Ping Tool", điều này đã gợi nhớ cho mình về 2 ping challenges của Cookie Hân Hoan ([Ping 0x01](https://battle.cookiearena.org/challenges/web/ping-0x01), [Ping 0x02](https://battle.cookiearena.org/challenges/web/ping-0x02)) và thực sự cách giải bài này cũng giống vậy

Đầu tiên khởi động Burp Suite, bật intercept để bắt request rồi chuyển sang tab Repeater để test cho tiện

Vì mình chắc 10 tỷ phần trăm đây là lỗi Command Injection, nên mình sẽ chèn command bằng cách thêm các ký tự như `;`, `&&`, `||` + với command thực thi

![Don't hack me](https://i.imgur.com/neJ8pPk.png)

Tới đây thì ta thấy web đã lọc hết các ký tự đó, tuy nhiên có vẻ nó không lọc tất cả mà vẫn còn sót lại dấu xuống dòng (như 2 ping challenge mình nhắc ở trên). You know what to do next =))

![flag.txt](https://i.imgur.com/dt8h8L7.png)

Chỉ với command `ls /` là có thể thấy ngay file flag.txt. Giờ ta chỉ cần `cat /flag.txt` nữa là xong

`Flag: HUTECH_CTF{You_are_master_CMD_Injection}`

### Note

Thật ra mình chỉ chạy `ls /` theo thói quen, vì flag thường sẽ nằm ở đây hay trong directory của user

Nhưng nếu không có thì mình sẽ chạy `env` để check hoặc tìm hết bằng command `find / -name flag* 2>/dev/null`

## R0T M0N

![r0t m0n](https://i.imgur.com/IFqxkyZ.png)

Sau khi vào web và click thử vào button "View", mình nhận ra web sẽ hiển thị các hình ảnh bằng cách truy cập file **ctdl.png** thông qua endpoint `file_name`

![file_name](https://i.imgur.com/pwlyYdL.png)

Đến đây thì mình khá chắc đây là lỗi [Path Traversal](https://viblo.asia/p/tim-hieu-ve-tan-cong-path-travelsal-m68Z0xQ2ZkG) nên mình đã thử thay **ctdl.png** thành `../etc/passwd`

Tuy kết quả trả về là "404 Not Found" nhưng đây lại là tín hiệu khả quan cho thấy endpoint này bị dính bug

Khi mình thử đến `../../../../etc/passwd`, kết quả trả về không còn là 404 nữa mà lại là thông báo lỗi. Điều này có thể giải thích vì nó chỉ dùng để hiển thị hình ảnh nên khi render file text sẽ xuất hiện lỗi

Mà nếu đã không xem được trên web thì ta tải xuống xem thôi

```sh
wget http://hutechctf.notrespond.com:8898/view.php?file_name=../../../../etc/passwd
```

![flag](https://i.imgur.com/J76V0Kt.png)

`Flag: HUTECH_CTF{You_are_Hacker_101}`

# Reverse

## HUTECHRev2

![HUTECHRev2](https://i.imgur.com/loG4HRZ.png)

Bài này chỉ cần [tải file](https://hutechctf.notrespond.com/files/158a89433f2b473d419dbf4d7ac5b62c/Password.rar) về rồi mở Ghidra lên đọc file là thấy ngay flag, cũng không đáng để viết writeup nhưng đây là bài reverse duy nhất mình làm được

Ngoài ra còn cách khác tà ma hơn là chạy command `strings Password.exe | grep HUTECH_CTF{` nhưng cái này chỉ áp dụng được với mấy bài dễ thôi

`Flag: HUTECH_CTF{Wellcome_Learn_Reversing}`

# Crypto

## Classic_and_basic

![Classic_and_basic](https://i.imgur.com/SDHv3Qj.png)

RSA_Basic.py:
```py
from Crypto.Util.number import getPrime, bytes_to_long

bits = 150
p = getPrime(bits)
q = getPrime(bits)
e = 65537
N = p*q
m = 0

with open('flag.txt', 'rb') as f:
    m = bytes_to_long(f.read())

c = pow(m, e, N)

print('p=', p)
print('e=', e)
print('N=', N)
print('c=', c)
```

output.txt:
```
*No hint

N= 944277460928218727444425796671228006440681423958756385944259965777648467343805051250778307
p= 1187132467668222120649135047910661042340315271
e= 65537
c= 509304373433095933741721585884760854821638120979366068441534204508880522869949802723478795
```

Bài này sử dụng hàm số Euler để decrypt, nhưng chi tiết thì mình không thật sự hiểu do mình chỉ copy code từ Google về chạy :(

solve.py:
```py
from Crypto.Util.number import long_to_bytes

N= 944277460928218727444425796671228006440681423958756385944259965777648467343805051250778307
p= 1187132467668222120649135047910661042340315271
e= 65537
c= 509304373433095933741721585884760854821638120979366068441534204508880522869949802723478795

# N = p * q
q = N // p
# Euler's totient function (phi(N))
phi_N = (p - 1) * (q - 1)
# d * e ≡ 1 (mod phi_N)
d = pow(e, -1, phi_N)
m = pow(c, d, N)
flag = long_to_bytes(m)
print('The flag is:', flag.decode('utf-8'))
```

`Flag: HUTECH_CTF{RSA_is_great_encryption}`

Mấy bài khác thì mình chịu nhưng mình sẽ update thêm nếu giải ra ._.

## References:

Đây là 2 challenges của Cookie Hân Hoan dành cho bạn nào muốn làm thêm:
- [https://battle.cookiearena.org/challenges/web/ping-0x01](https://battle.cookiearena.org/challenges/web/ping-0x01)
- [https://battle.cookiearena.org/challenges/web/ping-0x02](https://battle.cookiearena.org/challenges/web/ping-0x02)

Path Traversal:
- [https://viblo.asia/p/tim-hieu-ve-tan-cong-path-travelsal-m68Z0xQ2ZkG](https://viblo.asia/p/tim-hieu-ve-tan-cong-path-travelsal-m68Z0xQ2ZkG)
