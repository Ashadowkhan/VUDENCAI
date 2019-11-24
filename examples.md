
## Examples

Some samples from the dataset are presented here for demonstration purposes. Using the provided script, it is possible to load a piece of code and run the model on it to check for vulnerabilities. The script produces an output image with colored highlights corresponding to the vulnerability status of each code token.

There are examples for all relevant types of vulnerabilities:

| Vulnerability        | Source  | Link to commit   | Changed file | Example file |
| ---------------------|-------- |------------------| -------------| -------------|
|<sub> SQL injection </sub> | <sub>instacart/lore</sub> | <sub> [protect against potential sql injection](https://github.com/instacart/lore/commit/a0a5fd945a8bf128d4b9fb6a3ebc6306f82fa4d0) </sub> | <sub> /lore/io/connection.py </sub> | <sub> sql-1.py </sub> | 
|<sub>  SQL injection </sub> | <sub>uktrade/export-wins-data</sub> | <sub>[parameterise the sql query to avoid injection attacks ](https://github.com/uktrade/export-wins-data/commit/307587cc00d2290a433bf74bd305aecffcbb05a2) </sub> | <sub> /wins/views/flat_csv.py </sub> | <sub> sql-2.py </sub> | 
|<sub> SQL injection </sub> | <sub> kyojuceles/mud| [prevent sql injection attack](https://github.com/kyojuceles/mud/commit/47f5aa6aa2e82de7ce2a440aea870958edf0ae77) </sub> | <sub> /db/db_processor_mysql.py </sub> | <sub> sql-3.py </sub> |
|<sub> XSS </sub> | <sub> dongweiming/lyanna </sub> | <sub> [Fix comment's reflected xss vulnerability](https://github.com/dongweiming/lyanna/commit/fcefac79e4b7601e81a3b3fe0ad26ab18ee95d7d) </sub> | <sub> /models/comment.py | xss-1.py </sub> |
|<sub> XSS </sub> | <sub> inveniosoftware/invenio-records| [admin: xss vulnerability fix](https://github.com/inveniosoftware/invenio-records/commit/361def20617cde5a1897c2e81b70bfadaabae608) </sub> | <sub> /invenio_records/admin.py | xss-2.py </sub> |
|<sub> XSS </sub> | <sub> onefork/pontoon-sr</sub> | <sub>[Fix an XSS vulnerability in batch/views.py](https://github.com/onefork/pontoon-sr/commit/fc07ed9c68e08d41f74c078b4e7727f1a0888be8) </sub> | <sub> /pontoon/batch/views.py</sub> | <sub> xss-3.py </sub> |
|<sub> Commmand injection </sub> | <sub> saltstack/salt </sub> | <sub> [Fix command injection vulnerability in disk.usage ](https://github.com/saltstack/salt/commit/ebdef37b7e5d2b95a01d34b211c61c61da67e46a) </sub> | <sub>/salt/modules/disk.py </sub> | <sub> command_injection-1.py </sub> |
|<sub> Commmand injection </sub> | <sub> Atticuss/ajar </sub> | <sub>[fixed command injection issue](https://github.com/Atticuss/ajar/commit/5ed8aba271ad20e6168f2e3bd6c25ba89b84484f) </sub> | <sub>/ajar.py </sub> | <sub>command_injection-2.py </sub> |
|<sub> Commmand injection </sub> | <sub>yasong/netzob </sub> | <sub> [Remove security issue related to shell command injection](https://github.com/yasong/netzob/commit/557abf64867d715497979b029efedbd2777b912e) </sub> | <sub> /src/netzob/Simulator/Channels/RawEthernetClient.py </sub> | <sub> command_injection-3.py </sub> |
|<sub>  Name </sub> | <sub> yasong/netzob </sub> | <sub> []() </sub> | <sub> </sub> | <sub>name-1.py </sub> |
|<sub>  Name </sub> | <sub> yasong/netzob </sub> | <sub> []() </sub> | <sub> </sub> | <sub>name-1.py </sub> |





To try out one of the examples, simply execute:

```
python3 62Demonstrate.py sql 1
```

The first parameter specifies the type of vulnerability. It should be from the list "sql","xss","xsrf","command_injection","xsrf","remote_code_execution","sanitization".

The second paramter should be the number of the example between 1 and 3. 

An optional third parameter "fine" makes increases the resolution of colors. 

The script puts output to the screen that already highlights the vulnerable parts in red and the (probably) non-vulnerable parts in green, but the detailed outcome is printed as an image file. Refer to that one for a closer look at the predicions. It highlights which parts might be vulnerable according to the following color chart:

![Legende](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/legende2.png)


The following example was created using the fine resolution with the fourth sql example.


```
python3 demonstrate.py sql 4 fine
```

![Example](https://github.com/LauraWartschinski/VulnerabilityDetection/blob/master/example.png)

There is also the possibility to take the labeling that is present in the dataset into account. In this case, the skript can color false positives in a different color than true positives, and false negatives in a different color than true negatives. For this purpose, the script is used. It takes the same parameters as the previous one and also saves its result as a png file.

```
python3 demonstrate_labeled.py sql 4 
```