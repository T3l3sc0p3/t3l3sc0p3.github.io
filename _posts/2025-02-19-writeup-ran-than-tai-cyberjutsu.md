---
layout: post
title: Writeup Challenge Rắn Thần Tài CyberJutsu
categories: [CTF, Writeup]
tags: [web, lfi, sqli, bac]
date: 2025-02-19 18:39 +0700
img_path: '/assets/img/writeups/ran-than-tai-cbjs-2025/'
image:
  path: banner.png
---

Dịp Tết Ất Tỵ 2025 vừa qua, mình được một ông anh share cho challenge **Rắn Thần Tài** của bên CyberJutsu. Cơ mà lu bu mãi tới giờ mình mới lên bài được hehe =))

Vào việc thôi~

![Writeup](ran-than-tai.png)

Link: `http://206.189.39.54:8085/`

Như mọi khi, việc đầu tiên mình làm chính là recon, xem source trước, và mình tìm được ngay Easter Egg đầu tiên

![](easter-egg-1.png)

`Easter Egg 1: CBJS_EASTER_EGG{Part 1: https://lixi.momo.vn/}`

Tiếp theo, kiểm tra `robots.txt`, ta thấy `/appsettings.json` được đặt vô tình một cách đầy cố ý. Ngoài ra, khi truy cập vào các path như `/Areas`, `/Controllers`, không có gì trả về cả nhưng khi truy cập vào `/Admin` thì lại xuất hiện **404 not found**, khá lạ nhỉ

Mình thử bật **DevTools** lên, chuyển qua tab **Network** rồi load lại trang, vậy là mình thấy Easter Egg thứ hai

![](easter-egg-2.png)

`Easter Egg 2: CBJS_EASTER_EGG{Part 2: /lixi/9o3}`

Check tiếp tới `/Game`, đây cơ bản là game rắn săn mồi. Ở đây mình thấy khá nhiều bạn chơi được điểm cao nên mình cũng tò mò làm thử

Cụ thể thì sau mỗi lần thua, 1 **POST request** sẽ được gửi tới server để lưu kết quả lại, ta chỉ cần dùng **Burp Suite** chỉnh số cao lên là được :v

![](easter-egg-5.png)

`Easter Egg 5: CBJS_EASTER_EGG{Part 5 (final): 1R5b}`

Quay lại source của `/Game`, mình thấy có một vài endpoint như  `/Game/Feedback`, `/Admin/EditBackground` và `/api/ranking`, check lần lượt cả các endpoint này thì:

Trong `/Game/Feedback`, để ý 1 chút ta sẽ thấy 1 đoạn `base64` nằm ở dưới cùng, decode phát là ta đã có Easter Egg 3

![](easter-egg-3.png)

`Easter Egg 3: CBJS_EASTER_EGG{Part 3: XA5V}`

Khi truy cập `/Admin/EditBackground`, mình thấy nó redirect về `/Game`, tuy nhiên, mình có thể sử dụng **Burp Suite** để intercept request trước khi redirect

Xong mình chỉ lướt xuống là thấy ngay flag Admin Panel

![](flag-4.png)

`Flag 4: CBJS{Unauthorized_Access_On_Admin_Panel_Because_Lack_Of_Proper_Redirection}`

Đi sâu hơn tí nữa, mình biết được endpoint này dùng để thay background với param là `selectedBackground`

![](selectedBackground.png)

Vì vậy nên mình đã tạo một cái **POST request** để update xem sao, nhưng mà response trả về hơi lạ nhờ

![](lfi.png)

