# CTF 5 - Week 7 - XSS (Cross Site Scripting)

## Reconnaissance

We accessed the web server at `http://ctf-fsi.fe.up.pt:5007/`. The and as the guidelines indicated, the flag was located in an obvious spot, as a `.txt` file stored in the root (`/`). However, upon opening it, it says: `Nice try, I am only accessible via JavaScript shenanigans.`, which means we need to find a way to exploit the server using XSS. Another file, called `flag.gif`, was also present in the root, which, upon opening, rick-rolled us.

On the top-right, it mentions `Read-Only access` which, as we've seen so far, indicates that we can only read the files present in the `/` directory, but not write to them. We also cannot find a way to upload files to the server.
The `login` button right next to it - indicating that we are not logged in - takes us to [another page](http://ctf-fsi.fe.up.pt:5007/?h):

- confirms that we're not logged in ("howdy stranger (you're not logged in)").
- confirms that we can browse the files in the root directory (`/`).
- mentions client configuration:
  - option enable/disable `k304` (which, when we first enter the web-server, is enabled)
  - option to reset client settings, which will disable `k304` (indicating that this one is actually the default, contrarily to what the previous point suggests)
- mentions logging in for more:
  - with a text field and a `Login` button. Upon typing anything in the text field and clicking the button, it shows the following page, which automatically redirects to the starting page ()
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

We started by researching vulnerabilities related to the application and dependencies versions we found. Using the CVE database mentioned in [CTF3](CTF3.md) - which allows us to filter vulnerabilities by product/software and version affected - we searched for vulnerabilities related to the [1.8.6 version of the copyparty application](https://www.cvedetails.com/vulnerability-list/vendor_id-32380/product_id-155088/version_id-1640352/Copyparty-Project-Copyparty-1.8.6.html). The only vulnerability that affects this version is: [CVE-2023-38501](https://www.cvedetails.com/cve/CVE-2023-38501/), which mentions a reflected Cross-Site Scripting (XSS) vulnerability in the `k304` and `setck` parameters of the application, through the URL (`?k304=...` and `?setck=...`). This vulnerability allows an attacker to execute arbitrary JavaScript code in the context of the user's browser, which, in the worst case can allow moving, deleting or uploading new files on the server.

## Choosing the vulnerability and finding an exploit

Luckily, on our first try at searching for vulnerabilities for this CTF, we found a very plausible one, as not only is it the only vulnerability affecting the application's version, but also, the application is the main one running on the server. This lead us to focus on exploiting this vulnerability.

Even though we had previously accessed `copyparty`'s [GitHub repository](https://github.com/9001/copyparty) to look for proof that FEUP's server was running `copyparty`, we returned to it after finding the vulnerability, and went to the [security section](https://github.com/9001/copyparty/security), where 3 vulnerabilities were reported, 2 of which referred Reflected XSS: [the one we found in the CVE database](https://github.com/9001/copyparty/security/advisories/GHSA-f54q-j679-p9hh) and [one via the `?hc=...` parameter](https://github.com/9001/copyparty/security/advisories/GHSA-cw7j-v52w-fp5r), which wasn't usable, due to being patched on version 1.8.6, which the server is running.

Both security reports included a proof of concept (PoC):

`?hc=...`:

```
http://target-website/?hc="><script>alert(1);</script>
http://target-website/?pw=<script>alert(1);</script>
```

`?k304=...`:

```
https://target-website/?k304=y%0D%0A%0D%0A%3Cimg+src%3Dcopyparty+onerror%3Dalert(1)%3E
https://target-website/?setck=y%0D%0A%0D%0A%3Cimg+src%3Dcopyparty+onerror%3Dalert(1)%3E
```

## Exploiting the vulnerability

Given that we had proofs of concept that tried to execute a script in different ways, with slight differences in:

- syntax
- method (directly including the scripts vs. using `img`'s `onerror` event)
- encoding (`%3C%3E` (URL encoding) vs. `<>` (unsafe characters))
- parameters (`hc` and `pw` even though these were already patched, `k304` and `hc`)

we decided to try them all.
