
## Examples

Some samples from the dataset are presented here for demonstration purposes. Using the provided script, it is possible to load a piece of code and run the model on it to check for vulnerabilities. The script produces an output image with colored highlights corresponding to the vulnerability status of each code token.

There are examples for all relevant types of vulnerabilities:

| Vulnerability        | Source  | Link to commit   | Changed file | Example file |
| ---------------------|-------- |------------------| -------------| -------------|



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

There is also the possibility to take the labeling that is present in the dataset into account. In this case, the skript can color false positives in a different color than true positives, and false negatives in a different color than true negatives. For this purpose, the script is used. It takes the same parameters as the previous one and also saves its result as a png file.

```
python3 demonstrate_labeled.py sql 4 
```