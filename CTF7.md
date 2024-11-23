# CTF 5 - Week 7 - XSS (Cross Site Scripting)

## Reconnaissance

We accessed the web server at `http://ctf-fsi.fe.up.pt:5007/`. The and as the guidelines indicated, the flag was located in an obvious spot, as a `.txt` file stored in the root (`/`). However, upon opening it, it says: `Nice try, I am only accessible via JavaScript shenanigans.`, which means we need to find a way to exploit the server using XSS. Another file, called `flag.gif`, was also present in the root, which, upon opening, rick-rolled us.

**Question 1:** Why can't you access the secret flag directly?

**Answer 1:** Upon finding it, it seems the flag isn't directly accessible due to it being necessary to use JavaScript (a clue about XSS).

On the top-right, it mentions `Read-Only access` which, as we've seen so far, indicates that we can only read the files present in the `/` directory, but not write to them. We also cannot find a way to upload files to the server.
The `login` button right next to it - indicating that we are not logged in - takes us to the [control-panel page](http://ctf-fsi.fe.up.pt:5007/?h), which:

- confirms that we're not logged in (`howdy stranger (you're not logged in)`).
- confirms that we can browse the files in the root directory (`/`).
- mentions client configuration:
  - option enable/disable `k304` (which, when we first enter the web-server, is enabled)
  - option to reset client settings, which will disable `k304` (indicating that this one is actually the default, contrarily to what the previous point suggests)
- mentions logging in for more:
  - with a text field and a `Login` button. Upon clicking the button (having typed anything in the field or not), it shows the following page, which automatically redirects to the starting page (root directory), remaining logged out:
    
    ![login_failed](/images/CTF7/login_failed.png)
    
    Image 1: Login failed page
  
  - a button to switch to `https`, which breaks the connection to the server.

We started by opening all the files present in the server's root, to try to find any meaningful information about a vulnerability:

- In the `HELP.md` file, in the `copyparty` command options, the -emp option mentions XSS risk: `emp enable markdown plugins -- neat but dangerous, big XSS risk (default: False)`. It also provides us with the version of this server's main application:
- **copyparty v1.8.6 "argon"** (2023-07-21)

We know that this is the main component, given that `copyparty` is a file-sharing and hosting server application - exactly what `http://ctf-fsi.fe.up.pt:5007/` is - and the visual appearance and features of FEUP's web server are consistent with the application's screenshots and details in its [GitHub repository](https://github.com/9001/copyparty).

The `HELP.md` file also provided version for `copyparty`'s dependencies (necessary for the application to run):

- **CPython v3.10.12** on Linux64 [GCC 11.4.0],
- **sqlite v3.37.2\*1**
- **jinja2 v2.11.3**
- **pyftpd v1.5.7**

The other files present in the root directory (`CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE`, `README.md`, `SECURITY.md`, `flake.lock`, `flake.nix`, `pyoxidizer.bzl`, `pyproject.toml`, `server.conf`, `setup.py`) provided mostly the same information about the versions of the application and its dependencies. They also included further information about the server's configuration and setup, which, in part due to their significant length and complexity, and due to the fact that they did not seem to contain any relevant information about the vulnerability we were looking for, we decided to ignore.

## Researching the vulnerability

**Question 2:** This service is popular and may even have known vulnerabilities. Can they help you access the flag?

