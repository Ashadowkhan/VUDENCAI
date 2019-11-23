
## Examples

Some samples from the dataset are presented here for demonstration purposes. Using the provided script, it is possible to load a piece of code and run the model on it to check for vulnerabilities. The script produces an output image with colored highlights corresponding to the vulnerability status of each code token.

There are examples for all relevant types of vulnerabilities:

| Vulnerability        | Source  | Link to commit         | File |
| --------------------|--------- |-------------| -----|
| SQL injection        | ambagape/opendatang | [Fixed tag search SQL-injection attack vulnerability.](https://github.com/ambagape/opendatang/commit/f020853c54a1851f196d7fd8897c4620bccf9f6c) | sql-1.py |
| SQL injection        |  loxoalia/OCA-OCB  | [point_of_sale: Improved code. Removed sql injections.](https://github.com/loxoalia/OCA-OCB/commit/b48fb1cde6b7bbc49f502974a034ee1cf7e87e6c)   | sql-2.py |
| SQL injection        | onewyoming/onewyoming  | [fix sql injection vulnerability ](https://github.com/onewyoming/onewyoming/commit/54fc7b076fda2de74eeb55e6b75b28e09ef231c2)  | sql-3.py |
| SQL injection        | LukasJaeger307/brewdie  | [Added code that prevents SQL injection attacks](https://github.com/LukasJaeger307/brewdie/commit/c603201e401e414097358f32a23ca5521aa39dec) | sql-4.py |
| SQL injection        | russ-lewis/ttt_-_python_cgi  | [Reworked all execute() calls that had parameters, to prevent SQL injection](https://github.com/russ-lewis/ttt_-_python_cgi/commit/6096f43fd4b2d91211eec4614b7960c0816900da)| sql-5.py |
|xss| dongweiming/lyanna | [Fix comment's reflected xss vulnerability ](https://github.com/dongweiming/lyanna/commit/fcefac79e4b7601e81a3b3fe0ad26ab18ee95d7d) | xss-1.py |
|xss| gethue/hue| [ Protect against reflected XSS in search query parameters](https://github.com/gethue/hue/commit/37b529b1f9aeb5d746599a9ed4e2288cf3ad3e1d) | xss-2.py |
|xss| Technikradio/C3FOSite | [fix: XSS bug in now exposed user forms ](https://github.com/Technikradio/C3FOCSite/commit/6e330d4d44bbfdfce9993dffea97008276771600) | xss-3.py|
| command injection        | saltstack/salt  | [Fix command injection vulnerability in disk.usage](https://github.com/saltstack/salt/commit/ebdef37b7e5d2b95a01d34b211c61c61da67e46a) | command_injection-1.py |
| command injection        | w-martin/mindfulness  | [(issue #25) 'Auto-fill description form acts as a shell'](https://github.com/w-martin/mindfulness/commit/62e1d5ce9deb57468cf917ce0ce838120ec84c46) | command_injection-2.py |
| command injection        |  Atticus/ajar | [fixed command injection issue](https://github.com/Atticuss/ajar/commit/5ed8aba271ad20e6168f2e3bd6c25ba89b84484f) | command_injection-3.py |
| xsrf        | m13253/titlebot | [Add X-Requested-With header to prevent XSRF ](https://github.com/m13253/titlebot/commit/4164d239f0f59b9ef04e3d168e68f958991fe88f) | xsrf-1.py |
| xsrf        | NBISweden/swefreq  | [Proper XSRF Cookie protection ](https://github.com/NBISweden/swefreq/commit/d6e94e4208158460f9b468d28f94ea29fb2315ce) | xsrf-2.py |
| xsrf        | LucidUnicorn/BUCSS-CTF-Framework | [ Bug fix. Fixed an issue where the _xsrf cookie was being deleted.](https://github.com/LucidUnicorn/BUCSS-CTF-Framework/commit/1a6a1dd6540b0b1441d270e9ea62f9a8c0c6e1bf) | xsrf-3.py |
| xsrf        | nandoflorestan/bag | [Fix: XSRF cookie wouldn't stick after logging out ](https://github.com/nandoflorestan/bag/commit/3b55dd0c22fd9ba78a785be61f3da0cbdcafd5f9) | xsrf-4.py |
| remote code execution        | Scout24/monitoring-config-generator | [Prevent remote code execution](https://github.com/Scout24/monitoring-config-generator/commit/2191fe6c5a850ddcf7a78f7913881cef1677500d) | remote_code_execution-1.py |
| remote code execution        | pipermerriam/flex | [Fix remote code execution issue with yaml.load ](https://github.com/pipermerriam/flex/commit/329c0a8ae6fde575a7d9077f1013fa4a86112d0c) | remote_code_execution-2.py |
| remote code execution        | cea-hpc/shine | [improved proxy (remote) commands execution error handling (...)](https://github.com/cea-hpc/shine/commit/7ff203be36e439b535894764c37a8446351627ec) | remote_code_execution-3.py |
| sanitization        | EdinburghGenomics/Analysis-Driver | [ Sanitising sample ids in clarity.get_released_samples.](https://github.com/EdinburghGenomics/Analysis-Driver/commit/4dd59ba3302126bb3a31f24b385c714aaf0bfa86) | sanitize-1.py |
| sanitization        | matitalatina/randommet-telegram | [Improved sanitize message ](https://github.com/matitalatina/randommet-telegram/commit/a59f62da51c13bd655bb685db776ef9293a1d0a2) | sanitize-2.py |
| sanitization        |bmintz/CAPTAIN-CAPSLOCK  | [bot: improve sanitization a bit](https://github.com/bmintz/CAPTAIN-CAPSLOCK/commit/a70f89c14cdd079db8bd1edd2f9db5376fea543b) | sanitize-3.py |


To try out one of the examples, simply execute:

```
python3 62Demonstrate.py sql 1
```

The first parameter specifies the type of vulnerability. It should be from the list "sql","xss","xsrf","command_injection","xsrf","remote_code_execution","sanitization".

The second paramter should be the number of the example, usually between 1 and 5. 

An optional third parameter "fine" makes increases the resolution of colors. 

The script puts output to the screen that already highlights the vulnerable parts in red and the (probably) non-vulnerable parts in green, but the detailed outcome is printed as an image file. Refer to that one for a closer look at the predicions. It highlights which parts might be vulnerable according to the following color chart:

![Legende](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/legende2.png)


The following example was created using the fine resolution with the fourth sql example.


```
python3 demonstrate.py sql 4 fine
```

![Example](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/example.png)