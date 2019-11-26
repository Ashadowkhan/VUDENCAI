
## Examples

Some samples from the dataset are presented here for demonstration purposes. Using the provided script, it is possible to load a piece of code and run the model on it to check for vulnerabilities. The script produces an output image with colored highlights corresponding to the vulnerability status of each code token.

There are examples for all relevant types of vulnerabilities:

| Vulnerability        | Source  | Link to commit   | Changed file | Example file |
| ---------------------|-------- |------------------| -------------| -------------|
|<sub> SQL injection </sub> | <sub>instacart/lore</sub> | <sub> [protect against potential sql injection](https://github.com/instacart/lore/commit/a0a5fd945a8bf128d4b9fb6a3ebc6306f82fa4d0) </sub> | <sub> /lore/io/connection.py </sub> | <sub> sql-1.py </sub> | 
|<sub>  SQL injection </sub> | <sub>uktrade/export-wins-data</sub> | <sub>[parameterise the sql query to avoid injection attacks ](https://github.com/uktrade/export-wins-data/commit/307587cc00d2290a433bf74bd305aecffcbb05a2) </sub> | <sub> /wins/views/flat_csv.py </sub> | <sub> sql-2.py </sub> | 
|<sub> SQL injection </sub> | <sub> kyojuceles/mud </sub> | <sub> [prevent sql injection attack](https://github.com/kyojuceles/mud/commit/47f5aa6aa2e82de7ce2a440aea870958edf0ae77) </sub> | <sub> /db/db_processor_mysql.py </sub> | <sub> sql-3.py </sub> |
|<sub> XSS </sub> | <sub> dongweiming/lyanna </sub> | <sub> [Fix comment's reflected xss vulnerability](https://github.com/dongweiming/lyanna/commit/fcefac79e4b7601e81a3b3fe0ad26ab18ee95d7d) </sub> | <sub> /models/comment.py </sub> | <sub> xss-1.py </sub> |
|<sub> XSS </sub> | <sub> inveniosoftware/invenio-records </sub> | <sub> [admin: xss vulnerability fix](https://github.com/inveniosoftware/invenio-records/commit/361def20617cde5a1897c2e81b70bfadaabae608) </sub> | <sub> /invenio_records/admin.py </sub> | <sub> xss-2.py </sub> |
|<sub> XSS </sub> | <sub> onefork/pontoon-sr</sub> | <sub>[Fix an XSS vulnerability in batch/views.py](https://github.com/onefork/pontoon-sr/commit/fc07ed9c68e08d41f74c078b4e7727f1a0888be8) </sub> | <sub> /pontoon/batch/views.py</sub> | <sub> xss-3.py </sub> |
|<sub> Commmand injection </sub> | <sub> saltstack/salt </sub> | <sub> [Fix command injection vulnerability in disk.usage ](https://github.com/saltstack/salt/commit/ebdef37b7e5d2b95a01d34b211c61c61da67e46a) </sub> | <sub>/salt/modules/disk.py </sub> | <sub> command_injection-1.py </sub> |
|<sub> Commmand injection </sub> | <sub> Atticuss/ajar </sub> | <sub>[fixed command injection issue](https://github.com/Atticuss/ajar/commit/5ed8aba271ad20e6168f2e3bd6c25ba89b84484f) </sub> | <sub>/ajar.py </sub> | <sub>command_injection-2.py </sub> |
|<sub> Commmand injection </sub> | <sub>yasong/netzob </sub> | <sub> [Remove security issue related to shell command injection](https://github.com/yasong/netzob/commit/557abf64867d715497979b029efedbd2777b912e) </sub> | <sub> /src/netzob/Simulator/Channels/RawEthernetClient.py </sub> | <sub> command_injection-3.py </sub> |
|<sub> XSRF </sub> | <sub> deepnote/notebook </sub> | <sub> [add xsrf checks on files endpoints ](https://github.com/deepnote/notebook/commit/d7becafd593c2958d8a241928412ddf4ba801a42) </sub> | <sub> /notebook/files/handlers.py </sub> | <sub>xsrf-1.py </sub> |
|<sub> XSRF </sub> | <sub> wbrxcorp/forgetthespiltmilk </sub> | <sub> [xsrf token handling corrected ](https://github.com/wbrxcorp/forgetthespiltmilk/commit/51bed3f7f01079d91864ddc386a73eb3e1ca634b) </sub> | <sub> /frontend/app.py  </sub> | <sub>xsrf-2.py </sub> |
|<sub> XSRF </sub> | <sub> tricycle/lesswrong </sub> | <sub> [Implement proper modhash checking to stop xsrf ](https://github.com/tricycle/lesswrong/commit/ef303fe078c60d964e3f9e87d3da1a67fecd2c2b) </sub> | <sub>  r2/r2/models/account.py </sub> | <sub>xsrf-3.py </sub> |
|<sub>  Path disclosure </sub> | <sub>fkmclane/python-fooster-web</sub> | <sub> [prevent local file disclosure via url encoded nonormalized paths](https://github.com/fkmclane/python-fooster-web/commit/80202a6d3788ad1212a162d19785c600025e6aa4) </sub> | <sub>/fooster/web/file.py</sub> | <sub>path_disclosure-1.py </sub> |
|<sub>  Path disclosure </sub> | <sub>zms-publishing/zms4</sub> | <sub> [applied fix for disclosure of physical-path in zmi](https://github.com/zms-publishing/zms4/commit/3f28620d475220dfdb06f79787158ac50727c61a) </sub> | <sub> /ZMSItem.py </sub> | <sub>path_disclosure-2.py </sub> |
|<sub>  Path disclosure </sub> | <sub> zcutlip/pyweb </sub> | <sub> [more path checking in pyweb-add-conent](https://github.com/zcutlip/pyweb/commit/76918b12c408529eaf04f75917f128f56e250111) </sub> | <sub>pyweb_add_content.py</sub> | <sub>path_disclosure-3.py </sub> |
|<sub>  Open redirect </sub> | <sub> karambir/mozilla-django-oidc </sub> | <sub> [This uses Django's is_safe_url to sanitize the next url for the authentication view. This prevents open redirects.](https://github.com/karambir/mozilla-django-oidc/commit/22b6ecb953bbf40f0394a8bfd41d71a3f16e3465) </sub> | <sub> /mozilla_django_oidc/views.py</sub> | <sub>open_redirect-1.py </sub> |
|<sub>  Open redirect </sub> | <sub> nyaadevs/nyaa </sub> | <sub> [Fix open redirect](https://github.com/nyaadevs/nyaa/commit/b2ddba994ca5e78fa5dcbc0e00d6171a44b0b338) </sub> | <sub>/nyaa/views/account.py </sub> | <sub>open_redirect-2.py </sub> |
|<sub>  Open redirect </sub> | <sub> readthedocs/readthedocs.org </sub> | <sub> [Fix open redirect issue ](https://github.com/readthedocs/readthedocs.org/commit/e3bccfc582beb57800c33e4f0afe01351733f2a5) </sub> | <sub> /readthedocs/redirects/models.py</sub> | <sub>open_redirect-3.py </sub> |
|<sub>  Remote code execution </sub> | <sub>Scout24/monitoring-config-generator  </sub> | <sub> [Prevent remote code execution ](https://github.com/Scout24/monitoring-config-generator/commit/2191fe6c5a850ddcf7a78f7913881cef1677500d) </sub> | <sub>/src/main/python/monitoring_config_generator/yaml_tools/readers.py </sub> | <sub>remote_code_execution-1.py </sub> |
|<sub>  Remote code execution </sub> | <sub> ntc-chip-revived/ChippyRuxpin </sub> | <sub> [prevent remote code execution by passing argumrnts to subprocess.call](https://github.com/ntc-chip-revived/ChippyRuxpin/commit/0cd7d78e4d806852fd75fee03c24cce322f76014) </sub> | <sub> /chippyRuxpin.py </sub> | <sub>remote_code_execution-2.py </sub> |
|<sub>  Remote code execution </sub> | <sub>  johanbluecreek/reddytt</sub> | <sub> [Fix remote code execution. ](https://github.com/johanbluecreek/reddytt/commit/bd037e882d675ea27b96d41faf0deeac6563695c) </sub> | <sub> /reddytt.py</sub> | <sub>remote_code_execution-3.py </sub> |



To try out one of the examples, simply execute:

```
python3 62Demonstrate.py sql 1
```

The first parameter specifies the type of vulnerability. It should be either "sql","xss","command_injection","xsrf","path_disclosure","open_redirect" or "remote_code_execution".

The second paramter should be the number of the example between 1 and 3. 

An optional third parameter "fine" increases the resolution of colors. 

The script puts output to the screen that already highlights the vulnerable parts in red and the (probably) non-vulnerable parts in green, but the detailed outcome is printed as an image file. Refer to that one for a closer look at the predicions. It highlights which parts might be vulnerable according to the following color chart:

![color key](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/img/colorkey.png)

The following example was created using the fine resolution with the first example for the vulnerability path disclosure.

```
python3 demonstrate.py path_disclosure 1 fine
```

Alternatively, the script demonstrate_sourcecode.py can be used to ignore the dataset and directly load the example source code files. The outcome is essentially the same.

```
python3 demonstrate_sourcecode.py sql 3 fine
```

![Example](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/img/examplePathDisclosure.png)

There is also the possibility to take the labeling in the dataset into account. In this case, the skript can color false positives in a different color than true positives, and false negatives in a different color than true negatives. For this purpose, the script is used. It takes the same parameters as the previous one and also saves its result as a png file.


![color key labeled](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/img/colorkeylabeled.png)


The following example shows the prediction for the third example file for the open redirect vulnerability, using labels for coloring:

```
python3 demonstrate_labeled.py open_redirect 3 fine
```

You can see that both parts in the file that are vulnerable were recognized (light blue color), and most of the rest was correctly identified as not vulnerable (dark green), with some irregularities around the "edges" of the vulnerable code parts.

![Example](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/img/exampleOpenRedirect.png)