![](https://i.imgur.com/f5G9lxX.png)

Có vẻ như server đã đọc luôn file ảnh đó để làm **preview content**, nhưng điều này khiến nó bị dính vuln **Path Traversal**

Tận dụng vuln này, mình đã có thể lấy được `/tmp/FLAG_WEB`. Tuy nhiên thì mình lại không tiện tay lấy luôn `/tmp/FLAG_DBSERVER` được

![](flag-1.png)

`Flag 1: CBJS{Happy_Year_Of_The_Snake}`

Hmm, hồi đầu khi recon, mình có tìm được 1 file `/appsettings.json`, thế tại sao ta lại không thử luôn nhỉ?

Vậy là chỉ sau 2 lần `../`, mình đã có được Easter Egg cuối cùng :3

`Easter Egg 4: CBJS_EASTER_EGG{Part 4: VMNp}`

Còn 2 flag nữa nên mình clear cho xong luôn

Lúc nãy, ta vẫn còn 1 endpoint chưa test đó là `/api/ranking`. Tại đây mình có được param `sortParam`, tuy nhiên thì mình không tìm ra được bug

Bí nước, mình bắt đầu quay ra chạy scan, và mình scan được endpoint `search` và param `searchTerm`

![](scan.png)

Vì 2 flag còn lại đều liên quan tới database, nên mình cũng ít nhiều đoán được đây có thể là lỗ hổng liên quan tới SQL, và đúng là như thế thật

Chỉ cần quăng `test'OR 1=1;--`, mình đã có thể confirm điều này

Vấn đề còn lại là khai thác để lấy flag thôi, tuy nhiên, mình là một con gà về SQL, nên mình quyết định để cho `sqlmap` xử lý hết, cảm ơn `sqlmap` =)))

```sh
sqlmap -u 'http://206.189.39.54:8085/api/ranking/search?searchTerm=' -p "searchTerm" --dbs

back-end DBMS: Microsoft SQL Server 2022
[*] model
[*] msdb
[*] MyAppDB
[*] tempdb

sqlmap -u 'http://206.189.39.54:8085/api/ranking/search?searchTerm=' -p "searchTerm" -D MyAppDB --tables

Database: MyAppDB
[2 tables]
+-------------+
| CyberJutsu  |
| SnakeScores |
+-------------+

sqlmap -u 'http://206.189.39.54:8085/api/ranking/search?searchTerm=' -p "searchTerm" -D MyAppDB -T CyberJutsu --dump

Database: MyAppDB
Table: CyberJutsu
[1 entry]
+----+--------------------------------+
| Id | flag                           |
+----+--------------------------------+
| 1  | CBJS{SQL_Injection_is_a_jutsu} |
+----+--------------------------------+
```

`Flag 3: CBJS{SQL_Injection_is_a_jutsu}`


Còn lại flag 2, lúc nãy mình đã thử đọc thông qua lỗ hổng **Path Traversal** nhưng không được, nên mình suy đoán ta chỉ có thể đọc bằng lỗ hổng **SQL Injection**

Để đọc được cũng không khó, từ lần chạy `sqlmap`, mình đã biết đây là **Microsoft SQL Server** hay **MSSQL**

Research một tí, mình tìm được cách đọc file trong MSSQL bằng cách dùng [OPENROWSET](https://www.geeksforgeeks.org/reading-a-text-file-with-sql-server/). Vậy giờ ta chỉ cần xác định số lượng columns rồi lụm flag

Cơ mà văn vở vậy thôi, sau khi mình biết nó là **MSSQL** mình đã bay ngay vào [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MSSQL%20Injection.md) để tìm payload cho nhanh rồi

![](https://i.imgur.com/QyXtJR3.png)

```sql
0'union select 0,(select x from OpenRowset(BULK '/tmp/FLAG_DBSERVER',SINGLE_CLOB) R(x)),2;--
```

![](flag-2.png)

`Flag 2: CBJS{Have_you_Seen_Microsoft_SQL_Server_is_running_on_Linux?}`

Đây là link lì xì nè: [https://lixi.momo.vn/lixi/9o3XA5VVMNp1R5b](https://lixi.momo.vn/lixi/9o3XA5VVMNp1R5b)

Sad fact: Hồi đầu lúc challenge mới mở mình đã tìm được hết flag, nhưng vì Easter Egg 3 bị lỗi nên mình không húp lì xì được, lúc mình thấy link update thì lì xì đã hết :(

Cảm ơn mọi người đã đọc <3