To answer it, we started by researching vulnerabilities related to the application and dependencies versions we found. Using the CVE database mentioned in [CTF3](CTF3.md) - which allows us to filter vulnerabilities by product/software and version affected - we searched for vulnerabilities related to the [1.8.6 version of the copyparty application](https://www.cvedetails.com/vulnerability-list/vendor_id-32380/product_id-155088/version_id-1640352/Copyparty-Project-Copyparty-1.8.6.html). The only vulnerability that affects this version is: [CVE-2023-38501](https://www.cvedetails.com/cve/CVE-2023-38501/), which mentions a reflected Cross-Site Scripting (XSS) vulnerability in the `k304` and `setck` parameters of the application, through the URL (`?k304=...` and `?setck=...`). This vulnerability allows an attacker to execute arbitrary JavaScript code in the context of the user's browser, which, in the worst case can allow moving, deleting or uploading new files on the server.

## Choosing the vulnerability and finding an exploit

Luckily, on our first try at searching for vulnerabilities for this CTF, we found a very plausible one, as not only is it the only vulnerability affecting the application's version, but also, the application is the main one running on the server. This lead us to focus on exploiting this vulnerability.

Even though we had previously accessed `copyparty`'s [GitHub repository](https://github.com/9001/copyparty) to look for proof that FEUP's server was running `copyparty`, we returned to it after finding the vulnerability, and went to the [security section](https://github.com/9001/copyparty/security), where 3 vulnerabilities were reported, 2 of which referred Reflected XSS: [the one we found in the CVE database](https://github.com/9001/copyparty/security/advisories/GHSA-f54q-j679-p9hh) and [one via the `?hc=...` parameter](https://github.com/9001/copyparty/security/advisories/GHSA-cw7j-v52w-fp5r), which wasn't usable, due to being patched on version 1.8.6, which the server is running.

Both security reports included similar proofs of concept (PoCs):

`?hc=...`:

```
http://target-website/?hc="><script>alert(1);</script>
http://target-website/?pw=<script>alert(1);</script>
```

`?k304=...`:

```
https://target-website/?k304=y%0D%0A%0D%0A%3Cimg+src%3Dcopyparty+onerror%3Dalert(1)%3E
```

> THe last snippet is also shown in several [CVE-2023-38501](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-38501) exploits.

So, **to answer question 2**, we can use the vulnerability to access the flag, by exploiting the XSS vulnerability in the `k304` parameter, which allows us to execute arbitrary JavaScript code in the context of the user's browser, and thus, access the flag.

## Exploiting the vulnerability

Beginning with the PoC provided in the security report, we swapped the JavaScript code that triggers on the `onerror` event from `alert(1)` to a script that fetches the flag from the `/flag.txt` file, and displays it in an alert box:

```javascript
fetch("/flag.txt")
  .then((response) => response.text())
  .then((content) => alert(content))
  .catch((error) => console.error("Error while fetching the flag: ", error))
```

> To decide which type of request to make, we used the 'HTTP Header Live' extension to intercept the request and response headers, and see the requests being made to the server. We focused on the request made when directly accessing the flag through the `copyparty` application, and used the same type of request in the JavaScript code (GET):
> ![direct_flag_request](/images/CTF7/direct_flag_request.png)
> 
> Image 2: Direct access to `flag.txt`

- The `fetch()` function is used to make a request to the server. In this case, it is a GET request (default with `fetch()`) to `/flag.txt`, which is the file we want to access.
- As the request is asynchronous (returns a Promise that resolves to a Response object - `Promise<Response>`), the `then()` function is used to handle the response (if the HTTP request succeeds), which is converted from the `Response` object into plain-text using `response.text()`.
- As the `text()` function also returns a Promise (`Promise<string>`), because reading the response body is asynchronous, a second `then()` is needed to handle the returned text, which is displayed in alert box, using `alert(content)`, which is an easily visible way to display the flag.
- The `catch()` function is used to handle any errors that may occur in the `then()` chain during the request (network errors in `fetch()`, parsing failure in `response.text()`, errors inside the `then()` functions), which are logged to the console using `console.error()`.

An important aspect is that the code is executed when the `onerror` event is triggered, due to the `src` attribute referring to a file that doesn't and will never exist, due to the lack of a file extension.

After URL-encoding it and substituting in the proof of concept, we get:

```html
?k304=y%0D%0A%0D%0A%3Cimg+src%3Dcopyparty+onerror%3D%22fetch(%27%2Fflag.txt%27).then(response+%3D%3E+response.text()).then(content+%3D%3E+alert(content)).catch(error+%3D%3E+console.error(%27Error+while+fetching+the+flag%3A+%27%2C+error))%22%3E
```

> The encoding of the payload is necessary to avoid breaking the URL, as it contains reserved characters in URLs, such as spaces, `<`, `>`, `:`, that could cause several problems. Therefore, URL-encoding replaces these unsafe characters with their hexadecimal representation, preceded by `%`. Spaces are replaced by either `+` or `%20`, in the PoC's case, `+` was used.

Then, by appending the payload in the URL (`http://ctf-fsi.fe.up.pt:5007/`) - and the flag was displayed in the `alert()` pop-up: `flag{youGotMeReallyGood}`. Upon insert this flag in the CTF challenge, we completed it.

![flag_popup](/images/CTF7/flag_popup.png)

Image 3: Execution of the payload, displaying the flag in an alert box

**Question 3:** What is the type of XSS vulnerability (Reflected, Stored or DOM) that allowed you to access the flag?

**Answer 3:** This XSS vulnerability is Reflected XSS, as the payload was reflected back to the user in the response, and executed in the context of the user's browser, due to improper input validation or/and output encoding.

## Further analysis

Through 'HTTP Header Live', we observe the requests upon executing the payload, as expected, all of them are GET requests:
![exploit_req_resp](/images/CTF7/exploit_req_resp.png)

Image 4: Requests and responses made upon executing the payload

- the request with the payload in the `k304` parameter is followed by a 200 (OK) response.
- then, a request is made for the `copyparty` file, which completes with a 200 (OK) response, even though the file doesn't exist.
- therefore, the `onerror` event is triggered, and the JavaScript code is executed, which sends a GET request to fetch the flag from the `/flag.txt` - or so we thought - because the request fetches a file called `superblyHiddenFlagPGCT59TMXPLMNBT240F3.txt`, which contains the flag. The suffix of the file seems to be dynamically generated, as it changes every time we access the flag (see images below).

![flag_request1](/images/CTF7/flag_request1.png)

Image 5: Request for the flag (file is `superblyHiddenFlagU2B3W7UZSYAS3OW3SSMR.txt`)

![flag_request2](/images/CTF7/flag_request2.png)

Image 6: Request for the flag (file is `superblyHiddenFlag5M2N8Y2YQ7CX7HN74NZ3.txt`)

We don't know exactly how the server generates this file upon the XSS script being executed, making a different file be fetched instead of the one specified in the script. We suppose it is a temporary file created to store the flag, and is deleted after being accessed, to prevent further access to the flag through direct means.
